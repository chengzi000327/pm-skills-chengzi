# 流程图绘制规范

所有流程定义章节都必须有流程图 + 节点说明表。流程图表达流转,节点表补充输入、输出、异常和规则。

## 绘制规则

- 用 SVG 渲染流程图。
- viewBox 固定宽度 680,高度根据内容自适应,最后一个元素底部 + 40px。
- 连线不得穿过其他节点;需要绕行时用 L 形 path。
- 文字必须垂直居中:用 `dominant-baseline="central"`。
- 深色模式强制支持:颜色用 CSS color ramp 类,不要硬编码 hex。

## 箭头 marker

每张图都加:

```svg
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

## 字体

只用两种 class:

- `class="th"`:14px 加粗标题。
- `class="ts"`:12px 次要文字。

不要写裸 `<text>` 不带 class。

## 节点类型

| 节点类型 | class | 形状 | 说明 |
| --- | --- | --- | --- |
| 开始/结束 | `c-gray` | `rx=20` 圆角矩形 | 流程起止 |
| 工程节点 | `c-blue` | `rx=8` 矩形 | 代码/工程逻辑 |
| LLM 节点 | `c-teal` | `rx=8` 矩形 | 大模型调用 |
| 判断节点 | `c-amber` | 菱形 polygon | 条件分支 |
| 异常/拒绝 | `c-red` | `rx=8` 矩形 | 错误/拒绝路径 |

连线颜色:`stroke="var(--color-border-secondary)"` + `marker-end="url(#arrow)"`。分支旁用 12px `ts` 标注条件。

## 不同类型侧重

- Agent 类:区分工程、LLM、工具、判断、异常节点。
- 普通功能类:画清触发入口、主流程、异常/边界路径。
- 纯交互类:画清用户操作路径、状态切换条件、错误恢复路径。

## 节点数量

- <= 8 个节点:单张图,垂直布局。
- 9-15 个节点:单张图,可左右分支布局。
- > 15 个节点:拆成主流程图 + 子流程图。
