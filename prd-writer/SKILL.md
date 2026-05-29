---
name: prd-writer
description: Use when writing a complete delivery PRD or PRD v1 from a clarified requirement, PRD v0, Samples/Eval, two diagrams and one table, prototype, frontend exploration, design, or implementation-ready feature scope. Use for Agent/AI features, backend/business logic, frontend interaction specs, technical requirement docs, and requests like "写完整 PRD", "整理成交付文档", "补齐字段/状态/异常/验收". If the user only has a rough idea, use idea-to-prd first.
---

# PRD Writer

把已经澄清过的需求、PRD v0、Samples/Eval、两图一表、前端原型或 PRD 反哺清单,整理成面向研发、测试和评审的 **PRD v1 / 交付型 PRD**。

本 skill 不负责把粗想法直接写成完整 PRD。只有目标用户、核心问题、MVP 范围、关键 sample 和成功标准基本清楚后,才继续写 PRD v1;否则先转入 `idea-to-prd`。

## 核心原则

**写给开发和测试看。** 逻辑清楚、边界写明、字段定义清晰,比文档看起来完整更重要。

**说人话,但不口语化。** 每句话都要降低理解成本,不要堆"赋能、闭环、体验升级"这类空话。

**Frontend-to-PRD。** 如果输入包含前端原型、可预览页面或 PRD 反哺清单,要把界面探索暴露出的信息架构、流程缺口、状态补充、边界条件、文案假设和指标变化吸收到完整 PRD。

**Metric 必须落到三处。** 每个核心 Metric 都要转成验收标准、埋点事件和测试集/评测集,不能只停留在指标章节。

**两图一表不是附录。** 原型草图、流程/状态图、数据表要进入 PRD v1,并被细化成页面模块、流程节点、状态规则、字段、事件、验收和测试用例。

## 工作流

1. **判断输入成熟度。** 粗想法先转 `idea-to-prd`;已有 PRD v0 / 两图一表 / 原型 / 明确业务规则时继续。
2. **识别功能类型。** 分为 Agent/AI 类、普通功能类、纯交互/前端类;混合功能以风险最高、逻辑最复杂的部分为主。
3. **读取必要 reference。** 先读通用结构,再按类型读取详细模板;涉及两图一表或 Metric 时必须读对应 reference。
4. **补齐交付细节。** 将 samples、rubric、metric、原型和流程图转成字段、状态、异常、接口、埋点、验收和测试集。
5. **输出 PRD。** 直接输出 Markdown;不清楚但可合理推断的标 `[TODO: 待确认]`,真的缺信息的标 `[待补充: 需确认 xxx]`,文末汇总。

## 输入成熟度判断

| 输入状态 | 处理方式 |
| --- | --- |
| 只有粗想法,缺目标用户/问题/范围/成功标准 | 建议先用 `idea-to-prd` 做 PRD v0 |
| 已有 PRD v0 / 产品定义稿 / Samples/Eval / 两图一表 | 继续本 skill,补齐交付细节 |
| 已有原型/界面/设计稿/PRD 反哺清单 | 继续本 skill,把界面发现转成 PRD v1 |
| 已有明确功能范围和业务规则 | 继续本 skill,写完整交付 PRD |

## 类型识别

| 类型 | 判断信号 | 先读 |
| --- | --- | --- |
| Agent / AI 类 | 涉及大模型调用、意图识别、多轮对话、工具链、自动化执行、LLM 评测 | `references/agent-ai.md` |
| 普通功能类 | 有明确业务逻辑、数据库读写、接口交互,但不涉及 LLM | `references/business-feature.md` |
| 纯交互 / 前端类 | 重点是页面设计、交互流程、视觉反馈,后端逻辑简单或已有 | `references/frontend-interaction.md` |

不确定时默认按普通功能类写,但如果有 LLM、工具调用、样本评测或 agent trace,必须按 Agent/AI 类补充相关章节。

## Reference 读取规则

每次写 PRD 都先读:

- `references/prd-v1-structure.md`:完整 PRD v1 结构、通用章节、写作风格、输出格式。
- `references/two-diagrams-one-table.md`:如何把 PRD v0 的两图一表细化到 PRD v1。只要输入出现原型草图、流程/状态图、数据表、前端原型或 PRD 反哺清单,就必须读。
- `references/metrics-acceptance-tracking-tests.md`:如何把 Metric 转成验收标准、埋点和测试集。只要输入出现 Samples/Eval、Rubric、Metric、成功标准或测试要求,就必须读。

然后按类型读一个或多个:

- `references/agent-ai.md`:Agent State、LLM 节点、Prompt、工具调用、eval answer/trace、失败兜底。
- `references/business-feature.md`:业务流程、功能点、字段、校验、状态、接口、异常 case。
- `references/frontend-interaction.md`:页面/组件、交互流程、UI 状态、文案、权限、响应式和可访问性。
- `references/flowchart-svg.md`:需要画流程图时读取。流程定义章节必须有流程图 + 节点说明表。

## 输出要求

- 直接输出 Markdown,开头不要解释流程。
- 章节最深到 `###`,除非用户明确要求更细。
- 表格用 Markdown 表格;复杂结构给真实 JSON 示例。
- 流程定义章节必须包含流程图和节点说明表。
- 文末必须有待确认清单,汇总所有 `[TODO]` 和 `[待补充]`。
