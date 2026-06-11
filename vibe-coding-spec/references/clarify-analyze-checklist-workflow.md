# Clarify / Analyze / Checklist Workflow

## Clarify 工作流

在进入 `plan.md` 前先处理澄清问题。

规则：

- 每轮最多问 5 个问题。
- 问题必须能改变规格、计划、任务或 release gate；不要问偏好型闲聊问题。
- 只有这些问题阻塞 plan：
  - 数据模型或状态转换不清楚。
  - 安全、隐私、权限、审计、密钥处理不清楚。
  - 不可逆 UX 或破坏性操作不清楚。
  - 外部 API、事件、文件格式、adapter contract 不清楚。
  - P0 acceptance、evidence type、release gate 不清楚。
- 非阻塞问题写入 `clarify.md` 的 Open Questions，可以进入 plan，但必须在风险里标注。
- 已回答问题写入 `clarify.md` 的 Resolved Clarifications，并回填到受影响 artifact：
  - 需求变更回填 `spec.md`
  - 技术决策回填 `plan.md`
  - 任务顺序回填 `tasks.md`
  - 验证要求回填 `TEST_MATRIX.md` 或 `RELEASE_GATE.md`

## Analyze 工作流

实现前运行 analyzer：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version>
```

需要机器消费时：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version> --json
```

需要刷新 checklist 时：

```bash
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature <###-slug> --version <version> --write-checklist
```

处理顺序：

1. 先修 CRITICAL 和 HIGH。
2. MEDIUM 可以带风险进入实现，但必须在 final report 说明。
3. LOW 是结构建议，不应阻塞 spike；release readiness 时需要解释。

## Checklist 规则

`CHECKLIST.md` 是需求质量的单元测试，不是项目待办。

必须覆盖：

- 规格是否没有占位符。
- user stories 是否可独立测试。
- acceptance 是否可验证。
- plan 是否引用 `research.md`、`data-model.md`、`contracts/`、`quickstart.md`。
- tasks 是否有 dependency、parallel ownership、RED/GREEN、evidence。
- P0 是否映射到 TC 和 evidence ref。

## Hooks / Presets / Extensions

模板优先级：

```text
.specify/templates/overrides/
  > .specify/presets/templates/
  > .specify/extensions/templates/
  > skill fallback templates
```

`overrides` 用于单项目定制；`presets` 用于组织或领域模板；`extensions` 用于新增阶段或外部系统集成。

`.specify/extensions.yml` 可声明 hooks：

```yaml
hooks:
  before_analyze:
    - extension: security-review
      command: security.check
      description: Check secret handling before artifact analysis
      optional: false
  after_analyze:
    - extension: issue-export
      command: issues.create
      description: Export high findings as tracker issues
      optional: true
```

当前脚本只报告 hooks 存在与否，不执行 hooks。真正执行 hook 前必须明确知道对应命令和权限边界。
