---
name: vibe-coding-spec
description: Create or review a vibe-coding workflow that combines GitHub spec-kit style spec-driven development, PRD ingestion, directory/platform architecture rules, automated testing matrices, release gates, and superpower-style execution plans. Use when the user asks to build a spec, plan a feature, turn an idea or full PRD document into spec/plan/tasks, define a project convention, scaffold a feature workspace, combine spec-kit with superpowers, or create quality-gated AI coding workflows.
---

# Vibe Coding Spec

## 核心模型

使用这个 skill 把想法变成可追踪、可测试、可发布门禁审查的实现路径：

```text
Idea or PRD
  -> Constitution / engineering rules
  -> PRD source preservation / traceability
  -> Feature spec: what and why
  -> Clarify: open and resolved questions
  -> Research / data model / contracts / quickstart
  -> Technical plan: how and where
  -> Task plan: dependencies, parallel ownership, RED/GREEN steps
  -> Superpower execution: worktree, subagents, review
  -> Evidence / checklist / release gate
```

这个 skill 融合三套机制：

- **spec-kit workflow**：`constitution`、`specify`、`clarify`、`plan`、`tasks`、`analyze`、`checklist`、`implement`。
- **vibe-coding engineering spec**：目录边界、platform core、client/provider adapters、test matrix、evidence、release gate。
- **superpower execution plans**：明确文件、失败测试优先、fresh verification、worktree、subagent、review、finish branch。

## 默认流程

1. **分类请求**
   - 新功能：走完整 `spec -> clarify -> research/data/contracts -> plan -> tasks -> analyze -> implement`。
   - 完整 PRD：先走 `prd-source -> traceability -> normalize/split -> spec`，再进入 plan。
   - 架构或规范：生成或更新 constitution / engineering rules。
   - 已有计划的实现：转换为 superpower-style execution plan。
   - Review：检查目录边界、adapter 影响、测试矩阵、证据、release gate。

2. **锚定 constitution**
   - 默认应用 `references/vibe-engineering-constitution.md`。
   - 如果项目已有 `.specify/memory/constitution.md`、`AGENTS.md`、`CLAUDE.md`、`docs/specs/`、`quality/`，先读现有规范并保留本地约定。

3. **生成或更新 feature artifacts**
   - `prd-source.md`：保留 idea/PRD 原文、source index。
   - `traceability.md`：`PRD-S### -> FR/SC/User Story/TC/Task/Evidence`。
   - `spec.md`：what/why、users、requirements、non-goals、acceptance criteria。
   - `clarify.md`：open questions、blocking questions、resolved clarifications、impacted artifact。
   - `research.md`：技术调研问题、决策、替代方案。
   - `data-model.md`：entities、fields、relationships、state transitions。
   - `contracts/`：外部 API、事件、CLI、文件格式、adapter contract。
   - `quickstart.md`：运行和验证步骤。
   - `plan.md`：架构、目录影响、adapter 影响、测试策略、证据策略。
   - `tasks.md`：phase、dependency、parallel ownership、`[P]` 标记、RED/GREEN、evidence、commit point。
   - `CHECKLIST.md`、`TEST_MATRIX.md`、`TEST_REPORT.md`、`RELEASE_GATE.md`：质量检查、测试矩阵、报告和发布门禁。

4. **使用 superpower 执行纪律**
   - 任务必须可逐项执行。
   - 代码变更任务必须包含 expected RED failure 和 GREEN pass。
   - 每个任务写清 exact files、commands、expected output、evidence refs。
   - 可并行任务必须标记 `[P]`，且有 disjoint owned files。
   - 多 agent 执行时，主 agent 负责整合、冲突处理、最终 fresh verification。
   - 用 `- [ ]` / `- [x]` 追踪状态。

5. **用证据收尾**
   - 在当前执行 session 里运行 fresh verification 后，才能说完成、通过、修复、可发布。
   - 报告 tests run、evidence paths、untested scope、residual risks。
   - release gate 未通过时，不得声称 release-ready。

## 何时加载 References

- 端到端 lifecycle 和 artifact map：读 `references/spec-kit-superpower-workflow.md`。
- 完整 PRD 输入、PRD 拆分、source traceability：读 `references/prd-ingestion-workflow.md`。
- 目录、platform、adapter、governance 规则：读 `references/vibe-engineering-constitution.md`。
- clarify、analyze、checklist、hooks/presets/extensions：读 `references/clarify-analyze-checklist-workflow.md`。
- plan/task 强格式：读 `references/superpower-plan-template.md`。
- 多子 agent、parallel ownership、worktree 隔离：读 `references/subagent-execution-workflow.md`。
- review、finish branch、systematic debugging：读 `references/review-finish-debug-workflow.md`。
- release gate、test matrix、evidence：读 `references/quality-gate-template.md`。

## Scripts

需要生成文件或做一致性分析时使用脚本：

```bash
python3 scripts/scaffold_vibe_feature.py --root . --name "feature name" --version V0.1
python3 scripts/scaffold_vibe_feature.py --root . --prd docs/product/prd.md --version V0.1
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1
python3 scripts/check_vibe_structure.py --root . --feature 001-feature-name --version V0.1 --write-checklist
```

`scaffold_vibe_feature.py` 创建 `specs/###-feature-name/`、`quality/<version>/`、`.specify/templates/overrides/`、`.specify/presets/templates/`、`.specify/extensions/templates/`。传入 `--prd` 时会额外生成 `prd-source.md` 和 `traceability.md`。脚本不覆盖已有文件。

`check_vibe_structure.py` 检查推荐目录，并分析 `prd-source.md`、`traceability.md`、`spec.md`、`clarify.md`、`research.md`、`data-model.md`、`contracts/`、`quickstart.md`、`CHECKLIST.md`、`plan.md`、`tasks.md`、`TEST_MATRIX.md`、`RELEASE_GATE.md` 的覆盖关系。需要机器消费时加 `--json`。

## Output Rules

- Frontmatter `description` 使用英文；正文可以中文；artifact 字段、文件名、ID、命令保持英文标准化。
- spec 阶段保持 implementation-neutral；plan 阶段才写技术实现。
- PRD-first 输入必须保留 `prd-source.md`，并用 `traceability.md` 映射每个 `PRD-S###`。
- 完整 PRD 包含多个独立交付价值时，先拆 feature pack，再分别 plan/tasks。
- 默认使用 `specs/###-feature-name/`，除非项目已有更强约定。
- 模板优先级：`.specify/templates/overrides/` > `.specify/presets/templates/` > `.specify/extensions/templates/` > skill fallback。
- P0 行为必须有 `TEST_MATRIX.md` 行、task、evidence ref。
- requirement IDs 必须映射到 task IDs、test case IDs、evidence refs。
- evidence type 必须区分 `artifact`、`capture`、`true-integration`。
- 完成、通过、修复、可发布等结论必须引用 fresh verification；evidence before claims。
- 临时实验不得放进 `src/` 或 `platform/`；使用 `tmp/`、`quality/<version>/evidence/` 或 `docs/archive/`。
- 请求 release readiness 时，必须显式评估 `RELEASE_GATE.md`。
