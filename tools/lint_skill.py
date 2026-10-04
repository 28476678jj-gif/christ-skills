#!/usr/bin/env python3
"""技能结构与 frontmatter 校验器（零第三方依赖）。

用法：
    python tools/lint_skill.py skills/02-exegesis/expository-passage-study
    python tools/lint_skill.py skills/          # 递归校验全部技能目录

校验规则（任一失败即非零退出）：
1. 目录含 SKILL.md
2. frontmatter 必填字段：name、description、doctrine_status、version、sources、bible_anchor，
   且 reviewed_by / reviewed_at 字段存在
3. name 与目录名一致；description 长度 10-500；doctrine_status 为 core/disputed/sensitive 之一
4. doctrine_status=sensitive 时，reviewed_by 与 reviewed_at 必须非空
5. 正文八个必备章节齐全（见模板）
6. 工作流程中含强制经文检索声明（命中关键词）
7. 目录内不得含可执行文件（.exe/.bat/.cmd/.ps1/.com）
"""
import os
import re
import sys

REQUIRED_FIELDS = ["name", "description", "doctrine_status", "version", "sources", "bible_anchor"]
DOCTRINE_LEVELS = {"core", "disputed", "sensitive", "neutral"}
REQUIRED_SECTIONS = ["用途", "触发场景", "输入与输出", "工作流程", "经文依据", "争议标注", "质量校验清单", "免责与边界"]
RETRIEVAL_HINTS = ["不得凭记忆", "必须检索", "强制检索", "禁止凭记忆"]
FORBIDDEN_EXT = {".exe", ".bat", ".cmd", ".ps1", ".com"}


def parse_frontmatter(text):
    """解析简易 YAML frontmatter，返回 dict。只支持标量、[行内列表]、缩进 - 列表。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None, text
    data = {}
    current_key = None
    for line in m.group(1).split("\n"):
        item = re.match(r"^\s+-\s+(.*)$", line)
        kv = re.match(r"^([A-Za-z_][\w]*)\s*:\s*(.*)$", line)
        if item and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(item.group(1).strip().strip('"').strip("'"))
        elif kv:
            current_key = kv.group(1)
            raw = kv.group(2).strip()
            if raw == "":
                data[current_key] = ""
            elif raw.startswith("[") and raw.endswith("]"):
                inner = raw[1:-1].strip()
                data[current_key] = [x.strip().strip('"').strip("'") for x in inner.split(",")] if inner else []
            else:
                data[current_key] = raw.strip('"').strip("'")
    body = text[m.end():]
    return data, body


def lint_dir(path):
    errors = []
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [f"{path}: 缺少 SKILL.md"]

    with open(skill_md, "r", encoding="utf-8") as f:
        text = f.read()

    fm, body = parse_frontmatter(text)
    if fm is None:
        return [f"{skill_md}: 缺少 frontmatter（--- 包裹区）"]

    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] in ("", []):
            errors.append(f"{skill_md}: frontmatter 缺少必填字段或为空: {field}")
    for field in ("reviewed_by", "reviewed_at"):
        if field not in fm:
            errors.append(f"{skill_md}: frontmatter 缺少字段: {field}（非敏感级可留空字符串）")

    dir_name = os.path.basename(os.path.normpath(path))
    if fm.get("name") and fm["name"] != dir_name:
        errors.append(f"{skill_md}: name '{fm['name']}' 与目录名 '{dir_name}' 不一致")

    desc = fm.get("description") or ""
    if desc and not (10 <= len(desc) <= 500):
        errors.append(f"{skill_md}: description 长度 {len(desc)}，须在 10-500 字符之间")

    status = (fm.get("doctrine_status") or "").strip().lower()
    if status and status not in DOCTRINE_LEVELS:
        errors.append(f"{skill_md}: doctrine_status '{status}' 非法，应为 core/disputed/sensitive")
    if status == "sensitive":
        if not fm.get("reviewed_by"):
            errors.append(f"{skill_md}: sensitive 级必须填写 reviewed_by（具名人类审核者）")
        if not fm.get("reviewed_at"):
            errors.append(f"{skill_md}: sensitive 级必须填写 reviewed_at")

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+.*{re.escape(section)}", body, re.M):
            errors.append(f"{skill_md}: 缺少必备章节: ## {section}")

    # neutral 级（工具型）不产出经文引用，豁免强制检索声明
    if status != "neutral" and not any(hint in body for hint in RETRIEVAL_HINTS):
        errors.append(f"{skill_md}: 工作流程未声明强制经文检索（需含 {'/'.join(RETRIEVAL_HINTS)} 之一）")

    for root, _dirs, files in os.walk(path):
        for name in files:
            if os.path.splitext(name)[1].lower() in FORBIDDEN_EXT:
                errors.append(f"{path}: 含禁止的可执行文件 {name}")

    return errors


def iter_skill_dirs(root):
    if os.path.isfile(os.path.join(root, "SKILL.md")):
        yield root
        return
    for dirpath, _dirs, files in os.walk(root):
        if "SKILL.md" in files:
            yield dirpath


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/lint_skill.py <技能目录或根目录> [...]")
        sys.exit(2)
    all_errors = []
    checked = 0
    for arg in sys.argv[1:]:
        for d in iter_skill_dirs(arg):
            checked += 1
            all_errors.extend(lint_dir(d))
    if checked == 0:
        print("未发现任何技能目录（含 SKILL.md）。")
        sys.exit(2)
    for e in all_errors:
        print("FAIL:", e)
    if all_errors:
        print(f"\n{len(all_errors)} 个问题，{checked} 个技能。")
        sys.exit(1)
    print(f"OK: {checked} 个技能全部通过。")


if __name__ == "__main__":
    main()
