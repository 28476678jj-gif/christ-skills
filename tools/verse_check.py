#!/usr/bin/env python3
"""经文引用校验器（零第三方依赖）。

扫描 markdown 文件中的经文引用，对照本地 SQLite 数据库核验：
- error：经节在数据库中不存在（书卷/章/节越界）
- warning：书卷名无法解析、紧邻引文与数据库文本明显不一致（可能是默写错误或节选）

数据库定位顺序：
1. 环境变量 CHRIST_SKILLS_DATA（指向含 .bible 文件的目录）
2. 本仓库 data/bibles/（按脚本所在位置推导）
3. 环境变量 BIBLEMATE_DATA 或 ~/biblemate/data/bibles（本地多译本）

用法：
    python tools/verse_check.py file1.md [file2.md ...]
    python tools/verse_check.py skills/            # 递归扫描全部 md
    python tools/verse_check.py --version CUVS1919 skills/
退出码：0 通过；1 存在 error；2 用法错误或数据库缺失。
"""
import difflib
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_books import book_num, NUM_TO_BOOK

DEFAULT_VERSION = "CUVS1919"

# 中文引用：书卷名 1:2 或 1:2-3 / 1:2-2:3
ZH_REF = re.compile(
    r"([\u4e00-\u9fff]{1,12}?)\s*(\d+)\s*[:：]\s*(\d+)"
    r"(?:\s*[-–~]\s*(?:(\d+)\s*[:：]\s*)?(\d+))?"
)
# 英文引用：Book 1:2(-3) / (-2:3)
EN_REF = re.compile(
    r"\b([1-3]?\s?[A-Za-z][A-Za-z\.]*(?:\s[A-Za-z][A-Za-z\.]*)?)\s+(\d+):(\d+)"
    r"(?:\s*[-–]\s*(?:(\d+):)?(\d+))?\b"
)
QUOTE_PAIRS = [("「", "」"), ("“", "”"), ('"', '"'), ("'", "'")]


def find_bible_db(version):
    candidates = []
    env = os.environ.get("CHRIST_SKILLS_DATA")
    if env:
        candidates.append(env)
    repo_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "bibles"))
    candidates.append(repo_data)
    bm = os.environ.get("BIBLEMATE_DATA") or os.path.join(os.path.expanduser("~"), "biblemate")
    candidates.append(os.path.join(bm, "data", "bibles"))
    candidates.append(os.path.join(bm, "data_custom", "bibles"))
    for d in candidates:
        if not d or not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.lower().startswith(version.lower()) and name.lower().endswith(".bible"):
                return os.path.join(d, name)
    return None


class BibleDB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.path = path
        self._max = {}

    def max_verse(self, book, chapter):
        key = (book, chapter)
        if key not in self._max:
            row = self.conn.execute(
                "SELECT MAX(Verse) FROM Verses WHERE Book=? AND Chapter=?", key
            ).fetchone()
            self._max[key] = row[0] or 0
        return self._max[key]

    def max_chapter(self, book):
        row = self.conn.execute(
            "SELECT MAX(Chapter) FROM Verses WHERE Book=?", (book,)
        ).fetchone()
        return row[0] or 0

    def verse_exists(self, book, chapter, verse):
        row = self.conn.execute(
            "SELECT 1 FROM Verses WHERE Book=? AND Chapter=? AND Verse=?",
            (book, chapter, verse),
        ).fetchone()
        return row is not None

    def get_text(self, book, c1, v1, c2, v2):
        if c1 == c2:
            rows = self.conn.execute(
                "SELECT Scripture FROM Verses WHERE Book=? AND Chapter=? AND Verse BETWEEN ? AND ? ORDER BY Verse",
                (book, c1, v1, v2),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT Scripture FROM Verses WHERE Book=? AND ((Chapter=? AND Verse>=?) OR (Chapter>? AND Chapter<?) OR (Chapter=? AND Verse<=?)) ORDER BY Chapter, Verse",
                (book, c1, v1, c1, c2, c2, v2),
            ).fetchall()
        return "".join(r[0] for r in rows)


def longest_book_suffix(name):
    """从候选串中找最长可解析书卷名后缀，返回 (book, matched_sub)。"""
    name = name.strip().strip("读见参按如在的与和跟（(")
    if not name:
        return None, ""
    for end in range(0, len(name)):
        sub = name[end:]
        b = book_num(sub)
        if b:
            return b, sub
    return None, ""


def parse_refs(text):
    """产出 (start_pos, book, c1, v1, c2, v2, raw)。"""
    refs = []
    for m in ZH_REF.finditer(text):
        b, sub = longest_book_suffix(m.group(1))
        if not b:
            continue
        # 单字简称保护：命中的单字（如"罗"）前紧邻中文字符时（保罗/罗马人），不视为书卷名
        if len(sub) == 1 and "\u4e00" <= sub <= "\u9fff":
            name_start = m.start(1) + m.group(1).rfind(sub)
            prev = text[name_start - 1] if name_start > 0 else ""
            if "\u4e00" <= prev <= "\u9fff":
                continue
        c1, v1 = int(m.group(2)), int(m.group(3))
        if m.group(5):
            c2 = int(m.group(4)) if m.group(4) else c1
            v2 = int(m.group(5))
        else:
            c2, v2 = c1, v1
        refs.append((m.start(), b, c1, v1, c2, v2, m.group(0)))
    for m in EN_REF.finditer(text):
        b = book_num(m.group(1))
        if not b:
            continue
        c1, v1 = int(m.group(2)), int(m.group(3))
        if m.group(5):
            c2 = int(m.group(4)) if m.group(4) else c1
            v2 = int(m.group(5))
        else:
            c2, v2 = c1, v1
        refs.append((m.start(), b, c1, v1, c2, v2, m.group(0)))
    refs.sort(key=lambda r: r[0])
    # 去重（中英文正则可能重复命中同一位置附近）
    seen = set()
    uniq = []
    for r in refs:
        key = (r[1], r[2], r[3], r[4], r[5])
        if key not in seen or r[0] not in [u[0] for u in uniq if (u[1], u[2], u[3], u[4], u[5]) == key]:
            seen.add(key)
            uniq.append(r)
    return uniq


def normalize(s):
    s = re.sub(r"〔.*?〕", "", s)
    s = re.sub(r"[\s，。；：、！？「」“”‘’'\"（）()\[\]《》<>…—\-,.;:!?·]", "", s)
    return s


def nearby_quote(text, pos, span=30):
    """只认与引用标注紧邻的引号文本（前后各 span 字符内）。

    「引文」（书卷 X:Y） 与 书卷 X:Y：「引文」 两种格式覆盖；
    远处的强调/反语引号不参与比对，避免误报。"""
    candidates = []
    before = text[max(0, pos - span - 200):pos]
    for left, right in QUOTE_PAIRS:
        idx = before.rfind(left)
        if idx != -1:
            end = before.find(right, idx + 1)
            if end != -1 and len(before) - end - 1 <= span:
                # 引文与标注之间不得跨行，防止错配到上一条引文
                if "\n" not in before[end + 1:]:
                    c = before[idx + 1:end].strip()
                    if len(c) >= 8:
                        candidates.append((len(before) - end, c))
    after = text[pos:pos + span + 200]
    for left, right in QUOTE_PAIRS:
        idx = after.find(left)
        if idx != -1 and idx <= span:
            end = after.find(right, idx + 1)
            if end != -1 and "\n" not in after[:idx]:
                c = after[idx + 1:end].strip()
                if len(c) >= 8:
                    candidates.append((idx, c))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def check_file(path, db, as_warnings=False):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    errors, warnings = [], []
    refs = parse_refs(text)
    for pos, book, c1, v1, c2, v2, raw in refs:
        book_name = NUM_TO_BOOK[book]["zh"]
        label = f"{book_name} {c1}:{v1}" + (f"-{v2}" if (c2, v2) != (c1, v1) else "")
        if c2 < c1 or (c2 == c1 and v2 < v1):
            errors.append(f"{path}: {label} 范围起止颠倒（原文 '{raw}'）")
            continue
        mc = db.max_chapter(book)
        if c1 > mc or c2 > mc:
            errors.append(f"{path}: {label} 章数越界（{book_name}共 {mc} 章）")
            continue
        if v1 > db.max_verse(book, c1):
            errors.append(f"{path}: {book_name} {c1}:{v1} 不存在（该章共 {db.max_verse(book, c1)} 节）")
            continue
        if v2 > db.max_verse(book, c2):
            errors.append(f"{path}: {book_name} {c2}:{v2} 不存在（该章共 {db.max_verse(book, c2)} 节）")
            continue
        # 引文一致性（仅短范围）
        span = (c2 - c1) * 100 + (v2 - v1)
        if span <= 10:
            quote = nearby_quote(text, pos)
            if quote:
                q, t = normalize(quote), normalize(db.get_text(book, c1, v1, c2, v2))
                if q and t and q not in t and t not in q:
                    ratio = difflib.SequenceMatcher(None, q, t).ratio()
                    if ratio < 0.85:
                        warnings.append(
                            f"{path}: {label} 附近引文与数据库不一致（相似度 {ratio:.2f}），"
                            f"请确认是转述还是误引"
                        )
    return refs, errors, warnings


def iter_md(path):
    if os.path.isfile(path) and path.lower().endswith(".md"):
        yield path
    elif os.path.isdir(path):
        for root, _dirs, files in os.walk(path):
            for name in sorted(files):
                if name.lower().endswith(".md"):
                    yield os.path.join(root, name)


def main():
    args = sys.argv[1:]
    version = DEFAULT_VERSION
    if "--version" in args:
        i = args.index("--version")
        version = args[i + 1]
        del args[i:i + 2]
    if not args:
        print("Usage: python tools/verse_check.py [--version CUVS1919] <md 文件或目录> [...]")
        sys.exit(2)
    db_path = find_bible_db(version)
    if not db_path:
        print(f"Error: 找不到 {version} 数据库。请构建 data/bibles/ 或设置 CHRIST_SKILLS_DATA。")
        sys.exit(2)
    db = BibleDB(db_path)
    total_errors, total_warnings, total_refs, files = 0, 0, 0, 0
    for arg in args:
        for path in iter_md(arg):
            files += 1
            refs, errors, warnings = check_file(path, db)
            total_refs += len(refs)
            total_errors += len(errors)
            total_warnings += len(warnings)
            for e in errors:
                print("ERROR:", e)
            for w in warnings:
                print("WARN :", w)
    print(f"\n扫描 {files} 个文件，{total_refs} 处引用：{total_errors} 个错误，{total_warnings} 个警告。")
    print(f"（核验依据：{os.path.basename(db_path)}）")
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
