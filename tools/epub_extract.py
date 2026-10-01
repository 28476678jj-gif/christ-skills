#!/usr/bin/env python3
"""epub 章节提取器（零第三方依赖）。

伴读目录里的 epub 没有 PDF 页面，无法用渲染法阅读，先把章节导出成文本再细读。

用法：
    python tools/epub_extract.py <书籍.epub>                 # 列出章节目录
    python tools/epub_extract.py <书籍.epub> --unit 1        # 输出第 1 单元（1-2 章）文本
    python tools/epub_extract.py <书籍.epub> --unit 1 --out tmp.txt

单元划分：每个单元 1-2 个内容章节，且正文字符数控制在 8000-20000（一个细读单元约
15-25 页的体量）；不足则并下一章，超过则单章成单元。导言、封面、目录等短文件跳过。

退出码：0 成功；2 用法错误或文件不是 epub。
"""
import argparse
import html
import os
import re
import sys
import zipfile

MIN_CHARS = 300     # 短于这个长度的文档视为封面/目录/版权页，不计入单元
MIN_UNIT = 8000     # 短章累积到这个字数才成单元
MAX_CHARS = 20000   # 单章上限；超过则把长章切成多个单元（工具书常见）


def extract_text(zf, name):
    raw = zf.read(name).decode("utf-8", errors="ignore")
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|h[1-6]|li)>", "\n", raw)
    text = re.sub(r"<[^>]+>", "", raw)
    text = html.unescape(text)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def spine_docs(zf):
    """按 opf 的 spine 顺序返回内容文档名列表；没有 opf 时按文件名排序兜底。"""
    opf = None
    try:
        container = zf.read("META-INF/container.xml").decode("utf-8", errors="ignore")
        m = re.search(r'full-path="([^"]+\.opf)"', container)
        if m:
            opf = m.group(1)
    except KeyError:
        pass
    if opf is None:
        opfs = [n for n in zf.namelist() if n.lower().endswith(".opf")]
        opf = opfs[0] if opfs else None
    if opf is None:
        base = os.path.dirname("")
        return sorted(n for n in zf.namelist() if n.lower().endswith((".html", ".xhtml")))

    opf_dir = os.path.dirname(opf)
    opf_text = zf.read(opf).decode("utf-8", errors="ignore")
    manifest = dict(re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf_text))
    manifest.update(re.findall(r'<item[^>]*href="([^"]+)"[^>]*id="([^"]+)"', opf_text)[::1] and {})
    ids = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf_text)
    docs = []
    for i in ids:
        href = manifest.get(i)
        if not href:
            continue
        path = os.path.join(opf_dir, href).replace("\\", "/") if opf_dir else href
        if path in zf.namelist():
            docs.append(path)
    if not docs:
        docs = [n for n in zf.namelist() if n.lower().endswith((".html", ".xhtml"))]
        docs.sort()
    return docs


def build_units(zf):
    units = []
    cur = {"docs": [], "text": ""}

    def push(pending):
        """超过单章上限的长章（工具书常见）按 CHUNK 切分成多个单元。"""
        nonlocal cur
        if len(pending["text"]) <= MAX_CHARS:
            cur["docs"].extend(pending["docs"])
            cur["text"] += (("\n\n" if cur["text"] else "") + pending["text"])
            if len(cur["text"]) >= MIN_UNIT:
                units.append(cur)
                cur = {"docs": [], "text": ""}
            return
        head, body = pending["text"][:MAX_CHARS], pending["text"][MAX_CHARS:]
        if cur["text"]:
            units.append(cur)
            cur = {"docs": [], "text": ""}
        units.append({"docs": pending["docs"], "text": head})
        while len(body) > MAX_CHARS:
            units.append({"docs": pending["docs"], "text": body[:MAX_CHARS]})
            body = body[MAX_CHARS:]
        if body.strip():
            cur = {"docs": list(pending["docs"]), "text": body}

    for doc in spine_docs(zf):
        try:
            t = extract_text(zf, doc)
        except Exception:
            continue
        if len(t) < MIN_CHARS:
            continue
        push({"docs": [doc], "text": t})
    if cur["text"]:
        units.append(cur)
    return units


def main():
    ap = argparse.ArgumentParser(description="epub 章节提取器")
    ap.add_argument("epub")
    ap.add_argument("--unit", type=int, default=0, help="输出第 N 单元，0 或省略则只列目录")
    ap.add_argument("--out", help="文本写入文件（默认打印到标准输出）")
    args = ap.parse_args()

    if not os.path.isfile(args.epub) or not args.epub.lower().endswith(".epub"):
        print("需要一个 .epub 文件", file=sys.stderr)
        return 2

    with zipfile.ZipFile(args.epub) as zf:
        units = build_units(zf)
        if not units:
            print("未提取到任何内容章节（可能是纯图片 epub）", file=sys.stderr)
            return 1
        if not args.unit:
            print(f"共 {len(units)} 个阅读单元：")
            for i, u in enumerate(units, 1):
                head = re.sub(r"\s+", " ", u["text"][:60])
                print(f"  单元 {i}: {len(u['text'])} 字 | {len(u['docs'])} 个文档 | {head}")
            return 0
        if args.unit > len(units):
            print(f"只有 {len(units)} 个单元", file=sys.stderr)
            return 2
        text = units[args.unit - 1]["text"]

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"已写入 {args.out}（{len(text)} 字）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
