# 阶段 3:落地构建

按项目选形态。核心原则:**代码复杂度要匹配设计野心**——极繁风格需要大量动效和细节代码;极简/克制风格靠的是间距、字体、对比的精准,代码反而要克制。两者都成立,关键是把选定的方向执行到位,不要中途漂回"通用现代 SaaS"。

## 路线 A:单文件 HTML + Tailwind(简单落地页首选)

- 一个 `.html` 文件搞定 HTML / CSS / JS,Tailwind 用 CDN 引入,预览最快。
- 字体真的引进来(Google Fonts `<link>` 或 `@font-face`),不要退回系统字体。
- 配色用 CSS 变量统一(`:root { --bg / --accent / ... }`),方便整体调。
- 动效优先纯 CSS:一次编排好的入场(staggered reveal,用 animation-delay)比一堆零散 micro-interaction 更出彩。
- 需要的库从 cdnjs 引。

## 路线 B:React(.jsx)

适用:有交互状态、组件复用、或属于产品界面。

- 在 claude.ai artifact 里:默认导出一个组件;只能用 Tailwind 核心工具类(无自定义配置);hooks 从 `react` 引;可用 lucide-react、recharts、framer-motion(Motion)等。**不要用浏览器 storage(localStorage 等)**,状态用 useState/useReducer。
- 要做成正经项目(Next.js 等)时,在文件系统里搭工程结构,而不是塞进单文件。
- 动效在 React 里优先用 Motion 库。

## 在当前环境怎么给用户预览

- **claude.ai / app**:把成品文件放到 `/mnt/user-data/outputs/`,用 `present_files` 呈现。`.html` / `.jsx` 会在界面里渲染成可交互的 artifact,用户能直接看。
- 大文件先在 `/home/claude` 里迭代,定稿再拷到 outputs。
- 超过 ~20 行的代码一律建文件,不要只贴在对话里。

## 落地清单

- [ ] 严格按阶段 1 选定的字体 / 配色 / 版式骨架来,没有漂移。
- [ ] 字体已真正加载(不是 fallback 到系统字)。
- [ ] 配色走 CSS 变量,主色 + 强调 + 背景关系清晰。
- [ ] 响应式:至少照顾 375 / 768 / 1024 / 1440。
- [ ] 该有的入场动效 / hover 做了,但不过度。
- [ ] 占位内容真实可信(别 Lorem ipsum;按产品写合理文案)。
- [ ] 交付前再过一遍 `references/anti-slop.md`。
