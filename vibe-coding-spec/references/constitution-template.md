# Constitution Template

项目无关的 constitution 模板。当项目没有 `.specify/memory/constitution.md` 时，用这个模板**引导用户生成**，而不是默认套用某种特定架构。

## 生成流程

1. 询问项目类型（CLI / web 前端 / 后端服务 / 平台网关 / 数据管线 / 库 / 移动端 / 混合）。
2. 询问 3-7 条不可妥协的工程原则（测试要求、目录哲学、依赖政策、安全基线、性能底线）。
3. 如果是平台网关 / 多 client 多 provider 类项目，建议套用 platform-gateway preset（见 `vibe-engineering-constitution.md`）作为起点。
4. 用下面的模板生成 `.specify/memory/constitution.md`，版本号从 `1.0.0` 开始。

## 模板

```markdown
# <Project Name> Constitution

## Core Principles

### P1: <原则名，如 Test-First>
<规则正文。用 MUST / MUST NOT 表述，写明可检查的判定标准。>

### P2: <原则名，如 Directory by Responsibility>
<规则正文。>

### P3: <原则名，如 No Speculative Abstraction>
<规则正文。>

<按需增加 P4-P7。原则数量保持在 3-7 条；超过 7 条说明混入了普通规范，应下沉到 docs/。>

## Additional Constraints

<技术栈约束、合规要求、依赖政策等次级约束。>

## Development Workflow

<review 要求、质量门禁、发布流程的硬性要求。>

## Governance

- 本 constitution 优先级高于其他一切实践文档。
- 所有 plan 必须通过 Constitution Check（pre-research 和 post-design 两个 gate）。
- 违反任何原则必须在 plan 的 Complexity Tracking 表中书面辩护：违反哪条、为何本功能必须违反、为何更简单的替代方案被拒绝。
- 所有 PR / review 必须验证合规。
- 修订程序：修订必须以 PR 形式提出，写明动机和影响范围，获得批准后合入；合入时更新版本号和 Last Amended。

**Version:** 1.0.0 | **Ratified:** <YYYY-MM-DD> | **Last Amended:** <YYYY-MM-DD>
```

## 版本规则

constitution 使用 semantic versioning：

- **MAJOR**：删除或反向改写某条原则（之前禁止的变成允许）。
- **MINOR**：新增原则，或对既有原则做实质性扩充。
- **PATCH**：措辞澄清、错别字、不改变语义的整理。

每次修订必须：

1. 更新 `Version` 和 `Last Amended`。
2. 在 commit message 或 PR 描述中写 **Sync Impact Report**：哪些原则变了、哪些下游 artifact（plan 模板、checklist、进行中的 feature plan）需要同步检查。
3. 检查进行中 feature 的 plan 是否因新规则产生新的 Constitution Check 违规。

## 与本 skill 的关系

- plan 阶段的 Constitution Check gate 读取的就是这份文件（见 `superpower-plan-template.md`）。
- analyze 阶段检查 Complexity Tracking 表是否覆盖所有违规（见 `clarify-analyze-checklist-workflow.md`）。
- release gate 评估时，未辩护的 constitution 违规视为 gate 不通过。
