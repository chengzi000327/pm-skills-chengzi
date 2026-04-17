# pm-skills-chengzi

个人 Claude Code PM 技能合集。

## 包含内容

| Skill | 类型 | 说明 |
|-------|------|------|
| `write-prd` | 命令 | 链式调用多个 skill，生成可用于决策的 PRD |
| `product-decision` | Skill | 系统性判断产品方向与立项决策，覆盖方向验证和 AREA 五层分析 |

## 安装方式

克隆仓库后手动复制到 Claude Code 配置目录：

```bash
git clone https://github.com/chengzi000327/pm-skills-chengzi.git
cd pm-skills-chengzi

cp write-prd/commands/write-prd.md ~/.claude/commands/
cp -r product-decision/skills/product-decision ~/.claude/skills/
```

## 使用方式

```
/write-prd 用户在结账流程中流失率过高，需要优化
```
