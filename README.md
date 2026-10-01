# 基督信仰技能库（christ-skills）

以圣经为唯一真理锚点的中文 AI 技能集合。本地可调用，开源可共建。

## 这个库解决什么问题

让 AI 聊信仰，眼下有三个老毛病：

1. **编经文。** 模型会理直气壮地背出根本不存在的"经文"。本库的对策是强制检索：凡引用经文必须来自本地数据库核验，`tools/verse_check.py` 逐条验证，不过不准合并。
2. **没立场，还假装有。** 面对教义分歧，模型倾向于和稀泥或随机站队。本库的对策是三级教义标注：核心级按普世信经持守立场，争议级并列各宗派最强论证不下结论，敏感级强制人工审核加免责边界。
3. **中文内容空白。** 开源世界里结构化的中文信仰技能基本没有。本库从地基到技能全部中文原生，同时保留英文对照便于国际协作。

## 设计原则

- **锚点先行。** 一切技能受四份文件约束：`STATEMENT_OF_FAITH.md`（使徒信经与尼西亚信经为唯一强制锚点）、`DOCTRINE_POLICY.md`（三级教义标注与敏感类目政策）、`CITATION_STANDARD.md`（引用规范）、`GLOSSARY.md`（术语表）。先读这四份，再读任何技能。
- **数据可验。** 仓库自带公有领域经文数据库（和合本 1919 简体，SQLite，与 biblemate 数据格式兼容），不依赖外部 API，离线可核验。
- **版权干净。** 只收录公有领域文本（和合本 1919、KJV、WEB、ASV 等）。版权译本（和合本修订版、新译本、ESV、NIV 等）的全文数据一律不进仓库，作为使用者本地插件式数据处理。
- **机器校验。** 每个技能必须通过结构 lint 与经文校验；敏感类目额外强制具名人工审核。

## 目录结构

```
christ-skills/
├── STATEMENT_OF_FAITH.md   信仰锚点（先读）
├── DOCTRINE_POLICY.md      教义三级标注与敏感类目政策
├── CITATION_STANDARD.md    经文引用规范
├── GLOSSARY.md             术语表
├── taxonomy.md             类目总表与新增类目流程
├── CONTRIBUTING.md         贡献指南
├── CHANGELOG.md            版本与更新日志
├── LICENSE                 双许可说明（代码 MIT，文档 CC BY-SA 4.0）
├── skills/                 技能本体，按一级类目分目录
│   ├── 02-exegesis/        解经
│   └── 03-topical-study/   主题查经
├── templates/
│   └── SKILL_TEMPLATE.md   技能统一模板
├── tools/
│   ├── bible_books.py      六十六卷书卷映射（单一权威数据）
│   ├── build_bible_db.py   USFX XML -> SQLite 构建器
│   ├── verse_check.py      经文引用校验
│   └── lint_skill.py       技能结构与 frontmatter 校验
└── data/
    ├── sources/            公有领域源数据（USFX XML）
    └── bibles/             构建产物：CUVS1919.bible（SQLite）
```

## 安装与使用

技能遵循通用 Agent Skills 规范（含 `SKILL.md` 的目录），主流宿主均可加载：

- **WorkBuddy**：把需要的技能目录复制到 `~/.workbuddy/skills/`（用户级，全项目可用）或项目内 `.workbuddy/skills/`（项目级）。
- **Claude Code**：复制到 `~/.claude/skills/` 或项目内 `.claude/skills/`。
- 其他兼容宿主按其技能目录约定安装。

数据说明：技能内经文检索默认读仓库自带的 `data/bibles/CUVS1919.bible`。如果你本机装有 [biblemate](https://github.com/eliranwong/biblemate) 数据（`~/biblemate/data/bibles/*.bible` 或设 `BIBLEMATE_DATA`），校验与检索脚本会优先使用本地数据，便于多译本对照；本仓库不分发任何版权译本数据。

## 工具

```bash
# 构建经文数据库（从 USFX 源数据）
python tools/build_bible_db.py --src data/sources/chi-cuv-simp.usfx.xml \
    --out data/bibles/CUVS1919.bible --abbr CUVS1919 --title "和合本 1919（简体）"

# 校验某个技能文件中的全部经文引用
python tools/verse_check.py skills/02-exegesis/expository-passage-study/SKILL.md

# 校验技能结构与 frontmatter
python tools/lint_skill.py skills/02-exegesis/expository-passage-study
```

## 类目地图

现登记 19 个一级类目，分 P0 至 P3 四批落地，全表见 `taxonomy.md`。当前已含技能：

- `skills/02-exegesis/expository-passage-study`：逐段解经研究（P0）
- `skills/03-topical-study/topical-bible-study`：主题查经串珠（P0）
- `skills/04-preaching/sermon-prep`：讲章预备（P1 首发），从经文到逐字稿全流程，附[示例讲章](skills/04-preaching/sermon-prep/examples/sermon-phil-1-21.md)

## 快速开始：讲章预备

1. 安装：把 `skills/04-preaching/sermon-prep` 目录复制到你的宿主技能目录（WorkBuddy 用 `~/.workbuddy/skills/`，Claude Code 用 `~/.claude/skills/`），并把 `data/bibles/` 与 `tools/` 一并放在可读位置（技能内的经文检索指向它们）。
2. 在宿主中对新对话直接说：「下周主日我讲 腓立比书 1:21，帮我预备讲章，25 分钟」。
3. 宿主按技能流程产出四段式讲章预备包：解经摘要、命题与大纲、逐字稿、时长估算与上台提示。成品长什么样，先看[示例产出](skills/04-preaching/sermon-prep/examples/sermon-phil-1-21.md)。
4. 重要：产出是预备草稿。讲员须自己祷告消化、按自己的声音重写后再上台（技能内对此有硬性提醒）。

## 支持本项目

核心库永久免费开源（马太福音 10:8）；维护劳动接受支持（提摩太前书 5:18）。捐赠渠道与付费服务（培训工作坊、定制搭建、伴读材料）的原则与明细见 `SPONSORS.md`，赞助按钮配置见 `.github/FUNDING.yml`。传播关键词与合规边界见 `marketing/keywords.md`。

## 合规与免责

- 本库是个人学习与研究用途的资料集合，所有内容以圣经文本与公有领域文献为基础，不构成对任何教会、宗派、团体的官方立场声明。
- 本库内容不能替代牧者辅导，也不能替代医疗、法律、心理咨询等专业意见。敏感类目（异端辨别、属灵争战、疾病医治）的边界声明见各技能「免责与边界」一节。
- 提醒贡献者与分发者：在你所在的司法辖区，通过互联网向公众提供宗教信息可能受到法律法规规制（例如中国大陆《互联网宗教信息服务管理办法》）。公开分发、转载或基于本库提供公开服务前，请自行评估并遵守适用法律。

## 贡献

读 `CONTRIBUTING.md`。一句话：用模板写技能，过两道机器校验，PR 里填教义影响声明，敏感类目等人审。

## 许可

代码（`tools/` 下脚本）采用 MIT License；文档与技能内容（各 `SKILL.md` 及根目录 markdown）采用 CC BY-SA 4.0；经文源数据为公有领域，其原始版权状态不因收录而改变。详见 `LICENSE`。
