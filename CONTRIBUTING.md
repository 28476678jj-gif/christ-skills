# 贡献指南

欢迎共建。这个库的特殊性在于：它生产的是影响人信仰的内容，所以流程比一般代码仓库多几道闸。请把这看作对读者的责任，而不是门槛表演。

## 开始之前

按顺序读四份锚点文件：`STATEMENT_OF_FAITH.md`、`DOCTRINE_POLICY.md`、`CITATION_STANDARD.md`、`GLOSSARY.md`。你的贡献必须能在它们的框架内存活。

## 新增一个技能

1. **选类目。** 查 `taxonomy.md`，确认技能归属的一级与二级类目。类目不存在时，先在 issue 里按 taxonomy 的提案流程讨论，不要直接在 PR 里新开类目。
2. **复制模板。** 从 `templates/SKILL_TEMPLATE.md` 开始填。frontmatter 所有必填字段写全，特别是 `doctrine_status`、`sources`、`bible_anchor`。
3. **写内容。** 守住三条引用铁律（见 `CITATION_STANDARD.md`）：不凭记忆引经、不断章取义、不拼接改装。行文中译本标注齐全。
4. **过机器校验（本地跑通再提 PR）。**

```bash
python tools/lint_skill.py skills/<类目>/<你的技能>
python tools/verse_check.py skills/<类目>/<你的技能>/SKILL.md
```

5. **提 PR，填「教义影响声明」**（PR 模板内置）：

```
- 本技能触及的教义级别：core / disputed / sensitive
- 涉及的争议议题及处理方式：（争议级必填，说明并列了哪些立场）
- 敏感类目自查：（敏感级必填，说明免责边界、是否含当代团体评价）
- 我确认所有经文引用已通过 verse_check 核验：是 / 否
```

6. **审核。**
   - core 级：维护者审核，与信经冲突直接拒收。
   - disputed 级：维护者加一名复核人，复核人记录进 `reviewed_by`。
   - sensitive 级：必须具名人类审核，AI 审核不算数；`reviewed_by`、`reviewed_at` 缺一不合并。

## 修改现有技能

- 修正错别字、格式：直接 PR，注明 patch。
- 实质内容修改：按该技能的 `doctrine_status` 走对应审核级别。
- 修改后必须更新 frontmatter 的 `reviewed_at`；敏感类目还必须更新 `reviewed_by`。

## 数据与版权

- 只接受公有领域或明确自由许可的文本数据入库，提交时在 PR 里附版权依据链接。
- 现代出版物（在世作者的注释书、版权译本）只可少量引用并注明出处，不得整章整卷搬运。
- 不确定版权状态时，默认不放进来，先在 issue 里问。

## 安全

- 不接受携带可执行脚本的技能（技能应主要是提示词与文档；确需辅助脚本，放该技能 `scripts/` 内并在 PR 说明用途）。
- 所有外部 PR 会经过恶意代码扫描（SkillSpector）与人工过目，夹带混淆代码、外联下载、凭证读取的内容一律拒收。

## 行为约定

讨论聚焦于"怎么更符合圣经、怎么更清楚"，不做人身评价，不展开宗派优劣之争。争议级议题的 PR 讨论区尤其如此：呈现最强论证，不扣帽子。
