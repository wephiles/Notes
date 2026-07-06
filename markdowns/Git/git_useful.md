# 1. 删除分支:

```python
git branch -d <分支名>

# 强制删除
git branch -D <分支名>
```

# 2. 删除远程分支：

```python
git push origin --delete <分支名>
```

# 3. 创建新分支并推送到远程：

```python
git checkout -b <新分支名>
# 或者用较新的
git switch -c <新分支名>

git add & commit

git push -u origin <新分支名>
```

# 4. 关于git commit 怎么写的问题

## 4.1 约定式提交（Conventional Commits）核心规范

约定式提交规范是一种轻量级的约定，它要求提交信息遵循一种特定的结构conventionalcommits.org+1。

### 1. 基本格式结构

一份符合规范的提交信息由 **Header（头）**、**Body（正文）** 和 **Footer（脚注）** 三部分组成，其中 **Header 是必填项**，Body 和 Footer 是可选项csdn.net+1。

其核心格式是：

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

### 2. Header（头部）详解

Header 是最关键的部分，它被自动解析用于生成日志和判断版本类型，格式为 `<type>(<scope>): <subject>`php.cn+1。

| 部分        | 必填   | 说明与示例                                                   |
| :---------- | :----- | :----------------------------------------------------------- |
| **type**    | **是** | **变更类型**，必须是预定义的值之一，**小写**。详见下方类型表。 |
| **scope**   | 否     | **影响范围**，用于说明本次提交影响的模块、文件或功能。**用圆括号括起来**，例如 `(auth)`、`(database)`、`(ui)`。多个 scope 可用逗号分隔，如 `(auth,api)`。php.cn |
| **subject** | **是** | **简短描述**，**不超过50个字符**。**使用祈使句、现在时态**（如 “add” 而非 “added” 或 “adds”），**首字母小写**，**结尾不加句号**。oryoy.com+1 |

**Header 示例**：

```
feat(login): 添加OAuth2.0登录支持
fix(api): 修复用户信息返回格式错误
docs(readme): 更新安装依赖说明
style: 统一代码缩进为4空格
refactor(user-service): 简化用户查询逻辑
perf(query): 优化订单列表查询索引
test(login): 增加登录失败用例
chore(deps): 更新lodash至版本4.17.21
```

### 3. 提交类型（type）大全

`type` 是规范的核心，必须从以下常用类型中选择：

| 类型         | 描述                            | 示例                                         | 影响版本号           |
| :----------- | :------------------------------ | :------------------------------------------- | :------------------- |
| **feat**     | 新功能 (feature)                | `feat(ship): 添加飞船加速功能`               | **MINOR** (次版本号) |
| **fix**      | 修复 bug                        | `fix(alien): 修复外星人碰撞检测问题`         | **PATCH** (修订号)   |
| **docs**     | 仅文档变更                      | `docs(api): 更新用户接口文档注释`            | 不影响               |
| **style**    | 代码格式调整（不影响逻辑）      | `style: 统一项目代码缩进为2空格`             | 不影响               |
| **refactor** | 重构（既不新增功能也不修复bug） | `refactor(game): 重构主循环逻辑以提升可读性` | 不影响               |
| **perf**     | 性能优化                        | `perf(bullet): 优化子弹绘制性能`             | **PATCH**            |
| **test**     | 测试相关                        | `test(alien): 增加外星人移动边界测试`        | 不影响               |
| **build**    | 构建系统或依赖变更              | `build(maven): 升级Spring Boot插件版本`      | 不影响               |
| **ci**       | CI配置变更                      | `ci(github-actions): 修改自动化部署流程`     | 不影响               |
| **chore**    | 其他不修改src/test的杂项        | `chore: 更新.gitignore忽略文件`              | 不影响               |
| **revert**   | 回滚之前的提交                  | `revert: feat(ship): 恢复飞船加速功能`       | 取决于原提交         |

> 💡 **提示**：`feat` 和 `fix` 类型**必然**会出现在 CHANGELOG 中。其他类型（如 `docs`, `style`, `refactor`, `test`, `chore`）通常**不会**出现在 CHANGELOG 中，除非它们包含了破坏性变更（BREAKING CHANGE）。csdn.net+1

### 4. Body（正文）- 可选

Body 用于对 Header 中的 subject 进行**更详细的补充说明**，主要解释**“为什么”**（Why）和**“如何”**（How）做这个变更，而不是重复“做了什么”（What）csdn.net+1。

- **必须**：在 Header 和 Body 之间**空一行**。
- **建议**：每行不超过 **72个字符**，以便在各种 Git 工具中良好显示oryoy.com+1。
- **内容**：可以包含多个段落，也可以使用无序列表（-）来列举要点csdn.net。

**Body 示例**：

```
fix(login): 修复用户登录时的Session丢失问题

之前的实现使用本地变量存储Session ID，在多请求环境下可能被覆盖。
现已改用Redis存储Session，并设置合理的过期时间，确保用户状态一致性。

修改包括：
- 新增SessionService及其Redis实现
- 修改LoginController集成新的SessionService
- 添加Session相关的单元测试
```

### 5. Footer（脚注）- 可选

Footer 用于补充一些**元数据**，主要场景有两种csdn.net+1：

- **破坏性变更（BREAKING CHANGE）**：当本次提交**不兼容**上一个版本时，**必须**在 Footer 中以 `BREAKING CHANGE:` 开头，后面是对破坏性变更的详细描述、理由和迁移方法。conventionalcommits.org+1

```
    feat(api)!: 移除用户创建接口中的`role`字段

    BREAKING CHANGE: 用户角色现在需要通过独立的权限管理接口进行分配。
    请更新客户端代码，调用新的`/users/{userId}/roles`接口来分配角色。
```

   \> ⚠️ **注意**：如果 Header 中的 `type` 和 `scope` 后紧跟一个 **`!`**（如 `feat(api)!:`），也**等同于**声明了一个破坏性变更，此时 Footer 中**可以**省略 `BREAKING CHANGE:`。conventionalcommits.org+1

- **关联 Issue**：如果本次提交是针对某个 Issue 的，可以在 Footer 中关闭它。常用的关键词有 `Closes`, `Fixes`, `Resolves`。csdn.net+1

```
    Closes #123
    Fixes #456, #789
```

## 4.2 完整的提交信息示例

结合以上所有部分，一个完整的提交信息如下：

```
feat(alien): 添加外星人舰队 formations

实现三种不同的外星人舰队编队模式：直线型、V字型和波浪型。
玩家可以通过按数字键1-3在游戏过程中切换编队，增加游戏策略性。

- 在AlienFleet类中添加formation_type属性
- 实现三种编队的生成算法
- 修改主循环以支持编队切换
- 添加编队切换的UI提示

BREAKING CHANGE: 简化版移除了编队功能，此提交重新引入但接口有变。
旧版本的控制台指令已失效，请使用新的键盘快捷键。

Closes #156
```

## 4.3 如何让团队坚持规范？（工具与配置）

规范要落地，离不开工具的支持。这里介绍几种从轻量到自动化的方法。

### 1. 使用 Git 提交模板（最简单）

你可以配置一个全局的提交模板，每次 `git commit` 时，编辑器会自动加载它，提醒你遵循规范。csdn.net+1

**步骤**：

1. **创建模板文件**（例如 `~/.gitmessage`）：

```
    # <type>(<scope>): <subject>
    # |----|  |-------| |----------|
    # |        |         +-- 简短描述（50字符以内，首字母小写，结尾无句号）
    # |        +------------ 影响范围（可选）
    # +----------------- 提交类型（必填）
    #
    # 类型(type)必须为以下之一:
    #   feat:     新功能
    #   fix:      修复bug
    #   docs:     文档变更
    #   style:    代码格式调整（不影响逻辑）
    #   refactor: 重构（既不新增功能也不修复bug）
    #   perf:     性能优化
    #   test:     测试相关
    #   build:    构建系统或依赖变更
    #   ci:       CI配置变更
    #   chore:    其他杂项
    #
    # 正文(body)详细说明（每行不超过72字符）：
    #
    #
    # 页脚(footer)用于关联Issue或描述BREAKING CHANGE:
    # 例如: Closes #123, BREAKING CHANGE: 破坏性变更描述
```

1. **配置 Git 使用该模板**：

```
    git config --global commit.template ~/.gitmessage
```

1. **使用**：下次运行 `git commit` 时，模板内容会自动出现在编辑器中。你只需要**删除注释行（#开头的行）并填写实际内容**即可。

### 2. 使用 Commitizen（交互式提问）

Commitizen 是一个工具，它通过**命令行交互式问答**来帮你生成符合规范的提交信息，代替 `git commit`。csdn.net+1

**安装与使用（以 Node.js 项目为例）**：

```
# 1. 全局安装 Commitizen
npm install -g commitizen

# 2. 在项目中初始化适配器（如 cz-conventional-changelog）
commitizen init cz-conventional-changelog --save-dev --save-exact
```

此后，在项目目录下使用 **`git cz`** 代替 `git commit`，它会像向导一样一步步引导你选择 Type、输入 Scope、Subject 等，最终生成符合规范的提交信息。

### 3. 使用 Commitlint + Husky（强制校验）

这是**团队协作中最推荐**的方案，通过 Git 钩子在提交前**自动校验**你的提交信息格式，不符合则拒绝提交，从源头保证规范。juejin.cn+1

**安装与配置（以 Node.js 项目为例）**：

```
# 1. 安装依赖
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky

# 2. 创建 commitlint 配置文件
echo "module.exports = {extends: ['@commitlint/config-conventional']};" > commitlint.config.js

# 3. 初始化 Husky 并添加 commit-msg 钩子
npx husky install
npx husky add .husky/commit-msg 'npx --no-install commitlint --edit "$1"'
```

此后，每次你运行 `git commit -m "xxx"` 时，Husky 都会调用 commitlint 来检查你的信息是否符合规范。如果不符合，终端会显示错误信息并提交失败。

## 4.4 最佳实践

**最佳实践**：

- **原子提交（Atomic Commit）**：**一次提交只做一件事**，保持提交的纯粹性和可追踪性。避免将多个不相关的修改混在一个提交里juejin.cn。
- **尽早提交，频繁提交**：不要等到工作全部完成再提交，完成一个小的功能点或修复一个 bug 就提交一次。
- **使用祈使句**：就像你在给代码库下指令一样：“**If applied, this commit will…**” (如果应用这个提交，它将…). 例如：`Add` 而非 `Added` 或 `Adds`。csdn.net+1
- **现在时态，首字母小写**：`fix bug` 而非 `fixed bug` 或 `Fix bug`。csdn.net
- **正文空行分隔**：务必在 Header 和 Body 之间、Body 和 Footer 之间保留一个空行，以便 Git 工具正确解析。juejin.cn
- **关联 Issue**：如果提交是为了解决某个 Issue，**一定要在 Footer 中关闭它**（如 `Closes #123`）。csdn.net

**常见误区**：

- ❌ **信息过于模糊**：如 `update code`、`fix bug`、`optimize`。**❌ 永远不要这么写！** 要具体说明改了什么代码、修复了什么问题。
- ❌ **信息过于冗长**：Subject 行超过了50个字符，或者 Body 行超过了72个字符。
- ❌ **使用过去时或进行时**：如 `Added feature` 或 `Adding feature`。
- ❌ **Subject 以句号结尾**：`Fix a bug.`
- ❌ **Header 和 Body 混在一起**：忘记在它们之间空行。
- ❌ **忘记声明破坏性变更**：如果 API 或接口有重大变化，**必须**使用 `BREAKING CHANGE` 或 `!` 明确声明。

## 4.5 提交类型快速参考表

下表汇总了所有提交类型及其核心用途，方便你快速查阅。

| 类型         | 名称     | 描述                                               | 是否影响 CHANGELOG  | 版本号影响   |
| :----------- | :------- | :------------------------------------------------- | :------------------ | :----------- |
| **feat**     | 新功能   | 添加新的用户可见功能                               | **是**              | **MINOR**    |
| **fix**      | 修复 bug | 修复线上或测试环境的 bug                           | **是**              | **PATCH**    |
| **docs**     | 文档     | 修改 README、API 文档、注释等                      | 否（除非是 README） | 不影响       |
| **style**    | 格式     | 代码格式化、空格、分号等（不影响逻辑）             | 否                  | 不影响       |
| **refactor** | 重构     | 优化代码结构、简化逻辑、重命名变量（不改变行为）   | 否                  | 不影响       |
| **perf**     | 性能     | 提升性能、优化加载速度                             | **是**              | **PATCH**    |
| **test**     | 测试     | 添加或修改测试用例                                 | 否                  | 不影响       |
| **build**    | 构建     | 修改构建工具、依赖库版本（如 webpack, npm）        | 否                  | 不影响       |
| **ci**       | CI配置   | 修改持续集成配置（如 Travis, GitHub Actions）      | 否                  | 不影响       |
| **chore**    | 杂项     | 其他不修改 src 或 test 的更改（如更新 .gitignore） | 否                  | 不影响       |
| **revert**   | 回滚     | 撤销之前的某次提交                                 | 否                  | 取决于原提交 |

> 💡 **小贴士**：你可以为常用的提交类型添加**emoji**表情，让提交历史更生动（但这不是约定式规范的一部分）。例如：`✨ feat`, `🐛 fix`, `📝 docs`, `♻️ refactor`, `⚡ perf`, `✅ test`, `🔧 chore`, `⏪ revert`。juejin.cn









