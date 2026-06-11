---
name: vibe-coding-spec
description: Run any coding task through a vibe-coding workflow that combines GitHub spec-kit style spec-driven development (constitution gates, nine-category clarify, inline clarification markers), PRD ingestion with traceability, superpowers-style execution (fresh subagent per task, two-stage review, TDD, 2-5 minute steps), cross-session resume via run-state, and evidence-backed release gates. Use when the user asks to build a spec, plan a feature, fix a bug with discipline, turn an idea or full PRD document into spec/plan/tasks, define a project constitution, scaffold a feature workspace, resume an in-progress feature, combine spec-kit with superpowers, or create quality-gated AI coding workflows.
---

# Vibe Coding Spec

## 核心模型

使用这个 skill 把任何编码请求变成可追踪、可测试、可发布门禁审查、可跨 session 续跑的实现路径：

```text
Idea or PRD or Bug
  -> Constitution (versioned) + Constitution Check gates
  -> PRD source preservation / traceability
  -> Feature spec: what and why ([NEEDS CLARIFICATION] markers + Assumptions)
  -> Clarify: nine-category scan, multiple-choice questions, coverage summary
  -> Research / data model / contracts / quickstart
  -> Technical plan: how and where + Complexity Tracking
  -> Task plan: dependencies, parallel ownership, RED/GREEN, 2-5 min steps
  -> Superpower execution: worktree, fresh subagent per task, question loop,
     two-stage review, continuous execution, run-state tracking
  -> Final overall review -> structured finish (merge/PR/keep/discard)
  -> Evidence / checklist / release gate
```

这个 skill 融合三套机制：

- **spec-kit workflow**：`constitution`（版本治理 + 双重 Check gate）、`specify`（内联标记）、`clarify`（九类扫描 + 多选交互）、`plan`（Complexity Tracking）、`tasks`、`analyze`、`checklist`、`implement`、`taskstoissues`、执行状态持久化。
- **vibe-coding engineering spec**：目录边界、test matrix、evidence 三级分类、release gate、PRD ingestion + traceability。
- **superpower execution**：2-5 分钟单动作 step、fresh subagent per task、question loop、两阶段 review + final review、continuous execution、receiving-review 纪律、worktree、结构化收尾。

## 默认流程

1. **分类请求**（按请求规模选路径，不是所有任务都走完整 lifecycle）
   - **默认原则**：使用 skill 时必须做需求/计划/任务/验证审查，但默认不要在用户项目里生成文件；先在对话中给出检查结论、缺口、执行计划和验证证据。
   - **新功能 / 复杂改动**：默认走内存态轻量审查 `spec review -> plan review -> task review -> implement`；高风险、跨模块、外部契约、发布门禁或用户明确要求严格治理时，再升级为完整 `spec -> clarify -> research/data/contracts -> plan -> tasks -> analyze -> implement -> review -> gate`。
   - **完整 PRD**：先在内存中做 `source -> traceability -> normalize/split -> spec`；只有用户要求持久化时，才把 PRD 来源和 traceability 合并写入 `spec.md`。
   - **Bug 修复**：走 systematic debugging 轻量路径（复现 -> 根因 -> 单任务 RED/GREEN）；根因揭示架构问题时升级为 feature。见 `references/review-finish-debug-workflow.md`。
   - **小改动（1-2 个文件、行为明确）**：直接用单任务模板（失败测试 -> 最小实现 -> 验证 -> commit），不生成 spec pack；但 constitution 和 evidence 规则仍适用。
   - **架构或规范**：生成或更新 constitution（用 `references/constitution-template.md` 引导，遵循版本治理）。
   - **已有计划的实现**：转换为 superpower-style execution plan。
   - **续跑进行中的 feature**：读 `run-state.json` 走 resume 协议，见 `references/execution-state-and-resume.md`。
   - **Review**：检查目录边界、constitution 合规、测试矩阵、证据、release gate。

2. **锚定 constitution**
   - 如果项目已有 `.specify/memory/constitution.md`、`AGENTS.md`、`CLAUDE.md`、`docs/specs/`、legacy `quality/`，先读现有规范并保留本地约定。
   - 没有 constitution 时，用 `references/constitution-template.md` **引导用户生成**项目自己的 constitution（项目无关模板 + semver 版本治理），不要默认套用特定架构。
   - 平台网关 / 多 adapter 类项目可套用 platform-gateway preset：`references/vibe-engineering-constitution.md`。
   - 轻量模式在 plan 中记录相关项目约定即可；完整治理模式必须执行两次 Constitution Check gate（pre-research、post-design），违规必须进 Complexity Tracking 表书面辩护。

3. **生成或更新 feature artifacts**
   - 默认不生成 artifacts；审查内容先留在对话和最终报告中。
   - 只有在用户明确要求“生成规格包/落盘/可续跑/可审计/release gate”，或任务复杂到需要跨 session 状态时，才使用脚本生成 artifacts。
   - 手动轻量包创建 `spec.md`、`plan.md`、`tasks.md`、`run-state.json`。
   - PRD 输入时不额外创建目录；来源摘要、原文快照和 `PRD-S### -> FR/SC/User Story/TC/Task/Evidence` 映射合并写入 `spec.md`。
   - `run-state.json`：phase、任务进度、最近验证结果——跨 session 续跑锚点。
   - `spec.md`：what/why、users、P1/P2/P3 user stories（每个独立可交付）、requirements、non-goals、acceptance criteria、**Assumptions**（描述不足时采用的合理默认）、**Edge Cases**（"What happens when..."句式）；未解决歧义打 `[NEEDS CLARIFICATION: ...]` 内联标记。
   - `plan.md`：技术上下文、范围决策、实现路径、验证命令、风险。
   - `tasks.md`：phase、dependency、parallel ownership、`[P]` 标记、RED/GREEN、2-5 分钟 step、commit point。
   - 完整治理包（脚本加 `--full`）仍使用 compact SDD 文件：
   - `review.md`：clarify、checklist、test matrix、test report、release gate 合并在一个审查文件里。
   - `evidence/`：保存 release gate 引用的证据材料。
   - 审计包（脚本加 `--audit`）在 compact SDD 基础上增加 `audit/traceability.md`、`audit/test-matrix.md`、`audit/release-gate.md`、`audit/decision-log.md`，只用于合规、审计和正式发布。
   - plan 定稿后把长期技术决策增量同步到 agent context 文件（CLAUDE.md/AGENTS.md 的 auto-managed 区块）。

4. **使用 superpower 执行纪律**
   - **Brainstorming HARD-GATE**：设计未呈现并获用户批准前不写任何代码——对每个项目适用，无论多简单；澄清一次一问，方案给 2-3 个带 trade-offs 的选项。
   - **Pre-flight 门禁**（进入 implement 前）：分支保护（未经同意不在 main/master 上实现）、checklist 完成度扫描（有未完成项暂停要用户确认）、blocking clarification 清零、constitution gate 有记录、baseline 验证。
   - 任务必须可逐项执行；写 plan 时假设执行者对代码库零上下文且品味存疑。
   - 一个 step = 一个动作 = 2-5 分钟；代码变更任务必须包含 expected RED failure 和 GREEN pass。
   - 每个任务写清 exact files、commands、expected output、evidence refs。
   - 可并行任务必须标记 `[P]`，且有 disjoint owned files。
   - 多 agent 执行：每任务派 fresh subagent（用 `references/prompts/` 模板）、开工前 question loop、逐任务两阶段 review（spec -> quality）、全部完成后 final overall review；主 agent 负责整合、冲突处理、最终 fresh verification。环境不支持 subagent 时退化为顺序自执行模式（先批判性 review plan 再开工）。
   - **Continuous execution**：implement 阶段任务之间不向用户请求确认，只在 BLOCKED、真歧义或全部完成时停。
   - **失败隔离**：顺序任务失败立即 halt；`[P]` 组内失败不拖累其他并行任务；同一任务修两次仍失败转 systematic debugging。
   - 用 `- [ ]` / `- [x]` 追踪状态，并同步更新 `run-state.json`。

5. **用证据收尾**
   - 在当前执行 session 里运行 fresh verification 后，才能说完成、通过、修复、可发布。
   - 报告 tests run、evidence paths、untested scope、residual risks。
   - 收尾必须向用户呈现结构化选项：merge / PR / keep / discard，并按选项清理 worktree。
   - release gate 未通过时，不得声称 release-ready。

## 何时加载 References

- 端到端 lifecycle 和 artifact map：读 `references/spec-kit-superpower-workflow.md`。
- 完整 PRD 输入、PRD 拆分、source traceability：读 `references/prd-ingestion-workflow.md`。
- 生成或修订 constitution、版本治理：读 `references/constitution-template.md`。
- 平台网关类项目的目录、platform、adapter 规则（preset）：读 `references/vibe-engineering-constitution.md`。
- clarify 九类扫描、analyze、checklist 两层结构、hooks/presets/extensions：读 `references/clarify-analyze-checklist-workflow.md`。
- 生成领域需求质量 checklist（CHK 条目、句式规则、校准问题）：读 `references/checklist-authoring-workflow.md`。
- plan/task 强格式、Constitution Check gate、Complexity Tracking、任务粒度：读 `references/superpower-plan-template.md`。
- 多子 agent、question loop、两阶段 review、parallel ownership、worktree 隔离：读 `references/subagent-execution-workflow.md`。
- 派发 subagent 的 prompt 模板：读 `references/prompts/`（implementer / spec-reviewer / code-quality-reviewer）。
- review 意见处理纪律、结构化收尾、bug 修复轻量路径、systematic debugging：读 `references/review-finish-debug-workflow.md`。
- 跨 session 续跑、run-state、agent context 同步、tasks 导出 issues：读 `references/execution-state-and-resume.md`。
- release gate、test matrix、evidence：读 `references/quality-gate-template.md`。

## Scripts

只有用户明确要求落盘规格包、跨 session 续跑、审计链路、release gate，或已有 artifacts 需要一致性分析时，才使用脚本：

```bash
python3 scripts/scaffold_vibe_feature.py --root . --name "feature name" --version V0.1
python3 scripts/scaffold_vibe_feature.py --root . --prd docs/product/prd.md --version V0.1
python3 scripts/scaffold_vibe_feature.py --root . --name "feature name" --version V0.1 --full
python3 scripts/scaffold_vibe_feature.py --root . --name "feature name" --version V0.1 --audit
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1 --profile full
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1 --profile audit
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1 --write-checklist
```

`scaffold_vibe_feature.py` 默认创建轻量 `specs/###-feature-name/`：`spec.md`、`plan.md`、`tasks.md`、`run-state.json`。传入 `--prd` 时把 PRD source 和 traceability 合并写入 `spec.md`。传入 `--full` 时额外创建 `review.md` 和 `evidence/`。传入 `--audit` 时额外创建 `audit/` 四文件审计包。脚本不覆盖已有文件。

`check_vibe_structure.py` 检查推荐目录，并分析 artifacts。默认 `--profile auto`：存在 `audit/` 时按 audit 检查，存在 `review.md` 或 legacy 完整治理文件时按 full 检查，否则按 lite 检查。lite 只强制 `spec.md`、`plan.md`、`tasks.md`、`run-state.json`；full 会额外检查 `review.md`、Constitution Check gate 和 Complexity Tracking；audit 会额外检查 `audit/` 四文件。需要机器消费时加 `--json`。

## Output Rules

- Frontmatter `description` 使用英文；正文可以中文；artifact 字段、文件名、ID、命令保持英文标准化。
- spec 阶段保持 implementation-neutral；plan 阶段才写技术实现。
- spec 中未解决的歧义必须打 `[NEEDS CLARIFICATION: ...]` 内联标记；clarify 消费这些标记，回答后移除标记并回写正文。
- 描述不足时采用的合理默认必须写入 spec 的 Assumptions，不得静默假设。
- PRD-first 输入需要落盘时，必须在 `spec.md` 中保留 source snapshot 和 traceability 映射。
- 完整 PRD 包含多个独立交付价值时，先拆 feature pack，再分别 plan/tasks。
- 默认使用 `specs/###-feature-name/`，除非项目已有更强约定。
- plan 必须记录两次 Constitution Check 结果；存在违规而无 Complexity Tracking 辩护时，analyze 按 CRITICAL 处理。
- P0 行为必须有 `review.md` test matrix 行、task、evidence ref。
- requirement IDs 必须映射到 task IDs、test case IDs、evidence refs。
- evidence type 必须区分 `artifact`、`capture`、`true-integration`。
- 完成、通过、修复、可发布等结论必须引用 fresh verification；evidence before claims。
- 阶段推进和任务完成必须同步 `run-state.json`；新 session 接手时先走 resume 协议再动手。
- 临时实验不得放进 `src/` 或 `platform/`；使用 `tmp/`、`specs/<feature>/evidence/` 或 `docs/archive/`。
- 请求 release readiness 时，必须显式评估 `review.md` 的 release gate。
- 收到 review 意见时遵循 receiving-review 纪律：存疑先验证，不盲改，不性能化附和。
- 收尾时必须呈现 merge / PR / keep / discard 四个结构化选项，由用户决定。
- 设计未获用户批准前不得进入实现（brainstorming HARD-GATE）；"太简单不需要设计"是反模式。
- implement 开工前必须通过 Pre-flight 门禁；checklist 有未完成项时只有用户明确确认才放行。
- 需求质量 checklist 条目必须是检验需求的问题句（带 CHK 编号、质量维度标签、traceability 引用），禁止实现导向句式。
- 未经用户明确同意，不得在 main/master 分支上开始实现。
