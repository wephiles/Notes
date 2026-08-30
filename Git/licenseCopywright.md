<h1 align="center">Git License 与 Copyright 完全指南</h1>

# 1. 什么是 Git license

严格说，“Git 本身没有自己的许可证”。所谓 “Git license” 是指给仓库选择/添加的**软件许可证**：

- 一份法律声明，说明别人对你的代码能做什么、不能做什么、需满足什么条件（署名、开源、保留版权声明等）；
- 通常放在仓库根目录的 `LICENSE` / `LICENSE.md` / `LICENSE.txt`。

# 2. 为什么要有 License

1. **法律默认：没有许可 = 别人啥都不能干**。代码受版权保护，不明确许可则默认保留所有权利，复制/分发/修改/再发布都可能侵权；
2. **明确权利与边界**，减少后续纠纷；
3. **便于社区与企业使用**：企业通常只敢用标准许可证的项目，标准许可证能提高项目被采用的概率。

# 3. 如何添加 License

推荐：**不要自己写，直接用现成标准文本**。

1. 从权威站点复制标准文本：
   - [Choose a License](https://choosealicense.com/)（GitHub 官方推荐，含"权限/条件/限制"对照表）；
   - [OSI 开源许可证列表](https://opensource.org/) ；
   - [SPDX 许可证列表](https://spdx.org/)（含标准短标识符如 `MIT`、`Apache-2.0`）。
2. 仓库根目录新建 `LICENSE` 文件，粘贴全文，替换年份与版权持有人；
3. （可选）README 中写一句：`This project is licensed under the MIT License – see the LICENSE file for details.`

GitHub 点选方式：新建仓库时 “Add a license”；已有仓库通过 Add file → Create new file 输入 `LICENSE` 选模板。

# 4. 常见许可证分类

## 4.1 宽松型（Permissive）：允许闭源/商用，要求保留版权声明

- **MIT**：非常宽松，“随便用”，只需保留版权与许可声明；适合希望被注明出处即可的项目；
- **Apache 2.0**：允许闭源商用；明确授予专利授权；要求对修改文件做说明；含专利报复条款；适合在意专利且商用友好的项目；
- **BSD 2-Clause / 3-Clause**：类似 MIT；3-Clause 不能用作者名字做推广；
- **0BSD**：几乎放弃一切权利，仅保留版权声明；
- **BSL-1.0**：源码分发需保留版权声明，二进制分发无硬性要求；
- **Unlicense**：直接献入公共领域，几乎无条件。

## 4.2 强 Copyleft（传染型）：修改/分发必须同许可证开源

- **GPL-2.0 / GPL-3.0**：允许商用，但分发修改版必须整体以 GPL 开源并提供源码；适合希望"软件永远保持开源"；
- **AGPL-3.0**：比 GPL 更强，网络使用也算分发（提供 Web API 也须向用户提供源码）。

## 4.3 弱 Copyleft / 文件级

- **LGPL-2.1 / 3.0**：库本身开源，但允许闭源主程序以特定方式链接；
- **MPL-2.0**：文件级 copyleft——修改的 MPL 源文件必须开源，但可与其它许可证文件组合，作品整体不必 MPL。

## 4.4 非软件许可证

- **CC 系列（CC BY / CC BY-SA / CC0 等）**：GitHub 可识别，但 **CC 官方不推荐用于软件**，适合文档、图片、文章、数据集等；
- **自制许可证**：不推荐（见第 5 节）。

# 5. 能自己随便写 License 吗

- **法律上**：可以，版权是你的权利，可附加任何许可；
- **实践上**：强烈不建议：
  - 企业需请律师逐条分析，成本高，干脆不用你的项目；
  - SPDX 等治理工具只识别标准许可证，自制许可证难以被自动检测归类；
  - 标准许可证已被广泛审查测试，自写的易有漏洞或歧义。

## 5.1 "标准"来源

- OSI 认可的开源许可证（满足开源定义 OSD 10 条标准）；
- SPDX 许可证列表及短标识符（`MIT`、`GPL-3.0`、`Apache-2.0` 等）。

# 6. 需求："个人免费 + 标明出处 + 不可商用"怎么写

## 6.1 关键点：这不是开源许可证

OSD 第 6 条：许可证不得歧视任何领域，"不得用于商业"不符合开源定义。即**禁止商用的许可证不属于开源许可证**，社区通常也视其为非自由软件许可证。

## 6.2 可操作方案

**方案 A：自制"非商业+署名"许可证**（不推荐但常见），核心条款示意：

```
1. 源码再分发须保留版权声明、条件列表与免责声明；
2. 二进制再分发须在文档/材料中复现版权声明与免责声明；
3. 未经事先书面许可，不得用版权人名义推广衍生产品；
4. 未经版权人另行商业授权，不得用于商业用途或以盈利为主要目的。
```

缺点：非标准、工具链不识别、"商用"界定模糊（如学校内部项目算不算商用）易争议。

**方案 B：CC BY-NC 4.0**（不推荐用于软件）：CC 官方明确不建议用于软件，很多开源社区与公司会直接避开。

**方案 C：更稳妥的折中**

- **AGPL-3.0**：允许商用，但任何修改与网络使用必须开源；
- **双重许可**：开源社区用 AGPL-3.0，需要闭源商用的公司单独签商业授权。

# 7. 补充实用知识点

## 7.1 没有 License 会怎样

- 默认版权法生效，复制/分发/修改都可能侵权；
- GitHub 公开仓库可浏览和 Fork，但**不等于**获得使用/修改/再发布许可；
- 很多社区/企业直接拒绝无许可证的项目。

## 7.2 不要中途随便改许可证

- 单作者项目理论上可随时改，但不影响之前已获得的权利；
- 多人贡献项目：每个贡献者都是其部分代码的版权人，重大变更理论上需所有贡献者同意；实践中用 **CLA（贡献者许可协议）** 统一权利。

## 7.3 不要混搭太多许可证

常见标准许可证（MIT/Apache/BSD/GPL 系列）兼容性较好；依赖一旦使用自制许可证，法律复杂性急剧上升，公司难以评估风险。

## 7.4 正确的"署名"包含

- 保留原始版权声明；
- 保留许可声明（如 “Licensed under the MIT License”）；
- 保留免责声明；
- 有的还要求说明对文件做了哪些修改。

## 7.5 机器可读标注（SPDX）

源文件头注释：

```
// SPDX-License-Identifier: MIT
// SPDX-License-Identifier: (MIT OR Apache-2.0)
```

## 7.6 许可证兼容性

- 宽松型之间通常兼容；
- 强 Copyleft 与宽松型**单向兼容**（MIT 代码可放入 GPL 项目，反之不行）；
- GPL v2 vs v3、GPL vs AGPL 之间也有兼容性问题，需具体分析。

# 8. Copyright 写法

## 8.1 标准写法

```
Copyright (c) 2024 张三
```

常见变体：

```
Copyright (c) 2022-2024 张三                 # 年份范围，表示持续维护中
Copyright (c) 2024 张三, 李四                # 多作者
Copyright (c) 2024 北京智谱华章科技有限公司  # 机构名义
Copyright (c) 2020, 2022, 2024 张三          # 不连续年份，表示有实质性更新
```

## 8.2 各部分规范

- **`Copyright` / `©` / `(c)`**：强烈推荐 `Copyright (c)`，`©` 在老旧终端/纯 ASCII 环境可能乱码；
- **年份**：单一年份（首次发布）或年份范围（活跃维护）；**不需要每年手动更新**，版权保护期很长，不更新同样受保护；懒得管就写首次发布年份；
- **持有人**：
  - 个人：推荐法定姓名；网名在纠纷时难以证明身份，如要用建议 `张三 (网名: CodingCat)` 或留邮箱；
  - 公司：必须写**法定注册名称**（部门名不具备主体资格）；在职期间写的代码通常归公司（视劳动合同）。

## 8.3 源码文件头也要写

`LICENSE` 是项目级声明，核心源码文件（`.py`、`.java`、`.ts` 等）头部也建议加简短版权声明：

```
/*
 * Copyright (c) 2024 张三. All rights reserved.
 *
 * This software is licensed under the MIT license.
 * See the LICENSE file for details.
 */
```

好处：单文件被拷贝时版权声明跟着文件走。

## 8.4 多贡献者项目

- 无 CLA 时，**每个提交过代码的人都是其部分代码的版权人**；直接只写自己的名字属于侵权；
- 小项目：写 `Copyright (c) 2024 张三及贡献者`（法律上不严谨但社区可接受）；
- 规范项目：通过 Git 提交记录列出实质性贡献者 `Copyright (c) 2024 张三, 李四, 王五`；
- 企业项目：引入 CLA，让贡献者签署协议转让版权。

## 8.5 SPDX 写法（进阶）

```
SPDX-FileCopyrightText: 2024 张三
SPDX-License-Identifier: MIT
```

可被开源合规工具解析；一般 LICENSE 文件用传统写法，代码注释用 SPDX 写法。

# 9. 最终模板

## 9.1 LICENSE 文件（MIT）

```
MIT License

Copyright (c) [year] wephiles
Repository: https://github.com/wephiles/[your Repository name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## 9.2 Python 文件头（基础）

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 wephiles.
# This software is licensed under the MIT license.
# See the LICENSE file for details.

"""
这里写你的模块文档字符串
"""

# Write your code here.
```

## 9.3 Python 文件头（SPDX 专业版）

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 wephiles
# SPDX-License-Identifier: MIT

"""
这里写你的模块文档字符串
"""

# Write your code here.
```