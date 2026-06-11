# PRD Ingestion Workflow

## 两种入口

Idea-first：

- 输入是短想法、方向、用户问题或功能描述。
- 先通过 brainstorming 和 clarify 扩展为 `spec.md`。
- 需要落盘时，在 `spec.md` 的 Source 区记录为 idea input。

PRD-first：

- 输入是完整 PRD、PRD v0/v1、产品定义稿、Samples/Eval、两图一表、原型探索总结。
- 先做 ingestion，不要直接进入 plan。
- 需要落盘时，在 `spec.md` 中保留原文快照和 traceability。

协作链快速通道——如果 PRD 来自本合集的 `prd-writer`（特征：自带 FR-###/SC-### 编号、S-## sample 编号、假设区、`[NEEDS CLARIFICATION]` 标记、"当...时会发生什么"边界句式）：

- **复用其 FR/SC 编号**，不要重新编号；traceability 直接建 `PRD-S### -> 既有 FR-###` 映射。
- 其 `[NEEDS CLARIFICATION]` 标记直接进入 clarify 候选问题，其假设区直接进入 spec 的 Assumptions。
- S-## samples 直接转 `plan.md` Quickstart 场景和 `review.md` Test Matrix 行；F-##（反哺清单）条目检查是否已被吸收。
- 模糊词检查通常可以快速通过（上游已做同词表转换），抽查即可。

## PRD-first 标准流程

1. Preserve source
   - 保存原 PRD 路径或快照。
   - 不要在归一化时覆盖原文。

2. Normalize
   - 抽取 `Background`、`Users`、`Scenarios`、`Goals`、`Non-goals`。
   - 抽取 `Functional Requirements`、`Non-functional Requirements`、`Success Criteria`。
   - 抽取 `Samples/Eval`、`Rubric`、`Metric`、`Protocol`。
   - 抽取 `Data`、`State`、`Permissions`、`Edge Cases`、`Risks`。
   - 抽取 `Prototype / Flow / State Diagram / Data Table` 信息。

3. Split or keep
   - 如果 PRD 包含多个可独立交付的用户价值，拆成多个 `specs/###-slug/`。
   - 如果多个模块共享同一 foundation，但不能独立验收，保留一个 feature pack，并在 `tasks.md` 用 phases 管理。
   - 如果 PRD 包含平台改造和产品功能，优先拆分为 platform foundation feature 和 product-facing feature。

4. Trace
   - 每个 PRD section 生成 `PRD-S###`。
   - 每个 `PRD-S###` 必须映射到：
     - `FR-###`
     - `SC-###`
     - user story
     - `TC-###`
     - task ID
     - evidence ref
     - 或明确的 `out-of-scope` / `deferred` / `duplicate`

5. Clarify
   - PRD-first 只问 blocking questions。
   - 非阻塞问题写入 assumptions、risks 或 deferred。
   - 每轮最多 5 个问题。

6. Convert Samples/Eval
   - Samples 进入 `plan.md` Quickstart 和测试场景。
   - Rubric 进入 `review.md` Test Matrix acceptance。
   - Metric 进入 `SC-###` 和 release gate。
   - Judge/Evaluator/Protocol 进入 `plan.md` Research 或 Contracts。

## PRD 拆分规则

拆分为多个 feature pack，当满足任一条件：

- 有多个互不依赖的 P0 user journeys。
- 有独立上线或回滚边界。
- 涉及不同 owner 或不同代码区域。
- 一个 PRD 同时包含平台能力、前端体验、后台配置、数据分析等差异很大的模块。

保留一个 feature pack，当满足任一条件：

- 所有用户故事共享同一个数据模型和 release gate。
- 任意单独拆出都不能独立验证用户价值。
- 需求处于早期探索，拆分会制造假确定性。

## PRD 模糊表达处理

中文 PRD 常见模糊词：

- 高效、稳定、易用、安全、灵活、完善、尽快、快速、智能、自动、优化、提升体验、体验好、可扩展、高质量。

处理方式：

- 转成 measurable `SC-###`。
- 转成 Given/When/Then acceptance。
- 如果无法转，在 spec 对应条目打 `[NEEDS CLARIFICATION: ...]` 内联标记，并写入 `review.md` Clarifications 的 blocking 或 non-blocking ambiguity。
- 采用合理默认时写入 spec 的 Assumptions，不得静默假设。

ingestion 完成后，`run-state.json` 的 `phase` 从 `ingest` 推进到 `specify`（scaffold 脚本传 `--prd` 时初始 phase 即为 `ingest`）。

## CLI

从 idea 创建：

```bash
python3 vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --name "Feature name" --version V0.1
```

从 PRD 创建：

```bash
python3 vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --prd docs/product/prd.md --version V0.1
```

PRD + 指定 feature 名：

```bash
python3 vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --name "Billing Rules" --prd docs/product/billing-prd.md --version V1.0
```
