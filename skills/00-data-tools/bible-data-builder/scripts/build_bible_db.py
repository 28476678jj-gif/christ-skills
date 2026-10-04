#!/usr/bin/env python3
"""USFX XML -> biblemate 兼容 SQLite (.bible) 构建器。

将公有领域圣经译本（USFX 格式）转换为 biblemate 数据格式：
    表 Verses(Book INT, Chapter INT, Verse INT, Scripture TEXT)
Book 为新教正典 1-66 序号（1=创世记 ... 66=启示录），与 biblemate 检索脚本兼容。

用法：
    python tools/build_bible_db.py \
        --src data/sources/chi-cuv-simp.usfx.xml \
        --out data/bibles/CUVS1919.bible \
        --abbr CUVS1919 --title "和合本 1919（简体）" --license "Public Domain"
"""
import argparse
import os
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET

# USFX/OSIS 书卷代码 -> 正典序号（1-66）
BOOK_ORDER = [
    "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
    "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
    "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN",
    "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
    "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL",
    "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN",
    "JUD", "REV",
]
BOOK_NUM = {code: i + 1 for i, code in enumerate(BOOK_ORDER)}

# 内部文本不属于经文的元素（标题、脚注、交叉引用）
DROP_INLINE = {"s", "s1", "s2", "f", "x", "fr", "fq", "ft", "fk", "fl", "fp", "fv", "fdc", "xo", "xt"}


def norm_int(raw, what, stats):
    """把 '1' / '1a' 之类的 id 解析为整数；失败记数并返回 None。"""
    m = re.match(r"\s*(\d+)", str(raw))
    if not m:
        stats[f"bad_{what}"] += 1
        return None
    return int(m.group(1))


def collect_inline(elem, out):
    """收集内联元素的文本。标题/脚注/交叉引用丢内部文本，其余保留 itertext。"""
    if elem.tag in DROP_INLINE:
        if elem.tail:
            out.append(elem.tail)
        return
    for t in elem.itertext():
        out.append(t)
    if elem.tail:
        out.append(elem.tail)


def parse_usfx(src_path):
    """返回 [(book_num, chapter, verse, text), ...]，按文档顺序。"""
    tree = ET.parse(src_path)
    root = tree.getroot()
    verses = []
    stats = {"bad_chapter": 0, "bad_verse": 0, "skipped_v0": 0, "unknown_book": 0}

    for book in root.iter("book"):
        code = book.get("id", "").strip().upper()
        bnum = BOOK_NUM.get(code)
        if not bnum:
            stats["unknown_book"] += 1
            continue
        chapter = None
        verse = None
        buf = []
        for elem in book:
            tag = elem.tag
            if tag == "c":
                chapter = norm_int(elem.get("id"), "chapter", stats)
            elif tag == "v":
                verse = norm_int(elem.get("id"), "verse", stats)
                buf = [elem.tail] if elem.tail else []
            elif tag == "ve":
                if chapter and verse:
                    if verse == 0:
                        stats["skipped_v0"] += 1
                    else:
                        text = re.sub(r"\s+", " ", "".join(buf)).strip()
                        verses.append((bnum, chapter, verse, text))
                verse = None
                buf = []
            else:
                if verse is not None:
                    collect_inline(elem, buf)
    return verses, stats


def build_db(verses, out_path, abbr, title, license_):
    if os.path.exists(out_path):
        os.remove(out_path)
    conn = sqlite3.connect(out_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE Verses (Book INT, Chapter INT, Verse INT, Scripture TEXT)")
    cur.execute(
        "CREATE TABLE Metadata (Key TEXT PRIMARY KEY, Value TEXT)"
    )
    cur.executemany(
        "INSERT INTO Verses (Book, Chapter, Verse, Scripture) VALUES (?, ?, ?, ?)", verses
    )
    cur.executemany(
        "INSERT INTO Metadata (Key, Value) VALUES (?, ?)",
        [("abbreviation", abbr), ("title", title), ("license", license_)],
    )
    cur.execute("CREATE INDEX idx_verses_bcv ON Verses (Book, Chapter, Verse)")
    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM Verses").fetchone()[0]
    books = cur.execute("SELECT COUNT(DISTINCT Book) FROM Verses").fetchone()[0]
    conn.close()
    return total, books


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--abbr", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--license", default="Public Domain")
    args = ap.parse_args()

    verses, stats = parse_usfx(args.src)
    if not verses:
        print("Error: 未解析到任何经文。", file=sys.stderr)
        sys.exit(1)
    total, books = build_db(verses, args.out, args.abbr, args.title, args.license)
    print(f"OK: {args.out}")
    print(f"  卷数: {books}  节数: {total}")
    if any(stats.values()):
        print(f"  警告统计: {stats}")


if __name__ == "__main__":
    main()
