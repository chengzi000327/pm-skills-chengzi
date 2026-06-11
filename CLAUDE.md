# CLAUDE.md — 给在这个仓库工作的 AI 的上下文

这是 chengzi 的个人 Claude Code PM 技能合集，已发布为 npm 包 `pm-skills-chengzi`。
改动任何内容前先读这份文件和 `CHANGELOG.md`（完整演进史在那里）。

## 这个仓库是什么

5 个 skill 组成一条**协作链**，覆盖"产品方向判断 → 实现规格落地"：

```text
product-decision -> idea-to-prd -> prd-to-frontend -> prd-writer -> vibe-coding-spec
   方向交接卡        PRD v0+S-##     F-## 反哺清单      PRD v1        spec/plan/tasks/gate
```

每段交接有固定契约（写在各 skill 的「协作链」章节里）。`vibe-coding-spec` 是最重的一个，
融合了 GitHub spec-kit 和 obra/superpowers 两套方法论（吸收过程见 CHANGELOG 1.0.0）。

## 改动时必须维护的不变量

这些约定横跨多个文件，改一处必须同步另一处：

1. **模糊词词表**：`prd-writer/SKILL.md` 和 `vibe-coding-spec/references/prd-ingestion-workflow.md`
   使用同一份中文模糊词词表（高效/稳定/易用/安全...）。改词表两边同步。
2. **链路标记词汇**：`[NEEDS CLARIFICATION: ...]` 内联标记、Assumptions 假设区、
   确定性三档（已确认/推断/待验证）在全部 5 个 skill 中语义一致，不要单边改名。
3. **稳定编号体系**：S-##（samples）、C-##（能力）、F-##（反哺清单）、FR-###/SC-###（需求/成功标准）、
   PRD-S###（PRD 章节）、TC-###（测试用例）、T###（任务）、CHK###（checklist 条目）。
   下游按编号消费上游产物，改编号格式 = 破坏链路。
4. **skill 目录名 = frontmatter name**：曾经因为 `prd-to-frontend` 目录里写着
   `name: idea-to-frontend` 导致安装命令失效。重命名时目录、frontmatter、README、
   其他 skill 里的交叉引用四处都要改（grep 全仓库确认无残留）。
5. **vibe-coding-spec 的脚本和文档一致**：`scaffold_vibe_feature.py` 生成的 fallback 模板、
   `check_vibe_structure.py` 的检查项、`references/` 里的工作流描述三者要对得上。
   改了 plan 模板结构（如 Constitution Check 表）就要同步 scaffold fallback 和 analyzer 检查。

## 怎么验证改动

```bash
# vibe-coding-spec 脚本：在临时目录跑 scaffold + check（正向 + 负向场景）
cd /tmp && mkdir t && cd t && git init -q . && \
python3 <repo>/vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --name "Demo" --version V0.1 && \
python3 <repo>/vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature 001-demo --version V0.1

# 安装器：
node bin/install.js install --target /tmp/skills-test --dry-run
node bin/install.js install --target /tmp/skills-test && node bin/install.js list --target /tmp/skills-test

# 打包内容（不应混入 .claude/ .DS_Store 等）：
npm pack --dry-run
```

## 发布流程（npm）

```bash
npm version patch          # 或 minor / major；会自动 commit + tag
git push && git push --tags
npm publish                # 需要浏览器 2FA 确认；账号 chengzi000327
```

发布前：更新 `CHANGELOG.md`；`npm pack --dry-run` 确认 42 个左右文件、无杂物。
`package.json` 的 `files` 是白名单——新增 skill 目录要加进去。

## 维护纪律

- **每次实质性改动都更新 `CHANGELOG.md`**（加在 Unreleased 段，发版时归入版本号）。
  这是"下一个 AI 了解做了什么"的主要载体。
- 上游方法论会演进：spec-kit（github/spec-kit）和 superpowers（obra/superpowers）
  值得定期回看有没有新机制可吸收；上次对齐时间见 CHANGELOG。
- 不要把 `.DS_Store`、`.claude/` 提交进仓库。
