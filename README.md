# pm-skills-chengzi

个人 Claude Code PM 技能合集。

## 包含内容

| Skill | 说明 |
|-------|------|
| `product-decision` | 系统性判断产品方向与立项决策，覆盖方向验证和 AREA 五层分析 |
| `idea-to-prd` | 把粗略产品想法通过多轮追问梳理成 PRD v0 / 产品定义稿，并产出 Samples/Eval 与两图一表 |
| `idea-to-frontend` | 把 PRD v0 + Samples/Eval + 两图一表推进为风格方向、线框确认和可预览代码 |
| `prd-writer` | 把 PRD v0、Samples/Eval、两图一表与原型探索结果整理成完整交付型 PRD；主流程在 `SKILL.md`，详细模块写法放在 `references/` |

## 推荐工作流

在 AI 可以快速生成界面的时代，PRD 仍然需要存在，但它不应该只是“写给研发看的长文档”。更好的定位是：PRD 是产品经理用来定义问题、收敛方案、记录取舍、暴露边界、形成可验收共识的工作台。

推荐顺序不是单向的 `想法 -> PRD -> 前端`，也不是跳过思考的 `想法 -> 前端 -> 补 PRD`，而是：

```text
想法 -> 问题定义 -> Samples/Eval -> 共同能力 -> PRD v0 + 两图一表 -> PRD-to-Frontend -> Frontend-to-PRD -> 实现规格/开发计划
```

各阶段职责：

1. **想法卡片**：说明这是什么、给谁、解决什么问题、为什么现在值得做。
2. **问题定义**：确认目标用户、使用场景、当前痛点、现有方案为什么不够好、成功标准是什么。
3. **Samples/Eval**：用具体 case 定义现状，用 Rubric + Metric 定义理想态和完成标准。AI 产品的需求必须进入 sample 时代，评测即需求。
4. **共同能力抽象**：从具体 case 里抽象出产品必须具备的共性能力和边界，而不是凭空写能力清单。
5. **PRD v0 + 两图一表**：锁住产品逻辑，并产出原型草图、流程/状态图、数据表，让 AI 快速理解模块结构、业务流转和评价标准。没有 3-5 个 sample，不输出 PRD v0。
6. **PRD-to-Frontend**：基于 PRD v0 + Samples/Eval + 两图一表做前端/原型探索，用 sample 作为界面 demo 场景和状态校验用例，检查信息架构、CTA、用户路径、空状态、异常状态、边界状态和文案表达。
7. **Frontend-to-PRD**：把原型探索暴露的问题反哺进 PRD，补齐页面结构、交互流程、状态规则、字段定义、权限、边界条件和验收标准。
8. **实现规格/开发计划**：进入技术实现、任务拆分、接口、组件和测试。

这个时代的 PRD 至少应该包含：

- **背景与问题**：为什么这个问题值得解决。
- **目标用户与场景**：具体人在具体场景下遇到什么问题。
- **目标与非目标**：明确做什么，也明确不做什么。
- **核心假设**：产品正在验证哪些判断。
- **Samples/Eval**：Dataset(Samples + Context)、Rubric、Metric、Judge/Evaluator、Protocol。对 AI 产品来说，评测即需求，评测即完成标准。
- **方案与取舍**：最终方案是什么，为什么不选其他方案。
- **两图一表**：原型草图、流程/状态图、数据表，用来承载模块结构、业务流转和分析数据。
- **用户流程与信息架构**：可以是文字、流程图、线框或原型链接。
- **功能细节与状态**：正常、空、加载、错误、权限、边界、异常输入。
- **验收标准与指标**：怎么判断做完了，怎么判断做对了。

各 skill 的分工：

- `product-decision`：负责判断方向值不值得继续投入。
- `idea-to-prd`：负责从粗想法进入多轮追问，产出 PRD v0 / 产品定义稿 + Samples/Eval + 两图一表；没有 3-5 个 sample 时不输出 PRD v0。
- `idea-to-frontend`：负责 PRD-to-Frontend，把 PRD v0 + Samples/Eval + 两图一表变成风格、线框和可预览界面；samples 必须作为 demo 场景和状态校验用例。
- `prd-writer`：负责 Frontend-to-PRD，把 PRD v0、Samples/Eval、两图一表与前端/原型探索结果整理成完整 PRD v1 / 交付型 PRD，并把 Metric 转成验收标准、埋点和测试集；详细模板拆在 `references/`，按 Agent/AI、普通功能、前端交互、两图一表、Metric 映射分别读取。

## 安装方式

```bash
git clone https://github.com/chengzi000327/pm-skills-chengzi.git
cd pm-skills-chengzi

cp -r prd-writer ~/.claude/skills/
cp -r product-decision ~/.claude/skills/
cp -r idea-to-prd ~/.claude/skills/
cp -r idea-to-frontend ~/.claude/skills/
```
