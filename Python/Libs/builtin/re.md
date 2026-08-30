---
aliases:
  - course of study
  - course
  - re
  - re-tutorial
tags:
  - tutorial
  - computer-science
  - re
category: knowledge
datetime: " 2026-08-08 15:08:82 周六"
author: wephiles
rating: "2"
---

[TOC]

<h1 style="text-align: center;">re</h1>

# 1. 正则表达式基础概念

**正则表达式（`Regular Expression`）** 是一种用来描述字符串模式的工具。就像用"通配符"搜索文件一样，正则表达式可以帮你：

- 验证数据格式（如邮箱、手机号）
- 提取特定内容（如从网页抓取数据）
- 替换文本（如批量修改代码）
- 分割字符串（比普通分割更灵活）

# 2. `re` 模块概述

## 2.1 模块级函数

| 函数          | 用途                       | 使用场景                     |
| ------------- | -------------------------- | ---------------------------- |
| `match()`     | 从**开头**匹配             | 验证字符串开头格式           |
| `search()`    | **扫描**整个字符串找第一个 | 查找是否包含某模式           |
| `findall()`   | 找**所有**匹配             | 提取所有符合条件的内容       |
| `finditer()`  | 返回匹配**迭代器**         | 处理大量匹配结果             |
| `sub()`       | **替换**匹配内容           | 批量修改文本                 |
| `subn()`      | 替换并返回**次数**         | 需要知道替换了多少处         |
| `split()`     | **分割**字符串             | 比普通分割更灵活             |
| `compile()`   | **编译**正则表达式         | 多次使用同一模式（提高性能） |
| `fullmatch()` | **完整匹配**整个字符串     | 严格验证格式                 |
| `escape()`    | **转义**特殊字符           | 动态构建正则时避免冲突       |
| `purge()`     | 清除**缓存**               | 特殊场景释放内存             |

## 2.2 异常类

- `re.error`：正则表达式语法错误时抛出

## 2.3 对象类

- `re.Pattern`：编译后的正则表达式对象
- `re.Match`：匹配结果对象

# 3. 详细讲解与示例

## 3.1 `re.match` -- 从头开始匹配

**语法**：`re.match(pattern, string, flags=0)`

**特点**：只从字符串**开头**尝试匹配，开头不匹配则返回 None。

```python
import re

# ========== 示例1：基本用法 ==========
text = "Python is awesome"
result = re.match(r"Python", text)

print("===== re.match() 基本用法 =====")
print(f"匹配结果对象: {result}")
print(f"匹配内容: {result.group()}")

# ========== 示例2：开头不匹配 ==========
result2 = re.match(r"is", text)
print(f"\n开头不匹配 'is' 的结果: {result2}")  # None

# ========== 示例3：使用分组 ==========
text2 = "2023-12-25 日志信息"
pattern = r"(\d{4})-(\d{2})-(\d{2})"
result3 = re.match(pattern, text2)

print("\n===== 使用分组 =====")
if result3:
    print(f"完整匹配: {result3.group(0)}")  # 或 result3.group()
    print(f"年份(分组1): {result3.group(1)}")
    print(f"月份(分组2): {result3.group(2)}")
    print(f"日期(分组3): {result3.group(3)}")
```

输出结果：

```python
===== re.match() 基本用法 =====
匹配结果对象: <re.Match object; span=(0, 6), match='Python'>
匹配内容: Python

开头不匹配 'is' 的结果: None

===== 使用分组 =====
完整匹配: 2023-12-25
年份(分组1): 2023
月份(分组2): 12
日期(分组3): 25
所有分组元组: ('2023', '12', '25')

===== 命名分组 =====
姓名: 张三
邮箱: zhangsan@example.com
分组字典: {'name': '张三', 'email': 'zhangsan@example.com'}

13812345678 是有效的手机号开头
```

## 3.2 `re.search` -- 扫描整个字符串

**语法**：`re.search(pattern, string, flags=0)`

**特点**：扫描整个字符串，返回第一个匹配结果。

```python
import re

# ========== 示例1：search 与 match 对比 ==========
text = "今天气温 25 度，明天气温 30 度"

print("===== search vs match =====")
# search 在整个字符串中搜索
result1 = re.search(r"\d+ 度", text)
print(f"search 结果: {result1.group()}")  # 找到: 25 度

# match 只从开头匹配，找不到
result2 = re.match(r"\d+ 度", text)
print(f"match 结果: {result2}")  # None

# ========== 示例2：提取第一个邮箱 ==========
text2 = "联系我们：support@example.com 或 sales@company.cn"
email_pattern = r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}"
result = re.search(email_pattern, text2)

print("\n===== 提取第一个邮箱 =====")
if result:
    print(f"找到的邮箱: {result.group()}")
    print(f"位置: {result.span()}")  # (9, 29)

# ========== 示例3：提取商品价格 ==========
text3 = "商品A价格￥199，商品B价格￥299，商品C价格￥399"
price_result = re.search(r"￥(\d+)", text3)

print("\n===== 提取第一个价格 =====")
if price_result:
    print(f"完整匹配: {price_result.group(0)}")  # ￥199
    print(f"价格数字: {price_result.group(1)}")  # 199

# ========== 示例4：提取HTML标签内容 ==========
html = "<div>第一个</div><span>第二个</span><p>第三个</p>"
tag_result = re.search(r"<(\w+)>(.+?)</\1>", html)

print("\n===== 提取HTML标签 =====")
if tag_result:
    print(f"标签名: {tag_result.group(1)}")    # div
    print(f"内容: {tag_result.group(2)}")      # 第一个

# ========== 示例5：提取IP地址 ==========
log = "来源IP: 192.168.1.100 访问了服务器"
ip_result = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log)

print("\n===== 提取IP地址 =====")
if ip_result:
    print(f"找到IP: {ip_result.group()}")

# ========== 示例6：匹配多行文本 ==========
text4 = """第一行
第二行有target目标
第三行"""

# 普通模式
result = re.search(r"target", text4)
print(f"\n找到目标: {result.group() if result else '未找到'}")
```

输出结果:

```python
===== search vs match =====
search 结果: 25 度
match 结果: None

===== 提取第一个邮箱 =====
找到的邮箱: support@example.com
位置: (9, 29)

===== 提取第一个价格 =====
完整匹配: ￥199
价格数字: 199

===== 提取HTML标签 =====
标签名: div
内容: 第一个

===== 提取IP地址 =====
找到IP: 192.168.1.100

找到目标: target
```

## 3.3 `re.findall()` -- 查找所有匹配

**语法**：`re.findall(pattern, string, flags=0)`

**特点**：返回所有匹配的列表，工程中最常用。

```python
import re

# ========== 示例1：提取所有数字 ==========
text = "订单号：12345，金额：999元，数量：3"
numbers = re.findall(r"\d+", text)

print("===== 提取所有数字 =====")
print(f"数字列表: {numbers}")  # ['12345', '999', '3']

# ========== 示例2：提取所有邮箱 ==========
text2 = """
联系方式：
- 技术支持: support@example.com
- 销售: sales@company.cn
- 客服: service123@test.org
"""
emails = re.findall(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", text2)

print("\n===== 提取所有邮箱 =====")
print(f"邮箱列表: {emails}")

# ========== 示例3：有分组 vs 无分组 ==========
text3 = "苹果:5元 香蕉:3元 橙子:4元"

# 无分组 - 返回完整匹配
result1 = re.findall(r"\w+:\d+元", text3)
print(f"\n无分组结果: {result1}")  # ['苹果:5元', '香蕉:3元', '橙子:4元']

# 有分组 - 只返回分组内容
result2 = re.findall(r"(\w+):(\d+)元", text3)
print(f"有分组结果: {result2}")  # [('苹果', '5'), ('香蕉', '3'), ('橙子', '4')]

# ========== 示例4：提取所有链接 ==========
html = """
<a href="https://example.com">链接1</a>
<a href="http://test.cn/path">链接2</a>
<img src="image.png">
"""
links = re.findall(r'href="(https?://[^"]+)"', html)

print("\n===== 提取所有链接 =====")
print(f"链接列表: {links}")

# ========== 示例5：提取所有中文 ==========
text4 = "Hello 你好 World 世界 Python 编程"
chinese = re.findall(r"[\u4e00-\u9fa5]+", text4)

print("\n===== 提取所有中文 =====")
print(f"中文列表: {chinese}")  # ['你好', '世界', '编程']

# ========== 示例6：提取所有手机号 ==========
text5 = "联系人: 张三13812345678, 李四13987654321, 王五15012345678"
phones = re.findall(r"1[3-9]\d{9}", text5)

print("\n===== 提取所有手机号 =====")
print(f"手机号列表: {phones}")

# ========== 示例7：提取日期 ==========
text6 = "重要日期：2023-01-15, 2024-02-20, 2025-03-25"
dates = re.findall(r"(\d{4})-(\d{2})-(\d{2})", text6)

print("\n===== 提取所有日期 =====")
print(f"日期列表: {dates}")
for year, month, day in dates:
    print(f"  {year}年{month}月{day}日")

# ========== 示例8：忽略大小写提取 ==========
text7 = "Python python PYTHON"
words = re.findall(r"python", text7, re.IGNORECASE)

print("\n===== 忽略大小写提取 =====")
print(f"匹配结果: {words}")
```

输出结果:

```python
===== 提取所有数字 =====
数字列表: ['12345', '999', '3']

===== 提取所有邮箱 =====
邮箱列表: ['support@example.com', 'sales@company.cn', 'service123@test.org']

无分组结果: ['苹果:5元', '香蕉:3元', '橙子:4元']
有分组结果: [('苹果', '5'), ('香蕉', '3'), ('橙子', '4')]

===== 提取所有链接 =====
链接列表: ['https://example.com', 'http://test.cn/path']

===== 提取所有中文 =====
中文列表: ['你好', '世界', '编程']

===== 提取所有手机号 =====
手机号列表: ['13812345678', '13987654321', '15012345678']

===== 提取所有日期 =====
日期列表: [('2023', '01', '15'), ('2024', '02', '20'), ('2025', '03', '25')]
  2023年01月15日
  2024年02月20日
  2025年03月25日

===== 忽略大小写提取 =====
匹配结果: ['Python', 'python', 'PYTHON']
```

## 3.4 `re.finditer()` -- 返回匹配迭代器

**语法**：`re.finditer(pattern, string, flags=0)`

**特点**：返回Match对象迭代器，节省内存，可获取位置信息。

```python
import re

# ========== 示例1：基本用法与位置信息 ==========
text = "Python很棒，Python很强，Python很好学！"
matches = re.finditer(r"Python", text)

print("===== finditer() 基本用法 =====")
for i, match in enumerate(matches, 1):
    print(f"第{i}次匹配:")
    print(f"  内容: {match.group()}")
    print(f"  位置: {match.span()} (从{match.start()}到{match.end()})")

# ========== 示例2：对比 findall 和 finditer ==========
text2 = "word1 word2 word3 word4 word5"

print("\n===== findall vs finditer =====")
# findall 返回列表，一次性加载所有结果
result_list = re.findall(r"\w+", text2)
print(f"findall结果: {result_list}")

# finditer 返回迭代器，按需加载
result_iter = re.finditer(r"\w+", text2)
print("finditer结果:")
for m in result_iter:
    print(f"  {m.group()} at {m.span()}")

# ========== 示例3：实战-高亮关键词位置 ==========
text3 = "错误在 line 10，修复于 line 20，测试在 line 30"
print(f"\n原文: {text3}")

print("高亮位置:")
positions = []
for m in re.finditer(r"line (\d+)", text3):
    positions.append((m.start(), m.end(), m.group(1)))
    print(f"  行号 {m.group(1)} 位于 {m.span()}")

# ========== 示例4：提取带位置的数据 ==========
text4 = "价格:100,价格:200,价格:300"
print("\n===== 提取价格带位置 =====")

prices_info = []
for m in re.finditer(r"价格:(\d+)", text4):
    prices_info.append({
        'position': m.span(),
        'original': m.group(0),
        'price': int(m.group(1))
    })

for info in prices_info:
    print(f"  位置{info['position']}: {info['original']}")

print(f"价格列表: {[p['price'] for p in prices_info]}")

# ========== 示例5：处理大量数据（内存优化） ==========
print("\n===== 处理大量数据 =====")
# 模拟大数据
big_text = "数据," * 10000

# 使用 finditer，内存友好
count = 0
for m in re.finditer(r"数据", big_text):
    count += 1
print(f"使用 finditer 找到 {count} 个'数据'（内存友好）")

# 使用 findall，一次性加载所有结果
result = re.findall(r"数据", big_text)
print(f"使用 findall 找到 {len(result)} 个'数据'（占用更多内存）")

# ========== 示例6：提取并统计 ==========
log_text = """
2023-12-25 ERROR 数据库连接失败
2023-12-25 INFO 用户登录成功
2023-12-25 ERROR 文件读取错误
2023-12-25 WARN 内存使用率高
2023-12-25 ERROR 网络超时
"""

error_count = 0
error_messages = []

print("\n===== 日志分析 =====")
for m in re.finditer(r"ERROR\s+(.+)", log_text):
    error_count += 1
    error_messages.append(m.group(1))

print(f"错误数量: {error_count}")
print(f"错误信息: {error_messages}")

```

输出结果:

```python
===== finditer() 基本用法 =====
第1次匹配:
  内容: Python
  位置: (0, 6) (从0到6)
第2次匹配:
  内容: Python
  位置: (9, 15) (从9到15)
第3次匹配:
  内容: Python
  位置: (18, 24) (从18到24)

===== findall vs finditer =====
findall结果: ['word1', 'word2', 'word3', 'word4', 'word5']
finditer结果:
  word1 at (0, 5)
  word2 at (6, 11)
  word3 at (12, 17)
  word4 at (18, 23)
  word5 at (24, 29)

原文: 错误在 line 10，修复于 line 20，测试在 line 30
高亮位置:
  行号 10 位于 (4, 11)
  行号 20 位于 (16, 23)
  行号 30 位于 (28, 35)

===== 提取价格带位置 =====
  位置(0, 6): 价格:100
  位置(7, 13): 价格:200
  位置(14, 20): 价格:300
价格列表: [100, 200, 300]

===== 处理大量数据 =====
使用 finditer 找到 10000 个'数据'（内存友好）
使用 findall 找到 10000 个'数据'（占用更多内存）

===== 日志分析 =====
错误数量: 3
错误信息: ['数据库连接失败', '文件读取错误', '网络超时']
```

## 3.5 `re.sub()` 和 `re.subn()` -- 替换

**语法**：

- `re.sub(pattern, repl, string, count=0, flags=0)`
- `re.subn(pattern, repl, string, count=0, flags=0)`

**特点**：`sub`返回新字符串，`subn`返回元组`(新字符串, 替换次数)`。

```python
import re

# ========== 示例1：基本替换 ==========
text = "我喜欢Java，Java很棒"
result = re.sub(r"Java", "Python", text)

print("===== 基本替换 =====")
print(f"原文: {text}")
print(f"替换后: {result}")

# ========== 示例2：限制替换次数 ==========
text2 = "A-B-C-D-E-F"
result2 = re.sub(r"-", "_", text2, count=2)

print("\n===== 限制替换次数 =====")
print(f"原文: {text2}")
print(f"只替换前2个: {result2}")  # A_B_C-D-E-F

# ========== 示例3：使用函数替换 ==========
def price_adjust(match):
    """价格打8折"""
    original_price = int(match.group(1))
    new_price = int(original_price * 0.8)
    return f"￥{new_price}"

text3 = "原价￥100，原价￥200，原价￥300"
result3 = re.sub(r"￥(\d+)", price_adjust, text3)

print("\n===== 函数替换（打8折）=====")
print(f"原文: {text3}")
print(f"替换后: {result3}")

# ========== 示例4：使用反向引用 ==========
text4 = "hello world python"

# \1 引用第一个分组
result4 = re.sub(r"(\w+)", r"[\1]", text4)
print("\n===== 反向引用 =====")
print(f"原文: {text4}")
print(f"加方括号: {result4}")

# ========== 示例5：隐藏手机号中间4位 ==========
text5 = "张三13812345678，李四13987654321"
# \1 引用前3位，\2 引用后4位
result5 = re.sub(r"(1[3-9]\d)\d{4}(\d{4})", r"\1****\2", text5)

print("\n===== 手机号脱敏 =====")
print(f"原文: {text5}")
print(f"脱敏后: {result5}")

# ========== 示例6：subn 返回替换次数 ==========
text6 = "a-b-c-d-e"
result6, count = re.subn(r"-", "_", text6)

print("\n===== subn 替换并统计 =====")
print(f"原文: {text6}")
print(f"替换后: {result6}")
print(f"替换次数: {count}")

# ========== 示例7：批量清理HTML标签 ==========
html = "<div>内容</div><span>更多</span><p>段落</p>"
clean_text = re.sub(r"<[^>]+>", "", html)

print("\n===== 清理HTML标签 =====")
print(f"原文: {html}")
print(f"清理后: {clean_text}")

# ========== 示例8：邮箱脱敏 ==========
text7 = "邮箱: zhangsan@example.com 和 lisi@test.cn"
result7 = re.sub(r"(\w{2})[\w.+-]+(@[\w.]+)", r"\1***\2", text7)

print("\n===== 邮箱脱敏 =====")
print(f"原文: {text7}")
print(f"脱敏后: {result7}")

# ========== 示例9：日期格式转换 ==========
text8 = "日期: 2023-12-25 和 2024-01-01"
result8 = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\2/\3/\1", text8)

print("\n===== 日期格式转换 =====")
print(f"原文: {text8}")
print(f"转换后: {result8}")  # 日期: 12/25/2023 和 01/01/2024

# ========== 示例10：复杂函数替换 ==========
def uppercase_match(match):
    """将匹配内容转为大写"""
    return match.group(0).upper()

text9 = "hello WORLD python"
result9 = re.sub(r"[a-z]+", uppercase_match, text9)

print("\n===== 函数替换转大写 =====")
print(f"原文: {text9}")
print(f"替换后: {result9}")
```

输出结果:

```python
===== 基本替换 =====
原文: 我喜欢Java，Java很棒
替换后: 我喜欢Python，Python很棒

===== 限制替换次数 =====
原文: A-B-C-D-E-F
只替换前2个: A_B_C-D-E-F

===== 函数替换（打8折）=====
原文: 原价￥100，原价￥200，原价￥300
替换后: 原价￥80，原价￥160，原价￥240

===== 反向引用 =====
原文: hello world python
加方括号: [hello] [world] [python]

===== 手机号脱敏 =====
原文: 张三13812345678，李四13987654321
脱敏后: 张三138****5678，李四139****54321

===== subn 替换并统计 =====
原文: a-b-c-d-e
替换后: a_b_c_d_e
替换次数: 4

===== 清理HTML标签 =====
原文: <div>内容</div><span>更多</span><p>段落</p>
清理后: 内容更多段落

===== 邮箱脱敏 =====
原文: 邮箱: zhangsan@example.com 和 lisi@test.cn
脱敏后: 邮箱: zh***@example.com 和 li***@test.cn

===== 日期格式转换 =====
原文: 日期: 2023-12-25 和 2024-01-01
转换后: 日期: 12/25/2023 和 01/01/2024

===== 函数替换转大写 =====
原文: hello WORLD python
替换后: HELLO WORLD PYTHON
```

## 3.6 `re.split()` -- 分割字符串

**语法**：`re.split(pattern, string, maxsplit=0, flags=0)`

**特点**：比普通 `split()` 更强大，支持正则表达式分割。

```python
import re

# ========== 示例1：多种分隔符分割 ==========
text = "苹果,香蕉;橙子.葡萄"
result = re.split(r"[,;.\s]+", text)

print("===== 多种分隔符分割 =====")
print(f"原文: {text}")
print(f"分割结果: {result}")

# ========== 示例2：保留分隔符（捕获分组） ==========
text2 = "a1b2c3d"

# 无分组 - 分隔符被丢弃
result1 = re.split(r"\d+", text2)
print(f"\n无分组分割: {result1}")  # ['a', 'b', 'c', 'd']

# 有分组 - 分隔符保留
result2 = re.split(r"(\d+)", text2)
print(f"有分组分割: {result2}")  # ['a', '1', 'b', '2', 'c', '3', 'd']

# ========== 示例3：限制分割次数 ==========
text3 = "a-b-c-d-e"
result3 = re.split(r"-", text3, maxsplit=2)

print("\n===== 限制分割次数 =====")
print(f"原文: {text3}")
print(f"分割最多2次: {result3}")  # ['a', 'b', 'c-d-e']

# ========== 示例4：解析日志 ==========
log = "2023-12-25 10:30:45 [ERROR] Exception occurred"
parts = re.split(r"[\s\[\]]+", log)

print("\n===== 解析日志 =====")
print(f"日志: {log}")
print(f"分割结果: {parts}")

# ========== 示例5：分割并过滤空字符串 ==========
text4 = "a  b   c    d"
result4 = re.split(r"\s+", text4)
print(f"\n多个空格分割: {result4}")  # ['', 'a', 'b', 'c', 'd']

# 过滤空字符串
result5 = [p for p in re.split(r"\s+", text4) if p]
print(f"过滤空字符串: {result5}")

# ========== 示例6：解析CSV行 ==========
csv_line = '张三,25,"北京市朝阳区",工程师'
# 使用更复杂的正则处理引号内的逗号
parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', csv_line)

print("\n===== 解析CSV =====")
print(f"CSV行: {csv_line}")
print(f"分割结果: {parts}")

# ========== 示例7：按句子分割 ==========
text5 = "Hello World。How are you？I'm fine！测试一下。"
sentences = re.split(r"[。？！]", text5)

print("\n===== 按句子分割 =====")
print(f"原文: {text5}")
print(f"句子: {sentences}")

# ========== 示例8：分割HTML标签 ==========
html = "<div>内容</div><p>段落</p>"
# 分割并保留标签
parts = re.split(r"(<[^>]+>)", html)
parts = [p for p in parts if p]

print("\n===== 分割HTML =====")
print(f"HTML: {html}")
print(f"分割结果: {parts}")

```

输出结果:

```python
===== 多种分隔符分割 =====
原文: 苹果,香蕉;橙子.葡萄
分割结果: ['苹果', '香蕉', '橙子', '葡萄']

无分组分割: ['a', 'b', 'c', 'd']
有分组分割: ['a', '1', 'b', '2', 'c', '3', 'd']

===== 限制分割次数 =====
原文: a-b-c-d-e
分割最多2次: ['a', 'b', 'c-d-e']

===== 解析日志 =====
日志: 2023-12-25 10:30:45 [ERROR] Exception occurred
分割结果: ['2023-12-25', '10:30:45', 'ERROR', 'Exception', 'occurred']

多个空格分割: ['', 'a', 'b', 'c', 'd']
过滤空字符串: ['a', 'b', 'c', 'd']

===== 解析CSV =====
CSV行: 张三,25,"北京市朝阳区",工程师
分割结果: ['张三', '25', '"北京市朝阳区"', '工程师']

===== 按句子分割 =====
原文: Hello World。How are you？I'm fine！测试一下。
句子: ['Hello World', 'How are you', "I'm fine", '测试一下', '']

===== 分割HTML =====
HTML: <div>内容</div><p>段落</p>
分割结果: ['<div>', '内容', '</div>', '<p>', '段落', '</p>']
```

## 3.7 `re.compile()` - 编译正则表达式

**语法**：`re.compile(pattern, flags=0)`

**特点**：预编译正则表达式，提高性能，同一模式多次使用时推荐。

```python
import re

# ========== 示例1：基本编译与使用 ==========
print("===== 基本编译 =====")

# 编译手机号正则
phone_pattern = re.compile(r"1[3-9]\d{9}")

texts = [
    "张三13812345678",
    "李四：13987654321",
    "王五手机15012345678",
    "无效号码12345"
]

for text in texts:
    phone = phone_pattern.search(text)
    if phone:
        print(f"找到手机号: {phone.group()} 来自 '{text}'")
    else:
        print(f"未找到有效手机号 来自 '{text}'")

# ========== 示例2：编译时添加标志 ==========
print("\n===== 编译时添加标志 =====")

# 忽略大小写
email_pattern = re.compile(
    r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",
    re.IGNORECASE
)

text = "邮箱: Test@EXAMPLE.COM"
email = email_pattern.search(text)
print(f"找到邮箱: {email.group()}")

# ========== 示例3：多个标志组合 ==========
print("\n===== 多个标志组合 =====")

# re.IGNORECASE: 忽略大小写
# re.MULTILINE: 多行模式
pattern = re.compile(r"^hello", re.IGNORECASE | re.MULTILINE)

text = """Hello World
hello Python
HELLO Everyone"""

matches = pattern.findall(text)
print(f"匹配结果: {matches}")

# ========== 示例4：re.DOTALL 让点号匹配换行 ==========
print("\n===== re.DOTALL 示例 =====")

text = "Hello\nWorld"

# 默认 . 不匹配换行
pattern1 = re.compile(r"Hello.World")
print(f"默认模式: {pattern1.search(text)}")  # None

# 使用 DOTALL
pattern2 = re.compile(r"Hello.World", re.DOTALL)
print(f"DOTALL模式: {pattern2.search(text).group()}")

# ========== 示例5：re.VERBOSE 可读性正则 ==========
print("\n===== re.VERBOSE 可读性正则 =====")

# 复杂正则写成一行难以阅读
# pattern = r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})"

# 使用 VERBOSE 添加注释
datetime_pattern = re.compile(r"""
    (?P<year>\d{4})      # 年份
    -                    # 分隔符
    (?P<month>\d{2})     # 月份
    -                    # 分隔符
    (?P<day>\d{2})       # 日期
    \s+                  # 空格
    (?P<hour>\d{2})      # 小时
    :                    # 分隔符
    (?P<minute>\d{2})    # 分钟
    :                    # 分隔符
    (?P<second>\d{2})    # 秒
""", re.VERBOSE)

text = "2023-12-25 10:30:45"
match = datetime_pattern.search(text)
if match:
    print(f"解析结果: {match.groupdict()}")

# ========== 示例6：性能对比 ==========
print("\n===== 性能对比 =====")
import time

text = "测试文本abc123def456" * 1000

# 不编译，每次重新编译
start = time.time()
for _ in range(1000):
    re.search(r"\d+", text)
time1 = time.time() - start

# 预编译
pattern = re.compile(r"\d+")
start = time.time()
for _ in range(1000):
    pattern.search(text)
time2 = time.time() - start

print(f"不编译耗时: {time1:.4f}秒")
print(f"预编译耗时: {time2:.4f}秒")
print(f"性能提升: {(time1/time2):.2f}倍")

# ========== 示例7：Pattern对象的属性 ==========
print("\n===== Pattern对象属性 =====")

pattern = re.compile(r"(?P<name>\w+):\s*(?P<value>\d+)")
print(f"正则表达式: {pattern.pattern}")
print(f"标志: {pattern.flags}")
print(f"分组数量: {pattern.groups}")
print(f"命名分组映射: {pattern.groupindex}")

# ========== 示例8：Pattern对象的方法 ==========
print("\n===== Pattern对象方法 =====")

phone_pattern = re.compile(r"1[3-9]\d{9}")

# 使用 Pattern 对象的各种方法
text = "联系电话13812345678"

# match
m = phone_pattern.match(text)
print(f"match: {m}")

# search
s = phone_pattern.search(text)
print(f"search: {s.group()}")

# findall
text2 = "张三13812345678，李四13987654321"
f = phone_pattern.findall(text2)
print(f"findall: {f}")

# sub
sub_result = phone_pattern.sub("***********", text2)
print(f"sub: {sub_result}")
```

输出结果:

```python
===== 基本编译 =====
找到手机号: 13812345678 来自 '张三13812345678'
找到手机号: 13987654321 来自 '李四：13987654321'
找到手机号: 15012345678 来自 '王五手机15012345678'
未找到有效手机号 来自 '无效号码12345'

===== 编译时添加标志 =====
找到邮箱: Test@EXAMPLE.COM

===== 多个标志组合 =====
匹配结果: ['Hello', 'hello', 'HELLO']

===== re.DOTALL 示例 =====
默认模式: None
DOTALL模式: Hello
World

===== re.VERBOSE 可读性正则 =====
解析结果: {'year': '2023', 'month': '12', 'day': '25', 'hour': '10', 'minute': '30', 'second': '45'}

===== 性能对比 =====
不编译耗时: 0.0523秒
预编译耗时: 0.0158秒
性能提升: 3.31倍

===== Pattern对象属性 =====
正则表达式: (?P<name>\w+):\s*(?P<value>\d+)
标志: 32
分组数量: 2
命名分组映射: {'name': 1, 'value': 2}

===== Pattern对象方法 =====
match: None
search: 13812345678
findall: ['13812345678', '13987654321']
sub: 张三***********，李四***********
```

## 3.8 re.fullmatch() - 完整匹配

**语法**：`re.fullmatch(pattern, string, flags=0)`

**特点**：整个字符串必须完全匹配模式，用于严格验证。

```
import re

# ========== 示例1：验证手机号 ==========
print("===== 验证手机号 =====")

def is_valid_phone(phone):
    """验证是否为有效手机号"""
    return bool(re.fullmatch(r"1[3-9]\d{9}", phone))

test_phones = [
    "13812345678",    # 有效
    "1381234567",     # 位数不够
    "138123456789",   # 位数过多
    "abc13812345678", # 有其他字符
    "12812345678"     # 开头不是1[3-9]
]

for phone in test_phones:
    result = "有效" if is_valid_phone(phone) else "无效"
    print(f"{phone}: {result}")

# ========== 示例2：验证邮箱 ==========
print("\n===== 验证邮箱 =====")

def is_valid_email(email):
    """验证邮箱格式"""
    pattern = r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}"
    return bool(re.fullmatch(pattern, email))

test_emails = [
    "test@example.com",
    "test.user@example.cn",
    "invalid",
    "@example.com",
    "test@.com"
]

for email in test_emails:
    result = "有效" if is_valid_email(email) else "无效"
    print(f"{email}: {result}")

# ========== 示例3：验证IP地址 ==========
print("\n===== 验证IP地址 =====")

def is_valid_ip(ip):
    """验证IP地址格式和范围"""
    pattern = r"(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})"
    match = re.fullmatch(pattern, ip)
    if match:
        # 检查每个部分是否在0-255范围内
        parts = [int(match.group(i)) for i in range(1, 5)]
        return all(0 <= p <= 255 for p in parts)
    return False

test_ips = [
    "192.168.1.1",
    "255.255.255.255",
    "0.0.0.0",
    "256.1.1.1",      # 超出范围
    "192.168.1",      # 位数不够
    "192.168.1.1.1"   # 位数过多
]

for ip in test_ips:
    result = "有效" if is_valid_ip(ip) else "无效"
    print(f"{ip}: {result}")

# ========== 示例4：验证身份证号 ==========
print("\n===== 验证身份证号 =====")

def is_valid_id_card(id_card):
    """验证18位身份证号"""
    pattern = r"\d{17}[\dXx]"
    return bool(re.fullmatch(pattern, id_card))

test_ids = [
    "123456789012345678",
    "12345678901234567X",
    "123456789012345",   # 位数不够
    "1234567890123456789" # 位数过多
]

for id_card in test_ids:
    result = "有效" if is_valid_id_card(id_card) else "无效"
    print(f"{id_card}: {result}")

# ========== 示例5：验证URL ==========
print("\n===== 验证URL =====")

def is_valid_url(url):
    """验证URL格式"""
    pattern = r"https?://[\w./-]+"
    return bool(re.fullmatch(pattern, url))

test_urls = [
    "https://example.com" ,
    "http://test.cn/path" ,
    "ftp://invalid.com",  # 不支持ftp
    "example.com"         # 缺少协议
]

for url in test_urls:
    result = "有效" if is_valid_url(url) else "无效"
    print(f"{url}: {result}")

# ========== 示例6：验证日期格式 ==========
print("\n===== 验证日期格式 =====")

def is_valid_date(date_str):
    """验证YYYY-MM-DD格式"""
    pattern = r"\d{4}-\d{2}-\d{2}"
    return bool(re.fullmatch(pattern, date_str))

test_dates = [
    "2023-12-25",
    "2023-1-1",      # 位数不对
    "23-12-25",      # 年份位数不对
    "2023/12/25"     # 分隔符不对
]

for date in test_dates:
    result = "有效" if is_valid_date(date) else "无效"
    print(f"{date}: {result}")

# ========== 示例7：验证密码强度 ==========
print("\n===== 验证密码强度 =====")

def check_password_strength(password):
    """检查密码强度：至少8位，包含大小写字母和数字"""
    patterns = {
        'length': r".{8,}",
        'lowercase': r".*[a-z].*",
        'uppercase': r".*[A-Z].*",
        'digit': r".*\d.*"
    }
    
    results = {}
    for name, pattern in patterns.items():
        results[name] = bool(re.fullmatch(pattern, password))
    
    return results

passwords = [
    "abc",
    "abcdefgh",
    "Abcdefgh",
    "Abcdefgh1"
]

for pwd in passwords:
    results = check_password_strength(pwd)
    status = "强" if all(results.values()) else "弱"
    print(f"'{pwd}': {status} - {results}")

# ========== 示例8：对比 match 和 fullmatch ==========
print("\n===== match vs fullmatch =====")

text = "13812345678abc"

# match：只检查开头
m = re.match(r"1[3-9]\d{9}", text)
print(f"match结果: {m.group() if m else 'None'}")  # 能匹配

# fullmatch：检查整个字符串
f = re.fullmatch(r"1[3-9]\d{9}", text)
print(f"fullmatch结果: {f.group() if f else 'None'}")  # 不能匹配
```

**输出结果**：

```
===== 验证手机号 =====
13812345678: 有效
1381234567: 无效
138123456789: 无效
abc13812345678: 无效
12812345678: 无效

===== 验证邮箱 =====
test@example.com: 有效
test.user@example.cn: 有效
: 无效
@example.com: 无效
test@.com: 无效

===== 验证IP地址 =====
192.168.1.1: 有效
255.255.255.255: 有效
0.0.0.0: 有效
256.1.1.1: 无效
192.168.1: 无效
192.168.1.1.1: 无效

===== 验证身份证号 =====
123456789012345678: 有效
12345678901234567X: 有效
123456789012345: 无效
1234567890123456789: 无效

===== 验证URL =====
https://example.com : 有效
http://test.cn/path : 有效
ftp://invalid.com: 无效
example.com: 无效

===== 验证日期格式 =====
2023-12-25: 有效
2023-1-1: 无效
23-12-25: 无效
2023/12/25: 无效

===== 验证密码强度 =====
'abc': 弱 - {'length': False, 'lowercase': True, 'uppercase': False, 'digit': False}
'abcdefgh': 弱 - {'length': True, 'lowercase': True, 'uppercase': False, 'digit': False}
'Abcdefgh': 弱 - {'length': True, 'lowercase': True, 'uppercase': True, 'digit': False}
'Abcdefgh1': 强 - {'length': True, 'lowercase': True, 'uppercase': True, 'digit': True}

===== match vs fullmatch =====
match结果: 13812345678
fullmatch结果: None
```

## 3.9 re.escape() - 转义特殊字符

**语法**：`re.escape(string)`

**特点**：自动转义所有正则特殊字符，用于动态构建正则。

```
import re

# ========== 示例1：基本用法 ==========
print("===== 基本用法 =====")

# 包含正则特殊字符的字符串
special_chars = "price: $100 (special)"
escaped = re.escape(special_chars)

print(f"原始字符串: {special_chars}")
print(f"转义后: {escaped}")

# ========== 示例2：搜索包含特殊字符的文本 ==========
print("\n===== 搜索特殊字符 =====")

def search_literal(text, keyword):
    """搜索字面文本（忽略正则特殊字符）"""
    pattern = re.compile(re.escape(keyword))
    return pattern.search(text) is not None

text = "计算表达式: a+b*c = result"

# 直接用 a+b 会把 + 当成正则特殊字符
# 使用 escape 转义后就能正确搜索
print(f"搜索 'a+b': {search_literal(text, 'a+b')}")  # True
print(f"搜索 'b*c': {search_literal(text, 'b*c')}")  # True
print(f"搜索 'xyz': {search_literal(text, 'xyz')}")   # False

# ========== 示例3：动态构建正则表达式 ==========
print("\n===== 动态构建正则 =====")

def build_search_pattern(keywords):
    """根据关键词列表构建搜索模式"""
    escaped_keywords = [re.escape(kw) for kw in keywords]
    pattern = "|".join(escaped_keywords)
    return re.compile(pattern, re.IGNORECASE)

keywords = ["C++", "Python", "Java"]
pattern = build_search_pattern(keywords)

text = "我会 C++、Python 和 Java"
matches = pattern.findall(text)
print(f"找到的关键词: {matches}")

# ========== 示例4：批量替换用户输入 ==========
print("\n===== 批量替换用户输入 =====")

def safe_replace(text, old, new):
    """安全替换，处理特殊字符"""
    pattern = re.compile(re.escape(old))
    return pattern.sub(new, text)

text = "价格: $100, 价格:$200"
result = safe_replace(text, "$100", "￥680")
print(f"替换结果: {result}")

# ========== 示例5：路径搜索 ==========
print("\n===== 路径搜索 =====")

# Windows路径包含特殊字符
path = "C:\\Users\\test\\file.txt"
search_path = "C:\\Users"

# 使用 escape 处理路径
pattern = re.compile(re.escape(search_path))
if pattern.search(path):
    print(f"路径 '{path}' 包含 '{search_path}'")

# ========== 示例6：数学表达式处理 ==========
print("\n===== 数学表达式处理 =====")

expression = "a + b * (c - d) / e"

# 搜索特定运算符
operators = ["+", "-", "*", "/", "(", ")"]
for op in operators:
    count = len(re.findall(re.escape(op), expression))
    print(f"运算符 '{op}' 出现 {count} 次")

# ========== 示例7：哪些字符会被转义 ==========
print("\n===== 被转义的特殊字符 =====")

test_string = "a.b*c+d?e^f$g|h[i]j(k)l{m}n\\o"
escaped = re.escape(test_string)
print(f"原字符串: {test_string}")
print(f"转义后: {escaped}")

# 查看哪些字符被转义
import string
special_chars = r"\.^$*+?{}[]|()"
for char in special_chars:
    print(f"'{char}' -> '{re.escape(char)}'")
```

**输出结果**：

```
===== 基本用法 =====
原始字符串: price: $100 (special)
转义后: price:\ \$100\ \(special\)

===== 搜索特殊字符 =====
搜索 'a+b': True
搜索 'b*c': True
搜索 'xyz': False

===== 动态构建正则 =====
找到的关键词: ['C++', 'Python', 'Java']

===== 批量替换用户输入 =====
替换结果: 价格: ￥680, 价格: $200

===== 路径搜索 =====
路径 'C:\Users\test\file.txt' 包含 'C:\Users'

===== 数学表达式处理 =====
运算符 '+' 出现 1 次
运算符 '-' 出现 1 次
运算符 '*' 出现 1 次
运算符 '/' 出现 1 次
运算符 '(' 出现 1 次
运算符 ')' 出现 1 次

===== 被转义的特殊字符 =====
原字符串: a.b*c+d?e^f$g|h[i]j(k)l{m}n\o
转义后: a\.b\*c\+d\?e\^f\$g\|h\[i\]j\(k\)l\{m\}n\\o
'\' -> '\\'
'.' -> '\.'
'^' -> '\^'
'$' -> '\$'
'*' -> '\*'
'+' -> '\+'
'?' -> '\?'
'{' -> '\{'
'}' -> '\}'
'[' -> '\['
']' -> '\]'
'|' -> '\|'
'(' -> '\('
')' -> '\)'
```

## 3.10 re.error - 异常处理

**语法**：捕获正则表达式语法错误。

```
import re

# ========== 示例1：捕获语法错误 ==========
print("===== 捕获语法错误 =====")

def safe_compile(pattern_str):
    """安全编译正则表达式"""
    try:
        pattern = re.compile(pattern_str)
        return pattern, None
    except re.error as e:
        return None, str(e)

# 错误的正则（括号不匹配）
patterns = [
    r"((\d+)",      # 括号不匹配
    r"[a-z",        # 方括号不闭合
    r"*abc",        # 无效的重复
    r"\d+",         # 正确的正则
]

for p in patterns:
    pattern, error = safe_compile(p)
    if error:
        print(f"错误: '{p}' -> {error}")
    else:
        print(f"正确: '{p}'")

# ========== 示例2：常见错误示例 ==========
print("\n===== 常见错误示例 =====")

# 错误1：括号不匹配
try:
    re.compile(r"(abc")
except re.error as e:
    print(f"括号不匹配: {e}")

# 错误2：无效的重复
try:
    re.compile(r"a**")
except re.error as e:
    print(f"无效重复: {e}")

# 错误3：无效的转义
try:
    re.compile(r"\x")
except re.error as e:
    print(f"无效转义: {e}")

# 错误4：无效的字符集
try:
    re.compile(r"[z-a]")
except re.error as e:
    print(f"无效字符集: {e}")

# ========== 示例3：安全的正则搜索函数 ==========
print("\n===== 安全搜索函数 =====")

def safe_search(pattern_str, text):
    """安全的正则搜索"""
    try:
        pattern = re.compile(pattern_str)
        match = pattern.search(text)
        return match.group() if match else None
    except re.error as e:
        print(f"正则表达式错误: {e}")
        return None

# 测试
result1 = safe_search(r"\d+", "abc123")
print(f"正确正则: {result1}")

result2 = safe_search(r"[abc", "abc")
# 输出: 正则表达式错误: ...

# ========== 示例4：验证正则表达式 ==========
print("\n===== 验证正则表达式 =====")

def validate_regex(pattern_str):
    """验证正则表达式是否有效"""
    try:
        re.compile(pattern_str)
        return True, None
    except re.error as e:
        return False, str(e)

# 用户输入的正则
user_patterns = [
    r"\d{4}-\d{2}-\d{2}",  # 正确
    r"[a-zA-Z]+",          # 正确
    r"(unclosed",          # 错误
]

for p in user_patterns:
    valid, error = validate_regex(p)
    status = "有效" if valid else f"无效: {error}"
    print(f"'{p}': {status}")

# ========== 示例5：捕获错误的位置 ==========
print("\n===== 错误位置信息 =====")

try:
    re.compile(r"abc(123")
except re.error as e:
    print(f"错误信息: {e}")
    print(f"错误类型: {type(e)}")

# ========== 示例6：批量处理正则 ==========
print("\n===== 批量处理正则 =====")

patterns_dict = {
    'phone': r'1[3-9]\d{9}',
    'email': r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}',
    'invalid': r'[unclosed'
}

compiled_patterns = {}
errors = {}

for name, pattern_str in patterns_dict.items():
    try:
        compiled_patterns[name] = re.compile(pattern_str)
    except re.error as e:
        errors[name] = str(e)

print(f"编译成功: {list(compiled_patterns.keys())}")
print(f"编译失败: {errors}")
```

**输出结果**：

```
===== 捕获语法错误 =====
错误: '((\d+)' -> missing ), unterminated subpattern at position 0
错误: '[a-z' -> missing ], unterminated character set at position 0
错误: '*abc' -> nothing to repeat at position 0
正确: '\d+'

===== 常见错误示例 =====
括号不匹配: missing ), unterminated subpattern at position 0
无效重复: nothing to repeat at position 2
无效转义: bad escape (end of pattern at position 0)
无效字符集: bad character range 'z-a' at position 1

===== 安全搜索函数 =====
正确正则: 123

===== 验证正则表达式 =====
'\d{4}-\d{2}-\d{2}': 有效
'[a-zA-Z]+': 有效
'(unclosed': 无效: missing ), unterminated subpattern at position 0

===== 错误位置信息 =====
错误信息: missing ), unterminated subpattern at position 3
错误类型: <class 're.error'>

===== 批量处理正则 =====
编译成功: ['phone', 'email']
编译失败: {'invalid': 'missing ), unterminated character set at position 0'}
```

# 4. `Pattern` 对象详解

```python
import re

print("=" * 60)
print("Pattern 对象详解")
print("=" * 60)

# ========== Pattern 对象的创建 ==========
print("\n===== 创建 Pattern 对象 =====")

# 方式1：直接创建
pattern1 = re.compile(r"\d+")

# 方式2：带标志创建
pattern2 = re.compile(r"hello", re.IGNORECASE)

print(f"pattern1: {pattern1}")
print(f"pattern2: {pattern2}")

# ========== Pattern 对象的属性 ==========
print("\n===== Pattern 对象属性 =====")

# 创建一个带命名分组的Pattern
pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")

print(f"正则表达式字符串: {pattern.pattern}")
print(f"编译标志: {pattern.flags}")
print(f"捕获分组数量: {pattern.groups}")
print(f"命名分组映射字典: {pattern.groupindex}")

# ========== Pattern 对象的方法 ==========
print("\n===== Pattern 对象方法 =====")

phone_pattern = re.compile(r"1[3-9]\d{9}")
text = "联系电话：13812345678，备用：13987654321"

# match - 从开头匹配
m = phone_pattern.match(text)
print(f"match结果: {m}")  # None，因为开头不是手机号

# search - 搜索第一个
s = phone_pattern.search(text)
print(f"search结果: {s.group()}")  # 13812345678

# findall - 查找所有
f = phone_pattern.findall(text)
print(f"findall结果: {f}")  # ['13812345678', '13987654321']

# finditer - 返回迭代器
print("finditer结果:")
for match in phone_pattern.finditer(text):
    print(f"  {match.group()} at {match.span()}")

# sub - 替换
sub_result = phone_pattern.sub("***********", text)
print(f"sub结果: {sub_result}")

# subn - 替换并返回次数
sub_result2, count = phone_pattern.subn("***********", text)
print(f"subn结果: {sub_result2}, 替换次数: {count}")

# split - 分割
text2 = "手机13812345678和13987654321"
split_result = phone_pattern.split(text2)
print(f"split结果: {split_result}")

# fullmatch - 完整匹配
fm = phone_pattern.fullmatch("13812345678")
print(f"fullmatch结果: {fm.group() if fm else None}")

# ========== Pattern 对象的 pos 和 endpos 参数 ==========
print("\n===== pos 和 endpos 参数 =====")

pattern = re.compile(r"\d+")
text = "abc123def456ghi789"

# 限制搜索范围
result = pattern.search(text, pos=6, endpos=12)
print(f"在位置6-12搜索: {result.group() if result else None}")

# ========== 使用 Pattern 处理大量数据 ==========
print("\n===== 处理大量数据 =====")

# 预编译后重复使用（性能优化）
import time

texts = [f"文本{i}包含数字{12345+i}" for i in range(10000)]

# 使用预编译的Pattern
pattern = re.compile(r"\d+")
start = time.time()
for t in texts:
    pattern.search(t)
time1 = time.time() - start

# 不编译直接使用
start = time.time()
for t in texts:
    re.search(r"\d+", t)
time2 = time.time() - start

print(f"预编译耗时: {time1:.4f}秒")
print(f"未编译耗时: {time2:.4f}秒")
print(f"性能提升: {time2/time1:.2f}倍")
```

**输出结果**：

```
============================================================
Pattern 对象详解
============================================================

===== 创建 Pattern 对象 =====
pattern1: re.compile('\\d+')
pattern2: re.compile('hello', re.IGNORECASE)

===== Pattern 对象属性 =====
正则表达式字符串: (?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})
编译标志: 32
捕获分组数量: 3
命名分组映射字典: {'year': 1, 'month': 2, 'day': 3}

===== Pattern 对象方法 =====
match结果: None
search结果: 13812345678
findall结果: ['13812345678', '13987654321']
finditer结果:
  13812345678 at (6, 17)
  13987654321 at (22, 33)
sub结果: 联系电话：***********，备用：***********
subn结果: 联系电话：***********，备用：***********, 替换次数: 2
split结果: ['手机', '和', '']
fullmatch结果: 13812345678

===== pos 和 endpos 参数 =====
在位置6-12搜索: 456

===== 处理大量数据 =====
预编译耗时: 0.0089秒
未编译耗时: 0.0156秒
性能提升: 1.75倍
```

# 5. `Match` 对象详解

```python
import re

print("=" * 60)
print("Match 对象详解")
print("=" * 60)

# ========== 创建 Match 对象 ==========
text = "产品ID: ABC123, 价格: 999元"
pattern = re.compile(r"产品ID:\s*(\w+),\s*价格:\s*(\d+)元")
match = pattern.search(text)

# ========== Match 对象的方法 ==========
print("\n===== Match 对象方法 =====")

if match:
    # group() - 获取匹配内容
    print(f"group(0) 完整匹配: {match.group(0)}")
    print(f"group(1) 第一个分组: {match.group(1)}")
    print(f"group(2) 第二个分组: {match.group(2)}")
    print(f"group() 默认完整匹配: {match.group()}")
    
    # groups() - 返回所有分组元组
    print(f"\ngroups() 所有分组: {match.groups()}")
    
    # start(), end(), span() - 位置信息
    print(f"\nstart() 匹配开始位置: {match.start()}")
    print(f"end() 匹配结束位置: {match.end()}")
    print(f"span() 位置元组: {match.span()}")

# ========== 带命名分组的 Match ==========
print("\n===== 带命名分组的 Match =====")

text2 = "姓名: 张三, 年龄: 25, 城市: 北京"
pattern2 = re.compile(r"姓名:\s*(?P<name>\w+),\s*年龄:\s*(?P<age>\d+),\s*城市:\s*(?P<city>\w+)")
match2 = pattern2.search(text2)

if match2:
    # 通过名称获取分组
    print(f"姓名: {match2.group('name')}")
    print(f"年龄: {match2.group('age')}")
    print(f"城市: {match2.group('city')}")
    
    # groupdict() - 返回命名分组字典
    print(f"\ngroupdict() 分组字典: {match2.groupdict()}")

# ========== Match 对象的属性 ==========
print("\n===== Match 对象属性 =====")

if match:
    print(f"string 原始字符串: {match.string}")
    print(f"re Pattern对象: {match.re}")
    print(f"pos 搜索起始位置: {match.pos}")
    print(f"endpos 搜索结束位置: {match.endpos}")
    print(f"lastindex 最后分组索引: {match.lastindex}")

# ========== 多重匹配中的 Match ==========
print("\n===== 多重匹配示例 =====")

text3 = "2023-12-25, 2024-01-15, 2025-03-20"
pattern3 = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

for m in pattern3.finditer(text3):
    print(f"\n匹配: {m.group(0)}")
    print(f"年: {m.group(1)}, 月: {m.group(2)}, 日: {m.group(3)}")
    print(f"位置: {m.span()}")

# ========== expand() 方法 ==========
print("\n===== expand() 方法 =====")

text4 = "Hello World"
pattern4 = re.compile(r"(\w+) (\w+)")
match4 = pattern4.search(text4)

if match4:
    # 使用 expand 展开模板
    result = match4.expand(r"First: \1, Second: \2")
    print(f"expand结果: {result}")

# ========== Match 对象在替换中的应用 ==========
print("\n===== 在函数替换中使用 Match =====")

def format_price(match):
    """格式化价格"""
    price = int(match.group(1))
    currency = match.group(2)
    
    if currency == "USD":
        return f"${price:.2f}"
    elif currency == "CNY":
        return f"￥{price}"
    else:
        return match.group(0)

text5 = "价格: 100 USD, 价格: 200 CNY"
pattern5 = re.compile(r"(\d+)\s+(USD|CNY)")
result = pattern5.sub(format_price, text5)
print(f"替换结果: {result}")

# ========== 嵌套分组 ==========
print("\n===== 嵌套分组 =====")

text6 = "表达式 (abc123def) 匹配"
pattern6 = re.compile(r"\(([a-z]+)(\d+)([a-z]+)\)")
match6 = pattern6.search(text6)

if match6:
    print(f"完整匹配: {match6.group(0)}")
    print(f"外层分组: {match6.group(1)}, {match6.group(2)}, {match6.group(3)}")
    print(f"所有分组: {match6.groups()}")

# ========== 实战：解析复杂日志 ==========
print("\n===== 实战：解析日志 =====")

log_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s"
    r"\[(?P<level>\w+)\]\s"
    r"(?P<message>.+)"
)

log_line = "2023-12-25 10:30:45 [ERROR] Database connection failed"
match_log = log_pattern.match(log_line)

if match_log:
    print(f"时间: {match_log.group('timestamp')}")
    print(f"级别: {match_log.group('level')}")
    print(f"消息: {match_log.group('message')}")
    print(f"\n完整信息: {match_log.groupdict()}")

```

**输出结果**：

```
============================================================
Match 对象详解
============================================================

===== Match 对象方法 =====
group(0) 完整匹配: 产品ID: ABC123, 价格: 999元
group(1) 第一个分组: ABC123
group(2) 第二个分组: 999
group() 默认完整匹配: 产品ID: ABC123, 价格: 999元

groups() 所有分组: ('ABC123', '999')

start() 匹配开始位置: 0
end() 匹配结束位置: 21
span() 位置元组: (0, 21)

===== 带命名分组的 Match =====
姓名: 张三
年龄: 25
城市: 北京

groupdict() 分组字典: {'name': '张三', 'age': '25', 'city': '北京'}

===== Match 对象属性 =====
string 原始字符串: 产品ID: ABC123, 价格: 999元
re Pattern对象: re.compile('产品ID:\\s*(\\w+),\\s*价格:\\s*(\\d+)元')
pos 搜索起始位置: 0
endpos 搜索结束位置: 21
lastindex 最后分组索引: 2

===== 多重匹配示例 =====

匹配: 2023-12-25
年: 2023, 月: 12, 日: 25
位置: (0, 10)

匹配: 2024-01-15
年: 2024, 月: 01, 日: 15
位置: (12, 22)

匹配: 2025-03-20
年: 2025, 月: 03, 日: 20
位置: (24, 34)

===== expand() 方法 =====
expand结果: First: Hello, Second: World

===== 在函数替换中使用 Match =====
替换结果: 价格: $100.00, 价格: ￥200

===== 嵌套分组 =====
完整匹配: (abc123def)
外层分组: abc, 123, def
所有分组: ('abc', '123', 'def')

===== 实战：解析日志 =====
时间: 2023-12-25 10:30:45
级别: ERROR
消息: Database connection failed

完整信息: {'timestamp': '2023-12-25 10:30:45', 'level': 'ERROR', 'message': 'Database connection failed'}
```

# 6. 正则表达式语法速查表

## 6.1 元字符

| 元字符  | 说明                        | 示例                        |
| ------- | --------------------------- | --------------------------- |
| `.`     | 匹配任意字符（除换行 `\n`） | `a.c` 匹配 abc, a1c         |
| `^`     | 匹配字符串开头              | `^Hello` 匹配开头的Hello    |
| `$`     | 匹配字符串结尾              | `end$` 匹配结尾的end        |
| `*`     | 匹配前一个字符 0次或多次    | `ab*c` 匹配 ac, abc, abbc   |
| `+`     | 匹配前一个字符 1次或多次    | `ab+c` 匹配 abc, abbc       |
| `?`     | 匹配前一个字符 0次或1次     | `ab?c` 匹配 ac, abc         |
| `{m}`   | 精确匹配 m 次               | `a{3}` 匹配 aaa             |
| `{m,n}` | 匹配 m 到 n 次              | `a{2,4}` 匹配 aa, aaa, aaaa |
| `{m,}`  | 匹配至少 m 次               | `a{2,}` 匹配 aa, aaa, aaaa… |
| `{,n}`  | 匹配至多 n 次               | `a{,3}` 匹配空, a, aa, aaa  |
| `       | `                           | 或运算                      |
| `[]`    | 字符集                      | `[abc]` 匹配 a, b, c        |
| `[^]`   | 否定字符集                  | `[^abc]` 匹配非 a,b,c       |
| `()`    | 分组                        | `(ab)+` 匹配 ab, abab       |

## 6.2 特殊字符类

| 字符 | 说明       | 等价于          |
| ---- | ---------- | --------------- |
| `\d` | 数字       | `[0-9]`         |
| `\D` | 非数字     | `[^0-9]`        |
| `\w` | 单词字符   | `[a-zA-Z0-9_]`  |
| `\W` | 非单词字符 | `[^\w]`         |
| `\s` | 空白字符   | `[ \t\n\r\f\v]` |
| `\S` | 非空白字符 | `[^\s]`         |
| `\b` | 单词边界   | -               |
| `\B` | 非单词边界 | -               |

## 6.3 分组语法

| 语法            | 说明                 |
| --------------- | -------------------- |
| `(...)`         | 普通分组             |
| `(?P<name>...)` | 命名分组             |
| `(?:...)`       | 非捕获分组（不保存） |
| `(?=...)`       | 正向先行断言         |
| `(?!...)`       | 负向先行断言         |
| `(?<=...)`      | 正向后行断言         |
| `(?<!...)`      | 负向后行断言         |

## 6.4 标志(Flags)

| 标志            | 简写   | 说明           |
| --------------- | ------ | -------------- |
| `re.IGNORECASE` | `re.I` | 忽略大小写     |
| `re.MULTILINE`  | `re.M` | 多行模式       |
| `re.DOTALL`     | `re.S` | `.` 匹配换行符 |
| `re.VERBOSE`    | `re.X` | 可读性模式     |
| `re.ASCII`      | `re.A` | ASCII匹配      |
| `re.LOCALE`     | `re.L` | 本地化匹配     |

# 7. 工程实战案例

## 7.1 数据清洗工具类

```python
import re

class DataCleaner:
    """数据清洗工具类"""
    
    @staticmethod
    def clean_html(html_text):
        """清理HTML标签"""
        # 去除HTML标签
        text = re.sub(r"<[^>]+>", "", html_text)
        # 去除HTML实体
        text = re.sub(r"&[a-zA-Z]+;", "", text)
        # 去除多余空白
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    
    @staticmethod
    def clean_whitespace(text):
        """清理空白字符"""
        # 统一换行符
        text = re.sub(r"[\r\n]+", "\n", text)
        # 去除行首行尾空白
        text = re.sub(r"^\s+|\s+$", "", text, flags=re.MULTILINE)
        # 多个空格变一个
        text = re.sub(r" {2,}", " ", text)
        return text
    
    @staticmethod
    def clean_numbers(text):
        """统一数字格式"""
        # 去除千分位逗号
        text = re.sub(r"(\d),(\d)", r"\1\2", text)
        return text
    
    @staticmethod
    def remove_emojis(text):
        """移除表情符号"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # 表情
            "\U0001F300-\U0001F5FF"  # 符号
            "\U0001F680-\U0001F6FF"  # 交通
            "\U0001F1E0-\U0001F1FF"  # 旗帜
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub("", text)


# 使用示例
print("===== 数据清洗示例 =====")

cleaner = DataCleaner()

# 清理HTML
html = "<p>Hello   <b>World</b>!</p>"
print(f"清理HTML: '{cleaner.clean_html(html)}'")

# 清理空白
text = "Hello\n\n\nWorld   !"
print(f"清理空白: '{cleaner.clean_whitespace(text)}'")

# 移除表情
text_with_emoji = "Hello World! 😀🎉"
print(f"移除表情: '{cleaner.remove_emojis(text_with_emoji)}'")
```

## 7.2 日志解析器

```python
import re
from datetime import datetime

class LogParser:
    """日志解析器"""
    
    # 预编译常用正则
    TIMESTAMP_PATTERN = re.compile(
        r"(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})"
    )
    LEVEL_PATTERN = re.compile(r"\[(?P<level>\w+)\]")
    IP_PATTERN = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    
    @classmethod
    def parse_line(cls, line):
        """解析单行日志"""
        result = {
            'timestamp': None,
            'level': None,
            'ip': None,
            'message': line.strip()
        }
        
        # 提取时间戳
        ts_match = cls.TIMESTAMP_PATTERN.search(line)
        if ts_match:
            result['timestamp'] = f"{ts_match.group('date')} {ts_match.group('time')}"
        
        # 提取日志级别
        level_match = cls.LEVEL_PATTERN.search(line)
        if level_match:
            result['level'] = level_match.group('level')
        
        # 提取IP
        ip_match = cls.IP_PATTERN.search(line)
        if ip_match:
            result['ip'] = ip_match.group()
        
        return result
    
    @classmethod
    def parse_file(cls, content):
        """解析日志文件"""
        logs = []
        for line in content.strip().split('\n'):
            if line.strip():
                logs.append(cls.parse_line(line))
        return logs
    
    @classmethod
    def filter_by_level(cls, logs, level):
        """按级别过滤"""
        return [log for log in logs if log['level'] == level]
    
    @classmethod
    def get_error_logs(cls, logs):
        """获取错误日志"""
        return cls.filter_by_level(logs, 'ERROR')


# 使用示例
print("\n===== 日志解析示例 =====")

log_content = """
2023-12-25 10:30:45 [INFO] User login from 192.168.1.100
2023-12-25 10:31:20 [ERROR] Database connection failed
2023-12-25 10:32:15 [WARN] High memory usage detected
2023-12-25 10:33:00 [ERROR] API timeout from 10.0.0.55
"""

logs = LogParser.parse_file(log_content)
print(f"解析日志数: {len(logs)}")

for log in logs[:2]:
    print(f"  {log}")

errors = LogParser.get_error_logs(logs)
print(f"\n错误日志数: {len(errors)}")
for err in errors:
    print(f"  {err}")
```

## 7.3 表单验证器

```python
import re

class Validator:
    """表单验证器"""
    
    # 预编译常用正则
    PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
    EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$")
    ID_CARD_PATTERN = re.compile(r"^\d{17}[\dXx]$")
    URL_PATTERN = re.compile(r"^https?://[\w./-]+$")
    
    @classmethod
    def is_phone(cls, value):
        """验证手机号"""
        return bool(cls.PHONE_PATTERN.match(value))
    
    @classmethod
    def is_email(cls, value):
        """验证邮箱"""
        return bool(cls.EMAIL_PATTERN.match(value))
    
    @classmethod
    def is_id_card(cls, value):
        """验证身份证号"""
        return bool(cls.ID_CARD_PATTERN.match(value))
    
    @classmethod
    def is_url(cls, value):
        """验证URL"""
        return bool(cls.URL_PATTERN.match(value))
    
    @classmethod
    def is_ip(cls, value):
        """验证IP地址"""
        pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
        match = re.match(pattern, value)
        if match:
            parts = [int(match.group(i)) for i in range(1, 5)]
            return all(0 <= p <= 255 for p in parts)
        return False
    
    @classmethod
    def is_chinese(cls, value):
        """验证是否为中文"""
        return bool(re.fullmatch(r"[\u4e00-\u9fa5]+", value))
    
    @classmethod
    def check_password(cls, password):
        """检查密码强度"""
        checks = {
            'length': len(password) >= 8,
            'lowercase': bool(re.search(r"[a-z]", password)),
            'uppercase': bool(re.search(r"[A-Z]", password)),
            'digit': bool(re.search(r"\d", password)),
            'special': bool(re.search(r"[!@#$%^&*]", password))
        }
        checks['is_strong'] = all(checks.values())
        return checks
    
    @classmethod
    def validate(cls, data, rules):
        """批量验证"""
        errors = {}
        for field, rule_list in rules.items():
            value = data.get(field, '')
            for rule in rule_list:
                validator = getattr(cls, f'is_{rule}', None)
                if validator and not validator(value):
                    errors.setdefault(field, []).append(f"不符合{rule}格式")
        return errors if errors else None


# 使用示例
print("\n===== 表单验证示例 =====")

# 单个验证
print(f"手机号验证: {Validator.is_phone('13812345678')}")
print(f"邮箱验证: {Validator.is_email('test@example.com')}")
print(f"IP验证: {Validator.is_ip('192.168.1.1')}")

# 密码强度检查
password = "Abc123!@#"
result = Validator.check_password(password)
print(f"\n密码 '{password}' 强度: {result}")

# 批量验证
form_data = {
    'phone': '13812345678',
    'email': 'invalid-email',
    'ip': '300.1.1.1'
}

rules = {
    'phone': ['phone'],
    'email': ['email'],
    'ip': ['ip']
}

errors = Validator.validate(form_data, rules)
print(f"\n表单验证错误: {errors}")
```

## 7.4 数据提取器

```python
import re

class DataExtractor:
    """数据提取器"""
    
    # 预编译正则
    URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    EMAIL_PATTERN = re.compile(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}')
    PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')
    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fa5]+')
    NUMBER_PATTERN = re.compile(r'-?\d+\.?\d*')
    
    @classmethod
    def extract_urls(cls, text):
        """提取所有URL"""
        return cls.URL_PATTERN.findall(text)
    
    @classmethod
    def extract_emails(cls, text):
        """提取所有邮箱"""
        return cls.EMAIL_PATTERN.findall(text)
    
    @classmethod
    def extract_phones(cls, text):
        """提取所有手机号"""
        return cls.PHONE_PATTERN.findall(text)
    
    @classmethod
    def extract_chinese(cls, text):
        """提取所有中文"""
        return cls.CHINESE_PATTERN.findall(text)
    
    @classmethod
    def extract_numbers(cls, text):
        """提取所有数字"""
        numbers = cls.NUMBER_PATTERN.findall(text)
        return [float(n) if '.' in n else int(n) for n in numbers]
    
    @classmethod
    def extract_dates(cls, text):
        """提取所有日期 (YYYY-MM-DD)"""
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        return pattern.findall(text)
    
    @classmethod
    def extract_money(cls, text):
        """提取金额"""
        pattern = re.compile(r'[￥$]\s*(\d+(?:,\d{3})*(?:\.\d{2})?)')
        matches = pattern.findall(text)
        return [float(m.replace(',', '')) for m in matches]
    
    @classmethod
    def extract_all(cls, text):
        """提取所有类型数据"""
        return {
            'urls': cls.extract_urls(text),
            'emails': cls.extract_emails(text),
            'phones': cls.extract_phones(text),
            'chinese': cls.extract_chinese(text),
            'numbers': cls.extract_numbers(text),
            'dates': cls.extract_dates(text)
        }


# 使用示例
print("\n===== 数据提取示例 =====")

text = """
联系我们: support@example.com 或 sales@company.cn
电话: 13812345678, 13987654321
网站: https://example.com 和 http://test.cn/path
日期: 2023-12-25 至 2024-01-15
金额: ￥1,234.56 和 $999.99
中文内容: 你好世界
"""

print("提取URL:", DataExtractor.extract_urls(text))
print("提取邮箱:", DataExtractor.extract_emails(text))
print("提取手机:", DataExtractor.extract_phones(text))
print("提取日期:", DataExtractor.extract_dates(text))
print("提取金额:", DataExtractor.extract_money(text))

# 提取所有
all_data = DataExtractor.extract_all(text)
print("\n提取所有数据:")
for key, value in all_data.items():
    if value:
        print(f"  {key}: {value}")
```

# 8. 最佳实践总结

## 8.1 性能优先原则

```python
import re
import time

# ❌ 不推荐：每次都重新编译
def bad_practice(texts):
    results = []
    for text in texts:
        # 每次循环都重新编译正则
        match = re.search(r"\d+", text)
        results.append(match.group() if match else None)
    return results

# ✅ 推荐：预编译正则
def good_practice(texts):
    # 预编译一次
    pattern = re.compile(r"\d+")
    results = []
    for text in texts:
        match = pattern.search(text)
        results.append(match.group() if match else None)
    return results

# 性能测试
texts = [f"text{i}123" for i in range(10000)]

start = time.time()
bad_practice(texts)
time_bad = time.time() - start

start = time.time()
good_practice(texts)
time_good = time.time() - start

print(f"不预编译: {time_bad:.4f}秒")
print(f"预编译: {time_good:.4f}秒")
print(f"性能提升: {time_bad/time_good:.2f}倍")
```

## 8.2 代码可读性

```python
import re

# ❌ 不推荐：一行写完，难以阅读
pattern = r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})"

# ✅ 推荐：使用 re.VERBOSE 添加注释
datetime_pattern = re.compile(r"""
    (?P<year>\d{4})      # 年份：4位数字
    -                    # 日期分隔符
    (?P<month>\d{2})     # 月份：2位数字
    -                    # 日期分隔符
    (?P<day>\d{2})       # 日期：2位数字
    \s+                  # 空白分隔符（1个或多个）
    (?P<hour>\d{2})      # 小时：2位数字
    :                    # 时间分隔符
    (?P<minute>\d{2})    # 分钟：2位数字
    :                    # 时间分隔符
    (?P<second>\d{2})    # 秒：2位数字
""", re.VERBOSE)

text = "2023-12-25 10:30:45"
match = datetime_pattern.search(text)
if match:
    print(f"解析结果: {match.groupdict()}")
```

## 8.3 函数选择指南

| 需求场景           | 推荐函数       | 原因               |
| ------------------ | -------------- | ------------------ |
| 验证字符串开头格式 | `match()`      | 只检查开头，性能好 |
| 查找是否包含某模式 | `search()`     | 扫描整个字符串     |
| 提取所有匹配内容   | `findall()`    | 直接返回列表       |
| 处理大量匹配结果   | `finditer()`   | 迭代器，内存友好   |
| 严格验证整个字符串 | `fullmatch()`  | 完整匹配验证       |
| 批量替换文本       | `sub()`        | 支持函数替换       |
| 替换并统计次数     | `subn()`       | 返回替换次数       |
| 灵活分割字符串     | `split()`      | 支持正则分割       |
| 多次使用同一模式   | 先 `compile()` | 性能优化           |

## 8.4 常见错误避免

```python
import re

# 错误1：忘记转义特殊字符
# ❌ 错误
pattern = r"a.b"  # . 会匹配任意字符
# ✅ 正确
pattern = r"a\.b"  # 只匹配 a.b

# 错误2：贪婪匹配问题
text = "<div>内容1</div><div>内容2</div>"

# ❌ 贪婪匹配
result1 = re.findall(r"<div>.*</div>", text)
print(result1)  # ['<div>内容1</div><div>内容2</div>']

# ✅ 非贪婪匹配
result2 = re.findall(r"<div>.*?</div>", text)
print(result2)  # ['<div>内容1</div>', '<div>内容2</div>']

# 错误3：忘记处理 None
text = "abc"
match = re.search(r"\d+", text)
# ❌ 错误：可能报 AttributeError
# print(match.group())
# ✅ 正确：先检查
if match:
    print(match.group())

# 错误4：不处理异常
# ❌ 错误：正则语法错误会崩溃
# pattern = re.compile(r"[unclosed")
# ✅ 正确：捕获异常
try:
    pattern = re.compile(r"[unclosed")
except re.error as e:
    print(f"正则错误: {e}")

```

# 9. 总结

本文详细讲解了 Python re 模块的所有核心内容：

- **11个模块级函数**：match、search、findall、finditer、sub、subn、split、compile、fullmatch、escape、purge

- **3个类**：Pattern（编译后的正则）、Match（匹配结果）、error（异常）

- **工程实践**：数据清洗、日志解析、表单验证、数据提取

- **最佳实践**：预编译提升性能、VERBOSE增强可读性、异常处理保证健壮
