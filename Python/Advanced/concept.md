---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-14 19:08:48 周五"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">concept</h1>

# 1. LEGB 规则

Python 查找变量的顺序遵循 `LEGB` 规则：**L**ocal -> **E**nclosing -> **G**lobal -> **B**uilt-in。

- **`global`**：强制 Python 直接去 **G (Global)** 层寻找或创建变量。
- **`nonlocal`**：强制 Python 去 **E (Enclosing)** 层（外层函数）寻找变量。

