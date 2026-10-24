#!/usr/bin/env python
"""检查技能包是否存在「包外引用」——WorkBuddy 开放平台会因「内置文件缺失」驳回。

平台静态扫描 SKILL.md，把这些形态当作包内资源去解析，找不到即判失败：
  1. 反引号包裹的路径，如 `scripts/verse_check.py`
  2. 裸的斜杠路径（带扩展名或 ASCII 目录），如 data/bibles/CUVS1919.bible
  3. 其它技能的标识（连字符形式），如 expository-passage-study

用法：
  python tools/check_pkg_refs.py skills/            # 递归校验全部技能目录
  python tools/check_pkg_refs.py skills/04-preaching/sermon-prep
"""
import os
import re
import sys

# 允许出现在正文里的非路径斜杠短语（中文顿号/分号场景等）
FALSE_POSITIVE_HINTS = (
    "字/", "件/", "页/", "天/", "分钟", "次/", "遍/", "轮/", "层/", "步/",
    "号/", "册/", "卷/", "章/", "节/", "章/节", "父/", "子/", "国/",
)


def collect_inside(skill_dir):
    """包内实际存在的相对路径集合。"""
    inside = set()
    for root, _dirs, files in os.walk(skill_dir):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), skill_dir).replace("\\", "/")
            inside.add(rel)
            inside.add(os.path.basename(f))
    return inside


def all_skill_names(skills_root):
    names = set()
    for root, _dirs, files in os.walk(skills_root):
        if "SKILL.md" in files:
            names.add(os.path.basename(root))
    return names


def is_pathlike(token):
    """看起来像个文件路径。

    判定要严，避免把中文顿号短语（争议级/敏感级）、URL 片段
    （com/28476678jj-gif/christ-skills）误判成路径。
    规则：含扩展名，或各段均为纯 ASCII 且不含 http(s) 上下文。
    """
    if not token or "/" not in token:
        return False
    if any(ch in token for ch in "：，。；、（）「」【】“”"):
        return False
    if " " in token or "\u3000" in token:
        return False
    parts = [x for x in token.split("/") if x]
    if not parts:
        return False
    # URL 片段：前段像域名或用户/仓库名，且含 github/gitlab 等语境
    if re.match(r"^(com|org|net|io|co|me|dev|app|ai|github|gitlab)$", parts[0], re.I):
        return False
    if re.search(r"\.(md|py|bible|xml|sh|js|json|txt|csv|yaml|yml)$", parts[-1], re.I):
        return True
    # 纯 ASCII 目录段组合
    if all(re.match(r"^[A-Za-z0-9_.\-]+$", x) for x in parts):
        # 排除「英文单词/单词」式英文短语（两侧都是常见英文短词）
        if len(parts) == 2 and len(parts[0]) <= 12 and len(parts[1]) <= 12 \
           and parts[0].isalpha() and parts[1].isalpha() \
           and parts[0].lower() not in ("data", "tools", "scripts", "references", "templates"):
            return False
        return True
    return False


def check_skill(skill_dir, skill_names):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return [f"{skill_dir}: 缺少 SKILL.md"], 0
    with open(path, encoding="utf-8") as f:
        text = f.read()
    inside = collect_inside(skill_dir)
    own = os.path.basename(skill_dir)
    # 包内实际存在的目录（如 scripts/、references/）不算包外引用
    inside_dirs = set()
    for root, dirs, _files in os.walk(skill_dir):
        for d in dirs:
            inside_dirs.add(d)
            rel = os.path.relpath(os.path.join(root, d), skill_dir).replace("\\", "/")
            inside_dirs.add(rel)

    issues = []
    cands = set()
    cands |= set(re.findall(r"`([^`\n]+?)`", text))
    cands |= set(re.findall(r"(?<![\w/\-])([\w\-]+(?:/[\w\-.]+)+)", text))
    cands |= set(re.findall(r"\b([a-z]+(?:-[a-z]+)+)\b", text))

    for c in sorted(cands):
        if c in inside or c.rstrip("/") in inside_dirs:
            continue
        if any(c.startswith(h) for h in FALSE_POSITIVE_HINTS):
            continue
        if is_pathlike(c):
            issues.append(f"{skill_dir}: 引用了包外路径「{c}」")
        elif c in skill_names and c != own:
            issues.append(f"{skill_dir}: 引用了其它技能「{c}」")
    return issues, len(cands)


def iter_skill_dirs(root):
    if os.path.isfile(os.path.join(root, "SKILL.md")):
        yield root
        return
    for dirpath, _dirs, files in os.walk(root):
        if "SKILL.md" in files:
            yield dirpath


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    root = sys.argv[1]
    skills_root = root if os.path.isdir(root) else os.path.dirname(root)
    names = all_skill_names(skills_root)
    total_issues = 0
    checked = 0
    for sd in sorted(iter_skill_dirs(root)):
        checked += 1
        issues, _ = check_skill(sd, names)
        rel = os.path.relpath(sd, skills_root).replace("\\", "/")
        if issues:
            total_issues += len(issues)
            print(f"[FAIL] {rel}")
            for i in issues:
                print(f"       {i}")
        else:
            print(f"[ OK ] {rel}")
    print(f"\n检查 {checked} 个技能，发现 {total_issues} 处包外引用。")
    if total_issues:
        print("→ 会被平台判「内置文件缺失」驳回，请先修正。")
        return 1
    print("→ 全部自闭合，可提交。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
