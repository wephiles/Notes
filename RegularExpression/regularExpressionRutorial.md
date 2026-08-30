<h1 style="text-align: center;">正则表达式教程</h1>

**教程索引：**

- [**`regex learn`**](https://regexlearn.com): 这是目前对**新手最友好**的网站之一。它将知识点拆解为56个小节，**必须完成练习才能解锁下一关**，学习路径非常清晰。最棒的是它提供**完整的中文翻译**，不用担心语言障碍。
- [**`RegexOne`**](https://regexone.com/): 另一个非常优秀的交互式学习平台。相较于 `RegexLearn`，它的章节选择更**自由灵活**，你可以直接跳到想学的部分。教程的**文字解释通常更详细一些**，适合喜欢阅读理解的同学。缺点是没有中文界面。
- [**`Regex101`**](https://regex101.com/): 这几乎是**所有开发者必备的瑞士军刀**。它的核心优势是**强大的实时解析功能**：输入一个正则表达式后，右侧栏会立即**逐层、逐字符地解释**这个表达式在做什么，匹配过程一目了然。还支持切换不同编程语言的正则引擎（`PCRE`、`JavaScript`、`Python`等），并提供代码生成功能。
- [**`regexr`**](https://regexr.com/): 界面非常**干净美观**，操作直观。同样支持实时高亮匹配和详细的解释。它的特色是有一个**社区模式**，你可以浏览别人分享的正则表达式，学习别人的写法，或者分享自己的。
- [**`Regular-Expression.info`**](https://www.regular-expressions.info): 这是一个**历史悠久、内容极其全面**的正则表达式专题网站。从最基础的概念到高级的技巧（如回溯、贪婪与懒惰匹配、原子组等）都有非常详细的讲解。很多其他教程的引用都源自于此。
- [**`MDN Web Docs`**](https://developer.mozilla.org/en-US/): `Mozilla` 开发者网络（`MDN`）提供的Web技术文档权威且实用。其正则表达式章节**紧密结合JavaScript**，非常适合前端开发者学习如何在`Web` 开发（如表单验证、字符串处理）中应用正则表达式。
- [**`Regex Crossword`**](https://regexcrossword.com/): 用填字游戏的方式练习正则表达式，需要根据模式填写正确的字符，非常锻炼对模式的整体把握能力。
- [**`codewars`** ](https://www.codewars.com/): 编程练习平台，有大量社区贡献的正则表达式“`Kata`”（挑战）。你可以看到其他高手的解决方案，学习更优雅的写法。
- [**`Regex Golf`**](https://alf.nu/RegexGolf?world=regex&level=r00): 挑战用最短的正则表达式匹配所有目标字符串，同时不匹配干扰字符串。非常考验对正则表达式引擎特性的理解和优化技巧。
- 书籍：**《精通正则表达式》**:这本书是正则表达式领域的**“圣经”**，由 `Jeffrey E.F. Friedl` 所著。它**不依赖于任何一种编程语言**，而是深入讲解了正则表达式的核心原理和机制。读完这本书，你将对正则表达式有“醍醐灌顶”的理解，知其然更知其所以然。

# 1. 视频教程 1

> 视频链接:  [一节课精通正则表达式与re模块](https://www.bilibili.com/video/BV1gaiRYTETX?vd_source=2c9a5d5590d3759367594e264ff079c4)

`Regular Expression`，正则表达式。正则表达式是一套独立于编程语言，用于处理复杂文本信息的强大的高级文本操作工具。正则表达式拥有自己独特的规则语法以及一个独立的正则处理引擎，我们根据正则语法编写好规则（模式）以后，引擎不仅能够根据规则进行模糊文本查找，还可以进行模糊分割，替换等复杂的文本操作，能让开发者随心所欲地处理文本信息。正则引擎一般由编程语言提供操作，像 `Python` 就提供了 `re` 模块或 `regex` 模块来调用正则处理引擎。

正则表达式在处理文本上的效率不如系统自带的字符串操作，但功能却比系统自带的要大得多。

最早的正则表达式来源于Perl语言，后面其他的编程语言在提供正则表达式操作时基本沿用了Perl语言的正则语法，所以我们学习 `Python` 的正则以后，也可以在`java`，`php`，`go`，`javascript`, `sql`等编程语言中使用。

正则对字符串或文本的操作，无非是分割、匹配、查找和替换。

正则在线测试工具👉 [在线测试工具](https://www.regexp.cn/Regex) 

示例：

![image-20260805194303542](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260805194312042.png)

自此处开始，下面的示例全部由 `Python` 程序演示。

## 1.1 元字符(Meta characters)

元字符是具有特殊含义的字符。常用的 11 个元字符就是正则的灵魂。

### 1.1.1 通配符

`.` 通配符：万能通配符或通配元字符，匹配一个除了 `\n` 以外的任何字符。

示例：

```python
import re

s = 'apple ape agree age amaze animate advertise a\ne'

print(re.findall(r'apple', s))  # ['apple']
print(re.findall(r'a.e', s))  # ['ape', 'age', 'aze', 'ate']
print(re.findall(r'a..e', s))  # ['agre', 'adve']
print(re.findall(r'a...e', s))  # ['apple', 'agree', 'amaze']
```

### 1.1.2 字符集

`[]` 字符集，匹配一个中括号中出现的任意原子符号

示例：

```python
import re

s = 'a,e apge apple ape agree age amaze animate advertise a\ne a&e a@e a6e a9e'

print(re.findall(r'a.e', s))  # ['a,e', 'ape', 'age', 'aze', 'ate', 'a&e', 'a@e', 'a6e', 'a9e']
print(re.findall(r'a[abc]e', s))  # []
print(re.findall(r'a[p]e', s))  # ['ape']
print(re.findall(r'a[p,g]e', s))  # ['a,e', 'ape', 'age']
print(re.findall(r'a[a-zA-Z]e', s))  # ['ape', 'age', 'aze', 'ate']
print(re.findall(r'a[^0-9]e', s))  # ['a,e', 'ape', 'age', 'aze', 'ate', 'a\ne', 'a&e', 'a@e'] 字符集中的 ^: 取反
print(re.findall(r'a[^a-zA-Z]e', s))  # ['a,e', 'a\ne', 'a&e', 'a@e', 'a6e', 'a9e']
print(re.findall(r'a[^a-zA-Z0-9]e', s))  # ['a,e', 'a\ne', 'a&e', 'a@e']
```

### 1.1.3 重复元字符













































