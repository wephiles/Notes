---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-14 21:08:02 周五"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">uv</h1>

# 1. 什么是 `UV`

**uv** 是由 **Astral** 公司（即开发 Ruff 的同一团队）用 **Rust** 编写的极速 Python 包管理器。它旨在替代 `pip`、`pip-tools`、`pipenv`、`poetry`、`virtualenv` 等多个工具，成为 Python 生态中 **一站式** 的包管理与项目管理工具。

核心亮点:

| 特性                  | 说明                                                 |
| --------------------- | ---------------------------------------------------- |
| ⚡ **极快**            | 比 pip 快 **10-100 倍**，得益于 Rust 实现和全局缓存  |
| 🔄 **全功能**          | 包安装、虚拟环境、依赖锁定、Python 版本管理，一站式  |
| 📦 **兼容 pip**        | 支持 `pip install`、`requirements.txt` 等现有工作流  |
| 🗂️ **全局缓存**        | 相同包只下载一次，跨项目共享缓存                     |
| 🐍 **Python 版本管理** | 可自动下载和管理多个 Python 版本                     |
| 📐 **项目管理**        | 类似 `Poetry/PDM`，支持 `pyproject.toml` 和 lockfile |

# 2. 安装

方式 1：官方推荐（独立安装，不依赖 Python）

```
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

方式 2：通过 `pip`

```
pip install uv
```

方式 3：通过 `Homebrew`（`macOS`）

```
brew install uv
```

验证安装

```
uv --version
```

# 3. 核心功能 & 使用教程

## 3.1 Python 版本管理(代替 `pyenv`)

`uv` 可以自动安装和管理多个 Python 版本：

```python
# 安装指定 Python 版本
uv python install 3.12

# 安装多个版本
uv python install 3.10 3.11 3.12

# 查看已安装的 Python 版本
uv python list

# 固定项目使用的 Python 版本
uv python pin 3.12
# 这会生成 .python-version 文件
```

## 3.2 虚拟环境管理(代替 `venv/virtualenv`)

```python
# 创建虚拟环境（默认目录 .venv）
uv venv

# 指定 Python 版本创建虚拟环境
uv venv --python 3.11

# 指定虚拟环境目录名
uv venv myenv

# 激活虚拟环境
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows
```

> 💡 `uv` 会在创建虚拟环境时自动使用全局缓存，速度极快。

## 3.3 包安装与管理(代替 `pip`)

基本用法  -- 兼容 `pip` 习惯

```python
# 安装单个包
uv pip install requests

# 安装多个包
uv pip install requests flask numpy

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 安装当前项目（含开发依赖）
uv pip install -e ".[dev]"

# 升级包
uv pip install --upgrade requests

# 卸载包
uv pip uninstall requests

# 查看已安装的包
uv pip list

# 查看某个包的详情
uv pip show requests

# 冻结当前环境（导出依赖）
uv pip freeze > requirements.txt
```

⚡ `uv` 独有的高速安装模式

```python
# 使用 uv 的并行下载 + 全局缓存
uv pip install -r requirements.txt
# 第一次：下载到缓存
# 后续项目：直接从缓存链接，几乎瞬间完成
```

## 3.4 依赖锁定(代替 `pip-tools`)

```python
# 将 requirements.in 编译为锁定的 requirements.txt
uv pip compile requirements.in -o requirements.txt

# 同步环境（确保环境与 requirements.txt 完全一致）
uv pip sync requirements.txt
```

**示例 `requirements.in`：**

```python
requests>=2.28
flask
```

**编译后 `requirements.txt` 会锁定所有传递依赖的精确版本：**

```python
certifi==2024.2.2
charset-normalizer==3.3.2
flask==3.0.2
...
```

## 3.5 项目管理(代替 `Poetry/PDM`)

这是 `uv` 最强大的功能，使用 `pyproject.toml` 管理整个项目。

```python
# 创建新项目
uv init my-project
cd my-project
```

生成的目录结构：

```python
my-project/
├── .python-version       # Python 版本
├── pyproject.toml        # 项目配置
├── README.md
├── main.py               # 入口脚本
└── .gitignore
```

生成的 `pyproject.toml`：

```python
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = []
```

添加 / 移除依赖:

```python
# 添加生产依赖
uv add requests
uv add "flask>=3.0"

# 添加开发依赖
uv add --dev pytest
uv add --dev ruff black mypy

# 添加可选依赖组
uv add --group docs mkdocs

# 移除依赖
uv remove requests
```

管理依赖后的 `pyproject.toml`

```python
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.32",
    "flask>=3.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
]
docs = [
    "mkdocs>=1.6",
]
```

同步项目环境：

```python
# 安装所有依赖（生产 + 开发）
uv sync

# 仅安装生产依赖
uv sync --no-dev

# 安装指定依赖组
uv sync --group docs

# 安装全部（含所有可选组）
uv sync --all-groups
```

> `uv sync` 会自动：
>
> 1. 创建虚拟环境（如不存在）
> 2. 安装正确版本的 Python（如不存在）
> 3. 安装所有依赖
> 4. 生成/更新 `uv.lock` 锁文件

锁文件 `uv.lock`

```python
# 手动更新锁文件
uv lock

# 锁文件包含所有依赖的精确版本和哈希值
# 应该提交到版本控制中
```

## 3.6 运行命令(代替`pipx/direnv`)

uv 可以在项目虚拟环境中直接运行命令，无需手动激活：

```python
# 运行 Python 脚本
uv run main.py

# 运行模块
uv run python -m pytest

# 运行任意命令
uv run ruff check .
uv run black --check .

# 运行时自动确保依赖已安装
uv run flask run
```

> 💡 `uv run` 会自动确保虚拟环境和依赖是最新的，非常适合 CI/CD。

## 3.7 工具管理(代替`pipx`)

uv 可以全局安装命令行工具，不污染项目环境：

```python
# 全局安装工具
uv tool install ruff
uv tool install black
uv tool install httpie

# 运行工具（无需安装，临时执行）
uvx ruff check .          # 等同于 uv tool run ruff check .
uvx cowsay "hello"        # 临时运行，不安装

# 查看已安装工具
uv tool list

# 升级工具
uv tool upgrade ruff
uv tool upgrade --all

# 卸载工具
uv tool uninstall ruff
```

## 3.8 构建发布

```python
# 构建源码包和 wheel 包
uv build

# 仅构建 wheel
uv build --wheel

# 构建产物在 dist/ 目录
```

# 4. 完整工作流

```python
# ===== 步骤 1: 创建项目 =====
uv init demo-app
cd demo-app

# ===== 步骤 2: 添加依赖 =====
uv add requests rich
uv add --dev pytest ruff

# ===== 步骤 3: 同步环境（自动创建 .venv + 安装依赖）=====
uv sync

# ===== 步骤 4: 运行项目 =====
uv run main.py

# ===== 步骤 5: 运行测试 =====
uv run pytest

# ===== 步骤 6: 代码检查 =====
uv run ruff check .

# ===== 步骤 7: 提交代码（含 uv.lock）=====
git add pyproject.toml uv.lock main.py
git commit -m "init project"

# ===== 步骤 8: 构建发布 =====
uv build
# -> dist/demo_app-0.1.0-py3-none-any.whl
# -> dist/demo_app-0.1.0.tar.gz
```

# 5. `UV` 命令速查表

| 场景              | 命令                                              | 替代工具        |
| ----------------- | ------------------------------------------------- | --------------- |
| 安装 uv           | `curl -LsSf https://astral.sh/uv/install.sh | sh` | -               |
| 安装 Python       | `uv python install 3.12`                          | pyenv           |
| 创建虚拟环境      | `uv venv`                                         | python -m venv  |
| 创建项目          | `uv init my-project`                              | poetry new      |
| 添加依赖          | `uv add requests`                                 | poetry add      |
| 移除依赖          | `uv remove requests`                              | poetry remove   |
| 同步环境          | `uv sync`                                         | poetry install  |
| 锁定依赖          | `uv lock`                                         | poetry lock     |
| 运行命令          | `uv run python main.py`                           | poetry run      |
| 安装工具          | `uv tool install ruff`                            | pipx install    |
| 临时运行工具      | `uvx ruff check .`                                | pipx run        |
| 安装包(pip模式)   | `uv pip install requests`                         | pip install     |
| 编译依赖          | `uv pip compile requirements.in`                  | pip-compile     |
| 同步环境(pip模式) | `uv pip sync requirements.txt`                    | pip-sync        |
| 构建包            | `uv build`                                        | python -m build |

# 6. `UV` VS. 其他工具

| 性                  | `uv`        | `poetry`        | `pipenv`         | `pip`  | `pip-tools`          |
| ------------------- | ----------- | --------------- | ---------------- | ------ | -------------------- |
| **速度**            | ⚡⚡⚡⚡⚡       | 🐢               | 🐢                | 🐢      | 🐢                    |
| **语言**            | Rust        | Python          | Python           | Python | Python               |
| **项目管理**        | ✅           | ✅               | ✅                | ❌      | ❌                    |
| **锁文件**          | ✅ `uv.lock` | ✅ `poetry.lock` | ✅ `Pipfile.lock` | ❌      | ✅ `requirements.txt` |
| **Python 版本管理** | ✅           | ❌               | ❌                | ❌      | ❌                    |
| **工具安装**        | ✅ `uvx`     | ❌               | ❌                | ❌      | ❌                    |
| **pip 兼容**        | ✅           | ❌               | ❌                | -      | 部分                 |
| **全局缓存**        | ✅           | ❌               | ❌                | ❌      | ❌                    |

# 7. 最佳实践建议

## 7.1. 项目 `.gitignore` 应包含

```
.venv/
__pycache__/
dist/
```

## 7.2. `uv.lock` 应提交到版本控制

```
git add pyproject.toml uv.lock
```

## 7.3. CI/CD 中使用 `uv`

```
# GitHub Actions 示例
- name: Install uv
  uses: astral-sh/setup-uv@v3

- name: Install dependencies
  run: uv sync --frozen    # 使用 lockfile，不更新

- name: Run tests
  run: uv run pytest
```

## 7.4. Docker 中使用 uv

```
FROM python:3.12-slim

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# 安装依赖（利用 Docker 层缓存）
RUN uv sync --frozen --no-dev

COPY . .
CMD ["uv", "run", "python", "main.py"]
```

## 7.5. 从其他工具迁移

```
# 从 Poetry 迁移
uv add $(poetry export -f requirements.txt --without-hashes | cut -d= -f1)

# 从 pip 迁移
uv pip install -r requirements.txt

# 或者直接导入
uv add -r requirements.txt
```

# 8. 总结

**uv** 是当前 Python 生态中 **最快、最现代、最全面** 的包管理工具：

- 🚀 **速度**：Rust 实现，比传统工具快 10-100 倍
- 🛠️ **全能**：一个工具替代 pip + venv + pyenv + poetry + pipx + pip-tools
- 🔒 **可靠**：锁文件保证可复现的安装
- 📦 **兼容**：支持 pip 命令格式，迁移成本低
- 🐍 **自管理 Python**：自动下载和管理 Python 版本

# 9. 补充

## 9.1 全局安装命令行工具

```python
uv tool install ruff
```

这个命令做了什么:

1. 为这个工具创建一个**独立的隔离虚拟环境**（==与你的项目环境、系统环境完全隔离==）
2. 把工具安装在这个隔离环境中
3. 把工具的可执行文件软链接到 `~/.local/bin/`（或 Windows 的用户目录）
4. 这样你在**任何地方**打开终端都能直接用 `ruff` 命令

```python
装在 Python 主环境里吗?
❌ 不是！uv tool install xxx 不会装在系统 Python 里
❌ 也不会装在项目的 .venv 里
```

什么时候该用 `uv tool install`？

适合安装的是**命令行工具**，即那些你在终端里直接敲名字运行的程序，而不是在 Python 代码里 `import` 的库：

```python
# ✅ 适合 uv tool install（命令行工具）
uv tool install ruff          # 代码检查器
uv tool install black         # 代码格式化器
uv tool install httpie        # 命令行 HTTP 客户端
uv tool install ansible       # 自动化运维工具

# ❌ 不适合 uv tool install（是库，要在代码中 import）
# requests, flask, numpy, pandas 等
# 这些应该用 uv add 添加到项目依赖中
```

## 9.2 `uv lock` 和 `uv sync` 的区别？

```python
======================================================================
uv lock  vs  uv sync  的本质区别
======================================================================

┌─────────────────────────────────────────────────────────────┐
│                      uv lock                               │
├─────────────────────────────────────────────────────────────┤
│  作用：读取 pyproject.toml，计算所有依赖的精确版本          │
│        生成/更新 uv.lock 文件                               │
│                                                             │
│  类比：制定一份「精确的采购清单」                            │
│        （写明每个包要哪个版本、从哪下载）                    │
│                                                             │
│  动作：✅ 读 pyproject.toml                                 │
│        ✅ 解析依赖树                                        │
│        ✅ 生成/更新 uv.lock                                 │
│        ❌ 不安装任何东西！不创建虚拟环境！                    │
│                                                             │
│  触发时机：你改了 pyproject.toml（增删改依赖）后              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      uv sync                               │
├─────────────────────────────────────────────────────────────┤
│  作用：读取 uv.lock，按照锁文件安装精确版本的依赖             │
│        确保当前环境与锁文件完全一致                          │
│                                                             │
│  类比：拿着「采购清单」去仓库实际拿货并放到货架上             │
│                                                             │
│  动作：✅ 读 uv.lock                                        │
│       ✅ 创建虚拟环境（如果不存在）                         │
│       ✅ 安装 Python（如果不存在）                          │
│       ✅ 安装所有依赖到 .venv                              │
│       ✅ 如果 uv.lock 不存在，会先自动 lock                 │
│                                                             │
│  触发时机：克隆项目后 / 每次拉取新代码后                     │
└─────────────────────────────────────────────────────────────┘

======================================================================
📖 一个生活类比帮你彻底理解
======================================================================


  场景：你开了一家奶茶店

  pyproject.toml  =  菜单（写明需要「红茶」「牛奶」「珍珠」）
  
  uv lock         =  根据菜单，制定一份精确采购单
                     「立顿红茶包 x2（2024年产批次A）」
                     「伊利纯牛奶 250ml x1（保质期至2025.6）」
                     「手作珍珠 500g x1」
                     → 生成采购单 = uv.lock
  
  uv sync         =  按照采购单，实际去超市采购并把原料放到厨房
                     → 厨房 = .venv 虚拟环境（现在有东西可以用了）

======================================================================
🎯 回答问题
======================================================================

┌──────────────────────────────────────────────────────────────────┐
│  我写了一个项目，用哪个？                                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  主要用：uv sync                                                 │
│                                                                  │
│  因为 uv sync = uv lock + 实际安装，一步到位                      │
│                                                                  │
│  当你执行 uv add requests 时，uv 会自动 lock + sync              │
│  你只在以下情况需要手动 uv lock：                                │
│                                                                  │
│  场景1: 手动编辑了 pyproject.toml 中的依赖版本约束                │
│         uv lock    ← 重新计算锁定版本                            │
│         uv sync    ← 安装新的版本                                │
│                                                                  │
│  场景2: 想更新依赖版本（不改变约束，但想用最新版）                │
│         uv lock --upgrade   ← 重新锁定到最新可用版本              │
│         uv sync             ← 安装更新后的版本                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  我要运行别人的项目，用哪个？                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用：uv sync  （一步到位！）                                      │
│                                                                  │
│  别人的项目里已经有 uv.lock 文件（应该随代码一起提交）            │
│  uv sync 会：                                                    │
│    1. 读取 uv.lock（不重新计算版本，直接用锁定的）               │
│    2. 自动创建 .venv 虚拟环境                                     │
│    3. 自动安装正确版本的 Python                                   │
│    4. 按锁文件精确安装所有依赖                                    │
│    → 你的环境与原作者完全一致，不会出现版本冲突 ✅                 │
│                                                                  │
│  然后直接运行：                                                   │
│    uv run python main.py                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

```python
======================================================================
📋 完整工作流对比
======================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  场景 A：你自己开发项目
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  git clone <自己的仓库>        # 或者 uv init 新建项目
        │
        ▼
  uv sync                       # 首次：自动 lock + 创建 .venv + 安装依赖
        │
        ▼
  开发中...
        │
        ▼
  需要新依赖？
  ├─ uv add requests             # 自动 lock + sync，一步到位 ⭐
  │  uv add --dev pytest
  │
  └─ 或者手动编辑 pyproject.toml 后：
     uv lock                    # 重新计算锁定版本
     uv sync                    # 安装
        │
        ▼
  uv run python main.py          # 运行项目
        │
        ▼
  git add pyproject.toml uv.lock # ⚠️ 必须同时提交这两个文件！
  git commit -m "add requests"
  git push


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  场景 B：运行别人的项目
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  git clone <别人的仓库>
  cd <项目目录>
        │
        ▼
  uv sync                        # ⭐ 唯一需要执行的命令！
        │                        # 自动读取 uv.lock
        │                        # 自动创建 .venv
        │                        # 自动安装精确版本的依赖
        │                        # （不重新计算版本，与原作者完全一致）
        ▼
  uv run python main.py           # 运行项目
        │
        ▼  拉取了新代码后
  git pull
  uv sync                         # 重新同步（lockfile 可能变了）
  uv run python main.py


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  uv sync 的 --frozen 参数（CI/CD 常用）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  uv sync --frozen
  └── 严格按 uv.lock 安装，如果 lockfile 与 pyproject.toml 不一致
      会报错而不是自动重新 lock
      → 用于 CI/CD 确保环境完全锁定，防止意外更新依赖

  uv sync --no-dev
  └── 不安装开发依赖（如 pytest, ruff 等）
      → 用于生产部署，只装运行所需的依赖
```

## 9.3 总结

全局安装命令行工具:

| 要点         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **是什么**   | 把 `ruff`、`black` 等命令行工具装在一个**独立的隔离环境**中，全局可用 |
| **装在哪**   | **不**在系统 Python 里，**不**在项目 `.venv` 里，而是 `uv` 管理的独立目录 `~/.local/share/uv/tools/` |
| **怎么用**   | `uv tool install ruff` → 之后任何地方直接敲 `ruff` 就能用    |
| **适用场景** | 命令行工具（`ruff`、`black`、`httpie`），**不是**代码中 `import` 的库 |

`uv lock vs uv sync`:

|                  | `uv lock`                    | `uv sync`                       |
| ---------------- | ---------------------------- | ------------------------------- |
| **作用**         | 计算精确版本，生成 `uv.lock` | 按 `uv.lock` 安装依赖到 `.venv` |
| **安装东西吗**   | ❌ 不安装                     | ✅ 安装                          |
| **建虚拟环境吗** | ❌ 不建                       | ✅ 自动建                        |
| **类比**         | 制定采购清单                 | 按清单实际采购                  |

**写自己的项目** → 日常用 `uv add`（自动 `lock+sync`），改了 `pyproject.toml` 后才手动 `uv lock` + `uv sync`

**运行别人的项目** → 只需一条命令 `uv sync`，然后 `uv run python main.py`



