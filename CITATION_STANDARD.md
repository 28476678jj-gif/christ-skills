# 经文引用规范

本规范统一全库的经文引用写法、译本标注与核验流程。`tools/verse_check.py` 按本规范执行机器校验，校验不过的提交不得合并。

## 三条铁律

1. **禁止凭记忆引用经文。** 凡写入技能、文档、示例的经文，必须来自检索结果（本库数据库 `data/bibles/CUVS1919.bible` 或用户本地 biblemate 数据库），不得凭记忆默写。
2. **禁止断章取义。** 引用不得省略改变原意的上下文；引半节经文时必须确认语意完整。
3. **禁止拼接改装。** 不得把不同经节的字句拼成"一节"，不得在引文内增删字词。转述可以，但转述不得加引号、不得写成经文样式。

## 引用格式

- 完整格式：`书卷全名 章:节`，例如 `约翰福音 3:16`。章与节之间用半角冒号。
- 连续多节：`约翰福音 3:16-18`；跨章：`使徒行传 2:1-4:37` 或分段列出。
- 同一篇内容中，同一书卷再次引用可用规范简称：`约 3:16`。
- 多卷并列用顿号或分号：`诗篇 23:1；约翰福音 10:11`。
- 引文后标注译本，置于括号内：（和合本）。本库基准译本为**和合本 1919 简体（CUVS1919）**，省略标注时默认识别为和合本；引用任何其他译本（包括公有领域的 KJV、WEB，或使用者本地的版权译本）必须显式标注。

## 六十六卷规范名称对照表

书卷映射的权威数据以 `tools/bible_books.py` 为准（机器校验使用同一映射），本表为人工阅读版。

| 序号 | 中文全名 | 规范简称 | 英文 | USFX |
|---|---|---|---|---|
| 1 | 创世记 | 创 | Genesis | GEN |
| 2 | 出埃及记 | 出 | Exodus | EXO |
| 3 | 利未记 | 利 | Leviticus | LEV |
| 4 | 民数记 | 民 | Numbers | NUM |
| 5 | 申命记 | 申 | Deuteronomy | DEU |
| 6 | 约书亚记 | 书 | Joshua | JOS |
| 7 | 士师记 | 士 | Judges | JDG |
| 8 | 路得记 | 得 | Ruth | RUT |
| 9 | 撒母耳记上 | 撒上 | 1 Samuel | 1SA |
| 10 | 撒母耳记下 | 撒下 | 2 Samuel | 2SA |
| 11 | 列王纪上 | 王上 | 1 Kings | 1KI |
| 12 | 列王纪下 | 王下 | 2 Kings | 2KI |
| 13 | 历代志上 | 代上 | 1 Chronicles | 1CH |
| 14 | 历代志下 | 代下 | 2 Chronicles | 2CH |
| 15 | 以斯拉记 | 拉 | Ezra | EZR |
| 16 | 尼希米记 | 尼 | Nehemiah | NEH |
| 17 | 以斯帖记 | 斯 | Esther | EST |
| 18 | 约伯记 | 伯 | Job | JOB |
| 19 | 诗篇 | 诗 | Psalms | PSA |
| 20 | 箴言 | 箴 | Proverbs | PRO |
| 21 | 传道书 | 传 | Ecclesiastes | ECC |
| 22 | 雅歌 | 歌 | Song of Solomon | SNG |
| 23 | 以赛亚书 | 赛 | Isaiah | ISA |
| 24 | 耶利米书 | 耶 | Jeremiah | JER |
| 25 | 耶利米哀歌 | 哀 | Lamentations | LAM |
| 26 | 以西结书 | 结 | Ezekiel | EZK |
| 27 | 但以理书 | 但 | Daniel | DAN |
| 28 | 何西阿书 | 何 | Hosea | HOS |
| 29 | 约珥书 | 珥 | Joel | JOL |
| 30 | 阿摩司书 | 摩 | Amos | AMO |
| 31 | 俄巴底亚书 | 俄 | Obadiah | OBA |
| 32 | 约拿书 | 拿 | Jonah | JON |
| 33 | 弥迦书 | 弥 | Micah | MIC |
| 34 | 那鸿书 | 鸿 | Nahum | NAM |
| 35 | 哈巴谷书 | 哈 | Habakkuk | HAB |
| 36 | 西番雅书 | 番 | Zephaniah | ZEP |
| 37 | 哈该书 | 该 | Haggai | HAG |
| 38 | 撒迦利亚书 | 亚 | Zechariah | ZEC |
| 39 | 玛拉基书 | 玛 | Malachi | MAL |
| 40 | 马太福音 | 太 | Matthew | MAT |
| 41 | 马可福音 | 可 | Mark | MRK |
| 42 | 路加福音 | 路 | Luke | LUK |
| 43 | 约翰福音 | 约 | John | JHN |
| 44 | 使徒行传 | 徒 | Acts | ACT |
| 45 | 罗马书 | 罗 | Romans | ROM |
| 46 | 哥林多前书 | 林前 | 1 Corinthians | 1CO |
| 47 | 哥林多后书 | 林后 | 2 Corinthians | 2CO |
| 48 | 加拉太书 | 加 | Galatians | GAL |
| 49 | 以弗所书 | 弗 | Ephesians | EPH |
| 50 | 腓立比书 | 腓 | Philippians | PHP |
| 51 | 歌罗西书 | 西 | Colossians | COL |
| 52 | 帖撒罗尼迦前书 | 帖前 | 1 Thessalonians | 1TH |
| 53 | 帖撒罗尼迦后书 | 帖后 | 2 Thessalonians | 2TH |
| 54 | 提摩太前书 | 提前 | 1 Timothy | 1TI |
| 55 | 提摩太后书 | 提后 | 2 Timothy | 2TI |
| 56 | 提多书 | 多 | Titus | TIT |
| 57 | 腓利门书 | 门 | Philemon | PHM |
| 58 | 希伯来书 | 来 | Hebrews | HEB |
| 59 | 雅各书 | 雅 | James | JAS |
| 60 | 彼得前书 | 彼前 | 1 Peter | 1PE |
| 61 | 彼得后书 | 彼后 | 2 Peter | 2PE |
| 62 | 约翰一书 | 约一 | 1 John | 1JN |
| 63 | 约翰二书 | 约二 | 2 John | 2JN |
| 64 | 约翰三书 | 约三 | 3 John | 3JN |
| 65 | 犹大书 | 犹 | Jude | JUD |
| 66 | 启示录 | 启 | Revelation | REV |

## 译本标注速查

| 标注 | 全称 | 版权状态 |
|---|---|---|
| 和合本 / CUVS1919 | 和合本 1919 简体 | 公有领域，本库基准 |
| KJV | King James Version | 公有领域 |
| WEB | World English Bible | 公有领域 |
| ASV | American Standard Version 1901 | 公有领域 |

和合本修订版（RCUV）、新译本、现代中文译本、ESV、NIV 等仍在版权保护期内，**其全文数据不得进入本仓库**；使用者在本地环境引用时按本地已安装数据处理，并必须显式标注译本。
