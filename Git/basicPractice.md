<h1 align="center">Git 基础实战：从初始化到分支与远程协作</h1>

# 1. Git 简介

Git 是一个**分布式版本控制软件**：

- **分布式**：某个节点挂了，只要不是所有节点都挂，数据即可恢复；
- **版本控制**：管理同一文件/项目的多个版本；
- **软件**：安装在本机使用的工具。

版本控制方式演进：

| 方式          | 特点                                               | 缺点                     |
| ------------- | -------------------------------------------------- | ------------------------ |
| 文件拷贝      | 第一版/最终版/最终不修改版……                       | 文件泛滥、无法追溯       |
| 本地版本控制  | 本地只显示一个文件，历史存数据库                   | 不能多人协作             |
| 集中式（SVN） | 都提交到中心服务器                                 | 断网或中心宕机即无法提交 |
| 分布式（Git） | 中心和每个节点都保存全部版本，先提交本地再同步中心 | —                        |

# 2. 单人开发基础流程

## 2.1 首次配置（只需一次）

生成版本时需告诉 Git 是谁提交的：

```
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

## 2.2 初始化与管理

1. 进入要管理的文件夹，右键 → Git Bash Here：

1. 初始化，出现 `.git` 文件夹说明可被管理：

```
git init
```

1. 查看状态（红色 = 未管理）：

```
git status
```

1. 管理文件（变绿）：

```
git add 文件名     # 管理指定文件
git add .          # 管理当前文件夹下所有文件
```

1. 生成版本：

```
git commit -m "本次提交的概述信息"
```

提交后再 `git status` 无任何显示，说明已生成版本：

## 2.3 继续开发与查看记录

修改文件后（Git 自动检测到修改），重复 `add → commit` 生成新版本：

```
git log    # 查看版本记录
```

## 2.4 基础命令总结

```
git init                      # 初始化
git status                    # 查看文件状态
git add . / git add 文件名    # 管理
git commit -m "xxx"           # 生成版本
git log                       # 查看版本记录
```

文件状态变化：

- **红色**：新增或修改过的文件（未管理）→ `git add` 后变绿；
- **绿色**：已被管理但未生成版本 → `git commit` 生成版本；
- **已生成版本**：status 中不显示。

# 3. Git 三大区域

- **工作区**：正在操作的文件夹；含已管理文件与新增/修改文件（红色），`git add` 提交到暂存区；
- **暂存区**：绿色文件，`git commit` 提交到版本库；
- **版本库**：已生成的版本。

# 4. 版本回滚与恢复

## 4.1 回滚

```
git log                   # 查看版本号
git reset --hard 版本号   # 回滚到指定版本
```

## 4.2 恢复（撤销回滚）

回滚后 `git log` 中看不到之前的版本，需用 `git reflog`：

```
git reflog                # 查看已回滚的版本号
git reset --hard 版本号   # 恢复
```

# 5. 分支

## 5.1 应用场景

开发进行到一半时线上出现 bug：把当前开发进度放到分支（如 dev）上，主干（默认 `master`）保持可用，另建 bugfix 分支修复。

## 5.2 分支操作

```
git branch            # 查看分支
git branch dev        # 创建 dev 分支（从当前位置分出）
git checkout dev      # 切换到 dev 分支（dev 上开发不影响 master）
```

在 dev 上开发后 `add / commit`：

dev 上 `git log` 能看到 dev 的记录，切回 master 后看不到：

## 5.3 bug 修复与合并

```
# 注意：必须在 master 分支上创建 bugfix 分支
git branch bugfix
git checkout bugfix
# 修复 bug 后 add、commit，然后合并回 master：
git checkout master
git merge bugfix      # 谁合并谁：先切到目标分支，再合并来源分支
git branch -d bugfix  # 删除已合并的分支
```

## 5.4 合并冲突

将 dev 合并回 master 时**可能产生冲突**（同时修改同一行时），系统无法决定保留哪个，需**手动**打开冲突文件修改后重新提交；未同时修改同一行则不冲突。

## 5.5 分支命令总结

```
git branch            # 查看
git branch 分支名      # 创建
git checkout 分支名    # 切换
git merge 分支名       # 合并（可能冲突）
git branch -d 分支名   # 删除
```

> 分支本质：只保留修改的部分。

# 6. Git 工作流

新项目至少创建两个分支：`master`（主干）+ `dev`（开发），日常代码只写在 dev 上。

# 7. GitHub 远程协作

## 7.1 推送与拉取

```
git remote add origin https://github.com/wephiles/dbhot   # 给远程仓库起别名
git push -u origin master    # 推送 master 到远程
git clone https://. ..        # 新电脑第一次拉取（所有分支都已拉下，可直接切换）
git pull origin dev          # 已 clone 后再拉取远端 dev 更新
```

## 7.2 家—公司循环工作流

```
# 公司开发
git checkout dev
git merge master        # 仅执行一次，保持 dev 拿到 master 最新代码
# 写代码
git add .
git commit -m "xx"
git push origin dev

# 回家继续
git checkout dev
git pull origin dev
git add .
git commit -m "xx"
git push origin dev

# 开发完毕上线
git checkout master
git merge dev
git push origin master
git checkout dev
git push origin dev     # dev 也同步到远程
```

## 7.3 忘记推送导致冲突

公司未 push、家里写了别的功能并 push，第二天公司 `pull` 产生分叉与冲突：手动解决冲突文件后继续开发，最后 `add commit push` 一气呵成。

```
git pull origin dev = git fetch origin dev + git merge origin/dev
```

# 8. 命令总览

```
git init / status / add / commit -m / log / reflog
git reset --hard xxx
git branch / checkout / merge / branch -d
git remote add origin xxx
git push -u origin master
git clone xxx
git pull origin dev
git fetch origin dev
git merge origin/dev
```