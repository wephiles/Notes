# 一、关于 Git license

> 可以直接去此网站 copy LICENSE: https://choosealicense.com/licenses/
>
> 不想看些乱七八糟的，直接跳转重点 [总结](#三、总结)

## 1. 什么是 Git license？

严格说，“Git 本身没有自己的许可证”。
你看到的所谓 “Git license”，指的是你在 Git 仓库（尤其是 GitHub/GitLab 等）里给项目选择/添加的一份“软件许可证（software license）”。

- 它是一份法律声明，说明别人对你的代码能做什么、不能做什么，以及必须满足什么条件（如署名、开源、保留版权声明等）。github.com+1
- 通常放在仓库根目录的 `LICENSE` / `LICENSE.md` / `LICENSE.txt` 文件里。github.com

## 2. 为什么要有 Git license？

原因主要有三点：

1. 法律默认：没有许可=“别人啥都不能干”
   代码也是受版权保护的作品。如果不明确给许可，版权法默认你保留所有权利，别人复制、分发、修改、再发布都可能构成侵权。Choosealicense 明确说明：没有许可证，别人就不能复制、分发或修改你的作品。choosealicense.com
2. 明确权利与边界，降低争议
   许可证把“允许使用、修改、分发”“必须保留版权声明”“允许商业使用”等写清楚，减少后续纠纷。github.com+1
3. 便于社区与企业使用
   成熟、标准的许可证（如 MIT、Apache‑2.0、GPL 等）大家都熟悉，很多企业只敢用“标准许可证”的代码。使用标准许可证能提高你的项目被采用的概率。balter.com

## 3. ！！！我怎么写一个 Git license？

推荐做法：**“不要自己写，直接用现成标准许可证”**。

### 3.1 最简单的“写法”：直接复制标准文本

1. 去下面任一权威站点选择一个许可证，复制标准文本：
   - GitHub 官方推荐的 Choose a License（列出常用许可证及其“权限/条件/限制”）。choosealicense.com
   - 开源倡议（OSI）的“开源许可证”分类列表。opensource.org
   - SPDX 许可证列表（提供标准文本与短标识符，如 `MIT`、`Apache-2.0`）。spdx.org+1
2. 在仓库根目录新建一个文件，例如：
   - `LICENSE` 或 `LICENSE.md` 或 `LICENSE.txt`（GitHub 推荐做法）。github.com
3. 把许可证全文粘贴进去，并根据需要替换：
   - 年份
   - 版权持有人（姓名/机构名）

示例（MIT 风格）：

```
MIT License

Copyright (c) [年份] [你的名字或机构名]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

4)（可选）在 `README.md` 里用一句话写上：
“This project is licensed under the MIT License – see the `LICENSE` file for details.”github.com

### 3.2 在 GitHub 上“点选”许可证（更省事）

- 创建新仓库时，GitHub 页面有 “Add a license” 步骤，可以直接选 MIT/Apache‑2.0/GPL‑3.0 等。
- 已有仓库，也可以通过 “Add file → Create new file”，输入 `LICENSE`，并在模板里选择对应许可证，直接生成。github.com

## 4. GitHub 上有哪些 Git license？分别都代表什么意思？

GitHub 官方文档和搜索都支持一批常见许可证（包括它们的短标识符，如 `MIT`、`Apache-2.0`、`GPL-3.0` 等）。github.com
Choose a License 把主流许可证按“条件从多到少”排列，并给出“权限/条件/限制”的对照表。choosealicense.com

下面把最常见的一些列出来（按大类说明）：

### 4.1 宽松型（Permissive）：允许闭源/商用，要求保留版权声明

- MIT License
  - 特点：非常宽松，允许“随便用”，只要求保留版权声明和许可声明。choosealicense.com
  - 适用：希望别人随便用，你只求被“注明出处”。
- Apache License 2.0
  - 特点：允许闭源商用；要求保留版权与许可声明；明确授予专利授权，并对修改文件做一定说明；包含专利报复条款。choosealicense.com
  - 适用：对专利比较在意、又希望商用友好的项目。
- BSD 2‑Clause / BSD 3‑Clause（“简化 BSD” / “New BSD”）
  - 特点：类似 MIT，要求保留版权声明和许可声明；BSD 3‑Clause 还要求不能用作者名字做推广。github.com
  - 适用：学术/开源项目，要求不高但希望署名。
- 0BSD（Zero‑Clause BSD）
  - 特点：几乎等于“放弃一切权利”，只要保留版权声明即可。github.com
- BSL‑1.0（Boost Software License 1.0）
  - 特点：对源码分发要求保留版权声明，二进制分发没有硬性要求。choosealicense.com
- Unlicense
  - 特点：直接把作品“献给公共领域”，几乎没有任何条件。choosealicense.com

### 4.2 强 Copyleft（传染型开源）：修改/分发时必须以同许可证开源

- GPL‑2.0 / GPL‑3.0（GNU General Public License）
  - 特点：允许商用，但如果你分发修改后的版本，整个衍生作品必须同样以 GPL 开源（源码也要提供）。choosealicense.com
  - 适用：希望“软件永远保持开源”。
- AGPL‑3.0（GNU Affero General Public License v3）
  - 特点：比 GPL 更强，网络使用也被视为一种分发——如果你通过网络提供服务（比如 Web API），必须向用户提供源码。choosealicense.com

### 4.3 弱 Copyleft / 文件级 Copyleft

- LGPL‑2.1 / LGPL‑3.0（GNU Lesser GPL）
  - 特点：对库本身要求开源，但允许你把库链接到闭源主程序（以特定方式），主程序可以不开源。choosealicense.com
  - 适用：希望库本身保持开源，但允许闭源商业软件使用。
- MPL‑2.0（Mozilla Public License 2.0）
  - 特点：文件级 copyleft：你修改的 MPL 源文件必须以 MPL 开源，但可以和其它许可证文件组合成一个更大的作品，该作品整体不必 MPL 开源。choosealicense.com

### 4.4 不属于“开源许可证”的常见情况

- CC BY‑4.0 / CC BY‑SA‑4.0 / CC0‑1.0 等 Creative Commons 系列许可证
  - GitHub 支持用 CC 系列许可证（在搜索和识别上），但 CC 官方明确：**不推荐用于软件**，建议使用专门的软件许可证。github.com+1
  - 常用于文档、图片、文章、数据集等非软件作品。
- 自制/自定义许可证（“自写一版条款”）
  - 法律上你可以自己写；但从实践角度，非常不推荐（见下一节）。

## 5. 开发过程中 Git license 可以自己随便写吗？有什么标准？

### 5.1 法律层面：你可以自己写

- 版权是你的权利，你可以附加任何你愿意给出的许可（甚至“不给许可”）。balter.com
- 所以“从法律上讲”，你确实可以随便写。

### 5.2 实践层面：强烈不建议“自己写/改”

业界与社区普遍反对“自制/修改许可证”，理由包括：

- 别人（尤其是公司）需要请律师逐条分析你的许可证，成本很高，干脆就不用你的项目。
- 工具链和开源治理工具（比如 SPDX）只识别标准许可证；你写的非标准许可证很难被自动检测和归类。spdx.org+1
- 标准许可证已经被广泛审查和测试；自己写的，很容易出现漏洞或歧义。balter.com

Choose a License 与 Ben Balter（GitHub 前开源政策负责人）的文章都建议：
“除非确实必须，否则不要使用自定义/非标准许可证，这会成为别人使用你代码的障碍。”balter.com

### 5.3 所谓“标准”有哪些？

- 开源倡议（OSI）认可的“开源许可证（OSD）”列表；这些许可证满足“开源定义（OSD）”10 条标准。opensource.org+1
- SPDX 许可证列表，给每个许可证一个标准短标识符（如 `MIT`、`GPL-3.0`、`Apache-2.0`）。spdx.org+1

## 6. 想要：个人免费使用 + 标明出处 + 不可商用且盈利，该怎么写？

### 6.1 关键点：这不是“开源许可证”

- “开源定义（OSD）”第 6 条明确：
  许可证不得歧视任何特定领域，比如“不得用于商业”就不符合开源要求。opensource.org
- 也就是说：**“禁止商业使用”的许可证，不属于开源许可证**。

同时：

- CC 官方 FAQ 明确：不推荐用 CC 系列许可证来许可软件；建议使用专门软件许可证。creativecommons.org
- 你如果真的写一个“CC BY‑NC 4.0（仅署名+禁止商用）”，严格说：
  - CC 官方不建议用在软件上；
  - 社区通常也把它视为“非开源”，甚至不认为它是“自由软件许可证”。

### 6.2 实际可操作的写法（不推荐，但很多人在用）

如果你依然想要“可非商用+署名”的效果，一般有两种做法（各有利弊）：

#### 方案 A：自制“非商业+署名”许可证（简例）

示例（仅示意，非法律意见）：

text

复制

```
Non-Commercial Attribution License

Copyright (c) [年份] [你的名字/机构]

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. The name of the copyright holder may not be used to endorse or promote
   products derived from this software without specific prior written permission.
4. This software may not be used for commercial purposes or with the primary
   intent of generating revenue without a separate commercial license from
   the copyright holder.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

引用

优点：

- 理论上能满足你“个人可免费使用+署名+禁止商用”的要求。

缺点：

- 不是标准许可证，企业/大项目通常不敢用；
- 工具链不认识（SPDX 没有对应 ID），很难被自动识别；
- “商业使用”界定模糊，容易产生争议（比如学校内部项目是否算商用？）。

#### 方案 B：用 CC BY‑NC 4.0（不推荐用于软件，但常被误用）

- 使用 Creative Commons 的 “署名‑非商业（BY‑NC）”许可证文本。creativecommons.org
- 在仓库中放一个 `LICENSE` 文件，内容为 CC BY‑NC 4.0 的标准文本。

但：

- CC 官方明确不推荐用 CC 来许可软件，建议用专门的软件许可证。creativecommons.org
- CC BY‑NC 在软件领域会被视为“非开源/非自由软件”，很多开源社区和公司会直接避开。

### 6.3 更稳妥的折中方案（如果你希望被广泛使用）

如果你愿意稍微放一下“禁止商用”的门槛，但又想“别人用你的代码时要开源”，可以考虑：

- AGPL‑3.0：任何修改和网络使用都必须开源，但允许商业使用（比如公司可以拿来提供 SaaS，但必须开源）。choosealicense.com
- 或者双重许可：
  - 对开源社区用 AGPL‑3.0；
  - 对需要闭源商业使用的公司单独签订商业授权。

## 7. 补充：关于 Git/代码许可证的实用知识点

### 7.1 没有许可证时，会发生什么？

- 默认版权法生效：别人复制/分发/修改/再发布都可能侵权。choosealicense.com
- 在 GitHub 上公开仓库，别人可以“浏览和 Fork”，但不等于获得许可去使用/修改/再发布你的代码。github.com+1
- 很多社区/企业直接拒绝“无许可证”的项目，风险太大。

### 7.2 许可证不要“中途随便改”（特别是多人协作项目）

- 单一作者的项目，理论上可以随时更改许可证（比如从“无许可”改为 MIT），但这不影响之前已经获得的权利（很多人已经按旧版本获得了许可）。
- 多人贡献的项目，问题更复杂：每个贡献者都是版权人，理论上重大许可变更需要所有贡献者同意。实践中很多项目采用“贡献者许可协议（CLA）”来统一权利。

### 7.3 不要“混搭”太多不同许可证

- 项目依赖的库如果都使用常见标准许可证（MIT/Apache‑2.0/BSD/GPL 系列），通常兼容性比较好。balter.com
- 一旦某个依赖使用“自制许可证”，整个项目的法律复杂性会急剧上升，公司会很难评估风险。balter.com

### 7.4 正确的“署名（Attribution）”一般包含什么？

主流许可证对“署名”的要求大同小异，通常包括：

- 保留原始版权声明；
- 保留许可声明（例如 “Licensed under the MIT License”）；
- 如有“免责声明（disclaimer）”，也要保留；
- 有的还要求说明“对本文件做了哪些修改”。

### 7.5 如何在代码中“机器可读”地标注许可证（SPDX）

- 在文件头注释里写上：
  `// SPDX-License-Identifier: MIT`
  或
  `// SPDX-License-Identifier: (MIT OR Apache-2.0)`spdx.org+1
- 工具和仓库治理系统可以根据这个标记自动识别项目的许可证。

### 7.6 不同许可证之间的兼容性（非常关键）

- 简单理解：
  - 宽松型（MIT/BSD/Apache‑2.0）之间通常是兼容的；
  - 强 Copyleft（GPL/AGPL）和宽松型可以单向兼容（MIT 代码可以被放到 GPL 项目里，反过来不行）；
  - 不同版本 GPL（v2 vs v3）之间、GPL vs AGPL 之间也存在兼容性问题，需要具体分析。opensource.org+1

### 最后一点建议

- 想要“开源、被广泛采用”：直接用 MIT / Apache‑2.0 / GPL‑3.0 / LGPL‑3.0 等标准许可证。
- 想要“保留更多权利、限制商业使用”：可以自制“非商业+署名”许可证，但要清楚它会被视为“非开源”，并且企业用户会非常谨慎。
- 如果你真的是为“软件”设计条款，避免直接用 CC 系列（尤其是含 NC 条款）去“许可软件”，因为 CC 官方也不建议这么做。

# 二、关于 copyright

### 一、 标准写法与示例

最标准、最常见、绝对不会出错的写法是：

```
Copyright (c) 2024 张三
```

如果是持续维护的项目，或者有多人参与，常见的写法有：

```
# 年份范围（表示从2022年写到现在，且持续维护中）
Copyright (c) 2022-2024 张三

# 多个作者/机构（用逗号或顿号隔开）
Copyright (c) 2024 张三, 李四

# 机构名义
Copyright (c) 2024 北京智谱华章科技有限公司
```

### 二、 拆解说明：每个部分有什么遵循？

#### 1. `Copyright` 和 `(c)`

- **写法选择**：你可以写全拼 `Copyright`，也可以用符号 `©`，或者用括号 `(c)`。
- **遵循规范**：在代码世界里，**强烈推荐使用 `Copyright (c)`**。因为 `©` 属于特殊 Unicode 字符，在某些老旧的终端、纯 ASCII 码环境或特定的文本编辑器中可能会导致乱码或编译警告。`(c)` 是完全合法且最安全的替代写法。

#### 2. `[年份]` 怎么写？

年份代表版权生效的起始和终止时间，有三种常见写法：

- **写单一年份**（如 `2024`）：最常见，表示该代码首次发布的年份。
- **写年份范围**（如 `2022-2024`）：表示你是从2022年开始写，2024年还在更新。这能向外界传达一个信息：“这个项目还在活跃维护中”。
- **写多个不连续的年份**（如 `2020, 2022, 2024`）：表示这几年有实质性更新，中间断更了。
- **【遵循原则】**：
  - 不需要每年都去手动更新这个年份！版权法保护期很长（通常是作者终身+50年，或发表后50/70年），即使你不更新年份，你的代码依然受保护。
  - 如果懒得管，**直接写项目首次发布的年份即可**。

#### 3. `[你的名字或机构名]` 怎么写？

这里填写的是**版权持有人**，也就是拥有这段代码所有权的实体。

- **个人开发者**：
  - **推荐**：写法定姓名（如 `张三` 或 `San Zhang`）。
  - **可以但略有不妥**：写网名（如 `CodingCat`）。如果发生版权纠纷，网名很难证明是你本人，需要额外提供证据。如果非要写网名，建议格式：`张三 (网名: CodingCat)` 或留下邮箱。
- **公司/团队开发**：
  - 必须写**公司的法定注册名称**（如 `Zhipu AI` 或 `北京智谱华章科技有限公司`），不能随便写个部门名（如“算法组”在法律上不具备主体资格）。
- **【遵循原则】**：确保这个名字能唯一指向你或你的组织。如果你是在职期间写的代码，通常版权归属公司，这取决于你的劳动合同，此时你应该写公司名。

### 三、 高阶避坑与最佳实践

#### 1. 源代码文件里也要写吗？

**要的。** `LICENSE` 文件是项目级声明，但最好在每个核心源代码文件（如 `.py`, `.java`, `.ts`）的头部注释里也加上简短的版权声明。
例如：

```
/*
 * Copyright (c) 2024 张三. All rights reserved.
 * 
 * This software is licensed under the MIT license.
 * See the LICENSE file for details.
 */
```

这样做的好处是：如果别人只拷贝了你其中一个文件，版权声明也能跟着文件走。

#### 2. 开源项目有其他贡献者怎么办？

这是一个非常容易踩坑的地方！

- **法律事实**：只要你没有签过“贡献者许可协议（CLA）”把版权转让给你，**每一个向你的仓库提交过代码的人，都是他们那部分代码的版权所有人**。
- **错误做法**：你直接在 LICENSE 里写 `Copyright (c) 2024 张三`，把别人的功劳也算成自己的（这在法律上属于侵权）。
- **正确做法**：
  - **小项目/随便玩玩**：写 `Copyright (c) 2024 张三及贡献者` (虽然法律上不严谨，但社区通常能接受这种表述)。
  - **规范项目**：使用 Git 命令查看提交记录，把实质性贡献者的名字都列上：`Copyright (c) 2024 张三, 李四, 王五`。
  - **企业级项目**：一定要引入 CLA（Contributor License Agreement），让其他人提交代码前签署协议，把版权转让给你或你的公司，这样你才能心安理得地只写你自己的名字。

#### 3. 进阶标准：SPDX 规范（了解即可）

在现代化的开源工程中，为了让机器（如 GitHub、许可证扫描工具）能自动识别，业界遵循 **SPDX (Software Package Data Exchange)** 标准。如果你在源码文件里写版权，推荐这样写：

text

复制

```
SPDX-FileCopyrightText: 2024 张三
SPDX-License-Identifier: MIT
```

这种格式可以被各类开源合规工具直接解析，但对人类阅读不太友好。一般是在 `.LICENSE` 文件里用传统写法，在代码注释里用 SPDX 写法。

### 小结

对于绝大多数个人开发者，你只需要在 `LICENSE` 文件开头写上：
**`Copyright (c) 2024 你的法定姓名或常用网名`**

这就已经完全满足法律要求的“版权宣告”形式了，不用想得太复杂。

# 三、总结

写法：LICENSE文件以后按照这个写就行了

```markdown
MIT License

Copyright (c) 2026 wephiles

Repository: https://github.com/wephiles/host-management-system

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Python文件以后就按照这个写法就可以了:
```python
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

如果想要更专业一点，可以这样写:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 wephiles
# SPDX-License-Identifier: MIT

"""
这里写你的模块文档字符串
"""

# Write your code here.
```





















