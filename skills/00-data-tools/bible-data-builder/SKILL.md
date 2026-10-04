---
name: bible-data-builder
description: 把公有领域圣经译本（USFX XML 格式）构建成本地 SQLite 数据库，供经文检索与引用校验使用。用户需要本地经文数据库、想新增译本、重建或修复数据，或要给引用校验器准备数据底座时使用。产出与 biblemate 兼容的 .bible 数据库（66 卷结构），离线可用，不依赖任何外部接口。只处理公有领域文本，不处理版权译本。
slug: bible-data-builder
displayName: 公有领域圣经数据构建器
version: 1.0.0
summary: 将 USFX 格式的公有领域圣经译本构建为本地 SQLite 数据库（biblemate 兼容），离线可查、可用于引用核验。
tags:
  - bible
  - dataset
  - sqlite
  - usfx
  - public-domain
  - tooling
license: CC-BY-SA-4.0
homepage: https://github.com/28476678jj-gif/christ-skills
doctrine_status: neutral
reviewed_by: ""
reviewed_at: ""
sources:
  - 书卷映射表 scripts/bible_books.py（六十六卷，新教正典）
  - 公有领域源数据集 djwisdom/open-bibles（USFX XML）
bible_anchor: 不适用（neutral 级工具技能，不含教义内容）
---

# 公有领域圣经数据构建器

## 用途

把一个 USFX 格式的公有领域圣经译本，转成本地可用的 SQLite 数据库。产出的表结构与 biblemate 数据格式一致，因此既能被本仓库的引用校验器直接读取，也能被任何按 biblemate 约定写的检索脚本使用。全程离线，不调外部接口，构建完可断网使用。

## 触发场景

- "给我建一个本地经文数据库"、"我要给引用校验准备数据"
- 想加一个公有领域译本（如英文 WEB、KJV）做对照
- 数据库损坏或版本升级后需要重建
- 不适用：要处理仍在版权期内的译本（本技能明确拒绝）；要翻译或解释经文。

## 输入与输出

输入：

- 必需：USFX XML 源文件路径（`--src`）、输出数据库路径（`--out`）、版本缩写（`--abbr`，如 CUVS1919）
- 可选：`--title`（中文全称）、`--license`（版权状态，默认 Public Domain）

输出：

- SQLite 数据库文件（`.bible`），含 `Verses(Book, Chapter, Verse, Scripture)` 与 `Metadata(Key, Value)` 两张表，并在 `Verses` 上建索引
- 控制台汇总：卷数、节数；解析异常计数（无法识别的章号/节号、未知书卷）

## 工作流程

1. **确认版权状态（第一步，也是硬门槛）。** 数据库里的经文一律来自源数据文件，不由模型凭记忆生成。只处理公有领域或明确自由许可的译本。仍在版权期内的译本（例如和合本修订版、新译本、现代中文译本、ESV、NIV 等）不构建、不入库、不分发。使用者若在本机为个人使用自行处理，请自行确认授权范围。
2. **取得源文件。** 公有领域译本数据集（如 djwisdom/open-bibles 仓库）提供 USFX XML，例如简体和合本 `chi-cuv-simp.usfx.xml`。下载后放在 `data/sources/`。
3. **构建。**

```bash
python scripts/build_bible_db.py \
  --src data/sources/chi-cuv-simp.usfx.xml \
  --out data/bibles/CUVS1919.bible \
  --abbr CUVS1919 \
  --title "和合本 1919（简体）" \
  --license "Public Domain"
```

4. **抽查验证。** 构建完至少核对四处：创世记 1:1、诗篇 23:1、约翰福音 3:16、启示录 22:21。抽查能发现编码、节号错位、脚注误收三类问题。
5. **接入使用。** 把数据库放到 `data/bibles/`，或设环境变量 `CHRIST_SKILLS_DATA` 指向该目录，引用校验器会自动找到它。

## 数据格式说明

- `Book` 为新教正典 1 至 66 的序号（1 创世记，66 启示录），与 biblemate 一致
- 节号为 0 的条目（部分版本的题记）在构建时跳过，保持与 biblemate 行为一致
- 脚注、交叉引用、段落标题不属于经文正文，构建时丢弃；`<wj>`（主的话）等内联标记的文本保留
- 经文文本会做空白归一，便于比对

## 经文依据

本节不适用。本技能属 neutral 级工具，不作出任何教义主张，因此没有经文依据章节的内容。

## 争议标注

不适用。本技能不评价译本优劣、不比较神学立场。正典范围（六十六卷）是本构建器的实现约定，若使用者所属传统采用更广的正典，请自行扩展书卷映射表（`scripts/bible_books.py`），本工具不作裁定。

## 质量校验清单

- [ ] 源文本确认为公有领域或自由许可，并已记录来源
- [ ] 构建输出显示 66 卷，节数在预期范围（和合本简体约 31100 节）
- [ ] 已抽查至少四处经文，内容与原文一致
- [ ] 数据库可被引用校验器正常读取
- [ ] 未把任何版权期内的译本数据写入仓库或分发

## 免责与边界

- 本技能只做格式转换，不校对译文、不改字、不修正任何文本差异。源数据有错，产出就有错。
- 版本缩写（abbr）一旦确定，后续引用标注依赖它；改名会导致既有引用指向失效，属破坏性变更。
- 数据分发时请连同来源与版权状态一起说明；本工具不为用户自行加入的数据承担授权责任。
