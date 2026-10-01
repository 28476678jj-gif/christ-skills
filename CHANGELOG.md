# 更新日志

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)：

- MAJOR：类目体系、技能模板、锚点文件的不兼容重构
- MINOR：新增技能、新增类目、内容增补
- PATCH：经文勘误、教义表述修正、错别字与格式修复

## [Unreleased]

### Added

- P1 首发技能：`skills/04-preaching/sermon-prep`（讲章预备全流程：解经摘要、命题大纲、逐字稿、时长校准），附示例产出 `examples/sermon-phil-1-21.md`（腓立比书 1:21 十分钟短讲）。
- 变现与传播配置：`SPONSORS.md`（核心免费、服务收费的原则与平衡声明）、`.github/FUNDING.yml`（赞助按钮模板）、`marketing/keywords.md`（GitHub Topics、SEO 与中文传播关键词包）。
- README 新增「快速开始：讲章预备」与「支持本项目」两节。
- 参考书目机制 `references/BIBLIOGRAPHY.md`：登记维护者提供的牧者与学者著作（首批 14 种），明确版权边界与技能写作参考规则。

### Fixed

- `verse_check.py` 两处误报：单字简称歧义（"保罗在 1:23"被误判为罗马书引用，已加前文边界保护）；跨行引文错配（引文与标注之间允许换行导致错配上一条引文，已禁止）。
- 地基四件套：`STATEMENT_OF_FAITH.md`（使徒信经与尼西亚信经为锚）、`DOCTRINE_POLICY.md`（core/disputed/sensitive 三级标注与审核规则）、`CITATION_STANDARD.md`（引用规范与六十六卷对照表）、`GLOSSARY.md`（术语表）。
- 类目总表 `taxonomy.md`：19 个一级类目，P0 至 P3 四批路线。
- 技能统一模板 `templates/SKILL_TEMPLATE.md`。
- 数据底座：公有领域和合本 1919 简体 USFX 源数据，构建为 biblemate 兼容的 `data/bibles/CUVS1919.bible`（66 卷，31,100 节）。
- 工具链：`build_bible_db.py`（USFX 导入）、`bible_books.py`（书卷映射）、`verse_check.py`（经文引用校验）、`lint_skill.py`（技能结构校验）。
- 样板技能：`skills/02-exegesis/expository-passage-study`（逐段解经研究）、`skills/03-topical-study/topical-bible-study`（主题查经串珠）。
