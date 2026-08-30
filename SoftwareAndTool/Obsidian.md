---
tags:
  - common
  - note
rating: "0"
datetime: " 2026-08-28 18:08:85 周五"
category: note
tabulations: 👆 👇 👈 👉 ✍🏼 ✍🕓 🗓️ 📝 ✒️ 💡⏳✍ 🎨🎁 🚄 ✈️📝 👀📕📗✅❌ ♾️➕➖✖️➗
---
<h1 align="center">Obsidian</h1>

AI时代，笔记永远都有价值，但是视角变了，我们应该保存：

- 核心领域的知识（传统方式，个人核心竞争力）
- 思考过程和依据
- 判断
- 关键里程碑

AI 时代，如鱼得水的三种人：

- 有折腾能力的人
- 有自己方法论的人
- **有大量数据的人**

然后：

- 让笔记成为 AI 上下文
- 让 AI 更好地辅助个人
- 创造基于个人知识的智能体

Obsidian 实现 AI 功能：

- 插件生态开发
  - Text Generator
  - Copilot
  - Smart Connections
  - Local GPT
  - ...
- 结构开放
  - 资料库，即文件夹 + `.md` 文件
  - Agent 可以完全接管
- 文件开放
  - 基于 `MarkDown` 的语法

- 最终：实现 Agent 开放
  - Agent + LLM
  - 直接让 Agent 接管我们的资料库即可

# 1. Obsidian 能干什么

## 1.1 建立资料库

- 建立结构 + 笔记

## 1.2 让 Agent 接管资料库

- Agent 整理资料库结构
- Agent 整理、发现链接
- Agent 撰写、修改笔记
- Agent 整理 `frontmatter` 属性

## 1.3 形成工作流

- 记录随想、日常并且进行拓展
- 自动写日报、周报进行复盘 
- 每日推送回顾
- `...`

# 2. 上手 Obsidian

## 2.1 **Obsidian** 特性

- 本地存储
- 基于 Markdown
- 双链 -> 关系图谱
- 插件生态

资料库：Obsidian 管理的基本单位

延伸：使用工具的逻辑

- 使用工具提供的功能
- 管理工具支持的基本元素
- Obsidian 的基本元素：资料库、笔记

如何设置每次打开 Obsidian 打开指定的笔记？如下图所示，我们能够获取到一串路径：

```
obsidian://open?vault=aiFrontier&file=%E6%AC%A2%E8%BF%8E
```

![PixPin_2026-08-28_20-18-59](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828202138735.png)

然后在桌面新建快捷方式：

![image-20260828202425778](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828202430365.png)

然后点击“下一步”，输入一个自己容易找到的名字即可。

![image-20260828202637117](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828202638212.png)

这样，每次双击此链接就会直接打开这个文件了。

但是这样也有问题：我们不仅打开了资料库，又打开了里面的文件，所以需要将路径修改为：

```
obsidian://open?vault=aiFrontier&file=%E6%AC%A2%E8%BF%8E
	|
	| 将路径修改
	v
obsidian://open?vault=aiFrontier
```

![image-20260828203705243](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828203706187.png)

## 2.2 快速切换

**切换到某一个笔记**

![image-20260828204603002](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828204604022.png)

快捷键为 `Ctrl + o` （字幕`欧`而不是数字`零`）可以选择和搜索

找到想要的笔记后，如果想在新标签页打开想要切换到笔记，按住 `Ctrl` 点击笔记即可。

## 2.3 命令面板

![image-20260828204716232](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828204717816.png)

快捷键为 `Ctrl + p`

## 2.4 新建笔记

快捷键： `Ctrl + n`

## 2.5 打开笔记

按一下鼠标滚轮键，打开笔记到新标签页。

在打开的标签页按一下鼠标滚轮键，关闭打开的笔记。

拖动某一个笔记到右边（左右分屏）

拖动某一个笔记到下半部分（上下分屏）

## 2.6 堆叠标签页

![image-20260828212510171](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828212511224.png)

## 2.7 笔记面板

- 只读模式 `Ctrl + E`
  - 缩放
    - 放大 `Ctrl + =`
    - 缩小 `Ctrl+ -`
    - 还原 `Ctrl+ 0` --> 需要自己去 `设置 -- 快捷键 -- 重置缩放` 进行自定义绑定快捷键.

## 2.8 设置

![image-20260828213745017](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260828213746266.png)

## 2.9 插件

### 2.9.1 核心插件

建议开启的核心插件:

- 白板(`Canvas`)
- 标签列表
- 出链
- 大纲(笔记目录)
- 反向链接(入链)
- 关系图谱
- 快速切换
- 命令面板
- 模板
- 日记(可选)
- 数据库(`Bases`)
- 文件列表
- 字数统计





































