<h1 align="center">Git 进阶操作与配置：rebase、stash、amend、SSH 与多身份</h1>

# 1. rebase（变基）

## 1.1 作用

使提交记录变得简洁。

## 1.2 场景一：合并多条记录为一条

```
git rebase -i 版本号    # 当前版本到指定版本间的记录合并
git rebase -i HEAD~3   # 合并最近 3 条记录
```

执行后在编辑器中将第二行起的 `pick` 改为 `s`（合并到上一条），保存退出即可。

> ⚠️ 已推送到远程仓库的记录尽量不要合并，只合并未推送的本地记录。

## 1.3 场景二：分支处理（把 dev 塞到 master 上）

```
git log --graph       # 查看图形化分支历史
git log --graph --pretty=format:"%h %s"
git checkout dev
git rebase master     # 第一步：把 dev 的提交重放到 master 最新提交之后
git checkout master
git merge dev         # 第二步：合并，历史为一条直线
```

## 1.4 场景三：忘记 push 导致分叉

不要直接 `git pull`（= fetch + merge），改用：

```
git fetch origin dev
git rebase origin/dev
```

## 1.5 冲突处理

rebase 遇到冲突时，解决后：

```
git add .
git rebase --continue
```

# 2. Beyond Compare 快速解决冲突

```
git config --local merge.tool bc5
git config --local mergetool.path 'D:\\software\\beyondCompare\\Beyond Compare 5'
git config --local mergetool.keepBackup false   # 解决冲突后不保留源文件
git mergetool
```

# 3. git stash（临时储藏）

作用：**临时保存未写完的代码，并把工作区清理干净**，方便切分支处理紧急任务。

## 3.1 基础三步

```
git stash          # 藏起来（工作区变干净，可随意切分支）
# ……切分支、修 bug 等
git stash pop      # 拿出最近一次 stash 并删除该记录
```

## 3.2 常用管理命令

```
git stash list                       # 查看（数字越大越老）
git stash apply stash@{1}            # 恢复指定但不删记录
git stash drop stash@{0}             # 删除指定
git stash clear                      # 清空（慎用）
git stash push -m "备注"             # 起名（推荐）
git stash push -u -m "备注"          # 包含未跟踪的新文件（默认不含）
git stash show stash@{0}             # 看改了哪些文件
git stash show -p stash@{0}          # 看具体 diff
```

## 3.3 注意事项

- `pop` 冲突时需手动解决后重新 `add / commit`；
- 建议在哪个分支 stash 就回哪个分支 pop；
- stash 是临时缓冲区，不是长期备份，越快 pop 越好。

# 4. amend commit（修补上一次提交）

PyCharm 的 “Amend commit” 对应命令：

```
git commit --amend                  # 只改提交信息（打开编辑器）
git commit --amend -m "新信息"      # 直接替换提交信息
git add 遗漏文件
git commit --amend                  # 把暂存区内容并入上次提交
```

- 适用：修改写错的提交信息、补充遗漏文件；
- ⚠️ 本质是**生成新提交替换旧提交**（重写历史），只对**未 push** 的提交使用，且不要对受保护分支强行推送。

# 5. .gitignore 与缓存清理

## 5.1 .gitignore 写法

```
a.h            # 忽略 a.h
*.h            # 忽略所有 .h
files/         # 忽略 files 文件夹下所有文件
!c.h           # 特例：把 c.h 管理起来
```

自己写麻烦，直接去 GitHub 搜索 `gitignore` 复制对应语言模板（如 Python 模板含 `__pycache__/`、`.venv/`、`.idea/` 等）。

## 5.2 已误提交的文件如何停止追踪

```
git rm -r --cached .idea    # 只删追踪记录，不删本地文件（--cached 至关重要）
git commit -m "Stop tracking .idea directory"
git push
```

万能清理公式：

```
git rm -r --cached .        # 清除所有追踪缓存（不删本地文件）
git add .                   # 按 .gitignore 规则重新添加
git commit -m "Apply .gitignore rules"
```

# 6. 配置文件三级

```
git config --local user.name "xxx"    # 当前项目：./.git/config
git config --global user.name "xxx"   # 全局：~/.gitconfig
git config --system user.name "xxx"   # 系统：/etc/.gitconfig（需 root）
```

`git remote add origin xxx` 默认写入项目本地的 config。

# 7. 免密登录

## 7.1 URL 中带账号密码（不推荐）

```
git remote add origin https://用户名:密码@github.com/wephiles/dbhot
```

## 7.2 SSH 实现（推荐）

本地生成公钥私钥（默认在 `~/.ssh`），公钥添加到 GitHub 后即可免密 push/pull。

## 7.3 Git 自动管理凭证

# 8. SSH 密钥详解

## 8.1 组成与原理

- **私钥**：保存在本地，绝不泄露，用于解密与签名；
- **公钥**：添加到远程平台，用于验证身份。

基于非对称加密（RSA / ED25519）：本地用私钥签名，服务器用公钥验证。

## 8.2 用途

- 免密登录（push/pull 无需重复输密码），适用于 CI/CD 与自动化；
- 加密传输，防窃听、防中间人；
- 多账号、多平台管理；
- 团队权限控制。

## 8.3 配置流程（GitHub 为例）

```
ssh-keygen -t ed25519 -C "your_email@example.com"   # 旧系统可用 rsa -b 4096
cat ~/.ssh/id_ed25519.pub                            # 复制公钥
# GitHub → Settings → SSH and GPG keys → New SSH key 粘贴
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com                                # 测试，成功显示 Hi username!
```

## 8.4 SSH 与 HTTPS 对比

| 对比   | SSH                        | HTTPS       |
| ------ | -------------------------- | ----------- |
| 认证   | 密钥对免密                 | 用户名/密码 |
| 安全性 | 更高（非对称加密）         | 一般        |
| 场景   | 频繁操作、自动化、团队协作 | 临时访问    |

## 8.5 多台电脑共用一个账号

- 每台电脑**独立生成密钥对**，把各公钥都添加到**同一个 GitHub 账号**（公钥加在账号级，账号下所有仓库通用，无需区分仓库）；
- 不要复制私钥到多台电脑：独立密钥可在某台泄露时只撤销该公钥；
- 建议设置 passphrase，并定期审计删除不用的密钥。

# 9. 多账号与多身份配置

## 9.1 user.name / user.email 的作用与注意

- 用于 commit 时记录作者身份；Git 不验证真实性，但**强烈建议真实**：
  - 邮箱需与平台账号绑定，否则 contributions 不统计、提交显示为陌生人；
  - 邮箱用于开源社区联系与身份追溯。

## 9.2 三种方案

**方案一：单仓库手动配置（最简单）**

```
git config user.name "HomeName"
git config user.email "home@example.com"    # 不带 --global，仅当前仓库
```

**方案二：includeIf 目录自动化（多项目）**

`~/.gitconfig`：

```
[includeIf "gitdir:D:/work/"]
    path = ~/.gitconfig-work
[includeIf "gitdir:D:/personal/"]
    path = ~/.gitconfig-personal
```

对应文件中写各自的 `[user]` 段；公司项目放 `D:/work/`、个人项目放 `D:/personal/` 即自动切换身份。

**方案三：多 SSH Key + Host（多平台/严格隔离）**

```
ssh-keygen -t ed25519 -C "a@qq.com" -f ~/.ssh/id_ed25519_a
ssh-keygen -t ed25519 -C "b@qq.com" -f ~/.ssh/id_ed25519_b
```

`~/.ssh/config`：

```
Host github.com-a
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_a
    IdentitiesOnly yes

Host github.com-b
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_b
    IdentitiesOnly yes
```

使用：

```
ssh -T git@github.com-a
git clone git@github.com-a:username/repo_a.git
git remote set-url origin git@github.com-a:username/repo_a.git
```

注意：一个公钥只能绑定一个 GitHub 账号；每次提交前用 `git config user.name / user.email` 验证身份。

## 9.3 方案选择

| 场景                 | 推荐方案 |
| -------------------- | -------- |
| 单个仓库             | 方案一   |
| 多仓库、多目录       | 方案二   |
| 多平台、严格权限隔离 | 方案三   |

# 10. tag 打标签

```
git tag -a v1 -m "第一版"      # 创建附注标签
git push origin --tags         # 推送所有 tag（git push 默认不推 tag！）
```

发布场景务必用**附注标签**（含作者、日期、说明），而非轻量标签；SemVer 版本规范与 Release 发布详见《GitHub 协作与项目发布》笔记。

# 11. 常用分支命令补充

```
git branch -d <分支名>              # 删除分支
git branch -D <分支名>              # 强制删除
git push origin --delete <分支名>   # 删除远程分支
git checkout -b <新分支名>          # 创建并切换（或 git switch -c）
git push -u origin <新分支名>       # 推送新分支到远程
```