# Changelog

记录每个版本做了什么、为什么做。给下一个维护者（人或 AI）看：
改动背后的决策都在这里，细节可顺着 commit hash 找。

## [Unreleased]

## [1.0.2] - 2026-06-11

- `vibe-coding-spec` 改为默认不落盘：优先让 agent 遵循 SDD 工作方式，
  不再把 spec-kit 工具链目录复制进用户项目。
- `scaffold_vibe_feature.py` 调整为三档：
  - 默认轻量包：`spec.md`、`plan.md`、`tasks.md`、`run-state.json`。
  - `--full` compact SDD：额外生成 `review.md` 和 `evidence/`。
  - `--audit` 审计包：额外生成 `audit/traceability.md`、`audit/test-matrix.md`、
    `audit/release-gate.md`、`audit/decision-log.md`。
- `check_vibe_structure.py` 支持 `lite` / `full` / `audit` profile，并兼容旧版 artifact 路径读取。
- 同步更新 `vibe-coding-spec` references 和 README，明确 compact SDD 与 audit pack 的边界。
- 新增 `tests/test_vibe_scaffold.py`，覆盖轻量、PRD、compact full、audit 四种脚手架输出。

## [1.0.1] - 2026-06-11

- 新增 `CLAUDE.md`（仓库级 AI 上下文：不变量、验证方法、发布流程）和本 CHANGELOG，
  作为跨会话/跨 AI 的维护记忆。
- README 安装说明更新为已发布的 npm 包用法（`npx pm-skills-chengzi install`）——
  1.0.0 包里的 README 还是发布前的 GitHub 安装写法，本版修正。

## [1.0.0] - 2026-06-11

首个 npm 发布版本。这一天完成了四件大事（按 commit 顺序）：

### 1. vibe-coding-spec 吸收 spec-kit 机制（commit `7706690`）

对照 github/spec-kit（当时版本 v0.10.1）逐项吸收：

- **clarify 重写**：九类覆盖扫描（Clear/Partial/Missing）、Impact × Uncertainty 排序、
  多选表格呈现（推荐项置顶）、逐题原子回写、coverage summary、`[NEEDS CLARIFICATION]` 内联标记。
- **plan 升级**：双重 Constitution Check gate（pre-research + post-design）、
  Complexity Tracking 违规辩护表、File Structure 先行、2-5 分钟单动作 step。
- **constitution 改造**：新增项目无关的版本化模板（semver + 修订程序）；
  原 adapter 架构 constitution 降级为 platform-gateway preset。
- **执行状态持久化**：`run-state.json` schema + 跨 session resume 协议 +
  agent context 同步 + tasks→issues 导出协议。
- **subagent 工作流**：fresh subagent per task、question loop、逐任务两阶段 review、
  final overall review、continuous execution、三个独立 prompt 模板（references/prompts/）。
- **finish 流程**：receiving-review 纪律、merge/PR/keep/discard 四选项收尾、
  worktree 清理、bug 修复轻量路径。
- 脚本同步：scaffold 生成 run-state.json，analyzer 检查 constitution gate 和 run-state 一致性。

### 2. 吸收 superpowers 剩余优点（commit `3b72945`）

对照 obra/superpowers（14 个 skill）补齐：

- **checklist 方法论**（新 reference）：需求质量问题句条目、CHK 编号、维度标签、
  禁止实现导向句式；analyzer 可检测违规句式。
- **brainstorming HARD-GATE**：设计未批准不写代码 + "太简单不需要设计"反模式 +
  2-3 方案对比 + spec self-review。
- **implement Pre-flight 门禁**：分支保护、checklist 完成度扫描、blocking clarification、
  baseline、before/after_implement hooks。
- **失败隔离** + **无 subagent 顺序自执行备用模式**。

刻意不抄的：spec-kit 的 CLI 产品生态、workflow YAML 引擎本体、
superpowers 的 gateway 触发机制（形态差异，非功能差距）。

### 3. 五个 skill 串成协作链（commit `2ea47df`）

每个 skill 写明上下游交接契约：

- product-decision → idea-to-prd：**方向交接卡**（已确认/推断/待验证三档）。
- idea-to-prd → prd-to-frontend：PRD v0 + S-## samples + 两图一表。
- prd-to-frontend → prd-writer：**F-## 反哺清单**（六类固定类型表格）。
- prd-writer → vibe-coding-spec：PRD v1（FR-###/SC-### 编号 + 假设区 + 标记），
  ingestion 有识别上游产物的快速通道（复用编号不重造）。

全链统一：`[NEEDS CLARIFICATION]` 标记、Assumptions 区、稳定编号体系。
同时修复 prd-to-frontend 目录名与 frontmatter name 不一致的 bug（commit `56b1923`），
README 从 115 行精简到 46 行。

### 4. npm 打包发布（commit `4807895`、`8defd82`）

- `package.json` + `bin/install.js`（零依赖安装器：install/uninstall/list、
  --only/--target/--dry-run、过滤 .DS_Store）。
- 发布到 npm registry：`npx pm-skills-chengzi install` 一条命令安装。
- 包主页：https://www.npmjs.com/package/pm-skills-chengzi

## [史前] 2026-05 及更早

- 五个 skill 的初版各自独立创建（见 git log `417d6fd` 之前）。
- 曾用 `.claude-plugin` 和打包 `.skill` 文件分发，后改为目录 + 手动安装，
  最终演进为 npm 安装器。
