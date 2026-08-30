<h1 align="center">GitHub 协作与项目发布：Code Review、Tag 与 Release</h1>

# 1. 多人协作开发

## 1.1 工作流

## 1.2 创建组织与项目

- 普通邀请：settings → collaborators（适合小范围，公司不适合）；
- **创建组织**（公司推荐）：在组织内创建新仓库，先提交第一版。

## 1.3 打 tag 标记首版

```
git tag -a v1 -m "第一版"
git push origin --tags
```

## 1.4 邀请成员开发新功能

```
git checkout -b dev     # 创建 dev 并切换，push 到远程
```

组织 → 邀请成员（邮件同意加入）→ settings → Member privileges 查看权限；单个项目也可邀请合作者。

成员克隆项目后，在 dev 上再分出自己的功能分支开发。

## 1.5 Code Review（Pull Request）

配置：settings → Branches 添加保护规则。

流程：

1. 成员在自己 GitHub 进入 Pull request → 填写信息 → Create pull request；

1. 组长在 Pull requests 中看到 review 请求，可评论、通过；

1. 可在网站手动 merge review，也可命令行 review；

1. 领导 `pull` 更新 dev。

## 1.6 测试/预发布（release 分支）

从 dev 切出 release 分支给测试；测试完毕通过 PR/MR 合并，删除 release 分支，添加 tag 并 push；可能产生冲突，解决即可。

# 2. 给开源项目贡献代码

以 [tornado](https://github.com/tornadoweb/tornado) 为例：

1. **Fork** 源项目到自己仓库（只能在自家仓库修改）；

1. 克隆自己的仓库到本地并修改；
2. `add / commit / push` 到自己的仓库；
3. 向源项目作者发起 **Pull Request** 申请合并；

1. 作者接受后，改动即进入源码。

# 3. issues 与 wiki

- **issues**：文档与任务管理、讨论；
- **wiki**：项目百科。

# 4. 项目发布全流程

核心链路：**本地准备（LICENSE/README）→ 推送远程（git push）→ 打 tag（git tag）→ 创建 Release → 发布**。

## 4.1 LICENSE 文件

在仓库**根目录**创建全大写无后缀的 `LICENSE` 文件（写成 `license.txt` 等会导致 GitHub 无法自动识别展示）。选择建议：

| License    | 类型        | 核心特点                         | 适用场景               |
| ---------- | ----------- | -------------------------------- | ---------------------- |
| MIT        | 宽松型      | 只要求保留版权声明，允许任何用途 | 大多数开源项目、工具库 |
| Apache 2.0 | 宽松型      | MIT 基础上增加**专利授权**条款   | 涉及专利、企业级项目   |
| GPLv3      | 强 Copyleft | 衍生作品必须同样开源             | 强制保持开源的项目     |

从 [choosealicense.com](https://choosealicense.com/) 复制文本，替换 `[year]` 与 `[fullname]`。更多许可证知识详见《Git License 与 Copyright》笔记。

> 注意：不放 LICENSE = 法律上默认"保留所有权利"，别人理论上无权使用你的代码。

## 4.2 README 中英文切换

GitHub 不支持同一文件内自动切换语言，拆成两个文件，顶部互加导航：

```
your-repo/
├── README.md        # 英文版（默认展示，面向国际用户）
└── README_zh.md     # 中文版
```

`README.md` 顶部：

```
[English](README.md) | [简体中文](README_zh.md)
# Your Project Name
```

`README_zh.md` 顶部（当前语言不加链接）：

```
English | 简体中文
# 项目名称
```

命名 `README_zh.md` 与 `README.zh.md` 均可解析，前者更常见。

## 4.3 提交推送

```
git status
git add .
git commit -m "feat: initial release with LICENSE and bilingual README"
git push origin main
# 未关联远程时：
git remote add origin https://github.com/yourname/your-repo.git
git push -u origin main
```

推送后仓库首页自动展示 README，侧边栏显示识别到的 License。

## 4.4 打 Tag

**SemVer 语义化版本**：`MAJOR.MINOR.PATCH`

- MAJOR：不兼容的 API 修改；
- MINOR：向下兼容的新增功能；
- PATCH：向下兼容的问题修复。

预发布按稳定性递增：`1.0.0-alpha → alpha.1 → beta → rc.1 → 1.0.0`，习惯加 `v` 前缀。

发布务必用**附注标签**（存储打标签者、日期、说明，是独立 Git 对象；轻量标签只是"书签"）：

```
git tag -a v1.0.0 -m "Release version 1.0.0: first stable release"
git push origin v1.0.0      # 或 git push --tags
```

> ⚠️ `git push` 默认**不推 tag**，必须显式推送，否则创建 Release 时找不到标签。

## 4.5 创建 Release

**方式一：网页**

1. 仓库右侧栏 Releases → Draft a new release；
2. 选择已有 tag 或输入新 tag 名（基于默认分支自动创建）；
3. 填写标题与更新日志（新增功能、修复问题、重大变更）；
4. 可拖拽二进制附件；alpha/beta/rc 勾选 **Set as a pre-release**；
5. Publish release。GitHub 自动生成 Source code (zip/tar.gz)。

**方式二：gh CLI**

```
gh release create                                # 交互式
gh release create v1.0.0 --notes "首个稳定版本发布"
gh release create v1.2.3 --generate-notes        # 基于 PR/commit 自动生成
gh release create v1.2.3 -F release-notes.md
gh release create v1.0.0-beta.1 --prerelease --notes "测试版本"
gh release create v1.2.3 ./dist/*.tgz            # 附带二进制资产
gh release create v1.2.3 --notes-from-tag
```

远程无该 tag 时会自动从默认分支最新提交创建；推荐先 `git tag -a` 本地创建再推送。

**方式三：GitHub Actions 自动化**

`.github/workflows/release.yml`：

```
name: Release
on:
  push:
    tags: ['v*']
permissions:
  contents: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Build project
        run: |
          npm ci
          npm run build
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v3
        with:
          name: Release ${{ github.ref_name }}
          generate_release_notes: true
          prerelease: ${{ contains(github.ref_name, '-') }}
          files: |
            dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

本地 `git tag -a v1.2.0 -m "..." && git push origin v1.2.0` 即自动构建并发布。

## 4.6 常见坑

- License 文件名必须全大写 `LICENSE`；
- tag 需单独推送；
- 发布用附注标签，否则 Release Notes 取不到有效信息；
- 预发布版本必须显式标记（pre-release / `--prerelease`），否则会被当作稳定版推送给订阅用户；
- 双语 README 需同步维护，更新一份后检查另一份；
- Release 必须关联 tag，但 tag 可先于 Release 存在；删除 Release 不删 tag，反之亦然。

## 4.7 最佳实践

`v0.x.x` 用于功能验证，`v1.0.0` 为首个稳定版；发布前完整跑测试；Release Notes 写清 Breaking Changes 与 Migration Guide；用 Actions 固化发布流程，减少人为失误。

# 5. README 徽章

## 5.1 常用徽章

| 徽章类型                 | Markdown 代码                                                |
| ------------------------ | ------------------------------------------------------------ |
| License（自动检测）      | `[![License](https://img.shields.io/github/license/:user/:repo.svg)]` |
| Release 版本             | `![Release](https://img.shields.io/github/v/release/:user/:repo.svg)` |
| Actions 构建状态         | `![Build](https://img.shields.io/github/actions/workflow/status/:user/:repo/工作流文件名.yml)` |
| Static 徽章（stable 等） | `![Stable](https://img.shields.io/badge/stability-stable-brightgreen.svg)` |
| npm 版本                 | `![npm](https://img.shields.io/npm/v/包名.svg)`              |

## 5.2 点击徽章跳转

```
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/user/repo/blob/main/LICENSE)
```

- 只写图片语法：显示图片，点击无反应；
- 外层链接缺少 `(URL)`：退化为普通文本；
- 图片语法外套 `[...](URL)`：点击跳转（✅ 正确写法）。

