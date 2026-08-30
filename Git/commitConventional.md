<h1 align="center">Git 提交规范：Conventional Commits 与原子化提交</h1>

# 1. Conventional Commits 基本格式

```
<type>(<scope>): <subject>
[空行]
[optional body]
[空行]
[optional footer(s)]
```

| 部分    | 必填 | 说明                                             |
| ------- | ---- | ------------------------------------------------ |
| type    | 是   | 变更类型，小写                                   |
| scope   | 否   | 影响范围，圆括号，如 `(auth)`、`(auth,api)`      |
| subject | 是   | ≤50 字符，祈使句、现在时、首字母小写、结尾无句号 |

示例：

```
feat(login): 添加OAuth2.0登录支持
fix(api): 修复用户信息返回格式错误
refactor(user-service): 简化用户查询逻辑
```

# 2. 提交类型（type）大全

| 类型     | 描述                   | 版本号影响   | CHANGELOG |
| -------- | ---------------------- | ------------ | --------- |
| feat     | 新功能                 | MINOR        | 是        |
| fix      | 修复 bug               | PATCH        | 是        |
| docs     | 仅文档变更             | 不影响       | 否        |
| style    | 格式调整（不影响逻辑） | 不影响       | 否        |
| refactor | 重构（非新增非修复）   | 不影响       | 否        |
| perf     | 性能优化               | PATCH        | 是        |
| test     | 测试相关               | 不影响       | 否        |
| build    | 构建系统或依赖变更     | 不影响       | 否        |
| ci       | CI 配置变更            | 不影响       | 否        |
| chore    | 其他杂项               | 不影响       | 否        |
| revert   | 回滚之前的提交         | 取决于原提交 | 否        |

# 3. Body 与 Footer

## 3.1 Body（可选）

解释**为什么**与**如何**，而非重复"做了什么"；与 Header 之间空一行；每行 ≤72 字符；可用无序列表。

## 3.2 Footer（可选）

**破坏性变更**：必须以 `BREAKING CHANGE:` 开头，或在 type/scope 后加 `!`：

```
feat(api)!: 移除用户创建接口中的`role`字段

BREAKING CHANGE: 用户角色现在需要通过独立的权限管理接口进行分配。
请更新客户端代码，调用新的`/users/{userId}/roles`接口来分配角色。
```

**关联 Issue**：

```
Closes #123
Fixes #456, #789
Resolves #120
```

PR 合并到主干时自动关闭对应 Issue。

# 4. 完整示例

```
feat(alien): 添加外星人舰队 formations

实现三种编队模式：直线型、V字型和波浪型。
玩家可通过数字键1-3切换编队。

- 在AlienFleet类中添加formation_type属性
- 实现三种编队的生成算法
- 添加编队切换的UI提示

BREAKING CHANGE: 旧版本的控制台指令已失效，请使用新的键盘快捷键。
Closes #156
```

# 5. 原子化提交

## 5.1 原则

**一次 commit 只做一件小事，且提交后代码可运行**。避免"大块头提交"（难以定位问题、难以 review、难以回滚）。

## 5.2 示例

开发"用户登录"功能的正确拆分：

```
feat(login): 完成登录页面的基础UI布局
feat(login): 增加账号密码的非空校验和交互提示
feat(login): 对接后端登录接口并完成token存储
fix(login): 修正密码错误时提示图标的颜色显示异常
```

## 5.3 提交频率与合并时机

- **dev 是草稿纸**：可放心频繁原子提交，次数不限；
- **master 是答卷**：合并的唯一标准是**功能完整可上线、测试通过、不会导致构建失败**，与提交次数无关；
- 想拆分同一文件内的不同修改：`git add -p 文件名` 分块暂存。

## 5.4 合并时用 Squash 保持 master 干净

GitHub 合并选项推荐 **Squash and merge**：把 dev 上 N 次细碎提交压成 1 次宏观提交进入 master。命令行等价操作：

```
git checkout master
git merge --squash dev      # 只把 dev 的所有改动放进暂存区，不产生 commit
git commit -m "feat(login): 完成用户登录功能模块"   # 一句话总结
```

⚠️ 忘加 `--squash` 时：未 commit 前 `git merge --abort` 撤销；已 commit 且未推送则 `git reset --hard HEAD~1`。

## 5.5 多行提交

适用于重大功能、易踩坑修改、设计决策记录。格式：标题 + 空行 + 正文 + 页脚。

方式一：`git commit`（不加 `-m`）进入 Vim 编辑，写完 `Esc` → `:wq` 保存退出；

方式二：多个 `-m` 自动拼接为正文：

```
git commit -m "feat(login): 支持微信扫码登录" \
  -m "- 接入微信开放平台扫码登录接口" \
  -m "- 使用轮询方式获取登录状态" \
  -m "Closes #42"
```

方式三：结合 `git merge --squash` 后 `git commit` 写长篇合并总结。

# 6. PR 编号的使用

- PR（Pull Request / Merge Request）编号是平台（GitHub `#123` / GitLab `!456`）创建合并请求时自动生成的 ID；
- PR 本质：我做改动 → 请求仓库主人将改动合并到目标分支（不一定是 master，也可能是 dev/release）→ 等待批准；
- commit 信息里写 `(#2)` 只是生成一个跳转链接，方便溯源；
- **PR 更新靠分支绑定**：只要往 PR 绑定的分支 push，新 commit 自动进入该 PR，写不写 `#2` 无关；`#2` 通常写在第一个 commit 里；
- `Fixes/Closes/Resolves #编号` 用于自动关闭 **Issue**（不要对 PR 编号使用）；
- 纯 Git 命令查不到 PR（PR 是平台概念，不是 Git 概念），推送后看终端输出的链接，或用 GitHub CLI：

```
gh pr list
gh pr view
gh pr create --title "feat: xxx" --body "描述"
```

# 7. 团队落地工具

## 7.1 提交模板（最简单）

新建 `~/.gitmessage` 并配置：

```
git config --global commit.template ~/.gitmessage
git commit      # 不带 -m，编辑器自动加载模板
```

推荐模板：

```
# <type>(<scope>): <subject>
#
# 类型: feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert
# subject ≤50字符，祈使句，首字母小写，结尾无句号
#
# 正文（每行≤72字符）
#
# 页脚：Closes #123, BREAKING CHANGE: 描述
```

## 7.2 Commitizen（交互式生成）

```
npm install -g commitizen
commitizen init cz-conventional-changelog --save-dev --save-exact
git cz    # 代替 git commit，向导式生成规范信息
```

## 7.3 Commitlint + Husky（强制校验，团队推荐）

```
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
echo "module.exports = {extends: ['@commitlint/config-conventional']};" > commitlint.config.js
npx husky install
npx husky add .husky/commit-msg 'npx --no-install commitlint --edit "$1"'
```

不符合规范的提交会被直接拒绝。

# 8. 最佳实践与常见误区

- ✅ 祈使句、现在时、首字母小写、结尾无句号（`Add` 而非 `Added`）；
- ✅ Header 与 Body 之间空行；
- ✅ 修复的 Issue 在 Footer 中 `Closes`；
- ✅ 尽早提交、频繁提交、原子提交；
- ❌ 模糊信息：`update`、`fix bug`、`修改代码`；
- ❌ subject 超 50 字符 / body 行超 72 字符；
- ❌ 过去时（`Added`）或句号结尾；
- ❌ 有破坏性变更却不声明。

可选：给类型加 emoji（✨feat、🐛fix、📝docs、♻️refactor、⚡perf、✅test、🔧chore、⏪revert）。