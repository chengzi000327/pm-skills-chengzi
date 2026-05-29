# Agent / AI 类 PRD 模板

适用于涉及 LLM、意图识别、多轮对话、工具调用、自动化执行、AI 评测的功能。

## 必写章节

### 4. 流程定义

先画流程图,再写节点说明表。节点要区分工程节点、LLM 节点、工具节点、判断节点、异常节点。

| Node | 类型 | 触发条件 | 输入 | 输出 | 成功流转 | 失败/异常流转 |
| --- | --- | --- | --- | --- | --- | --- |
| 等待用户输入 | 工程 | 新任务/补充输入 | user_message | task_context | 读取 State | 输入为空则提示 |
| 意图识别 | LLM | 收到输入 | message + memory | intent | 进入对应技能 | reject / clarify |
| 工具执行 | 工程 | 技能需要数据 | tool params | tool result | 生成结果 | 工具失败兜底 |
| END | 工程 | 完成/拒绝/升级 | final output | state update | 结束 | 记录失败 |

### 5. Agent State 设计

State 是流程流转核心,所有节点都读写它。

| 分类 | 字段 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 基础 | trace_id | string | 是 | 自动生成 | 链路追踪 ID |
| 基础 | user_id | string | 是 | - | 用户 ID |
| 回合状态 | intent | string | 是 | unknown | 当前意图 |
| 回合状态 | need_clarification | boolean | 是 | false | 是否需要用户补充 |
| 执行控制 | max_transitions_per_turn | integer | 是 | 10 | 防死循环 |
| 风险 | risk_level | enum | 是 | low | low/medium/high |

### 6. LLM 节点说明

每个 LLM 节点单独写:

| 项 | 必写内容 |
| --- | --- |
| 用途 | 节点做什么,在哪个流程调用 |
| 输入 | system、历史记忆、参考数据、用户输入、工具结果 |
| 输出 | 格式、字段、真实示例 |
| 解析 | 如何解析,解析失败怎么处理 |
| 限制 | 不得编造、不得越权、模糊时如何兜底 |
| 重试 | 重试次数、重试条件、失败后状态 |
| 评测 | 对应 sample、rubric、metric |

### 7. Prompt 设计

先列 Prompt 汇总表:

| Prompt 名称 | 用途 | 调用节点 | 模型 | 输出格式 | 关键风险 |
| --- | --- | --- | --- | --- | --- |

每个 Prompt 展开:

```text
### [Prompt 名称]

用途:

System Prompt 结构:
1. 角色定义
2. 任务目标
3. 判断逻辑 / 优先级
4. Few-shot 示例
5. 输出格式约束
6. 限制 & 兜底

输入 Message 构成:
| role | 内容 | 说明 |

输出格式:
[给真实示例,不要只写 JSON]

解析方式:
[伪代码或规则]

边界 & 限制:
- 输出为空
- 格式异常
- 输入缺字段
- 多轮上下文冲突
```

### 8. 工具 / 技能调用

| 工具名 | 用途 | 触发条件 | 输入参数 | 输出 | 失败处理 |
| --- | --- | --- | --- | --- | --- |

必须写:

- 参数校验。
- 权限校验。
- 超时和重试。
- 幂等策略。
- 工具结果如何进入下一轮 LLM。

### 9. 异常与兜底

区分业务异常和系统异常:

| 异常 | 类型 | 触发条件 | 用户反馈 | 系统处理 | 是否可重试 |
| --- | --- | --- | --- | --- | --- |
| 缺少必要信息 | 业务 | order_id 为空 | 提示补充订单 | 状态 NEED_INFO | 是 |
| 模型超时 | 系统 | LLM timeout | 生成失败,可重试 | 记录 error_code | 是 |
| 高风险 | 业务/合规 | risk_level=high | 建议升级人工 | 禁用采纳 | 否 |

### 10. Eval

必须写 eval answer 和 eval trace:

- eval answer:最终回复是否准确、安全、完整、可执行。
- eval trace:工具、参数、状态、分支、失败恢复是否正确。

参考 `metrics-acceptance-tracking-tests.md` 写验收、埋点和测试集。
