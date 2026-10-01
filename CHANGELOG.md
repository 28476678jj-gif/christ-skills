# 更新日志

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)：

- MAJOR：类目体系、技能模板、锚点文件的不兼容重构
- MINOR：新增技能、新增类目、内容增补
- PATCH：经文勘误、教义表述修正、错别字与格式修复

## [Unreleased]

### Added

- 参考书目机制 `references/BIBLIOGRAPHY.md`：登记维护者提供的牧者与学者著作（首批 14 种），明确版权边界与技能写作参考规则。
- 地基四件套：`STATEMENT_OF_FAITH.md`（使徒信经与尼西亚信经为锚）、`DOCTRINE_POLICY.md`（core/disputed/sensitive 三级标注与审核规则）、`CITATION_STANDARD.md`（引用规范与六十六卷对照表）、`GLOSSARY.md`（术语表）。
- 类目总表 `taxonomy.md`：19 个一级类目，P0 至 P3 四批路线。
- 技能统一模板 `templates/SKILL_TEMPLATE.md`。
- 数据底座：公有领域和合本 1919 简体 USFX 源数据，构建为 biblemate 兼容的 `data/bibles/CUVS1919.bible`（66 卷，31,100 节）。
- 工具链：`build_bible_db.py`（USFX 导入）、`bible_books.py`（书卷映射）、`verse_check.py`（经文引用校验）、`lint_skill.py`（技能结构校验）。
- 样板技能：`skills/02-exegesis/expository-passage-study`（逐段解经研究）、`skills/03-topical-study/topical-bible-study`（主题查经串珠）。
