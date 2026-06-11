# pm-skills-chengzi

个人 Claude Code PM 技能合集：从产品方向判断到实现规格落地的完整链路，5 个 skill 各管一段。

## Skills

按工作流顺序排列：

| 阶段 | Skill | 一句话说明 |
|---|---|---|
| 1. 该不该做 | `product-decision` | 方向验证 + 立项决策（AREA 五层分析、偏见自查、情景推演） |
| 2. 想清楚 | `idea-to-prd` | 粗想法 → 多轮追问 → PRD v0 + Samples/Eval + 两图一表 |
| 3. 看得见 | `prd-to-frontend` | PRD v0 → 设计风格 → 线框 → 可预览前端页面 |
| 4. 写完整 | `prd-writer` | 原型探索反哺 → PRD v1 / 交付型 PRD（字段、状态、异常、验收） |
| 5. 做出来 | `vibe-coding-spec` | 想法或 PRD → spec/plan/tasks → 质量门禁执行（融合 spec-kit + superpowers） |

```text
想法 -> product-decision -> idea-to-prd -> prd-to-frontend -> prd-writer -> vibe-coding-spec -> 代码
        该不该做           PRD v0+Eval     原型探索          PRD v1        规格+任务+release gate
```

每个阶段都可以单独进入：有想法直接用 `idea-to-prd`，有现成 PRD 直接进 `vibe-coding-spec`，只要个页面直接用 `prd-to-frontend`。

核心理念：**评测即需求**——PRD 必须带 Samples/Eval（没有 3-5 个 sample 不输出 PRD v0）；**evidence before claims**——实现必须带测试矩阵和发布门禁。

## 安装

```bash
git clone https://github.com/chengzi000327/pm-skills-chengzi.git
cd pm-skills-chengzi

cp -r product-decision idea-to-prd prd-to-frontend prd-writer vibe-coding-spec ~/.claude/skills/
```

## 详细文档

每个 skill 的完整用法、工作流和模板都在各自目录的 `SKILL.md` 和 `references/` 里。`vibe-coding-spec` 另带两个脚本：

```bash
# 从想法或 PRD 创建规格包
python3 vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --name "Feature" --version V0.1
python3 vibe-coding-spec/scripts/scaffold_vibe_feature.py --root . --prd docs/prd.md --version V0.1

# 实现前一致性分析
python3 vibe-coding-spec/scripts/check_vibe_structure.py --root . --feature 001-feature --version V0.1
```
