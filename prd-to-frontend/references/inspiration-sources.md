# 灵感来源 & 检索 playbook

本 skill **不自带页面库**,也无法自动爬下面这些画廊(variant 是浏览型、mobbin 要登录还有付费墙、craftwork 是浏览型)。所谓"找合适的设计页面",靠的是在**阶段 1 定风格时主动检索**:把这些来源当作检索目标,用搜索/图片工具拉一组真实参考摆给用户看。

## 工具可用性(先确认环境)

- 在 **claude.ai / Claude app** 环境:有 `web_search`、`web_fetch`、`image_search`,可以直接现搜现拉参考截图。
- 在 **Claude Code / 其他 harness**:看那边配没配联网与搜索工具。没有的话,就把下面这些链接**列给用户让他自己去看并截图回来**,或者改用文字描述方向。

## 三个核心灵感源(用户指定)

| 来源 | 强在哪 | 怎么用 |
| --- | --- | --- |
| **variant.com/community** | 审美高的 vibe-coding 项目,适合找"有想法、不套路"的整体气质 | 找落地页/创意站的整体调性参考,尤其想避开 SaaS 模板时 |
| **mobbin.com**(Top Apps / iOS) | 真实落地的好设计,App / 产品界面的交互与组件 | 做**产品界面**时看具体页面怎么布局、组件长什么样(需登录,通常让用户自己截图回来) |
| **craftwork.design/curated/websites** | 泛设计灵感,网站方向广 | 拓宽风格视野,找配色/版式/排版的点子 |

## 检索 playbook(在阶段 1 执行)

定下气质词后,按这个顺序拉参考:

1. **图片搜真实页面**:用 `image_search`,query 用"气质词 + 界面类型",例如 `editorial landing page typography`、`developer tool dark landing page`、`minimal fintech dashboard ui`。一次拉 3-4 张,挑和方向匹配的。
2. **搜带来源的灵感**:`web_search` 带上画廊名,如 `landing page inspiration site:variant.com`、`bento grid website design craftwork`、`mobbin <品类> app onboarding`。
3. **有现成链接就 fetch**:用户在阶段 0 给了喜欢/讨厌的页面链接,用 `web_fetch` 拉来看结构,提炼"要学的点"和"要避开的点"。
4. **每个风格方向配 1-2 个真实参考**摆进阶段 1 的输出里,让用户是"看着实物挑",而不是看着形容词猜。

## 并行提速(有 subagent 时)

每个风格方向的检索互相独立——给每个方向开一个 subagent,各自跑上面的 playbook(image_search + web_search + fetch)并带回挑好的参考。N 个方向并行 ≈ 1 个方向的耗时。没有 subagent 就按顺序跑,结果一样,只是慢些。

## 注意

- 引用参考是为了**提炼气质和手法**(版式逻辑、配色关系、字体气质),**不要照抄**某个具体页面的独特视觉或受版权保护的素材。
- 给用户看参考时,说清楚"这个是参考它的 X(比如留白节奏),不是要做成一样"。
