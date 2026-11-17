---
name: code-commenter
description: >-
  为代码补充解释“为什么”（业务意图、约束、设计决策）而非复述“是什么”的注释，格式遵循所在语言的文档规范。
  Use when writing or modifying code that contains non-obvious logic, business rules, magic numbers,
  public interfaces, or design decisions. Skip self-explanatory code, or when the user says no comments are needed.
---

# 代码注释生成器

注释写给三个月后的维护者：他们不看实现，也要能读懂代码的意图、约束和存在理由。

唯一检验：注释只承载代码读不出的信息——意图、约束、理由。代码本身就能读出的东西（语法结构、显而易见的赋值与遍历），写下来只是噪音。

## 按代码单元分层

| 代码单元 | 必须包含的注释要素 |
|---|---|
| 文件/模块头 | 模块职责、对外暴露的核心能力 |
| 类/接口 | 职责边界、使用场景、生命周期 |
| 函数/方法 | 功能意图、参数的业务含义、返回值、可能抛出的异常 |
| 复杂逻辑块 | 业务规则的来源、边界条件、选择该实现方案的理由 |
| 魔法数字 | 数值的业务含义（86400 → 一天的秒数） |

块内注释超过约 30 词时，上移为函数级注释。文档注释使用所在语言的标准格式（JSDoc / Python Docstring / Javadoc 等）。

## 差例 vs 好例

❌ 每行都在复述代码：

```python
# 循环遍历订单列表
for order in orders:
    # 如果状态是已过期
    if order.status == "expired":
        # 跳过
        continue
```

✅ 一条注释讲清业务理由：

```python
# 过滤已过期订单，避免下游重复发货
for order in orders:
    if order.status == "expired":
        continue
```

## 输出

输出前逐行核对分层表：每个单元的必备要素是否齐备，每条注释是否都承载了代码读不出的信息。

只输出添加注释后的完整代码。注释密度跟随复杂度——零注释的简单代码同样是合格产出。
