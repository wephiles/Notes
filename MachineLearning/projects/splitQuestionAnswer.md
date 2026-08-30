---
tags:
  - type/reference
  - lang/python
  - domain/computer-science
  - domain/computer-science/ml
  - topic/ml/train-and-use
  - status/published
  - source/self-study
author: wephiles
projectName:
aliases:
  - splitQuestionAnswer
datetime: " 2026-08-29 07:08:49 周六"
rating:
introduction: 学习机器学习，使用 www.aoshu.world 这个网址的爬虫数据作为数据源，训练一个可以拆分出题干答案和解析的机器学习模型。
---

<h1 align="center">splitQuestionAnswer</h1>

---

# 1. 第一步

## 1.1 环境搭建

### 1.1.1 检查显卡驱动

```python
nvidia-smi
```

看右上角 `CUDA Version`：**≥12.8 最稳**；如果显示 12.4/12.6，通常也能跑（CUDA 向下小版本兼容），但若后面报错就先升级驱动。

![image-20260829074033863](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829074043059.png)

### 1.1.2 创建项目与虚拟环境

Python 建议 3.11 或 3.12

```python
mkdir question-answer-parser && cd question-answer-parser
python -m venv .venv
.\.venv\Scripts\activate
```

我们采用 `Python 3.12.10`

![image-20260829074906195](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829074907074.png)

### 1.1.3 装基础镜像

走清华镜像源，速度较快。

```python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install lxml pandas matplotlib tqdm openai
```

> `openai` 现在不用，下周连本地 `Ollama` 的 `OpenAI` 兼容接口时用。

注意上述配置的时候别写错，如果写错网址会导致错误：

```python
ERROR: Could not find a version that satisfies the requirement lxml (from versions: none)
ERROR: No matching distribution found for lxml
```

如果出现错误，可以用下面的命里检查：

```python
pip config list -v
pip debug -v
```

 **`pip debug -v` 命令，它会显示 `index_urls` 字段，这个地址才是 pip 真正会去下载的源**。

如果你发现路径错误，可以使用下面的命令重新配置路径：

```python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

确认是否生效：

```python
pip config list
# 应显示：global.index-url='https://pypi.tuna.tsinghua.edu.cn/simple'
```

如果任然报错，尝试清除缓存后重试：

```python
pip cache purge
pip install pandas
```

### 1.1.4 装 `PyTorch cu128`

⚠️ 5060 Ti 的命门

```python
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

> `wheel` 约 3GB，耐心等。**千万不要** 直接 `pip install torch`（默认版本不支持 `sm_120`，会报 `no kernel image is available`）。

![image-20260829080802405](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829080803288.png)

下载成功:

![image-20260829081759300](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829081800698.png)

验证:

```python
import torch

print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
```

期望输出:

```python
2.11.0+cu128 True NVIDIA GeForce RTX 5060 Ti (12, 0)
```

![image-20260829083107721](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829083108884.png)

如果报错:

```python
Microsoft Visual C++ Redistributable is not installed, this may lead to the DLL load failure.
It can be downloaded at https://aka.ms/vs/17/release/vc_redist.x64.exe
Traceback (most recent call last):
  File "E:\Code\PyProjects\question-answer-parser\main.py", line 17, in <module>
    import torch
  File "E:\Code\PyProjects\question-answer-parser\.venv\Lib\site-packages\torch\__init__.py", line 285, in <module>
    _load_dll_libraries()
  File "E:\Code\PyProjects\question-answer-parser\.venv\Lib\site-packages\torch\__init__.py", line 281, in _load_dll_libraries
    raise err
OSError: [WinError 126] 找不到指定的模块。 Error loading "E:\Code\PyProjects\question-answer-parser\.venv\Lib\site-packages\torch\lib\c10.dll" or one of its dependencies.
```

这是因为:

> **缺少 `Microsoft Visual C++ Redistributable` 运行库**，这是 `PyTorch` 在 `Windows` 上运行的基础依赖。`c10.dll` 是 `PyTorch` 的核心 C++ 库，它依赖 `vcruntime140.dll` 和 `msvcp140.dll` 等 `Visual C++` 运行时组件。这些组件不属于 Windows 系统自带文件，尤其在全新安装或精简版系统中经常缺失。

去报错信息中提示的官网 `https://aka.ms/vs/17/release/vc_redist.x64.exe` 中下载安装即可。

### 1.1.5 装 `Ollama`

去 [ollama.com](https://ollama.com/) 下载 Windows 安装包安装；

拉取模型:

```python
ollama pull qwen2.5:7b-instruct
ollama run qwen2.5:7b-instruct "用一句话自我介绍"   # 冒烟测试
curl http://localhost:11434/v1/models              # 验证API可用（下周要用）
```

![image-20260829081513258](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829081514173.png)

拉取成功：

![image-20260829082246559](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829082247905.png)

冒烟测试：

![image-20260829082524478](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829082525489.png)

验证 API 是否可用：

![image-20260829082608563](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260829082609508.png)

### 1.1.6 建立仓库骨架

```python
aoshu-parser/
├─ data/raw/pages.jsonl     # 原始数据（版权原因，绝不 commit 到公开仓库）
├─ scripts/profile_pages.py # 本周的体检脚本
├─ reports/                 # 体检报告输出
├─ figs/                    # 统计图（README 素材）
├─ src/                     # 后续管道代码
├─ README.md
└─ .gitignore               # 写入：.venv/ data/ __pycache__/
```

关于上述步骤可能出现的问题及解决方法：

| 症状                              | 原因          | 解决                                          |
| --------------------------------- | ------------- | --------------------------------------------- |
| `no kernel image is available`    | torch 版本旧  | 重装 cu128 wheel                              |
| `torch.cuda.is_available()=False` | 驱动旧/装错包 | 升级驱动；确认版本号带 `+cu128`               |
| pip 极慢                          | 默认源        | 已设清华镜像；torch 走 pytorch 官方源是正常的 |

## 1.2 数据体检脚本

保存为 `scripts/profile_pages.py`

```python

```

关于上述脚本，有一些重要知识点需要注意：

### 1.2.1 `tree = lxml.html.fromstring()`

它接收一个包含 HTML 内容的**字符串**（或字节串），将其解析构建成一棵**树状结构**（DOM 树）。

- 特性
  - **容错性强**：即使你传入的 HTML 标签不闭合（如 `<div>...` 缺少 `</div>`）或格式混乱，它也会像浏览器一样自动修复补全。
  - **与 XML 区别**：`lxml.html` 专门针对 HTML（比 `lxml.etree` 解析 XML 更宽松，且能正确处理 `<br>`、`<hr>` 等自闭合标签）。

- 返回的 `tree` 是什么对象
  - 返回一个**`lxml.html.HtmlElement`** 对象（本质上是 `lxml.etree._Element` 的子类）
  - **特别注意**：它返回的是**整个 HTML 文档的根节点**（即 `<html>` 标签对应的元素），**而不是**一个包含整个文档的“列表”或“包装器”。
    - 可以类比为**“指向树根的遥控器”**，而不是“装树的箱子”。

- 如何使用返回的 `tree` 对象

  - `CSS` 选择器

    ```python
    # 提取 <h1> 的文本
    title = tree.cssselect('h1')[0].text_content()
    print(title)  # 输出: 标题
    
    # 提取 id 为 main 的 div
    div = tree.cssselect('#main')[0]
    ```

  - `XPATH`

    ```python
    # 提取所有段落文本
    paragraphs = tree.xpath('//p/text()')
    
    # 提取所有 a 标签的 href 属性
    links = tree.xpath('//a/@href')
    
    # 提取 class 包含 "price" 的元素
    prices = tree.xpath('//*[contains(@class, "price")]')
    ```

  - 遍历与直接属性访问

    - **`.text_content()`**：获取该元素及其子元素内的所有**文本内容**（去标签，递归获取）。
    - **`.text`**：只获取**当前标签直系的第一层**文本。如果文本在子标签里，`.text` 获取不到或返回 `None`。
    - **`.get(key, default)`**：获取某个属性值。例如 `.get('href')`。
    - **`.items()`**：获取所有属性键值对。
    - **`.findall()` / `.find()`**：支持简单的 `ElementPath` 语法（但建议用 `CSS` 或 `XPath` 替代）。

  - 动态修改HTML

    ```python
    # 修改文本
    div = doc.cssselect('div')[0]
    div.text = "新内容"
    
    # 添加新属性
    div.set('class', 'highlight')
    
    # 添加子元素
    new_p = html.fromstring('<p>追加的段落</p>')  # 注意这里重新解析，或使用 etree.SubElement
    div.append(new_p)
    
    # 转回 HTML 字符串
    output_html = html.tostring(doc, encoding='unicode', pretty_print=True)
    print(output_html)
    ```

### 1.2.2 `tree.iter()`

它的作用是**递归地、深度优先地遍历**当前节点下的**所有后代元素节点**（不包括文本节点，只遍历标签）。

特性：

- 默认遍历所有标签（`html`、`body`、`div`、`p`……）。
- 支持**过滤**，只遍历指定标签。
- 返回一个**生成器（迭代器）**，内存友好，适合处理大文档。

```python
html_str = """
<div>
    <p>段落1</p>
    <span>文字</span>
    <div><a href="a/b.html">链接</a></div>
</div>
"""
root = html.fromstring(html_str)

# 1. 遍历所有元素标签
for elem in root.iter():
    print(elem.tag)  
# 输出: div, p, span, div, a  （注意：根 div 也会被遍历到）

# 2. 只遍历所有的 <a> 标签（过滤）
for a in root.iter('a'):
    print(a.get('href'))  # 输出: a/b.html
```

### 1.2.3 `tree.xpath`

**永远返回一个 Python 列表（`list`）。**

但**列表里面装的东西**取决于写的 `XPath` 表达式，分为以下三种情况：

| XPath 表达式类型     | 列表中的元素类型             | 举例                                                     |
| :------------------- | :--------------------------- | :------------------------------------------------------- |
| **匹配标签（元素）** | `lxml.html.HtmlElement` 对象 | `tree.xpath('//div')` → `[<Element div>, ...]`           |
| **提取文本**         | **Python 字符串（`str`）**   | `tree.xpath('//p/text()')` → `['段落1', '段落2']`        |
| **提取属性**         | **Python 字符串（`str`）**   | `tree.xpath('//a/@href')` → `['https://...', '/page/2']` |
| **计算或布尔判断**   | **布尔值（`bool`）或浮点数** | `tree.xpath('count(//p)')` → `3.0`                       |

如果 `XPath` 没有匹配到任何内容，返回的是**空列表 `[]`**（而不是 `None`）。所以在写代码时，直接用 `if results:` 判断即可，不用担心报错。

### 1.2.4 `tree.xpath("...")[0]`

可以直接遍历此标签元素，但是只会遍历直系标签且不会遍历文本。

```python
from lxml import html

html_str = """
<html>
    <body>
        <div>
            <p>我是孙子</p>
        </div>
        <span>我是直系</span>
    </body>
</html>
"""
root = html.fromstring(html_str)
hits = root.xpath('//body')  # 获取 body 元素
body = hits[0]

print("使用 for kid in body: 遍历结果：")
for kid in body:
    print(kid.tag)  # 输出: div , span

print("\n使用 body.iter() 递归遍历结果：")
for kid in body.iter():
    print(kid.tag)  # 输出: body, div, p, span
```

注意点：

- **它只遍历“标签”，完全忽略文本节点**
- **如果该元素没有任何子标签，循环直接跳过（不会报错）**
- **`tree.xpath("...")[0]` 可能是字符串（致命陷阱）**

### 1.2.5 `element.tail`

`ele.tail` 返回的是一个**字符串（`str`）**，或者**`None`**（当没有尾部文本时）。

这是 `lxml`（以及 `ElementTree`）中**最容易被新手忽略，但处理“内联标签”时又极其重要**的属性。

一个核心口诀：

> **`.text` 是“闭合标签之前”的文本，`.tail` 是“闭合标签之后”的文本。**

示例：

```html
<p>
	你好
	<b>加粗</b>
	后面的文字
</p>
```

在 `lxml` 中，`<b>` 标签对应的元素 `ele`，它的文本分布是这样的：

- `ele.text` → `"加粗"` （标签 `<b>` 开始到 `</b>` 结束之间的文本）
- `ele.tail` → `"后面的文字"` （标签 `</b>` **结束之后**，到下一个兄弟标签 `<xxx>` 或父标签 `</p>` **之前**的文本）

再举一个例子：

```python
<div>
开头
    <span>A</span>
    中间
    <span>B</span>
    结尾
</div>
```

- `span_A.tail` → `"中间"` （因为 A 闭合后，直到下一个 span 前的文字是“中间”）
- `span_B.tail` → `"结尾"` （因为 B 闭合后，直到 div 闭合前的文字是“结尾”）

示例：

```python
html_string = """<html>
<body>
        <root>
            <div>
                哈哈哈
                <img>
                <div></div>
                <div class="test-data">
                    嘻嘻嘻
                    <a>aaa</a>
                    嘤嘤嘤
                    <a>bbb</a>
                    喂喂喂
                    <a>ccc</a>
                    哈哈哈
                </div>
                呜呜呜啦啦啦
            </div>
            哼哼哼
            <div></div>
        </root>
    </body>
</html>
"""

root = html.fromstring(html_string).xpath('//div[@class="test-data"]')[0]
print('-' * 64)
print(root.text_content())
print('-' * 64)
print(root.text)
print('-' * 64)
print(root.tail)
```

```python
----------------------------------------------------------------

                    嘻嘻嘻
                    aaa
                    嘤嘤嘤
                    bbb
                    喂喂喂
                    ccc
                    哈哈哈
                
----------------------------------------------------------------

                    嘻嘻嘻
                    
----------------------------------------------------------------

                呜呜呜啦啦啦
            
```

关于在实际业务中使用这个标签：

#### 1.2.5.0 补充：HTML 中的块级标签和行内标签

- **块级标签**：**霸道总裁**。独占一整行，宽度默认撑满父容器。
- **行内标签**：**社交达人**。宽高由内容决定，只占必要空间，与其他行内元素肩并肩排列。

| 对比维度       | 块级标签 (Block)                | 行内标签 (`Inline`)                                          |
| :------------- | :------------------------------ | :----------------------------------------------------------- |
| **换行行为**   | 前后自带换行（从新行开始）      | 不换行，在一行内依次排列                                     |
| **默认宽度**   | `width: 100%`（撑满父级）       | 由内容或内部元素撑开                                         |
| **`CSS` 宽高** | 可设置 `width` / `height`       | **设置无效**（除非改成 `display: inline-block`）             |
| **内外边距**   | `margin` / `padding` 四边都生效 | `margin` 上下无效，左右有效；`padding` 上下不撑开背景但会覆盖 |
| **HTML 嵌套**  | 可包含块级和行内标签            | **一般情况下不建议包含块级标签**（会造成渲染异常，但在 `HTML5` 中语义上允许 `a` 包 `div`） |

##### 1.2.5.0.1 🔵 块级标签（Block-level Elements）

- **布局骨架类**
  - `<div>`（最常用容器）、`<hr>`（水平分割线）
  - 标题：`<h1>` ~ `<h6>`
  - 段落与引用：`<p>`、`<blockquote>`、`<pre>`（保留格式）
- **列表类**
  - `<ul>`（无序）、`<ol>`（有序）、`<dl>`（定义列表）以及它们的子项 `<li>`、`<dt>`、`<dd>`（子项也默认为块级）
- 表格与表单类
  - `<table>`、`<form>`、`<fieldset>`
- `HTML5` 语义化新标签
  - `<header>`、`<footer>`、`<section>`、`<article>`、`<nav>`、`<aside>`、`<main>`、`<figure>`

##### 1.2.5.0.2 🔴 行内标签（Inline-level Elements）

- **文本样式类**（常用作内联修饰）：

  - `<span>`（最常用行内容器）

  - `<a>`（超链接）

  - 文字强调：`<strong>`（加粗强调）、`<em>`（斜体强调）、`<b>`（纯加粗）、`<i>`（纯斜体）、`<u>`（下划线）

  - 上下标：`<sup>`、`<sub>`

  - 缩写与代码：`<abbr>`、`<code>`、`<kbd>`

- **特殊置换元素（行内但可以设置宽高）**：
  - `<img>`（图片）、`<input>`（输入框）、`<button>`（按钮）、`<textarea>`、`<select>`
  - 注意：这些虽是行内标签，但 `CSS` 默认为 **`inline-block`**，因此 `width`/`height` 有效，且自带高度撑开。

##### 1.2.5.0.3 在 `lxml` 爬虫中可能遇到的坑

理解了分类，你写爬虫时就要格外注意 **`text_content()` 对空格的处理差异**：

| 场景             | 代码示例                                                     | 输出结果                         | 原因                                                         |
| :--------------- | :----------------------------------------------------------- | :------------------------------- | :----------------------------------------------------------- |
| **块级标签拼接** | `<div>Hello</div><div>World</div>` 对父节点取 `text_content()` | `'HelloWorld'`（**中间无空格**） | 虽然浏览器渲染时两个 div 会换行，但 `lxml` 纯取文本**不会自动加换行符或空格**。 |
| **行内标签拼接** | `<span>Hello</span><span>World</span>`                       | `'HelloWorld'`（同样无空格）     | 正常情况。                                                   |
| **混合换行缩进** | `<div>\n <span>A</span>\n</div>`                             | `'\n A\n'`                       | 源码中的换行和缩进会被当作空白文本节点保留。                 |

**结论**：**不要依赖标签类型来获取文本间距**。如果你想拼接两个块级标签的内容，必须手动加分隔符（如 `" "` 或 `"\n"`），否则会粘在一起。

#### 1.2.5.1 提取一段带内联标签的完整文本（精准还原）

如果你用 `ele.text_content()`，它会自动递归拼接所有子标签的文本和 tail，**一行代码就能拿到所有文本**。但在某些特殊情况下，如果你**在遍历子标签**，就必须手动加上 `.tail`，否则会漏掉标签之间的文字。

```python
from lxml import html

raw = "<div>开头<span>A</span>中间<span>B</span>结尾</div>"
root = html.fromstring(raw)
div = root.xpath('//div')[0]

# 方法1（最推荐，省心）：直接取整个 div 的文本
print(div.text_content())  # 输出: 开头A中间B结尾

# 方法2（手动遍历子标签，必须加 tail）：
text_parts = []
for child in div:
    text_parts.append(child.text)  # A, B
    if child.tail:
        text_parts.append(child.tail)  # 中间, 结尾
# 但注意开头 "开头" 是 div.text，也要加上，所以通常复杂场景不建议手拼。
```

#### 1.2.5.2 爬取“答案选项”时提取字母后文字

常见于题库 HTML：`<li>A. 北京</li><li>B. 上海</li>`。虽然这里不太用 tail，但如果有人写成了 `<label>A.</label> 北京`，那么提取时就需要用 `.tail` 来拿选项内容。

### 1.2.6 `collections.Counter()`

`Counter` 是 Python 标准库 `collections` 模块中的一个类，专门用于**计数**。它是一个字典的子类，用来统计可哈希对象出现的次数。

```python
from collections import Counter

# 统计列表中元素出现的次数
nums = [1, 2, 2, 3, 3, 3]
c = Counter(nums)
print(c)  # Counter({3: 3, 2: 2, 1: 1})

# 统计字符串中字符出现次数
s = Counter("hello")
print(s)  # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

# 统计单词
words = Counter("the quick brown fox jumps over the dog".split())
print(words)  # Counter({'the': 2, 'quick': 1, ...})
```

#### 1.2.6.1. 访问计数

```
c = Counter("banana")
print(c['a'])   # 3
print(c['x'])   # 0  ← 关键：不存在的键返回 0，不会报错！
```

#### 1.2.6.2 最常见的 n 个元素

```
c = Counter("banana apple")
print(c.most_common(2))  # [('a', 4), ('n', 2)]
print(c.most_common())   # 全部，按次数从高到低
```

#### 1.2.6.3 更新计数

```
c = Counter("abc")
c.update("aab")     # 增加
print(c)            # Counter({'a': 3, 'b': 2, 'c': 1})

c.subtract("aaa")   # 减少
print(c)            # Counter({'b': 2, 'c': 1, 'a': 0})
```

#### 1.2.6.4 数学运算

```
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=5)

print(c1 + c2)  # 相加：Counter({'a': 4, 'b': 6})
print(c1 - c2)  # 相减（只保留正数）：Counter({'a': 2})
print(c1 & c2)  # 取交集（较小值）：Counter({'a': 1, 'b': 1})
print(c1 | c2)  # 取并集（较大值）：Counter({'b': 5, 'a': 3})
```

#### 1.2.6.5 使用技巧

```python
c = Counter([1, 2, 2, 3])

# 转成列表/字典
list(c.elements())   # [1, 2, 2, 3] 按计数展开元素
dict(c)              # {1: 1, 2: 2, 3: 1}

# 求总和
sum(c.values())      # 6

# 找出所有不重复元素
list(c)              # [1, 2, 3]

# total() 方法（Python 3.10+）
c.total()            # 6
```

**总结**：`Counter` 就是一个"为计数而生"的字典，访问缺失键不报错、提供频率排序和数学运算，是处理统计需求的首选工具。

#### 1.2.6.6 和 `defaultdict` 的区别

两者都是 `dict` 的子类，但设计目的完全不同：

| 特性               | `Counter`                                  | `defaultdict`                          |
| ------------------ | ------------------------------------------ | -------------------------------------- |
| **用途**           | 专门统计元素出现次数                       | 给字典提供默认值工厂                   |
| **默认值**         | 缺失键固定返回 `0`                         | 由你指定（`int`、`list`、`set` 等）    |
| **缺失键的副作用** | **不会**往字典里插入该键                   | **会**插入该键（值是默认值的初始状态） |
| **额外功能**       | `most_common()`、数学运算、`elements()` 等 | 无，就是一个普通字典                   |

1. 默认值机制不同

```
from collections import Counter, defaultdict

c = Counter()
d = defaultdict(int)

print(c['a'])   # 0
print(d['a'])   # 0 —— 效果一样，但原理不同
```

看起来一样，但检查一下字典内容：

```
print(c)  # Counter() —— 没有插入 'a'
print(d)  # defaultdict(int, {'a': 0}) —— 'a' 被插进去了！
```

**这是最容易被忽视的坑**：`defaultdict` 只是*读取*不存在的键，也会改变字典的长度。

2. defaultdict 更通用

`defaultdict(int)` 确实能模拟计数器：

```
d = defaultdict(int)
for x in [1, 2, 2, 3]:
    d[x] += 1
```

但 `defaultdict` 的真正强项是**值为容器**的场景：

```
# 按首字母分组 —— Counter 做不到
d = defaultdict(list)
for word in ['apple', 'banana', 'avocado']:
    d[word[0]].append(word)
print(d)  # {'a': ['apple', 'avocado'], 'b': ['banana']}

# 去重分组
d = defaultdict(set)
```

3. Counter 有专属功能

```
c = Counter("banana")

c.most_common(2)     # 取前 2 高频元素
c.elements()         # 按次数展开元素
c1 + c2, c1 - c2     # 计数运算
c.total()            # 总数
```

这些 `defaultdict` 都没有。

4. 允许的值不同

```
c = Counter()
c['a'] = -5       # 允许负数
c['b'] = "hello"  # 甚至允许非数字（虽然没意义）

d = defaultdict(int)
```

`Counter` 不强制值为整数，但它的数学运算（`+`、`-` 等）假定值为数字。另外 `+c`、`c1 & c2` 等操作会**自动丢弃非正数结果**。

如何选择？

- **只做计数** → 用 `Counter`，一行搞定还有配套工具

```
  Counter(data)  # ✅ 推荐
```

- **值为 list/set，需要分组、聚合** → 用 `defaultdict`

```
  defaultdict(list)  # ✅ 这种场景 Counter 无法胜任
```

- **需要控制缺失键的行为** → `defaultdict`（注意读也会插入键；如果想只读不插入，用普通 `dict` 的 `d.get(k, default)`）

**一句话总结**：`Counter` 是“专精计数器”，`defaultdict` 是“可定制默认值的字典”。计数用 Counter，分组用 defaultdict。

### 1.2.7 `statistics`

`statistics` 是 Python 标准库，专门用于**数理统计计算**，提供均值、中位数、方差、标准差等常用统计量。不用装第三方包，开箱即用。

常用函数一览

1. 平均数类

```
import statistics

data = [1, 2, 3, 4, 5]

statistics.mean(data)      # 3.0  算术平均
statistics.harmonic_mean(data)  # 2.189... 调和平均（算平均速率用）
statistics.geometric_mean(data) # 2.605... 几何平均（算平均增长率用）
statistics.fmean(data)     # 3.0  更快的浮点平均（推荐大数据用）
```

2. 中位数与分位数

```
statistics.median(data)         # 3     中位数
statistics.median_low(data)     # 3     偶数个元素时取较小那个
statistics.median_high(data)    # 3     偶数个元素时取较大那个
statistics.median_grouped(data) # 3     分组数据的中位数

statistics.quantiles(data, n=4)  # 四分位数（需至少2个数据点，示例见下）
statistics.quantiles(range(1, 11), n=4)
# [2.75, 5.5, 8.25] → 25%、50%、75% 分位点
```

3. 离散程度（波动大小）

```
data = [1, 2, 3, 4, 5]

statistics.pstdev(data)  # 1.414... 总体标准差
statistics.stdev(data)   # 1.581... 样本标准差（n-1，最常用）
statistics.pvariance(data)  # 2.0  总体方差
statistics.variance(data)   # 2.5  样本方差
```

4. 其他

```
statistics.mode([1, 2, 2, 3])   # 2    众数（出现最多）
statistics.multimode([1,1,2,2]) # [1, 2] 多众数
statistics.correlation(x, y)    # 相关系数（3.10+）
statistics.linear_regression(x, y)  # 线性回归（3.10+）
```

重点：median 的作用

**中位数**：把数据排序后位于正中间的数，一半数据比它大，一半比它小。

```
statistics.median([1, 3, 5])       # 3  奇数个 → 正中间那个
statistics.median([1, 3, 5, 7])    # 4  偶数个 → 中间两个的平均 (3+5)/2
statistics.median([5, 1, 3])       # 3  会自动先排序
statistics.median([1.5, 2.2, 0.8]) # 1.5 支持浮点数
```

median 的核心价值：抗极端值（抗离群点）

对比均值和中位数：

```
salaries = [3000, 3500, 4000, 4500, 100000]  # 有人工资特别高

statistics.mean(salaries)     # 22200  ← 被极端值拉高，严重失真
statistics.median(salaries)   # 4000   ← 更能代表"典型工资"
```

这就是为什么统计“平均房价”“人均收入”时，中位数往往比均值更真实。

三个变体的区别:

当元素个数是**偶数**时，中间有两个数：

```
data = [1, 2, 3, 100]

statistics.median(data)       # 2.5   取两数平均
statistics.median_low(data)   # 2     取较小的
statistics.median_high(data)  # 3     取较大的
```

- `median_low/high` 保证结果是**数据中真实存在的值**，适合如“中位价格的报价必须实际存在”的场景
- `median`（平均版）更符合数学定义

什么时候用 statistics？

✅ 数据量不大、需求简单（算个均值/中位数/标准差）
✅ 不想引入依赖

❌ 大规模数值计算、数组运算 → 用 **`NumPy`**（`np.median`、`np.mean` 快得多）
❌ 更专业的统计分析（假设检验、分布拟合）→ 用 **`SciPy**、**pandas`**

```
# 对比 NumPy 写法
import numpy as np
np.median([1, 3, 5])    # 3.0 —— 功能一样，但面向数组批量计算更快
```

**一句话总结**：`statistics` 是标准库里的“统计学瑞士军刀”；`median` 用来找中位数——排序后最中间的值，最大优点是不受极端值影响，适合描述偏态分布数据的“典型水平”。

### 1.2.8 `round` 函数

`round()` 是 Python 的内置函数，用于对数字进行**四舍五入（近似）**。

```python
round(number, ndigits=None)
```

- `number`：要近似的数字
- `ndigits`：保留几位小数，**可选**。不传则返回整数

```python
round(3.14159)      # 3    不带参数 → 返回 int
round(3.14159, 2)   # 3.14 保留 2 位小数
round(3.14159, 4)   # 3.1416
round(1234, -2)     # 1200 ← 负数表示对小数点左边"取整"到十位/百位
round(1567, -2)     # 1600
```

⚠️ 最重要的坑：不是传统“四舍五入”！

Python 3 的 `round` 采用 **银行家舍入法（round half to even）**：正好在中间时，舍入到**最近的偶数**。

```
round(0.5)    # 0  → 舍向偶数
round(1.5)    # 2  → 舍向偶数
round(2.5)    # 2  → 不是 3！
round(3.5)    # 4
round(-0.5)   # 0
round(-2.5)   # -2
```

⚠️ 第二个坑：浮点数精度问题

很多“看起来该进位”的数，实际二进制表示略小于 .5：

```
round(2.675, 2)   # 2.67，不是 2.68！
# 因为 2.675 在内存中实际是 2.67499999...
```

这是所有浮点数的通病（IEEE 754），不是 round 的 bug。

返回值类型：

```python
round(3.7)        # 4     int
round(3.7, 0)     # 4.0   float ← 指定位数（哪怕0位）返回 float
round(3.7, None)  # 4     int
```

为什么用银行家舍入？

传统“逢五必进”在大量数据上会**系统性偏高**（0.1~0.4 舍、0.5~0.9 进，进的机会多）。舍向偶数让 .5 的情况一半进一半舍，统计上更公平。这也是金融、统计领域的标准做法。

补充：

- `round()` 是**返回新值**，不修改原对象
- 对显示格式而言，`f"{x:.2f}"` 或 `format(x, ".2f")` 往往更合适（`round` 不会补零）：















































