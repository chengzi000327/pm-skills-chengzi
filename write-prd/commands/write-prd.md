---
name: write-prd
description: 通过链式调用问题框架、需求定义和故事拆分，生成一份可用于决策的 PRD。
argument-hint: "<功能、计划或产品变更>"
uses:
  - problem-statement
  - proto-persona
  - user-story
  - user-story-splitting
outputs:
  - 结构化 PRD
  - 核心用户画像与需求
  - 可执行的初始用户故事
---

# /write-prd

从策略到交付，生成一份流程清晰的 PRD。

## 调用方式

```text
/write-prd 客服团队收件箱重新设计，目标是加快工单分流效率
```

## 工作流

1. 使用 `problem-statement` 定义问题上下文。
2. 使用 `proto-persona` 对齐用户假设。
3. 基于以上信息直接生成完整 PRD 文档。
4. 使用 `user-story` 起草初始用户故事。
5. 使用 `user-story-splitting` 拆分较大的故事条目。

## 关键检查点

- 在写需求之前，先验证范围边界。
- 确保成功指标可衡量，并与结果指标挂钩。
- 在风险部分至少指出一个反模式。

## 后续步骤

- 运行 `/plan-roadmap` 来排期交付顺序。
- 若范围超出当前资源，运行 `/prioritize` 做优先级排序。
