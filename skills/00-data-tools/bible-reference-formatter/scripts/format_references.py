#!/usr/bin/env python3
"""经文引用格式规范化（零第三方依赖）。

识别 markdown 中的圣经书卷名与章节引用，统一为规范写法：
- 书卷名按六十六卷映射表归一（支持繁体与英文缩写识别，按指定风格输出）
- 章与节之间用半角冒号，书卷名与章号之间保留一个空格
- 范围用半角连字符，跨章写作 c1:v1-c2:v2
只替换引用标注本身，不动引文内容。

用法：
    python tools/format_references.py 文档.md                    # 预览（默认，不改写）
    python tools/format_references.py 文档.md --style abbr       # 输出规范简称
    python tools/format_references.py 目录/ --style full --inplace
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_books import NUM_TO_BOOK
from verse_check import ZH_REF, EN_REF, longest_book_suffix


def is_cjk(ch):
    return "\u4e00" <= ch <= "\u9fff"


def build_ref(book, c1, v1, c2, v2, style):
    info = NUM_TO_BOOK[book]
    name = info["zh"] if style == "full" else info["abbr"]
    if (c2, v2) == (c1, v1):
        return f"{name} {c1}:{v1}"
    if c2 == c1:
        return f"{name} {c1}:{v1}-{v2}"
    return f"{name} {c1}:{v1}-{c2}:{v2}"


def find_refs(text, style):
    """返回 [(start, end, old, new)]，按位置排序。"""
    hits = []
    for m in ZH_REF.finditer(text):
        b, sub = longest_book_suffix(m.group(1))
        if not b:
            continue
        if len(sub) == 1 and is_cjk(sub):
            name_start = m.start(1) + m.group(1).rfind(sub)
            prev = text[name_start - 1] if name_start > 0 else ""
            if is_cjk(prev):
                continue
        c1, v1 = int(m.group(2)), int(m.group(3))
        if m.group(5):
            c2 = int(m.group(4)) if m.group(4) else c1
            v2 = int(m.group(5))
        else:
            c2, v2 = c1, v1
        old = m.group(0)
        hits.append((m.start(), m.end(), old, build_ref(b, c1, v1, c2, v2, style)))
    for m in EN_REF.finditer(text):
        from bible_books import book_num
        b = book_num(m.group(1))
        if not b:
            continue
        c1, v1 = int(m.group(2)), int(m.group(3))
        if m.group(5):
            c2 = int(m.group(4)) if m.group(4) else c1
            v2 = int(m.group(5))
        else:
            c2, v2 = c1, v1
        hits.append((m.start(), m.end(), m.group(0), build_ref(b, c1, v1, c2, v2, style)))
    hits.sort(key=lambda x: x[0])
    return [h for h in hits if h[2] != h[3]]


def format_text(text, style):
    hits = find_refs(text, style)
    out = text
    for start, end, old, new in reversed(hits):
        out = out[:start] + new + out[end:]
    return out, hits


def iter_md(path):
    if os.path.isfile(path) and path.lower().endswith(".md"):
        yield path
    elif os.path.isdir(path):
        for root, _dirs, files in os.walk(path):
            for name in sorted(files):
                if name.lower().endswith(".md"):
                    yield os.path.join(root, name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--style", choices=["full", "abbr"], default="full")
    ap.add_argument("--inplace", action="store_true")
    ap.add_argument("--max-show", type=int, default=30)
    args = ap.parse_args()

    total = 0
    files = 0
    for path in iter_md(args.path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text, hits = format_text(text, args.style)
        if not hits:
            continue
        files += 1
        total += len(hits)
        if args.inplace:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"{path}: 改写 {len(hits)} 处")
        else:
            print(f"{path}: 将改动 {len(hits)} 处")
            for _s, _e, old, new in hits[: args.max_show]:
                print(f"    {old}  ->  {new}")
            if len(hits) > args.max_show:
                print(f"    ...（其余 {len(hits) - args.max_show} 处略）")
    print(f"\n合计：{files} 个文件，{total} 处改动。" + ("（已写入）" if args.inplace else "（预览，未改写；加 --inplace 生效）"))


if __name__ == "__main__":
    main()
