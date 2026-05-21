<h1 style="text-align: center;">Scrapy 基本概念</h1>

[TOC]

# 1 命令行工具

Scrapy 通过 `scrapy` 命令行工具进行控制，这里称之为“Scrapy 工具”，以区分于子命令，子命令我们直接称为“命令”或“Scrapy 命令”。

Scrapy 工具提供多种命令，用于多种目的，每个命令接受不同的参数和选项集。

（`scrapy deploy` 命令已在 1.0 版本中移除，取而代之的是独立的 `scrapyd-deploy`。请参阅 [部署你的项目](https://scrapyd.readthedocs.io/en/latest/deploy.html)。）

## 1.1 配置设置

Scrapy 会在标准位置查找 ini 风格的 `scrapy.cfg` 文件中的配置参数

1. `/etc/scrapy.cfg` 或 `c:\scrapy\scrapy.cfg`（系统范围），
2. `~/.config/scrapy.cfg` (`$XDG_CONFIG_HOME`) 和 `~/.scrapy.cfg` (`$HOME`) 用于全局（用户范围）设置，以及
3. Scrapy 项目根目录内的 `scrapy.cfg`（见下一节）。

这些文件中的设置按列出的优先级顺序合并：用户定义的值高于系统范围的默认值，而项目范围的设置（如果定义）将覆盖所有其他设置。

Scrapy 也理解并可以通过一些环境变量进行配置。目前这些变量包括

- `SCRAPY_SETTINGS_MODULE`（见 [指定设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-module-envvar)）
- `SCRAPY_PROJECT`（见 [在项目之间共享根目录](https://docs.scrapy.net.cn/en/latest/topics/commands.html#topics-project-envvar)）
- `SCRAPY_PYTHON_SHELL`（见 [Scrapy shell](https://docs.scrapy.net.cn/en/latest/topics/shell.html#topics-shell)）

## 1.2 Scrapy 项目的默认结构

在深入了解命令行工具及其子命令之前，让我们首先了解 Scrapy 项目的目录结构。

虽然可以修改，但所有 Scrapy 项目默认都具有相同的文件结构，类似于这样

```
scrapy.cfg
myproject/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
```

`scrapy.cfg` 文件所在的目录称为 *项目根目录（project root directory）*。该文件包含定义项目设置的 Python 模块的名称。以下是一个示例

```
[settings]
default = myproject.settings
```

## 1.3 在项目之间共享根目录

项目根目录，即包含 `scrapy.cfg` 的目录，可以由多个 Scrapy 项目共享，每个项目都有自己的设置模块。

在这种情况下，你必须在 `scrapy.cfg` 文件的 `[settings]` 下为这些设置模块定义一个或多个别名

```
[settings]
default = myproject1.settings
project1 = myproject1.settings
project2 = myproject2.settings
```

默认情况下，`scrapy` 命令行工具将使用 `default` 设置。使用 `SCRAPY_PROJECT` 环境变量指定 `scrapy` 要使用的不同项目

```
$ scrapy settings --get BOT_NAME
Project 1 Bot
$ export SCRAPY_PROJECT=project2
$ scrapy settings --get BOT_NAME
Project 2 Bot
```

## 1.4 使用 Scrapy 工具

你可以通过不带参数运行 Scrapy 工具开始，它将打印一些用法帮助和可用的命令

例如：我在我的 Scrapy 项目根目录下面使用 Scrapy 工具：

```bash
(BasicScrapyVenv) PS E:\Code\PyProjects\BasicScrapyDemo01> scrapy
Scrapy 2.13.4 - active project: BasicScrapyDemo01

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  check         Check spider contracts
  crawl         Run a spider
  edit          Edit spider
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  list          List available spiders
  parse         Parse URL (using its spider) and print the results
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

Use "scrapy <command> -h" to see more info about a command
```

---

```
Scrapy X.Y - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  crawl         Run a spider
  fetch         Fetch a URL using the Scrapy downloader
[...]
```

如果你在 Scrapy 项目内部，第一行将打印当前活动的项目。在这个示例中，它是在项目外部运行的。如果在项目内部运行，它会打印类似这样的内容

```
Scrapy X.Y - project: myproject

Usage:
  scrapy <command> [options] [args]

[...]
```

### 1.4.1 创建项目

使用 `scrapy` 工具通常做的第一件事是创建你的 Scrapy 项目

```
scrapy startproject myproject [project_dir]
```

这将在 `project_dir` 目录下创建一个名为 `myproject` 的 Scrapy 项目。如果未指定 `project_dir`，则 `project_dir` 将与 `myproject` 相同。

接下来，进入新的项目目录

```
cd project_dir
```

然后你就可以使用 `scrapy` 命令来管理和控制你的项目了。

### 1.4.2 控制项目

你在项目内部使用 `scrapy` 工具来控制和管理它们。

例如，要创建一个新的爬虫

```
scrapy genspider mydomain mydomain.com
```

一些 Scrapy 命令（如 [`crawl`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-crawl)）必须在 Scrapy 项目内部运行。请参阅下面的[命令参考](https://docs.scrapy.net.cn/en/latest/topics/commands.html#topics-commands-ref)，了解哪些命令必须在项目内部运行，哪些不必。

还要记住，在项目内部运行时，某些命令的行为可能会略有不同。例如，如果被抓取的 URL 与某些特定爬虫关联，fetch 命令将使用爬虫覆盖的行为（例如，`user_agent` 属性会覆盖用户代理）。这是有意为之的，因为 `fetch` 命令旨在用于检查爬虫如何下载页面。

## 1.5 可用的工具命令

本节包含内置命令列表及其说明和一些用法示例。请记住，你始终可以通过运行以下命令获取每个命令的更多信息

```
scrapy <command> -h
```

你也可以通过以下命令查看所有可用命令

```
scrapy -h
```

命令有两种类型，一种是只在 Scrapy 项目内部起作用的命令（项目特定命令），另一种是即使没有活动的 Scrapy 项目也起作用的命令（全局命令），尽管它们在项目内部运行时行为可能略有不同（因为它们会使用项目覆盖的设置）。

全局命令

- [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject)
- [`genspider`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-genspider)
- [`settings`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-settings)
- [`runspider`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-runspider)
- [`shell`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-shell)
- [`fetch`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-fetch)
- [`view`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-view)
- [`version`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-version)

仅限项目内的命令

- [`crawl`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-crawl)
- [`check`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-check)
- [`list`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-list)
- [`edit`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-edit)
- [`parse`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-parse)
- [`bench`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-bench)

### 1.5.1 startproject

- 语法: `scrapy startproject <project_name> [project_dir]`
- 需要项目: *否*

在 `project_dir` 目录下创建一个名为 `project_name` 的新 Scrapy 项目。如果未指定 `project_dir`，则 `project_dir` 将与 `project_name` 相同。

用法示例

```
$ scrapy startproject myproject
```

### 1.5.2 genspider

- 语法: `scrapy genspider [-t template] <name> <domain or URL>`
- 需要项目: *否*

*版本 2.6.0 新增：*增加了传递 URL 而不是域名的能力。

在当前文件夹或当前项目的 `spiders` 文件夹中创建新的爬虫，如果从项目内部调用的话。`<name>` 参数被设置为爬虫的 `name`，而 `<domain or URL>` 用于生成爬虫的 `allowed_domains` 和 `start_urls` 属性。

用法示例

```
$ scrapy genspider -l
Available templates:
  basic
  crawl
  csvfeed
  xmlfeed

$ scrapy genspider example example.com
Created spider 'example' using template 'basic'

$ scrapy genspider -t crawl scrapyorg scrapy.org
Created spider 'scrapyorg' using template 'crawl'
```

这只是一个基于预定义模板创建爬虫的便捷快捷命令，但绝不是创建爬虫的唯一方法。你可以自己创建爬虫源代码文件，而不是使用此命令。

### 1.5.3 crawl

- 语法: `scrapy crawl <spider>`
- 需要项目: *是*

使用指定的爬虫开始抓取。

支持的选项

- `-h, --help`: 显示帮助消息并退出
- `-a NAME=VALUE`: 设置爬虫参数（可重复）
- `--output FILE` 或 `-o FILE`: 将抓取的 item 追加到 FILE 末尾（使用 - 表示标准输出）。要定义输出格式，请在输出 URI 末尾设置冒号（例如 `-o FILE:FORMAT`）
- `--overwrite-output FILE` 或 `-O FILE`: 将抓取的 item 写入 FILE，覆盖任何现有文件。要定义输出格式，请在输出 URI 末尾设置冒号（例如 `-O FILE:FORMAT`）

用法示例

```powershell
$ scrapy crawl myspider
[ ... myspider starts crawling ... ]

$ scrapy crawl -o myfile:csv myspider
[ ... myspider starts crawling and appends the result to the file myfile in csv format ... ]

$ scrapy crawl -O myfile:json myspider
[ ... myspider starts crawling and saves the result in myfile in json format overwriting the original content... ]
```

### 1.5.4 check

- 语法: `scrapy check [-l] <spider>`
- 需要项目: *是*

运行契约检查。

用法示例

```
$ scrapy check -l
first_spider
  * parse
  * parse_item
second_spider
  * parse
  * parse_item

$ scrapy check
[FAILED] first_spider:parse_item
>>> 'RetailPricex' field is missing

[FAILED] first_spider:parse
>>> Returned 92 requests, expected 0..4
```

### 1.5.5 list

- 语法: `scrapy list`
- 需要项目: *是*

列出当前项目中的所有可用爬虫。输出为每行一个爬虫。

用法示例

```
$ scrapy list
spider1
spider2
```

### 1.5.6 edit

- 语法: `scrapy edit <spider>`
- 需要项目: *是*

使用 `EDITOR` 环境变量或（如果未设置）[`EDITOR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-EDITOR) 设置中定义的编辑器编辑给定的爬虫。

此命令仅作为最常见情况的便捷快捷方式提供，开发者当然可以自由选择任何工具或 IDE 来编写和调试爬虫。

用法示例

```
$ scrapy edit spider1
```

### 1.5.7 fetch

- 语法: `scrapy fetch <url>`
- 需要项目: *否*

使用 Scrapy 下载器下载给定的 URL 并将内容写入标准输出。

此命令有趣之处在于，它会像爬虫下载页面一样抓取页面。例如，如果爬虫具有覆盖用户代理的 `USER_AGENT` 属性，它将使用该属性。

因此，此命令可用于“查看”你的爬虫如何抓取某个页面。

如果在项目外部使用，则不会应用任何特定的爬虫行为，它只会使用默认的 Scrapy 下载器设置。

支持的选项

- `--spider=SPIDER`: 绕过爬虫自动检测，强制使用指定的爬虫
- `--headers`: 打印响应的 HTTP 头部而不是响应体
- `--no-redirect`: 不遵循 HTTP 3xx 重定向（默认为遵循）

用法示例

```
$ scrapy fetch --nolog http://www.example.com/some/page.html
[ ... html content here ... ]

$ scrapy fetch --nolog --headers http://www.example.com/
{'Accept-Ranges': ['bytes'],
 'Age': ['1263   '],
 'Connection': ['close     '],
 'Content-Length': ['596'],
 'Content-Type': ['text/html; charset=UTF-8'],
 'Date': ['Wed, 18 Aug 2010 23:59:46 GMT'],
 'Etag': ['"573c1-254-48c9c87349680"'],
 'Last-Modified': ['Fri, 30 Jul 2010 15:30:18 GMT'],
 'Server': ['Apache/2.2.3 (CentOS)']}
```

### 1.5.8 view

- 语法: `scrapy view <url>`
- 需要项目: *否*

在浏览器中打开给定的 URL，如同你的 Scrapy 爬虫“看到”它一样。有时爬虫看到的页面与普通用户不同，因此这可用于检查爬虫“看到”的内容并确认是否符合你的预期。

支持的选项

- `--spider=SPIDER`: 绕过爬虫自动检测，强制使用指定的爬虫
- `--no-redirect`: 不遵循 HTTP 3xx 重定向（默认为遵循）

用法示例

```
$ scrapy view http://www.example.com/some/page.html
[ ... browser starts ... ]
```

### 1.5.9 shell

- 语法: `scrapy shell [url]`
- 需要项目: *否*

启动给定 URL（如果给定）的 Scrapy shell，如果未给定 URL 则启动空 shell。还支持 UNIX 风格的本地文件路径，可以是带有 `./` 或 `../` 前缀的相对路径，也可以是绝对路径。有关更多信息，请参阅 [Scrapy shell](https://docs.scrapy.net.cn/en/latest/topics/shell.html#topics-shell)。

支持的选项

- `--spider=SPIDER`: 绕过爬虫自动检测，强制使用指定的爬虫
- `-c code`: 在 shell 中评估代码，打印结果并退出
- `--no-redirect`: 不遵循 HTTP 3xx 重定向（默认为遵循）；这仅影响你作为命令行参数传递的 URL；一旦进入 shell，`fetch(url)` 默认仍将遵循 HTTP 重定向。

用法示例

```
$ scrapy shell http://www.example.com/some/page.html
[ ... scrapy shell starts ... ]

$ scrapy shell --nolog http://www.example.com/ -c '(response.status, response.url)'
(200, 'http://www.example.com/')

# shell follows HTTP redirects by default
$ scrapy shell --nolog http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F -c '(response.status, response.url)'
(200, 'http://example.com/')

# you can disable this with --no-redirect
# (only for the URL passed as command line argument)
$ scrapy shell --no-redirect --nolog http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F -c '(response.status, response.url)'
(302, 'http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F')
```

### 1.5.10 parse

- 语法: `scrapy parse <url> [options]`
- 需要项目: *是*

抓取给定的 URL 并使用处理它的爬虫进行解析，解析方法使用 `--callback` 选项传递的方法，如果未指定则使用 `parse`。

支持的选项

- `--spider=SPIDER`: 绕过爬虫自动检测，强制使用指定的爬虫

- `--a NAME=VALUE`: 设置爬虫参数（可重复）

- `--callback` 或 `-c`: 用作解析响应的回调的爬虫方法

- `--meta` 或 `-m`: 将传递给回调请求的附加请求 meta 信息。这必须是一个有效的 json 字符串。示例：--meta='{“foo” : “bar”}'

- `--cbkwargs`: 将传递给回调的附加关键字参数。这必须是一个有效的 json 字符串。示例：--cbkwargs='{“foo” : “bar”}'

- `--pipelines`: 通过 item pipeline 处理 item

- `--rules` 或 `-r`: 使用 [`CrawlSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider) 规则来发现用于解析响应的回调（即爬虫方法）

- `--noitems`: 不显示抓取的 item

- `--nolinks`: 不显示提取的链接

- `--nocolour`: 避免使用 pygments 对输出进行着色

- `--depth` 或 `-d`: 请求应递归跟踪的深度级别（默认值：1）

- `--verbose` 或 `-v`: 显示每个深度级别的信息

- `--output` 或 `-o`: 将抓取的 item 写入文件

    *版本 2.3 新增。*

用法示例

```
$ scrapy parse http://www.example.com/ -c parse_item
[ ... scrapy log lines crawling example.com spider ... ]

>>> STATUS DEPTH LEVEL 1 <<<
# Scraped Items  ------------------------------------------------------------
[{'name': 'Example item',
 'category': 'Furniture',
 'length': '12 cm'}]

# Requests  -----------------------------------------------------------------
[]
```

### 1.5.11 settings

- 语法: `scrapy settings [options]`
- 需要项目: *否*

获取 Scrapy 设置的值。

如果在项目内部使用，它将显示项目设置的值，否则将显示该设置的默认 Scrapy 值。

用法示例

```
$ scrapy settings --get BOT_NAME
scrapybot
$ scrapy settings --get DOWNLOAD_DELAY
0
```

### 1.5.12 runspider

- 语法: `scrapy runspider <spider_file.py>`
- 需要项目: *否*

运行一个包含在 Python 文件中的自包含爬虫，无需创建项目。

用法示例

```
$ scrapy runspider myspider.py
[ ... spider starts crawling ... ]
```

### 1.5.13 version

- 语法: `scrapy version [-v]`
- 需要项目: *否*

打印 Scrapy 版本。如果与 `-v` 一起使用，它还会打印 Python、Twisted 和平台信息，这对于错误报告很有用。

### 1.5.14 bench

- 语法: `scrapy bench`
- 需要项目: *否*

运行快速性能测试。[性能测试](https://docs.scrapy.net.cn/en/latest/topics/benchmarking.html#benchmarking)。

## 1.6 自定义项目命令

你还可以通过使用 [`COMMANDS_MODULE`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-setting-COMMANDS_MODULE) 设置添加自定义项目命令。请参阅 [scrapy/commands](https://github.com/scrapy/scrapy/tree/master/scrapy/commands) 中的 Scrapy 命令，了解如何实现你的命令。

### 1.6.1 COMMAND_MODULE

默认值: `''` (空字符串)

一个用于查找自定义 Scrapy 命令的模块。这用于为你的 Scrapy 项目添加自定义命令。

示例

```
COMMANDS_MODULE = "mybot.commands"
```

### 1.6.2 通过 setup.py 入口注册命令

你还可以通过在库的 `setup.py` 文件的入口点中添加 `scrapy.commands` 部分来从外部库添加 Scrapy 命令。

以下示例添加了 `my_command` 命令

```
from setuptools import setup, find_packages

setup(
    name="scrapy-mymodule",
    entry_points={
        "scrapy.commands": [
            "my_command=my_scrapy_module.commands:MyCommand",
        ],
    },
)
```

# 2 爬虫(Spiders)

Spider 是类，它们定义了如何抓取某个网站（或一组网站），包括如何执行抓取（即跟随链接）以及如何从页面中提取结构化数据（即抓取 Item）。换句话说，Spider 是定义特定网站（或在某些情况下，一组网站）的爬取和解析页面自定义行为的地方。

对于爬虫而言，抓取周期大致如下：

1. 你首先生成初始请求来爬取第一个 URL，并指定一个回调函数来处理从这些请求下载到的响应。

    要执行的第一个请求是通过迭代 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 方法获得的，该方法默认会为 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls) spider 属性中的每个 URL 生成一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象，并将 [`parse`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 方法设置为 [`callback`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.callback) 函数来处理每个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)。

2. 在回调函数中，你解析响应（网页）并返回 [Item 对象](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)、[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象，或者这些对象的迭代器。这些 Request 也将包含一个回调（可能是同一个），然后由 Scrapy 下载，其响应再由指定的回调处理。

3. 在回调函数中，你解析页面内容，通常使用 [Selector](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#topics-selectors)（但你也可以使用 BeautifulSoup、lxml 或任何你喜欢的机制），并用解析后的数据生成 Item。

4. 最后，从 spider 返回的 Item 通常会持久化到数据库（在某些 [Item Pipeline](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline) 中）或使用 [Feed 导出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-exports) 写入文件。

尽管这个周期（或多或少）适用于任何类型的 spider，但 Scrapy 内置了不同类型的默认 spider，用于不同的目的。我们将在这里讨论这些类型。

## 2.1 scrapy.Spider

### 2.1.1 `class scrapy.spiders.Spider`

### 2.1.2 `class scrapy.Spider(*args: Any, **kwargs: Any)`

所有 spider 都必须继承的基类。

它提供了一个默认的 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 实现，根据 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls) 类属性发送请求，并为每个响应调用 [`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 方法。

- name[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.name)

    一个字符串，定义了该 spider 的名称。spider 名称是 Scrapy 定位（并实例化） spider 的方式，因此它必须是唯一的。但是，这并不妨碍你实例化同一个 spider 的多个实例。这是最重要的 spider 属性，并且是必需的。如果 spider 抓取单个域，一个常见的做法是将 spider 命名为该域的名称，可以包含或不包含 [TLD (顶级域名)](https://en.wikipedia.org/wiki/Top-level_domain)。例如，一个抓取 `mywebsite.com` 的 spider 通常会被命名为 `mywebsite`。

- allowed_domains[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.allowed_domains)

    一个可选的字符串列表，包含此 spider 允许爬取的域名。如果启用了 [`OffsiteMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.offsite.OffsiteMiddleware)，则属于此列表中指定域名（或其子域名）之外的 URL 请求将不会被跟随。假设你的目标 url 是 `https://www.example.com/1.html`，那么将 `'example.com'` 添加到此列表。

- start_urls*: [list](https://docs.pythonlang.cn/3/library/stdtypes.html#list)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)]*[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls)

    起始 URL。参见 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start)。

- custom_settings[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.custom_settings)

    一个设置字典，运行此 spider 时会覆盖项目范围的配置。它必须被定义为类属性，因为设置是在实例化之前更新的。有关可用内置设置的列表，请参见：[内置设置参考](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-ref)。

- crawler[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.crawler)

    此属性由 [`from_crawler()`](https://docs.scrapy.net.cn/en/latest/topics/components.html#from_crawler) 类方法在初始化类后设置，并链接到此 spider 实例所绑定的 [`Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 对象。Crawler 封装了项目中的许多组件，以便进行单一入口访问（例如扩展、中间件、信号管理器等）。要了解更多信息，请参见 [Crawler API](https://docs.scrapy.net.cn/en/latest/topics/api.html#topics-api-crawler)。

- settings[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.settings)

    运行此 spider 的配置。这是一个 [`Settings`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.settings.Settings) 实例，关于此主题的详细介绍，请参见 [设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings) 主题。

- logger[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.logger)

    使用 Spider 的 [`name`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.name) 创建的 Python logger。你可以使用它来发送日志消息，详见 [从 Spider 记录日志](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-from-spiders)。

- state[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.state)

    一个字典，你可以用来在批次之间持久化一些 spider 状态。要了解更多信息，请参见 [在批次之间保持持久状态](https://docs.scrapy.net.cn/en/latest/topics/jobs.html#topics-keeping-persistent-state-between-batches)。

- from_crawler(*crawler*, **args*, ***kwargs*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders.html#Spider.from_crawler)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.from_crawler)

    这是 Scrapy 用来创建你的 spider 的类方法。你可能不需要直接覆盖此方法，因为默认实现充当 [`__init__()`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#init__) 方法的代理，并使用给定的位置参数 `args` 和命名参数 `kwargs` 调用它。尽管如此，此方法在新实例中设置了 [`crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#module-scrapy.crawler) 和 [`settings`](https://docs.scrapy.net.cn/en/latest/topics/api.html#module-scrapy.settings) 属性，以便之后在 spider 代码中访问它们。*版本 2.11 中的变化:* `crawler.settings` 中的设置现在可以在此方法中修改，这对于你想基于参数修改设置时很方便。因此，这些设置不是最终值，因为它们可能在之后被例如 [附加组件](https://docs.scrapy.net.cn/en/latest/topics/addons.html#topics-addons) 修改。出于同样的原因，此时大多数 [`Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 属性尚未初始化。最终设置和初始化的 [`Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 属性可在 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 方法、[`engine_started`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-engine_started) 信号的处理程序以及更晚的时候使用。参数:**crawler** ([`Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 实例) – spider 将绑定到的 crawler**args** ([*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 传递给 [`__init__()`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#init__) 方法的参数**kwargs** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 传递给 [`__init__()`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#init__) 方法的关键字参数

- *classmethod *update_settings(*settings*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders.html#Spider.update_settings)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.update_settings)

    `update_settings()` 方法用于修改 spider 的设置，并在初始化 spider 实例时调用。它接受一个 [`Settings`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.settings.Settings) 对象作为参数，可以添加或更新 spider 的配置值。此方法是一个类方法，意味着它在 [`Spider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider) 类上调用，并允许所有 spider 实例共享相同的配置。虽然可以在 [`custom_settings`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.custom_settings) 中设置每个 spider 的设置，但使用 `update_settings()` 可以让你根据其他设置、spider 属性或其他因素动态添加、删除或更改设置，并使用 `'spider'` 之外的设置优先级。此外，在子类中通过覆盖 `update_settings()` 可以轻松地扩展它，而对 [`custom_settings`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.custom_settings) 做同样的事情可能会很困难。例如，假设一个 spider 需要修改 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS)`import scrapy  class MySpider(scrapy.Spider):    name = "myspider"    custom_feed = {        "/home/user/documents/items.json": {            "format": "json",            "indent": 4,        }    }     @classmethod    def update_settings(cls, settings):        super().update_settings(settings)        settings.setdefault("FEEDS", {}).update(cls.custom_feed) `

- *async* start()→ AsyncIterator[Any][[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders.html#Spider.start)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start)

    生成要发送的初始 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。*版本 2.13 中新增。*例如`from scrapy import Request, Spider  class MySpider(Spider):    name = "myspider"     async def start(self):        yield Request("https://toscrape.com/") `默认实现从 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls) 读取 URL，并为每个 URL 生成一个启用 [`dont_filter`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.dont_filter) 的请求。它在功能上等同于`async def start(self):    for url in self.start_urls:        yield Request(url, dont_filter=True) `你也可以生成 [Item](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)。例如`async def start(self):    yield {"foo": "bar"} `要编写适用于 Scrapy 2.13 之前版本的 spider，还需要定义一个返回可迭代对象的同步 `start_requests()` 方法。例如`def start_requests(self):    yield Request("https://toscrape.com/") `另请参阅[起始请求](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#start-requests)

- parse(*response*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders.html#Spider.parse)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse)

    这是 Scrapy 用来处理下载的响应的默认回调，当它们的请求未指定回调时。`parse` 方法负责处理响应并返回抓取的数据和/或更多要跟随的 URL。其他 Request 回调的要求与 [`Spider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider) 类相同。此方法以及任何其他 Request 回调，必须返回一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象、一个 [Item 对象](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)、包含任何这些对象的迭代器，或者 `None`。参数:**response** ([`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)) – 要解析的响应

- log(*message***[**, *level*, *component***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders.html#Spider.log)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.log)

    通过 Spider 的 [`logger`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.logger) 发送日志消息的包装器，保留用于向后兼容。要了解更多信息，请参见 [从 Spider 记录日志](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-from-spiders)。

- closed(*reason*)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.closed)

    在 spider 关闭时调用。此方法为 [`spider_closed`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-spider_closed) 信号提供了 signals.connect() 的快捷方式。

让我们看一个例子

```
import scrapy


class MySpider(scrapy.Spider):
    name = "example.com"
    allowed_domains = ["example.com"]
    start_urls = [
        "http://www.example.com/1.html",
        "http://www.example.com/2.html",
        "http://www.example.com/3.html",
    ]

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
```

从单个回调返回多个 Request 和 Item

```
import scrapy


class MySpider(scrapy.Spider):
    name = "example.com"
    allowed_domains = ["example.com"]
    start_urls = [
        "http://www.example.com/1.html",
        "http://www.example.com/2.html",
        "http://www.example.com/3.html",
    ]

    def parse(self, response):
        for h3 in response.xpath("//h3").getall():
            yield {"title": h3}

        for href in response.xpath("//a/@href").getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
```

你可以直接使用 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 而不是 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls)；为了给数据更多结构，你可以使用 [`Item`](https://docs.scrapy.net.cn/en/latest/topics/items.html#scrapy.Item) 对象

```
import scrapy
from myproject.items import MyItem


class MySpider(scrapy.Spider):
    name = "example.com"
    allowed_domains = ["example.com"]

    async def start(self):
        yield scrapy.Request("http://www.example.com/1.html", self.parse)
        yield scrapy.Request("http://www.example.com/2.html", self.parse)
        yield scrapy.Request("http://www.example.com/3.html", self.parse)

    def parse(self, response):
        for h3 in response.xpath("//h3").getall():
            yield MyItem(title=h3)

        for href in response.xpath("//a/@href").getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
```

## 2.2 Spider 参数

Spider 可以接收修改其行为的参数。spider 参数的一些常见用途是定义起始 URL 或将爬取限制在网站的某些部分，但它们可以用于配置 spider 的任何功能。

spider 参数通过 [`crawl`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-crawl) 命令使用 `-a` 选项传递。例如

```
scrapy crawl myspider -a category=electronics
```

Spider 可以在它们的 __init__ 方法中访问参数

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"http://www.example.com/categories/{category}"]
        # ...
```

默认的 __init__ 方法将接受任何 spider 参数并将它们作为属性复制到 spider 中。上面的例子也可以写成如下形式

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"

    async def start(self):
        yield scrapy.Request(f"http://www.example.com/categories/{self.category}")
```

如果你是[从脚本运行 Scrapy](https://docs.scrapy.net.cn/en/latest/topics/practices.html#run-from-script)，可以在调用 [`CrawlerProcess.crawl`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerProcess.crawl) 或 [`CrawlerRunner.crawl`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerRunner.crawl) 时指定 spider 参数

```
process = CrawlerProcess()
process.crawl(MySpider, category="electronics")
```

请记住，spider 参数仅为字符串。spider 本身不会进行任何解析。如果你要从命令行设置 `start_urls` 属性，则必须使用 [`ast.literal_eval()`](https://docs.pythonlang.cn/3/library/ast.html#ast.literal_eval) 或 [`json.loads()`](https://docs.pythonlang.cn/3/library/json.html#json.loads) 等方法将其解析为列表，然后将其设置为属性。否则，你将会遍历 `start_urls` 字符串（一个非常常见的 Python 陷阱），导致每个字符被视为一个单独的 url。

一个有效的用例是设置由 [`HttpAuthMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware) 使用的 http 认证凭据或由 [`UserAgentMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.useragent.UserAgentMiddleware) 使用的用户代理。

```
scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot
```

Spider 参数也可以通过 Scrapyd `schedule.json` API 传递。参见 [Scrapyd documentation](https://scrapyd.readthedocs.io/en/latest/)。

## 2.3 起始请求

**起始请求**是 从 spider 的 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 方法或 [spider 中间件](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware) 的 [`process_start()`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#scrapy.spidermiddlewares.SpiderMiddleware.process_start) 方法生成的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。

另请参阅

> [起始请求顺序](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#start-request-order)

### 2.3.1 延迟起始请求迭代

你可以按如下方式覆盖 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 方法，以便在有计划中的请求时暂停其迭代

```
async def start(self):
    async for item_or_request in super().start():
        if self.crawler.engine.needs_backoff():
            await self.crawler.signals.wait_for(signals.scheduler_empty)
        yield item_or_request
```

这有助于在任何给定时间最小化调度器中的请求数量，从而最小化资源使用（内存或磁盘，取决于 [`JOBDIR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-JOBDIR)）。

## 2.4 通用爬虫

Scrapy 内置了一些有用的通用爬虫，你可以继承它们来创建你的 spider。它们旨在为一些常见的抓取场景提供便利功能，例如根据某些规则跟随网站上的所有链接，从 [Sitemaps](https://www.sitemaps.org/index.html) 爬取，或解析 XML/CSV feed。

对于以下 spider 中使用的示例，我们假设你有一个项目，其中在 `myproject.items` 模块中声明了一个 `TestItem`

```
import scrapy


class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
```

### 2.4.1 CrawlSpider

class scrapy.spiders.CrawlSpider 

这是最常用的爬虫，用于抓取常规网站，因为它通过定义一组规则提供了一种方便的跟随链接机制。它可能不是最适合你的特定网站或项目，但它对于多种情况来说足够通用，因此你可以从它开始，并根据需要覆盖它以实现更自定义的功能，或者直接实现你自己的 spider。

除了从 Spider 继承的属性（你必须指定）之外，此类还支持一个新属性

- rules[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider.rules)

    它是一个包含一个（或多个）[`Rule`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Rule) 对象的列表。每个 [`Rule`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Rule) 定义了爬取网站的特定行为。Rule 对象在下面描述。如果多个规则匹配同一个链接，将根据它们在此属性中定义的顺序使用第一个匹配的规则。

此 spider 还公开了一个可覆盖的方法

- parse_start_url(*response*, ***kwargs*)[](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/crawl.html#CrawlSpider.parse_start_url)

    此方法会对 spider 的 `start_urls` 属性中 URL 生成的每个响应调用。它允许解析初始响应，并且必须返回一个 [Item 对象](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)、一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象，或包含其中任何一个的迭代器。

#### 2.4.1.1 爬取规则

- *class*scrapy.spiders.Rule(*link_extractor: LinkExtractor | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *callback: CallbackT | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cb_kwargs: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *follow: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *process_links: ProcessLinksT | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *process_request: ProcessRequestT | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) |[None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *errback: Callable[[Failure], Any] | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) |[None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/crawl.html#Rule)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Rule)

    `link_extractor` 是一个 [Link Extractor (链接提取器)](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#topics-link-extractors) 对象，它定义了如何从每个爬取的页面提取链接。每个提取的链接都将用于生成一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象，该对象将在其 `meta` 字典中包含链接的文本（键为 `link_text`）。如果省略，将使用一个不带参数创建的默认链接提取器，这将提取所有链接。`callback` 是一个可调用对象或一个字符串（在这种情况下，将使用 spider 对象中同名的方法），用于处理使用指定链接提取器提取的每个链接。此回调函数接收一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 作为其第一个参数，并且必须返回单个实例或一个由 [item 对象](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items) 和/或 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象（或它们的任何子类）组成的可迭代对象。如上所述，收到的 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象将在其 `meta` 字典中包含生成 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 的链接文本（键为 `link_text`）。`cb_kwargs` 是一个字典，包含要传递给回调函数的关键字参数。`follow` 是一个布尔值，指定是否应从使用此规则提取的每个响应中跟踪链接。如果 `callback` 为 None，则 `follow` 默认为 `True`，否则默认为 `False`。`process_links` 是一个可调用对象或一个字符串（在这种情况下，将使用 spider 对象中同名的方法），它将针对使用指定的 `link_extractor` 从每个响应中提取的链接列表调用。这主要用于过滤目的。`process_request` 是一个可调用对象（或一个字符串，在这种情况下，将使用 spider 对象中同名的方法），它将针对此规则提取的每个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 调用。此可调用对象应将该请求作为第一个参数，并将生成该请求的 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 作为第二个参数。它必须返回一个 `Request` 对象或 `None`（以过滤掉请求）。`errback` 是一个可调用对象或一个字符串（在这种情况下，将使用 spider 对象中同名的方法），用于在处理规则生成的请求时发生任何异常时调用。它接收一个 [`Twisted Failure`](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html) 实例作为第一个参数。警告由于其内部实现，在编写基于 [`CrawlSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider) 的 spider 时，您必须为新请求显式设置回调函数；否则可能发生意外行为。*添加到 2.0 版本：* *errback* 参数。

#### 2.4.1.2 CrawlSpider 示例

现在让我们来看一个带有规则的 CrawlSpider 示例

```
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):
    name = "example.com"
    allowed_domains = ["example.com"]
    start_urls = ["http://www.example.com"]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r"category\.php",), deny=(r"subsection\.php",))),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r"item\.php",)), callback="parse_item"),
    )

    def parse_item(self, response):
        self.logger.info("Hi, this is an item page! %s", response.url)
        item = scrapy.Item()
        item["id"] = response.xpath('//td[@id="item_id"]/text()').re(r"ID: (\d+)")
        item["name"] = response.xpath('//td[@id="item_name"]/text()').get()
        item["description"] = response.xpath(
            '//td[@id="item_description"]/text()'
        ).get()
        item["link_text"] = response.meta["link_text"]
        url = response.xpath('//td[@id="additional_data"]/@href').get()
        return response.follow(
            url, self.parse_additional_page, cb_kwargs=dict(item=item)
        )

    def parse_additional_page(self, response, item):
        item["additional_data"] = response.xpath(
            '//p[@id="additional_data"]/text()'
        ).get()
        return item
```

此 spider 将开始爬取 example.com 的主页，收集类别链接和商品链接，并使用 `parse_item` 方法解析商品链接。对于每个商品响应，将使用 XPath 从 HTML 中提取一些数据，并使用这些数据填充一个 [`Item`](https://docs.scrapy.net.cn/en/latest/topics/items.html#scrapy.Item) 对象。

### 2.4.2 XMLFeedSpider

#### 2.4.2.1 `class scrapy.spiders.XMLFeedSpider`

XMLFeedSpider 设计用于通过按某个节点名称迭代来解析 XML feeds。迭代器可以选择：`iternodes`、`xml` 和 `html`。建议出于性能原因使用 `iternodes` 迭代器，因为 `xml` 和 `html` 迭代器会一次性生成整个 DOM 以进行解析。但是，在解析标记错误的 XML 时，使用 `html` 作为迭代器可能会很有用。

要设置迭代器和标签名称，必须定义以下类属性：

- iterator[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.iterator)

    一个字符串，定义要使用的迭代器。可以是以下之一：`'iternodes'` - 基于正则表达式的快速迭代器`'html'` - 使用 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 的迭代器。请记住，这使用 DOM 解析，必须将所有 DOM 加载到内存中，这对于大型 feed 可能是一个问题。`'xml'` - 使用 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 的迭代器。请记住，这使用 DOM 解析，必须将所有 DOM 加载到内存中，这对于大型 feed 可能是一个问题。默认为：`'iternodes'`。

- itertag[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.itertag)

    一个字符串，包含要迭代的节点（或元素）的名称。示例：`itertag = 'product' `

- 命名空间[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.namespaces)

    namespaces[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.namespaces)一个 `(prefix, uri)` 元组列表，定义将由该 spider 处理的文档中可用的命名空间。`prefix` 和 `uri` 将用于使用 [`register_namespace()`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector.register_namespace) 方法自动注册命名空间。然后可以在 [`itertag`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.itertag) 属性中指定带命名空间的节点。`class YourSpider(XMLFeedSpider):     namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]    itertag = 'n:url'    # ... `

示例：

- 除了这些新属性外，此 spider 还具有以下可覆盖的方法：

    adapt_response(*response*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/feed.html#XMLFeedSpider.adapt_response)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.adapt_response)

- 一个方法，在 spider 开始解析之前，收到响应后立即被调用。它可以用于在解析响应体之前修改它。此方法接收一个响应，并返回一个响应（可以是同一个或另一个）。

    parse_node(*response*, *selector*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/feed.html#XMLFeedSpider.parse_node)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.parse_node)

- 此方法针对匹配提供的标签名称 (`itertag`) 的节点调用。接收响应和每个节点的 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 对象。覆盖此方法是强制性的。否则，您的 spider 将无法工作。此方法必须返回一个 [item 对象](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)、一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象，或包含它们中任何一个的可迭代对象。

    process_results(*response*, *results*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/feed.html#XMLFeedSpider.process_results)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider.process_results)

警告

此方法针对 spider 返回的每个结果（item 或 request）调用，其目的是在将结果返回给框架核心之前执行任何最后的处理，例如设置 item ID。它接收结果列表和生成这些结果的响应。它必须返回结果（item 或 request）列表。

由于其内部实现，在编写基于 [`XMLFeedSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.XMLFeedSpider) 的 spider 时，您必须为新请求显式设置回调函数；否则可能发生意外行为。

#### 2.4.2.2 XMLFeedSpider 示例

这些 spider 非常易于使用，让我们看一个示例：

```python
from scrapy.spiders import XMLFeedSpider
from myproject.items import TestItem


class MySpider(XMLFeedSpider):
    name = "example.com"
    allowed_domains = ["example.com"]
    start_urls = ["http://www.example.com/feed.xml"]
    iterator = "iternodes"  # This is actually unnecessary, since it's the default value
    itertag = "item"

    def parse_node(self, response, node):
        self.logger.info(
            "Hi, this is a <%s> node!: %s", self.itertag, "".join(node.getall())
        )

        item = TestItem()
        item["id"] = node.xpath("@id").get()
        item["name"] = node.xpath("name").get()
        item["description"] = node.xpath("description").get()
        return item
```

基本上，我们在上面做的是创建一个 spider，它从给定的 `start_urls` 下载一个 feed，然后迭代其每个 `item` 标签，将它们打印出来，并将一些随机数据存储在 [`Item`](https://docs.scrapy.net.cn/en/latest/topics/items.html#scrapy.Item) 中。

### 2.4.3 CSVFeedSpider

#### 2.4.3.1 `classscrapy.spiders.CSVFeedSpider`

- 此 spider 与 XMLFeedSpider 非常相似，不同之处在于它迭代行，而不是节点。每次迭代中调用的方法是 [`parse_row()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider.parse_row)。

    delimiter[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider.delimiter)

- 一个字符串，表示 CSV 文件中每个字段的分隔符。默认为 `','`（逗号）。

    quotechar[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider.quotechar)

- 一个字符串，表示 CSV 文件中每个字段的包围字符。默认为 `'"'`（引号）。

    headers[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider.headers)

- CSV 文件中的列名列表。

    parse_row(*response*, *row*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/spiders/feed.html#CSVFeedSpider.parse_row)[](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider.parse_row)

接收一个响应和一个字典（代表每一行），字典的每个键对应于 CSV 文件中提供的（或检测到的）每个头部。此 spider 还提供了覆盖 `adapt_response` 和 `process_results` 方法以进行预处理和后处理的机会。

#### 2.4.3.2 CSVFeedSpider 示例

让我们看一个与前面类似的示例，但使用 [`CSVFeedSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CSVFeedSpider)：

```python
from scrapy.spiders import CSVFeedSpider
from myproject.items import TestItem


class MySpider(CSVFeedSpider):
    name = "example.com"
    allowed_domains = ["example.com"]
    start_urls = ["http://www.example.com/feed.csv"]
    delimiter = ";"
    quotechar = "'"
    headers = ["id", "name", "description"]

    def parse_row(self, response, row):
        self.logger.info("Hi, this is a row!: %r", row)

        item = TestItem()
        item["id"] = row["id"]
        item["name"] = row["name"]
        item["description"] = row["description"]
        return item
```

### 2.4.4 SitemapSpider

#### 2.4.4.1 `classscrapy.spiders.CrawlSpider`

SitemapSpider 让您能够通过解析 Sitemaps 来发现 URL 并爬取网站。

它兼容嵌套的 sitemaps，并能够从 robots.txt 文件中识别 sitemap URLs。

- sitemap_urls[](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.SitemapSpider.sitemap_urls)

    一个包含您想要爬取的 sitemaps 的 URL 列表。您也可以指定一个 [robots.txt](https://www.robotstxt.org/) 文件，该文件将被解析以从中提取 sitemap URLs。

- sitemap_rules[](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.SitemapSpider.sitemap_rules)

    一个由元组 `(regex, callback)` 组成的列表，其中：

    - `regex` 是用于匹配从 sitemaps 中提取的 URL 的正则表达式。`regex` 可以是一个字符串或一个已编译的正则表达式对象。
    - `callback` 是用于处理与正则表达式匹配的 URL 的回调函数。`callback` 可以是一个字符串（表示蜘蛛方法的名称）或一个可调用对象。

    例如：
    `sitemap_rules = [('/product/', 'parse_product')]`

    规则按顺序应用，只有第一个匹配的规则会被使用。
    如果您省略这个属性，所有在 sitemaps 中找到的 URL 将使用 `parse` 回调函数处理。

- sitemap_follow[](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.SitemapSpider.sitemap_follow)

    一个应被跟随的 sitemap 正则表达式列表。这仅适用于使用 [Sitemap 索引文件](https://www.sitemaps.org/protocol.html#index) 指向其他 sitemap 文件的站点。默认情况下，所有 sitemaps 都会被跟随。

- sitemap_alternate_links[](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.SitemapSpider.sitemap_alternate_links)

    指定是否应跟随同一 `url` 块中提供的同一网站的其他语言链接。例如：

    ```
    <url>
        <loc>http://example.com/</loc>
        <xhtml:link rel="alternate" hreflang="de" href="http://example.com/de"/>
    </url>
    ```

    如果启用了 `sitemap_alternate_links`，这将获取两个 URL。如果禁用了 `sitemap_alternate_links`，则只获取 `http://example.com/`。默认情况下禁用 `sitemap_alternate_links`。

- sitemap_filter(*entries*)[[source\]](https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/sitemap.html#SitemapSpider.sitemap_filter)[](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.SitemapSpider.sitemap_filter)

    这是一个可以被重写的过滤函数，用于根据条目的属性选择sitemap条目。例如：
    ```xml
    <url>
        <loc>http://example.com/</loc>
        <lastmod>2005-01-01</lastmod>
    </url>
    ```
    我们可以定义一个 `sitemap_filter` 函数，通过日期过滤 `entries`：
    ```python
    from datetime import datetime
    from scrapy.spiders import SitemapSpider
    class FilteredSitemapSpider(SitemapSpider):
        name = "filtered_sitemap_spider"
        allowed_domains = ["example.com"]
        sitemap_urls = ["http://example.com/sitemap.xml"]
        def sitemap_filter(self, entries):
            for entry in entries:
                date_time = datetime.strptime(entry["lastmod"], "%Y-%m-%d")
                if date_time.year >= 2005:
                    yield entry
    ```
    这将只检索2005年及以后年份修改的 `entries`。条目是从sitemap文档中提取的字典对象。通常，键是标签名称，值是其中的文本。
    需要注意的重要一点是：
    - 由于需要loc属性，因此没有此标签的条目将被丢弃。
    - 备用链接存储在一个以 `alternate` 为键的列表中（参见 `sitemap_alternate_links`）。
    - 命名空间被移除，因此lxml标签名为 `{namespace}tagname` 的变为仅 `tagname`。
    如果您省略此方法，将处理在sitemap中找到的所有条目，同时观察其他属性及其设置。

#### 2.4.4.2 SitemapSpider 示例

### 直译
最简单的例子：使用 `parse` 回调处理通过 sitemaps 发现的所有 URL：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/sitemap.xml"]
    def parse(self, response):
        pass  # ... 在这里抓取项目 ...
```
使用特定的回调处理一些 URL，而使用不同的回调处理其他 URL：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/sitemap.xml"]
    sitemap_rules = [
        ("/product/", "parse_product"),
        ("/category/", "parse_category"),
    ]
    def parse_product(self, response):
        pass  # ... 抓取产品 ...
    def parse_category(self, response):
        pass  # ... 抓取类别 ...
```
跟随在 [robots.txt](https://www.robotstxt.org/) 文件中定义的 sitemaps，并且只跟随 URL 包含 `/sitemap_shop` 的 sitemaps：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/robots.txt"]
    sitemap_rules = [
        ("/shop/", "parse_shop"),
    ]
    sitemap_follow = ["/sitemap_shops"]
    def parse_shop(self, response):
        pass  # ... 在这里抓取商店 ...
```
将 SitemapSpider 与其他 URL 来源结合使用：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/robots.txt"]
    sitemap_rules = [
        ("/shop/", "parse_shop"),
    ]
    other_urls = ["http://www.example.com/about"]
    async def start(self):
        async for item_or_request in super().start():
            yield item_or_request
        for url in self.other_urls:
            yield Request(url, self.parse_other)
    def parse_shop(self, response):
        pass  # ... 在这里抓取商店 ...
    def parse_other(self, response):
        pass  # ... 在这里抓取其他内容 ...
```
***
### 问题
1. 在第一个代码示例中，“pass  # ... scrape item here ...”直译为“pass  # ... 在这里抓取项目 ...”，这种表达符合中文编程习惯。
2. 在第二个代码示例中，“sitemap_rules = [("/product/", "parse_product"), ("/category/", "parse_category"), ]”这部分不需要改动，因为代码格式和内容已经很清晰。
3. 在第三个代码示例中，“sitemap_follow = ["/sitemap_shops"]”这部分不需要改动，因为代码格式和内容已经很清晰。
4. 在第四个代码示例中，“async def start(self):”这部分不需要改动，因为代码格式和内容已经很清晰。但是，“yield Request(url, self.parse_other)”中的“Request”应该是一个未定义的类，可能是作者笔误，应该是“yield scrapy.Request(url, self.parse_other)”。
5. 在第四个代码示例中，“pass  # ... scrape other here ...”直译为“pass  # ... 在这里抓取其他内容 ...”，这种表达符合中文编程习惯。
***
### 意译
最简单的例子：使用 `parse` 回调处理通过 sitemaps 发现的所有 URL：
```python
from scrapy.spiders import SitemapSpider


class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/sitemap.xml"]

    def parse(self, response):
        pass  # ... scrape item here ...
```
使用特定的回调处理一些 URL，而使用不同的回调处理其他 URL：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/sitemap.xml"]
    sitemap_rules = [
        ("/product/", "parse_product"),
        ("/category/", "parse_category"),
    ]
    def parse_product(self, response):
        pass  # ... 抓取产品 ...
    def parse_category(self, response):
        pass  # ... 抓取类别 ...
```
跟随在 [robots.txt](https://www.robotstxt.org/) 文件中定义的 sitemaps，并且只跟随 URL 包含 `/sitemap_shop` 的 sitemaps：
```python
from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/robots.txt"]
    sitemap_rules = [
        ("/shop/", "parse_shop"),
    ]
    sitemap_follow = ["/sitemap_shops"]
    def parse_shop(self, response):
        pass  # ... 在这里抓取商店 ...
```
将 SitemapSpider 与其他 URL 来源结合使用：
```python
from scrapy.spiders import SitemapSpider


class MySpider(SitemapSpider):
    sitemap_urls = ["http://www.example.com/robots.txt"]
    sitemap_rules = [
        ("/shop/", "parse_shop"),
    ]

    other_urls = ["http://www.example.com/about"]

    async def start(self):
        async for item_or_request in super().start():
            yield item_or_request
        for url in self.other_urls:
            yield Request(url, self.parse_other)

    def parse_shop(self, response):
        pass  # ... scrape shop here ...

    def parse_other(self, response):
        pass  # ... scrape other here ...   
```

# 3 选择器

当你抓取网页时，最常见的任务是从 HTML 源代码中提取数据。有几种库可以实现这一点，例如：

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 是 Python 程序员中非常流行的网页抓取库，它根据 HTML 代码的结构构建 Python 对象，并且能够很好地处理糟糕的标记，但它有一个缺点：速度慢。
- [lxml](https://lxml.de/) 是一个 XML 解析库（也解析 HTML），它基于 [`ElementTree`](https://docs.pythonlang.cn/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) 提供了符合 Python 习惯的 API。（lxml 不是 Python 标准库的一部分。）

Scrapy 有自己的一套数据提取机制。它们被称为选择器（selectors），因为它们可以通过 [XPath](https://www.w3.org/TR/xpath/all/) 或 [CSS](https://www.w3.org/TR/selectors) 表达式来“选择” HTML 文档的特定部分。

[XPath](https://www.w3.org/TR/xpath/all/) 是一种用于选择 XML 文档节点的语言，也可用于 HTML。[CSS](https://www.w3.org/TR/selectors) 是一种用于给 HTML 文档应用样式的语言。它定义了选择器来将这些样式与特定的 HTML 元素关联起来。

注意

Scrapy 选择器是 [parsel](https://parsel.readthedocs.io/en/latest/) 库的一个轻量级封装；这个封装的目的是为了更好地与 Scrapy Response 对象集成。

[parsel](https://parsel.readthedocs.io/en/latest/) 是一个独立的网页抓取库，可以在不使用 Scrapy 的情况下使用。它底层使用了 [lxml](https://lxml.de/) 库，并在 lxml API 的基础上实现了一个简易的 API。这意味着 Scrapy 选择器在速度和解析精度上与 lxml 非常相似。

## 3.1 使用选择器

补充：Scrapy 选择器核心方法中文速查表

| 类别           | 方法 / 语法                        | 作用                                      | 示例                                                         | 结果                        |
| -------------- | ---------------------------------- | ----------------------------------------- | ------------------------------------------------------------ | --------------------------- |
| **基础选择**   | `response.xpath("xpath_expr")`     | 用 XPath 表达式选取节点                   | `response.xpath("//title/text()")`                           | 返回 `SelectorList`         |
|                | `response.css("css_expr")`         | 用 CSS 选择器选取节点                     | `response.css("title::text")`                                | 返回 `SelectorList`         |
| **数据提取**   | `.get()`                           | 提取**第一个**匹配结果，无匹配返回 `None` | `response.xpath("//title/text()").get()`                     | `'Example website'`         |
|                | `.get(default="值")`               | 无匹配时返回指定默认值                    | `response.xpath("//div[@id='not-exists']/text()").get(default="not-found")` | `'not-found'`               |
|                | `.getall()`                        | 提取**所有**匹配结果，返回列表            | `response.css("img::attr(src)").getall()`                    | `['image1_thumb.jpg', ...]` |
|                | `.attrib["属性名"]`                | 从选择器获取指定属性值                    | `response.css("base").attrib["href"]`                        | `'http://example.com/'`     |
| **CSS 伪元素** | `::text`                           | 选取节点文本内容                          | `response.css("title::text").get()`                          | `'Example website'`         |
|                | `::attr(属性名)`                   | 选取节点指定属性                          | `response.css("base::attr(href)").get()`                     | `'http://example.com/'`     |
| **嵌套选择**   | `css().xpath()` 或 `xpath().css()` | 链式调用选取嵌套节点                      | `response.css("img").xpath("@src").getall()`                 | `['image1_thumb.jpg', ...]` |

### 3.1.1 构建选择器

响应对象会在 .selector 属性上暴露一个 Selector 实例：

```
>>> response.selector.xpath("//span/text()").get()
'good'
```

使用 XPath 和 CSS 语法查询响应是极为常见的操作，因此响应对象额外提供了两个快捷方法：response.xpath() 和 response.css()：

```
>>> response.xpath("//span/text()").get()
'good'
>>> response.css("span::text").get()
'good'
```

Scrapy 选择器是 Selector 类的实例，可通过传入 TextResponse 对象，或传入字符串形式的标记文本（通过 text 参数）来构建。

通常无需手动构建 Scrapy 选择器：Spider 回调函数中可直接获取 response 对象，因此大多数情况下，使用 response.css() 和 response.xpath() 快捷方法会更便捷。通过 response.selector 或这些快捷方法，还能确保响应体仅被解析一次。

但如果有需要，也可直接使用 Selector 类：

#### 3.1.1.1 从文本构建：

```
>>> from scrapy.selector import Selector
>>> body = "<html><body><span>good</span></body></html>"
>>> Selector(text=body).xpath("//span/text()").get()
'good'
```

#### 3.1.1.2 从响应对象构建（HtmlResponse 是 TextResponse 的子类之一）：

```
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
>>> response = HtmlResponse(url="http://example.com", body=body, encoding="utf-8")
>>> Selector(response=response).xpath("//span/text()").get()
'good'
```

Selector 会根据输入类型自动选择最优的解析规则（XML 或 HTML）。

### 3.1.2 使用选择器

为了说明如何使用选择器，我们将借助 Scrapy shell（一款提供交互式测试功能的工具），并以 Scrapy 文档服务器上的一个示例页面为例：

https://docs.scrapy.org/en/latest/_static/selectors-sample1.html

为保证内容完整，以下是该页面的完整 HTML 代码：

```html
<!DOCTYPE html>

<html>
  <head>
    <base href='http://example.com/' />
    <title>Example website</title>
  </head>
  <body>
    <div id='images'>
      <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' alt='image1'/></a>
      <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' alt='image2'/></a>
      <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' alt='image3'/></a>
      <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' alt='image4'/></a>
      <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' alt='image5'/></a>
    </div>
  </body>
</html>
```

首先，打开 shell

`scrapy shell https://docs.scrapy.org/en/latest/_static/selectors-sample1.html`

然后，待 Shell 加载完成后，你可以通过 `response` 这个 Shell 变量获取响应对象，而响应对象附带的选择器则存储在 `response.selector` 属性中。

由于我们处理的是 HTML 内容，该选择器会自动使用 HTML 解析器。

那么，接下来我们对照该页面的 HTML 代码，编写一个用于选取 `<title>` 标签内文本内容的 XPath 表达式：

```shell
>>> response.xpath("//title/text()")
[<Selector query='//title/text()' data='Example website'>]
```

若要**实际提取文本数据**，你需要调用选择器的 `.get()` 或 `.getall()` 方法，示例如下：

```shell
>>> response.xpath("//title/text()").getall()
['Example website']
>>> response.xpath("//title/text()").get()
'Example website'
```

`.get()` 方法始终返回单个结果：若存在多个匹配项，则返回**第一个匹配项**的内容；若没有匹配项，则返回 `None`。`.getall()` 方法会返回一个包含**所有匹配结果**的列表。

需要注意的是，CSS 选择器可以通过 CSS3 伪元素来选取文本节点或属性节点：

```shell
>>> response.css("title::text").get()
'Example website'
```

可以看到，`.xpath()` 和 `.css()` 方法会返回一个 **`SelectorList` 实例**，该实例本质是由一系列新选择器组成的列表。借助这套 API，我们可以快速选取**嵌套数据**，示例如下：

```shell
>>> response.css("img").xpath("@src").getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

若你只需提取**首个匹配的元素**，可以调用选择器的 `.get()` 方法（或其别名 `.extract_first()`—— 该方法在早期 Scrapy 版本中较为常用）：

```shell
>>> response.xpath('//div[@id="images"]/a/text()').get()
'Name: My image 1 '
```

如果未找到匹配元素，该方法会返回 `None`：

```shell
>>> response.xpath('//div[@id="not-exists"]/text()').get() is None
True
```

你可以传入一个参数作为默认返回值，以此替代 `None`：

```shell
>>> response.xpath('//div[@id="not-exists"]/text()').get(default="not-found")
'not-found'
```

除了使用 `@src` 这类 XPath 语法外，还可以借助选择器的 `.attrib` 属性来查询节点属性：

```shell
>>> [img.attrib["src"] for img in response.css("img")]
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

作为一种快捷用法，`SelectorList` 也可直接调用 `.attrib` 属性；该属性会返回**首个匹配元素**的属性：

```shell
>>> response.css("img").attrib["src"]
'image1_thumb.jpg'
```

该用法在**预期仅能得到单个结果**时最为实用，例如通过 ID 选取元素，或是选取网页中的唯一元素：

```shell
>>> response.css("base").attrib["href"]
'http://example.com/'
```

现在，我们来获取基准 URL 和若干图片链接：

```shell
>>> response.xpath("//base/@href").get()
'http://example.com/'

>>> response.css("base::attr(href)").get()
'http://example.com/'

>>> response.css("base").attrib["href"]
'http://example.com/'

>>> response.xpath('//a[contains(@href, "image")]/@href').getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']

>>> response.css("a[href*=image]::attr(href)").getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']

>>> response.xpath('//a[contains(@href, "image")]/img/@src').getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']

>>> response.css("a[href*=image] img::attr(src)").getall()
['image1_thumb.jpg',
'image2_thumb.jpg',
'image3_thumb.jpg',
'image4_thumb.jpg',
'image5_thumb.jpg']
```

### 3.1.3 CSS 选择器的扩展

按照 W3C 标准，CSS 选择器**不支持**选取文本节点或属性值。但在网页爬取场景中，这类选取操作是必不可少的，因此 Scrapy（依托 parsel 库）实现了两种非标准伪元素：

- 若要选取文本节点，使用 `::text`
- 若要选取属性值，使用 `::attr(name)`，其中 `name` 为你想要获取值的属性名称

> [!Warning]
>
> 这些伪元素是 **Scrapy/parsel 专属的**。它们大概率无法在其他类库（如 `lxml` 或 `PyQuery`）中正常使用。

示例:

`title::text` 用于选取后代 `<title>` 元素的子文本节点：

```shell
>>> response.css("title::text").get()
'Example website'
```

`*::text` 用于选取当前选择器上下文内的**所有后代文本节点**：

```shell
>>> response.css("#images *::text").getall()
['\n   ',
'Name: My image 1 ',
'\n   ',
'Name: My image 2 ',
'\n   ',
'Name: My image 3 ',
'\n   ',
'Name: My image 4 ',
'\n   ',
'Name: My image 5 ',
'\n  ']
```

若 `foo` 元素**存在但不包含任何文本**（即文本内容为空），`foo::text` 将不会返回任何结果。

```shell
>>> response.css("img::text").getall()
[]

This means ``.css('foo::text').get()`` could return None even if an element
exists. Use ``default=''`` if you always want a string:
```

```shell
>>> response.css("img::text").get()
>>> response.css("img::text").get(default="")
''
```

`a::attr(href)` 用于选取后代链接元素的 `href` 属性值。

```shell
>>> response.css("a::attr(href)").getall()
['image1.html',
'image2.html',
'image3.html',
'image4.html',
'image5.html']
```

> [!Note]
>
> 另请参阅：**选取元素属性**

> [!Note]
>
> 这些伪元素**无法进行链式调用**。但在实际应用中，链式调用它们也没有太大意义：文本节点本身不具备属性，而属性值本质已是字符串类型，不存在子节点。

### 3.1.4 选择器嵌套

选择方法（`.xpath()` 或 `.css()`）会返回一个**同类型选择器组成的列表**，因此你也可以对这些选择器调用选择方法。示例如下：

```shell
>>> links = response.xpath('//a[contains(@href, "image")]')
>>> links.getall()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg" alt="image1"></a>',
'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg" alt="image2"></a>',
'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg" alt="image3"></a>',
'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg" alt="image4"></a>',
'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg" alt="image5"></a>']

>>> for index, link in enumerate(links):
... 	href_xpath = link.xpath("@href").get()
... 	img_xpath = link.xpath("img/@src").get()
... 	print(f"Link number {index} points to url {href_xpath!r} and image {img_xpath!r}")

Link number 0 points to url 'image1.html' and image 'image1_thumb.jpg'
Link number 1 points to url 'image2.html' and image 'image2_thumb.jpg'
Link number 2 points to url 'image3.html' and image 'image3_thumb.jpg'
Link number 3 points to url 'image4.html' and image 'image4_thumb.jpg'
Link number 4 points to url 'image5.html' and image 'image5_thumb.jpg'
```

### 3.1.5 选取元素属性

获取属性值有多种方法。首先，可以使用 XPath 语法：

```shell
>>> response.xpath("//a/@href").getall()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

XPath 语法具备几项优势：它是 XPath 的一项标准特性，且 `@属性` 语法可用于 XPath 表达式的其他部分 —— 例如，能够根据属性值进行过滤。

Scrapy 还为 CSS 选择器提供了一种扩展语法（`::attr(...)`），通过该语法可以获取属性值：

```shell
>>> response.css("a::attr(href)").getall()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

除此之外，`Selector` 还提供了 `.attrib` 属性。如果你更倾向于在 Python 代码中直接查询属性（无需使用 XPath 语法或 CSS 扩展语法），则可以使用该属性：

```shell
>>> [a.attrib["href"] for a in response.css("a")]
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

该属性同样可在 `SelectorList` 上调用；它会返回一个包含**首个匹配元素属性**的字典。当你预期选择器仅会返回单个结果时（例如通过元素 ID 选取，或选取网页中的唯一元素时），使用该属性会非常便捷。

```shell
>>> response.css("base").attrib
{'href': 'http://example.com/'}
>>> response.css("base").attrib["href"]
'http://example.com/'
```

空 `SelectorList` 的 `.attrib` 属性为空：

```shell
>>> response.css("foo").attrib
{}
```

### 3.1.6 结合正则表达式使用选择器

选择器还提供了 `.re()` 方法，用于通过正则表达式提取数据。但与 `.xpath()` 或 `.css()` 方法不同的是，`.re()` 会返回字符串列表，因此无法构建嵌套的 `.re()` 调用。

以下是一个示例，用于从上述 HTML 代码中提取图片名称：

```shell
>>> response.xpath('//a[contains(@href, "image")]/text()').re(r"Name:\s*(.*)")
['My image 1 ',
'My image 2 ',
'My image 3 ',
'My image 4 ',
'My image 5 ']
```

`.re()` 方法还配有一个辅助方法 `.re_first()`，它与 `.get()`（及其别名 `.extract_first()`）的作用相对应；使用该方法可仅提取首个匹配的字符串：

```shell
>>> response.xpath('//a[contains(@href, "image")]/text()').re_first(r"Name:\s*(.*)")
'My image 1 '
```

### 3.1.7 extract() 和 extract_first()

如果你是 Scrapy 的长期使用者，大概率已经熟悉选择器的 `.extract()` 和 `.extract_first()` 方法。许多博客文章和教程也在使用这两个方法。Scrapy 目前仍支持这些方法，暂无弃用计划。

不过，Scrapy 的官方使用文档现已改用 `.get()` 和 `.getall()` 方法。我们认为，这些新方法能让代码更简洁、可读性更强。

以下示例将展示这些方法之间的对应关系。

1. `SelectorList.get()` 与 `SelectorList.extract_first()` 的功能完全相同

    ```
    >>> response.css("a::attr(href)").get()
    'image1.html'
    >>> response.css("a::attr(href)").extract_first()
    'image1.html'
    ```

2. `SelectorList.getall()` 与 `SelectorList.extract()` 的功能完全相同

    ```
    >>> response.css("a::attr(href)").getall()
    ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    >>> response.css("a::attr(href)").extract()
    ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
    ```

3. `Selector.get()` 与 `Selector.extract()` 的功能完全相同

    ```
    >>> response.css("a::attr(href)")[0].get()
    'image1.html'
    >>> response.css("a::attr(href)")[0].extract()
    'image1.html'
    ```

4. 为保持一致性，`Selector` 还提供了 `getall()` 方法，该方法会返回一个列表
    ```
    >>> response.css("a::attr(href)")[0].getall()
    ['image1.html']
    ```

因此，两者的核心区别在于，`.get()` 和 `.getall()` 方法的输出结果更具可预测性：`.get()` 始终返回**单个结果**，`.getall()` 始终返回**包含所有提取结果的列表**。而使用 `.extract()` 方法时，返回的结果究竟是列表还是单个值，往往无法直观判断；若要获取单个结果，则需要根据情况调用 `.extract()` 或 `.extract_first()` 方法。

## 3.2 Xpath 语法使用技巧

以下是一些实用技巧，可帮助你在 Scrapy 选择器中高效运用 XPath。如果你目前对 XPath 还不太熟悉，不妨先参考这份 XPath 教程。

> 这些技巧中的一部分源自 **Zyte 博客**上的这篇文章。

### 3.2.1 使用相对 Xpath 表达式

需要注意的是，如果你在嵌套使用选择器时，使用了以 `/` 开头的 XPath 表达式，该 XPath 表达式将基于整个文档（绝对路径）进行匹配，而非相对于调用它的那个选择器（相对路径）。

例如，假设你想要提取所有 `<div>` 元素内部的 `<p>` 元素。首先，你需要先获取所有 `<div>` 元素：

```shell
>>> divs = response.xpath("//div")
```

一开始，你可能会忍不住想用下面这种方法 —— 但这种写法是错误的，因为它实际上会提取**整个文档中所有的 `<p>` 元素**，而非仅提取 `<div>` 元素内部的 `<p>` 元素。

```shell
>>> for p in divs.xpath("//p"):  # this is wrong - gets all <p> from the whole document
...     print(p.get())
... 
```

这才是正确的写法（注意 `//p` 前加了**点号**的 XPath 表达式）

```shell
>>> for p in divs.xpath(".//p"):  # extracts all <p> inside
... 	print(p.get())
...
```

另一种常见的场景是提取所有**直接子元素 `<p>`**：

```shell
>>> for p in divs.xpath("p"):
...     print(p.get())
...
```

有关相对 XPath 表达式的更多细节，请参阅 XPath 规范中的**位置路径**章节。

### 3.2.2 按类查询时，建议使用 CSS 选择器。

由于一个元素可以包含多个 CSS 类，因此使用 XPath 按类选择元素的写法会相当冗长。

```shell
*[contains(concat(' ', normalize-space(@class), ' '), ' someclass ')]
```

示例：

```shell
>>> from scrapy import Selector
>>> text = """<!DOCTYPE html>
... <html lang="en">
... <head>
...     <meta charset="UTF-8">
...     <title>Title</title>
... </head>
... <body>
...     <div class="someclass anotherclass">目标元素</div>
...     <div class="someclassname">不要匹配我</div>
...     <div class="notsomeclass">也不要匹配我</div>
...     <div class="someclass">也要匹配我</div>
...     <div class="anotherclass">同样要匹配我</div>
... </body>
... </html>
... """
>>>
>>> sel = Selector(text=text)
>>> sele.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " someclass ")]').getall()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'sele' is not defined. Did you mean: 'sel'?
>>>
>>>
>>> sel.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " someclass ")]').getall()
['<div class="someclass anotherclass">目标元素</div>', '<div class="someclass">也要匹配我</div>']
```

如果使用 `@class='someclass'` 这种写法，你可能会遗漏那些包含其他类名的元素；而如果为了避免这种遗漏，改用 `contains(@class, 'someclass')` 的写法，又可能会匹配到超出预期的元素 —— 比如那些类名中包含 `someclass` 这个字符串的其他类。

实际使用中，Scrapy 选择器支持链式调用。因此大多数情况下，你可以先用 CSS 选择器按类名完成筛选，再根据需要切换为 XPath 进行后续操作。

```shell
>>> from scrapy import Selector
>>> sel = Selector(
... text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>'
... )
>>> sel.css(".shout").xpath("./time/@datetime").getall()
['2014-07-23 19:00']
```

示例：

```shell
>>> from scrapy import Selector
>>> text = """<!DOCTYPE html>
... <html lang="en">
... <head>
...     <meta charset="UTF-8">
...     <title>Title</title>
... </head>
... <body>
...     <div class="someclass anotherclass">目标元素</div>
...     <div class="someclassname">不要匹配我</div>
...     <div class="notsomeclass">也不要匹配我</div>
...     <div class="someclass">也要匹配我</div>
...     <div class="anotherclass">同样要匹配我</div>
... </body>
... </html>
... """
>>> 
>>> sel = Selector(text=text)
>>> 
>>> 
>>> sel.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " someclass ")]').getall()
['<div class="someclass anotherclass">目标元素</div>', '<div class="someclass">也要匹配我</div>']
>>>
>>> 
>>> sel.css('.someclass').getall() 
['<div class="someclass anotherclass">目标元素</div>', '<div class="someclass">也要匹配我</div>']
```

这种写法比前文提到的那种冗长的 XPath 技巧要简洁得多。只需记住，在后续要编写的 XPath 表达式里加上英文句点（`.`）即可。

### 3.2.3 **注意区分 `//node[1]` 与 `(//node)[1]` 的差异**

`//node[1]` 会选取**每个父节点下排在首位的所有子节点**。

`(//node)[1]` 会先选取**文档中的所有 `node` 节点**，再从中提取出**第一个节点**。

示例：

```shell
>>> from scrapy import Selector
>>> sel = Selector(
...     text="""
...     <ul class="list">
...         <li>1</li>
...         <li>2</li>
...         <li>3</li>
...     </ul>
...     <ul class="list">
...         <li>4</li>
...         <li>5</li>
...         <li>6</li>
...     </ul>"""
... )
>>> xp = lambda x: sel.xpath(x).getall()
```

该表达式会选取**任意父节点下的首个 `<li>` 元素**。

```shell
>>> xp("//li[1]")
['<li>1</li>', '<li>4</li>']
```

而该表达式会选取**整个文档中的首个 `<li>` 元素**:

```shell
>>> xp("//ul/li[1]")
['<li>1</li>', '<li>4</li>']
```

而该表达式会选取**整个文档中所有 `<ul>` 父节点下的首个 `<li>` 元素**。

```shell
>>> xp("(//ul/li)[1]")
['<li>1</li>']
```

### 3.2.4 **在条件判断中使用文本节点**

当你需要将文本内容作为参数传入 XPath 字符串函数时，应避免使用 `.//text()`，转而直接使用 `.`。

这是因为表达式 `.//text()` 会返回一个文本元素的集合 —— 也就是一个**节点集**。而当节点集被转换为字符串时（比如将其传入 `contains()` 或 `starts-with()` 这类字符串函数时，就会触发这种转换），最终只会提取该节点集中**第一个元素的文本内容**。

示例：

```shell
>> from scrapy import Selector
>>> sel = Selector(
...     text='<a href="#">Click here to go to the <strong>Next Page</strong></a>'
... )
```

将节点集转换为字符串：

```shell
>>> sel.xpath("//a//text()").getall()  # take a peek at the node-set
['Click here to go to the ', 'Next Page']
>>> sel.xpath("string(//a[1]//text())").getall()  # convert it to string
['Click here to go to the ']
```

然而，将一个节点转换为字符串时，会拼接该节点本身及其**所有子节点**的文本内容。

```shell
>>> sel.xpath("//a[1]").getall()  # select the first node
['<a href="#">Click here to go to the <strong>Next Page</strong></a>']
>>> sel.xpath("string(//a[1])").getall()  # convert it to string
['Click here to go to the Next Page']
```

因此，在这种情况下，使用 `.//text()` 节点集**无法选中任何内容**。

```shell
>>> sel.xpath("//a[contains(.//text(), 'Next Page')]").getall()
[]
```

而使用 `.` 指代节点的写法，是有效的。

```shell
>>> sel.xpath("//a[contains(., 'Next Page')]").getall()
['<a href="#">Click here to go to the <strong>Next Page</strong></a>']
```

### 3.2.5 Xpath 表达式中的变量

XPath 允许你在表达式中引用变量，语法格式为 `$变量名`。这种用法与 SQL 中的参数化查询或预处理语句有些相似 —— 在 SQL 里，你可以用 `?` 这类占位符替代查询语句中的部分参数，再在执行查询时传入具体值进行替换。

以下是一个示例，展示如何根据元素的 `id` 属性值匹配元素，且无需硬编码该属性值（此前的示例采用的是硬编码方式）：

```shell
>>> # `$val` used in the expression, a `val` argument needs to be passed
>>> response.xpath("//div[@id=$val]/a/text()", val="images").get()
'Name: My image 1 '
```

这是另一个示例：查找包含 5 个 `<a>` 子元素的 `<div>` 标签的 `id` 属性（此处我们将数值 5 以整数形式传入）：

```shell
>>> response.xpath("//div[count(a)=$cnt]/@id", cnt=5).get()
'images'
```

调用 `.xpath()` 方法时，所有变量引用都必须绑定对应的值（否则会抛出 `ValueError: XPath error: exception` 异常）。只需传入所需数量的命名参数即可完成变量绑定。

为 Scrapy 选择器提供底层支持的 [`parsel`]([Parsel — Parsel 1.10.0 documentation](https://parsel.readthedocs.io/en/latest/)) 库，在其文档中包含了更多关于 XPath 变量的细节说明与使用示例。

### 3.2.6 移除命名空间

在处理爬虫项目时，将命名空间完全移除、仅通过元素名编写 XPath 表达式往往会便捷得多，能让 XPath 写法更简洁 / 易用。你可以使用 `Selector.remove_namespaces()` 方法来实现这一操作。

下面我们以 Python Insider 博客的 Atom 订阅源为例，演示该方法的使用。

首先，我们打开 Scrapy 交互式终端，并传入想要爬取的目标 URL：

```shell
scrapy shell https://feeds.feedburner.com/PythonInsider
```

文件开头是这样的：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ...
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
      xmlns:blogger="http://schemas.google.com/blogger/2008"
      xmlns:georss="http://www.georss.org/georss"
      xmlns:gd="http://schemas.google.com/g/2005"
      xmlns:thr="http://purl.org/syndication/thread/1.0"
      xmlns:feedburner="http://rssnamespace.org/feedburner/ext/1.0">
  ...
```

你会看到多个命名空间声明，其中包括一个默认的命名空间 `http://www.w3.org/2005/Atom`，以及另一个以 `gd:` 为前缀、指向 `http://schemas.google.com/g/2005` 的命名空间。

进入交互式终端后，我们尝试选取所有 `<link>` 元素，会发现这一操作无法生效（原因是 Atom XML 命名空间对这些节点进行了 “隐藏”，导致无法直接匹配）：

```shell
>>> response.xpath("//link")
[]
```

但一旦我们调用 `Selector.remove_namespaces()` 方法，所有节点就都可以直接通过节点名来访问了：

```shell
>>> response.selector.remove_namespaces()
>>> response.xpath("//link")
[<Selector query='//link' data='<link rel="alternate" type="text/html" h'>,
    <Selector query='//link' data='<link rel="next" type="application/atom+'>,
    ...
```

如果你疑惑为什么**命名空间移除操作**没有默认自动执行，而是需要手动调用，原因有两点，按重要性排序如下：

1. 移除命名空间需要遍历并修改文档中的所有节点。对于 Scrapy 爬取的所有文档来说，默认执行这个操作的开销相当大。
2. 某些场景下**命名空间的使用是必需的**—— 比如不同命名空间下存在同名元素时。不过这类情况十分少见。

### 3.2.7 使用 EXSLT 扩展

 Scrapy 选择器基于 `lxml` 构建，因此支持部分 EXSLT 扩展，并且内置了这些预注册的命名空间，可直接在 XPath 表达式中使用：

| prefix | namespace                            | usage                                                     |
| ------ | ------------------------------------ | --------------------------------------------------------- |
| re     | http://exslt.org/regular-expressions | [regular expressions](http://exslt.org/regexp/index.html) |
| set    | http://exslt.org/sets                | [set manipulation](http://exslt.org/set/index.html)       |

#### 3.2.7.1 正则表达式

例如，当 XPath 的 `starts-with()` 或 `contains()` 函数不足以满足需求时，`test()` 函数会被证明是相当实用的。

示例：选取列表项中 “class” 属性值以数字结尾的链接元素：

```shell
>>> from scrapy import Selector
>>> doc = """
... <div>
...     <ul>
...         <li class="item-0"><a href="link1.html">first item</a></li>
...         <li class="item-1"><a href="link2.html">second item</a></li>
...         <li class="item-inactive"><a href="link3.html">third item</a></li>
...         <li class="item-1"><a href="link4.html">fourth item</a></li>
...         <li class="item-0"><a href="link5.html">fifth item</a></li>
...     </ul>
... </div>
... """
>>> sel = Selector(text=doc, type="html")
>>> sel.xpath("//li//@href").getall()
['link1.html', 'link2.html', 'link3.html', 'link4.html', 'link5.html']
>>> sel.xpath('//li[re:test(@class, "item-\d$")]//@href').getall()
['link1.html', 'link2.html', 'link4.html', 'link5.html']
```

> [!Warning]
>
> C 语言库 libxslt **本身并不原生支持** EXSLT 正则表达式，因此 lxml 库的实现方案是通过**钩子函数**调用 Python 的 `re` 模块。基于这一机制，在 XPath 表达式中使用正则表达式相关函数时，可能会产生一定的**性能损耗**。

#### 3.2.7.2 集合运算

这类操作十分实用，例如在提取文本元素前，可用于排除文档树中的部分内容。

示例：提取包含多组 `itemscope` 及对应 `itemprop` 的微数据（示例内容摘自 https://schema.org/Product）：

```shell
>>> doc = """
... <div itemscope itemtype="http://schema.org/Product">
...   <span itemprop="name">Kenmore White 17" Microwave</span>
...   <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
...   <div itemprop="aggregateRating"
...     itemscope itemtype="http://schema.org/AggregateRating">
...    Rated <span itemprop="ratingValue">3.5</span>/5
...    based on <span itemprop="reviewCount">11</span> customer reviews
...   </div>
...   <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
...     <span itemprop="price">$55.00</span>
...     <link itemprop="availability" href="http://schema.org/InStock" />In stock
...   </div>
...   Product description:
...   <span itemprop="description">0.7 cubic feet countertop microwave.
...   Has six preset cooking categories and convenience features like
...   Add-A-Minute and Child Lock.</span>
...   Customer reviews:
...   <div itemprop="review" itemscope itemtype="http://schema.org/Review">
...     <span itemprop="name">Not a happy camper</span> -
...     by <span itemprop="author">Ellie</span>,
...     <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
...     <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
...       <meta itemprop="worstRating" content = "1">
...       <span itemprop="ratingValue">1</span>/
...       <span itemprop="bestRating">5</span>stars
...     </div>
...     <span itemprop="description">The lamp burned out and now I have to replace
...     it. </span>
...   </div>
...   <div itemprop="review" itemscope itemtype="http://schema.org/Review">
...     <span itemprop="name">Value purchase</span> -
...     by <span itemprop="author">Lucas</span>,
...     <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
...     <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
...       <meta itemprop="worstRating" content = "1"/>
...       <span itemprop="ratingValue">4</span>/
...       <span itemprop="bestRating">5</span>stars
...     </div>
...     <span itemprop="description">Great microwave for the price. It is small and
...     fits in my apartment.</span>
...   </div>
...   ...
... </div>
... """
>>> sel = Selector(text=doc, type="html")
>>> for scope in sel.xpath("//div[@itemscope]"):
...     print("current scope:", scope.xpath("@itemtype").getall())
...     props = scope.xpath(
...        """
...                 set:difference(./descendant::*/@itemprop,
...                                .//*[@itemscope]/*/@itemprop)"""
...     )
...     print(f"    properties: {props.getall()}")
...     print("")


current scope: ['http://schema.org/Product']
    properties: ['name', 'aggregateRating', 'offers', 'description', 'review', 'review']

current scope: ['http://schema.org/AggregateRating']
    properties: ['ratingValue', 'reviewCount']

current scope: ['http://schema.org/Offer']
    properties: ['price', 'availability']

current scope: ['http://schema.org/Review']
    properties: ['name', 'author', 'datePublished', 'reviewRating', 'description']

current scope: ['http://schema.org/Rating']
    properties: ['worstRating', 'ratingValue', 'bestRating']

current scope: ['http://schema.org/Review']
    properties: ['name', 'author', 'datePublished', 'reviewRating', 'description']

current scope: ['http://schema.org/Rating']
    properties: ['worstRating', 'ratingValue', 'bestRating']
```

在这里，我们首先遍历所有 `itemscope` 元素，然后针对每个 `itemscope` 元素，查找其下所有的 `itemprop` 元素，并**排除那些本身嵌套在另一个 `itemscope` 元素内部**的 `itemprop` 元素。

### 3.2.8 其他 XPath 扩展

Scrapy 选择器还提供了一个极为实用的 XPath 扩展函数 has-class，该函数会对包含所有指定 HTML 类名的节点返回布尔值 True。
以下是对应的 HTML 示例：

```shell
>>> from scrapy.http import HtmlResponse
>>> response = HtmlResponse(
...     url="http://example.com",
...     body="""
... <html>
...     <body>
...         <p class="foo bar-baz">First</p>
...         <p class="foo">Second</p>
...         <p class="bar">Third</p>
...         <p>Fourth</p>
...     </body>
... </html>
... """,
...     encoding="utf-8",
... )
```

你可以像这样使用它：

```shell
>>> response.xpath('//p[has-class("foo")]')
[<Selector query='//p[has-class("foo")]' data='<p class="foo bar-baz">First</p>'>,
<Selector query='//p[has-class("foo")]' data='<p class="foo">Second</p>'>]
>>> response.xpath('//p[has-class("foo", "bar-baz")]')
[<Selector query='//p[has-class("foo", "bar-baz")]' data='<p class="foo bar-baz">First</p>'>]
>>> response.xpath('//p[has-class("foo", "bar")]')
[]
```

因此，XPath 表达式 `//p[has-class("foo", "bar-baz")]` 大致等价于 CSS 选择器 `p.foo.bar-baz`。**请注意**，该 XPath 表达式在大多数情况下运行速度会更慢 —— 因为 `has-class` 是一个纯 Python 函数，需要对每个目标节点逐一调用；而 CSS 选择器在底层会被转换为原生 XPath 执行，运行效率更高。因此，从性能角度来看，`has-class` 的适用场景仅限于那些难以用 CSS 选择器直接描述的情况。

Parsel 库还通过 `set_xpathfunc()` 方法，简化了自定义 XPath 扩展函数的添加流程。

## 3.3 内置选择器参考文档

### 3.3.1 Selector objects

#### 3.3.1.1 `scrapy.Selector(*args: Any, **kwargs: Any)`

选择器（Selector）的实例是对响应（response）的一层封装，用于选取响应内容中的特定部分。

`response` 是一个 **HtmlResponse** 或 **XmlResponse** 对象，用于数据的选取与提取操作。

当无法获取 `response` 对象时，可传入 `text` 参数，其值可以是 Unicode 字符串或 UTF-8 编码的文本。**注意**：同时传入 `text` 和 `response` 会导致未定义行为。

`type` 参数用于指定选择器类型，可选值为 `"html"`、`"xml"`、`"json"` 或 `None`（默认值）。

若 `type` 为 `None`，选择器会根据 `response` 的类型自动选择最优的解析类型（详见下文）；若搭配 `text` 参数使用，则默认采用 `"html"` 类型。

若 `type` 为 `None` 且已传入 `response` 对象，选择器类型将按如下规则从 `response` 类型中推导：

- 若为 **HtmlResponse** 类型 → 解析类型为 `"html"`
- 若为 **XmlResponse** 类型 → 解析类型为 `"xml"`
- 若为 **TextResponse** 类型 → 解析类型为 `"json"`
- 其他类型 → 解析类型为 `"html"`

反之，若显式设置了 `type` 参数，则会强制使用该解析类型，不再进行自动检测。

- `xpath(query: str, namespace: Mapping[str, str] | None = None, **kwargs: Any) -> SelectorList[_SelectorType]`

    查找与 XPath 查询匹配的节点，并将结果以 **SelectorList 实例**的形式返回，其中所有元素均已被扁平化处理。该列表中的元素同样实现了 **Selector 接口**。

    `query` 是一个字符串，内含待执行的 XPath 查询语句。

    `namespaces` 是一个可选的**前缀 - 命名空间 URI 映射字典**，用于为那些通过 `register_namespace(prefix, uri)` 注册的前缀补充额外命名空间。与 `register_namespace()` 不同的是，这些前缀不会被保存，供后续调用使用。

    你还可以传入其他任意命名参数，为 XPath 表达式中的 XPath 变量赋值，例如：

    ```python
    selector.xpath('//a[href=$url]', url="http://www.example.com")
    ```

    > **注意**
    >
    > 为方便使用，该方法也可直接通过 `response.xpath()` 调用。

- `css(query: str) -> SelectorList[_SelectorType]`

    应用指定的 CSS 选择器，并返回一个 **SelectorList 实例**。

    `query` 是一个字符串，内含待执行的 CSS 选择器语句。

    底层实现上，CSS 查询语句会通过 **cssselect 库**转换为 XPath 查询语句，随后调用 `.xpath()` 方法执行。

    > **注意**
    >
    > 为方便使用，该方法也可直接通过 `response.css()` 调用。

- `jmespath(query: str,**kwargs: Any) → SelectorList[_SelectorType]`

    查找与 **JMESPath 查询语句**匹配的对象，并将结果以 **SelectorList 实例**的形式返回，其中所有元素均已做扁平化处理。该列表中的元素同样实现了 **Selector 接口**。

    `query` 是一个字符串，内含待执行的 JMESPath 查询语句。

    所有额外传入的命名参数，都会被传递至底层的 `jmespath.search` 调用中，例如：

    ```python
    selector.jmespath('author.name', options=jmespath.Options(dict_cls=collections.OrderedDict))
    ```

    > **注意**
    >
    > 为方便使用，该方法也可直接通过 `response.jmespath()` 调用。

- `get() -> Any`

    对于 HTML 和 XML 类型的数据，返回结果始终为字符串格式，且经过百分号编码的内容会被解码还原。

    > 另请参阅：
    >
    > `extract()` 方法与 `extract_first()` 方法

- `attrib`

    返回底层元素的属性字典。

    另请参阅：**选择元素属性**

- `re(regex: str | Pattern[str], replace_entities: bool = True) -> List[str]`

    应用指定的正则表达式，并返回包含所有匹配结果的字符串列表。

    `regex` 参数可以是一个已编译的正则表达式对象，也可以是一个字符串（该字符串会通过 `re.compile(regex)` 编译为正则表达式对象）。

    默认情况下，字符实体引用会被替换为对应的字符（`&` 和 `<` 除外）。将 `replace_entities` 参数设为 `False` 可关闭此类替换操作。

- `re_first(regex: str | Pattern[str], default: None = None, replace_entities: bool = True) -> str | None`

    `re_first(regex: str | Pattern[str], default: str, replace_entities: bool = True) -> str`

    应用指定的正则表达式，并返回第一个匹配到的字符串。若未找到匹配项，则返回默认值（若未传入该参数，默认值为 None）。

    默认情况下，字符实体引用会被替换为对应的字符（`&` 和 `<` 除外）。将 `replace_entities` 参数设为 `False` 可关闭此类替换操作。

- `register_namespace(prefix: str, uri: str) -> None`

    为当前选择器注册指定的命名空间。**若未注册命名空间，将无法从非标准命名空间中选取或提取数据**。详情请参见 XML 响应对应的选择器示例。

- `remove_space() -> None`

    移除所有命名空间，从而允许使用**无命名空间的 XPath 表达式**遍历文档。详情请参见《移除命名空间》章节。

- `__bool__() -> bool`

    若选择器匹配到了有效内容，则返回 `True`；反之则返回 `False`。换句话说，**选择器的布尔值由其匹配到的内容决定**。

- `getall() -> List[str]`

    将匹配到的节点序列化，并以**单元素字符串列表**的形式返回。

    该方法是为了保证接口一致性而添加到 `Selector` 中的；它在 `SelectorList` 上的实用性更强。另请参阅：`extract()` 方法与 `extract_first()` 方法。

### 3.3.2 SelectorList objects

#### 3.3.2.1 `class scrapy.selector.SelectorList(iterable=(), /)`

`SelectorList` 类是 Python 内置 `list` 类的子类，它提供了若干额外的方法。

------

`xpath(xpath: str, namespaces: Mapping[str, str] | None = None, **kwargs: Any) → SelectorList[_SelectorType]`〔源代码〕

对当前列表中的**每一个元素**调用 `.xpath()` 方法，并将所有结果做扁平化处理，返回一个新的 `SelectorList` 对象。

- `xpath` 参数的作用与 `Selector.xpath()` 方法中的同名参数完全一致。

- `namespaces` 是一个可选的**前缀 - 命名空间 URI 映射字典**，用于为通过 `register_namespace(prefix, uri)` 注册的前缀补充额外命名空间。与 `register_namespace()` 方法不同的是，此处传入的前缀不会被保存，无法用于后续调用。

- 你可以传入任意额外的命名参数，为 XPath 表达式中的变量赋值，例如：

    ```python
    selector.xpath('//a[href=$url]', url="http://www.example.com")
    ```

`css(query: str) → SelectorList[_SelectorType]`

对当前列表中的**每一个元素**调用 `.css()` 方法，并将所有结果做扁平化处理，返回一个新的 `SelectorList` 对象。

- `query` 参数的作用与 `Selector.css()` 方法中的同名参数完全一致。

`jmespath(query: str, **kwargs: Any) → SelectorList[_SelectorType]`〔源代码〕

对当前列表中的**每一个元素**调用 `.jmespath()` 方法，并将所有结果做扁平化处理，返回一个新的 `SelectorList` 对象。

- `query` 参数的作用与 `Selector.jmespath()` 方法中的同名参数完全一致。

- 所有额外传入的命名参数，都会被传递至底层的

    ```
    jmespath.search
    ```

    调用中，例如：

    ```python
    selector.jmespath('author.name', options=jmespath.Options(dict_cls=collections.OrderedDict))
    ```

`getall() → List[str]`〔源代码〕

对当前列表中的**每一个元素**调用 `.get()` 方法，并将所有结果做扁平化处理，返回一个字符串列表。

另请参阅：`extract()` 方法与 `extract_first()` 方法。

`get(default: None = None) → str | None`

`get(default: str) → str`

返回当前列表**第一个元素**调用 `.get()` 方法的结果。若列表为空，则返回指定的默认值。

另请参阅：`extract()` 方法与 `extract_first()` 方法。

`re(regex: str | Pattern[str], replace_entities: bool = True) → List[str]`〔源代码〕

对当前列表中的**每一个元素**调用 `.re()` 方法，并将所有结果做扁平化处理，返回一个字符串列表。

默认情况下，字符实体引用会被替换为对应的字符（`&` 和 `<` 除外）。将 `replace_entities` 参数设为 `False` 即可关闭此类替换操作。

`re_first(regex: str | Pattern[str], default: None = None, replace_entities: bool = True) → str | None`〔源代码〕

`re_first(regex: str | Pattern[str], default: str, replace_entities: bool = True) → str`

对当前列表**第一个元素**调用 `.re()` 方法，并返回字符串格式的结果。若列表为空，或正则表达式未匹配到任何内容，则返回指定的默认值（若未传入该参数，默认值为 `None`）。

默认情况下，字符实体引用会被替换为对应的字符（`&` 和 `<` 除外）。将 `replace_entities` 参数设为 `False` 即可关闭此类替换操作。

`attrib`

返回当前列表**第一个元素**的属性字典。若列表为空，则返回一个空字典。

另请参阅：**选择元素属性**章节。

## 3.4 示例

### 3.4.1 HTML 响应的选择器示例

以下是一些选择器示例，用于阐释相关概念。在所有示例中，我们均假定已通过一个 `HtmlResponse` 对象实例化了一个选择器，代码如下：

```python
sel = Selector(html_response)
```

从 HTML 响应体中选取所有 `<h1>` 元素，返回一个由选择器对象组成的列表（即一个 `SelectorList` 对象）：

```python
sel.xpath("//h1")
```

从 HTML 响应体中提取所有 `<h1>` 元素的文本内容，返回一个字符串列表：

```python
sel.xpath("//h1").getall()  # 该写法的结果包含 h1 标签
sel.xpath("//h1/text()").getall()  # 该写法的结果不包含 h1 标签
```

遍历所有 `<p>` 标签并打印其 `class` 属性：

```python
for node in sel.xpath("//p"):
    print(node.attrib["class"])
```

### 3.4.2 XML 响应的选择器示例

以下是一些示例，用于阐释通过 `XmlResponse` 对象实例化的选择器对象相关概念：

```python
sel = Selector(xml_response)
```

从 XML 响应体中选取所有 `<product>` 元素，返回一个由选择器对象组成的列表（即一个 `SelectorList` 对象）：

python

```python
sel.xpath("//product")
```

从 Google Base XML 数据提要中提取所有价格信息（该操作需要注册命名空间）：

```python
sel.register_namespace("g", "http://base.google.com/ns/1.0")
sel.xpath("//g:price").getall()
```

# 4 Items

网页爬虫的核心目标是**从非结构化数据源（通常为网页）中提取结构化数据**。爬虫可将提取到的数据封装为 `Item`（项目）对象返回，这是一种用于定义键值对的 Python 对象。

Scrapy 支持**多种类型的 `Item` 对象**。创建 `Item` 时，你可以选用任意一种类型；而在编写接收 `Item` 的代码时，则应保证代码对**所有 `Item` 类型都能兼容运行**。

## 4.1 Item Types

Scrapy 通过 **itemadapter** 库支持以下几种 Item 类型：字典（`dict`）、`Item` 对象、数据类（`dataclass`）对象以及 `attrs` 对象。

### 4.1.1 字典

作为一种 Item 类型，字典使用起来既便捷又易于上手。

### 4.1.2 Item 对象

`Item` 提供了类字典（dict-like）的编程接口，同时还具备一些额外功能，这使其成为**功能最完善的 Item 类型**，具体特性如下：

#### 4.1.2.1 `scrapy.Item(*args: Any, **kwargs: Any)`

所有 scrapied Item 的基类。

在 Scrapy 中，若一个对象受 `itemadapter` 库支持，则会被认定为 “爬取项（Item）”。例如，当解析爬虫回调函数的输出结果时，仅有这类对象会被传递至**项目管道（Item Pipeline）**。`Item` 是 `itemadapter` 库默认支持的类之一。

爬取项必须声明 `Field` 类型的属性，这些属性会被处理并存储在 `fields` 属性中。这一机制**限制了允许使用的字段名范围**，可有效避免拼写错误 —— 当引用未定义的字段时，会触发 `KeyError` 异常。此外，字段可用于定义元数据，并控制数据在框架内部的处理方式。更多信息请参阅关于字段（Field）的官方文档。

与字典（`dict`）实例不同，`Item` 实例可被追踪，便于调试内存泄漏问题。

------

`copy() → Self`

`deepcopy() → Self`

返回当前爬取项的深度拷贝（`deepcopy()`）对象。

------

`fields: dict[str, Field] = {}`

一个字典，包含当前 `Item` 中**所有已声明的字段**（而非仅已赋值的字段）。字典的键为字段名，值为 `Item` 声明时使用的 `Field` 对象。

`Item` 对象复刻了标准字典（`dict`）的编程接口（API），包括其 `__init__` 初始化方法。

`Item` 支持定义字段名，这带来以下特性：

1. 当使用未定义的字段名时，会触发 `KeyError` 异常（即避免拼写错误被忽略）；
2. 即使首个爬取到的对象并未包含所有字段的值，`Item` 导出器也能默认导出全部字段；
3. `Item` 还支持定义字段元数据，可用于自定义序列化逻辑。

`trackref` 模块会追踪 `Item` 对象，助力排查内存泄漏问题（详见《使用 trackref 调试内存泄漏》章节）。

**示例代码**：

```python
from scrapy.item import Item, Field


class CustomItem(Item):
    one_field = Field()
    another_field = Field()
```

### 4.1.3 Dataclass 对象

新增于 2.2 版本。

`dataclass()` 支持定义包含字段名的爬取项（Item）类，因此即便首个爬取到的对象并未包含所有字段的值，Item 导出器也能默认导出全部字段。

此外，基于数据类（dataclass）的爬取项还支持你实现以下操作：

1. 为每个已定义的字段指定类型和默认值；
2. 通过 `dataclasses.field()` 定义自定义字段元数据，该元数据可用于自定义序列化逻辑。

**示例代码**：

```python
from dataclasses import dataclass


@dataclass
class CustomItem:
    one_field: str
    another_field: int
```

> **注意**
>
> 字段类型不会在运行时强制执行。

### 4.1.4 attr.s 对象

新增于 2.2 版本。

`attr.s()` 支持定义包含字段名的爬取项（Item）类，因此即便首个爬取到的对象并未包含所有字段的值，Item 导出器也能默认导出全部字段。

此外，基于 `attr.s()` 定义的爬取项还支持：

1. 为每个已定义的字段指定类型和默认值；
2. 定义自定义字段元数据，该元数据可用于自定义序列化逻辑。

使用此类型的爬取项，需先安装 `attrs` 包。

```python
import attr


@attr.s
class CustomItem:
    one_field = attr.ib()
    another_field = attr.ib()
```

## 4.2 Items 使用技巧

### 4.2.1 声明 Item 子类

Item 子类可通过简洁的类定义语法结合 `Field` 对象来声明。以下是一个示例：

```python
import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
```

> [!Note]
>
> 熟悉 Django 的开发者会发现，Scrapy Item 的声明方式与 Django 模型（Model）十分相似，不同之处在于 **Scrapy Item 要简单得多**—— 它并没有 “不同字段类型” 这一概念。

### 4.2.2 声明字段

`Field` 对象用于为每个字段指定元数据。例如，前文示例中为 `last_updated` 字段配置的序列化函数，就是元数据的一种应用。

你可以为每个字段指定**任意类型的元数据**。`Field` 对象对接收的值没有任何限制，正因如此，也不存在一份包含所有可用元数据键的参考清单。`Field` 对象中定义的每一个键，都可能被不同的组件调用，且只有这些组件知晓其具体用途。你也可以根据自身需求，在项目中定义和使用其他任何自定义的 `Field` 键。`Field` 对象的核心作用，是提供**一个集中定义所有字段元数据的统一入口**。通常，那些行为会随字段不同而变化的组件，会通过特定的字段键来配置自身逻辑。你需要查阅对应组件的文档，了解它们各自会使用哪些元数据键。

需要重点注意的是：用于声明 Item 的 `Field` 对象，**不会被保留为类属性**。相反，你需要通过 `fields` 属性来访问这些 `Field` 对象。

`class scrapy.Field`

字段元数据容器

`Field` 类只是一个内置 `dict` 类的别名，它不提供任何额外的功能或属性。换句话说， `Field` 对象是普通的 Python 字典。使用单独的类来支持基于类属性的 Items 声明语法。

> [!Note]
>
> 字段元数据也可以为 `dataclass` 和 `attrs` 项目声明。请参阅 dataclasses.field 和 attr.ib 的文档以获取更多信息。

### 4.2.3 使用 Item 对象

这里有一些使用上述声明的 `Product` 项目的常见任务示例。您会注意到 API 与 `dict` API 非常相似。

#### 4.2.3.1 创建项目

```shell
>>> product = Product(name="Desktop PC", price=1000)
>>> print(product)
Product(name='Desktop PC', price=1000)
```

#### 4.2.3.2 获取字段值

```shell
>>> product["name"]
Desktop PC
>>> product.get("name")
Desktop PC

>>> product["price"]
1000

>>> product["last_updated"]
Traceback (most recent call last):
    ...
KeyError: 'last_updated'

>>> product.get("last_updated", "not set")
not set

>>> product["lala"]  # getting unknown field
Traceback (most recent call last):
    ...
KeyError: 'lala'

>>> product.get("lala", "unknown field")
'unknown field'

>>> "name" in product  # is name field populated?
True

>>> "last_updated" in product  # is last_updated populated?
False

>>> "last_updated" in product.fields  # is last_updated a declared field?
True

>>> "lala" in product.fields  # is lala a declared field?
False
```

#### 4.2.3.3 设置字段值

```shell
>>> product["last_updated"] = "today"
>>> product["last_updated"]
today

>>> product["lala"] = "test"  # setting unknown field
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

#### 4.2.3.4 访问所有已填充的值

要访问所有已填充的值，只需使用常规的 `dict` API：

```python
>>> product.keys()
['price', 'name']

>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]
```

#### 4.2.3.5 复制项目

要复制一个项目，你必须首先决定你想进行浅复制还是深复制。

如果你的项目包含像列表或字典这样的可变值，浅拷贝将保留所有不同副本中对相同可变值的引用。

例如，如果你有一个包含标签列表的项目，如果你对这个项目进行浅复制，那么原始项目和复制后的项目将拥有相同的标签列表。向其中一个项目的列表中添加标签也会将标签添加到另一个项目中。

如果这不是期望的行为，请使用深度复制。

有关更多信息，请参见 `copy` 。

要创建一个项目的浅拷贝，你可以对现有项目调用 `copy()` （ `product2 = product.copy()` ），或者从现有项目实例化你的项目类（ `product2 = Product(product)` ）。

要创建深度副本，请调用 `deepcopy()` 而不是 `product2 = product.deepcopy()` 。

#### 4.2.3.6 其他常见任务

从项目创建字典：

```python
>>> dict(product)  # create a dict from all populated values
{'price': 1000, 'name': 'Desktop PC'}

Creating items from dicts:

>>> Product({"name": "Laptop PC", "price": 1500})
Product(price=1500, name='Laptop PC')

>>> Product({"name": "Laptop PC", "lala": 1500})  # warning: unknown field in dict
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

## 4.3 扩展 Item 子类

您可以通过声明您的原始 Item 的子类来扩展 Items（以添加更多字段或更改某些字段的元数据）。

例如：

```python
class DiscountedProduct(Product):
    discount_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()
```

您还可以通过使用先前的字段元数据并附加更多值或更改现有值来扩展字段元数据，如下所示：

```python
class SpecificProduct(Product):
    name = scrapy.Field(Product.fields["name"], serializer=my_serializer)
```

这添加（或替换）了 `name` 字段的 `serializer` 元数据键，同时保留了所有先前存在的元数据值。

## 4.4 支持的所有 Item 类型

在接收项目的代码中，例如项目管道方法或蜘蛛中间件，使用 `ItemAdapter` 类编写适用于任何支持的项目类型的代码是一种良好的实践。

## 4.5 与 Item 相关的其他类

`class scrapy.item.ItemMeta(class_name: str, bases: tuple[type, ...], attrs: dict[str, Any])`

处理字段定义的 `Item` 的元类。

# 5 Item 加载器

Item Loaders 提供了一种方便的机制来填充抓取的项目。尽管项目可以直接填充，但 Item Loaders 通过在分配之前自动执行一些常见任务（如解析原始提取数据）来提供一种更方便的 API，用于从抓取过程中填充它们。

换句话说，项目提供了抓取数据的容器，而项目加载器提供了填充该容器的机制。

项目加载器旨在提供一种灵活、高效且易于扩展和覆盖不同字段解析规则的方法，无论是通过爬虫，还是通过源格式（HTML、XML 等），而不会成为维护噩梦。

> [!Note]
>
> 项目加载器是 itemloaders 库的扩展，通过添加对响应的支持，使其更易于与 Scrapy 一起使用。

## 5.1 使用项目加载器填充项目

要使用 Item Loader，您必须首先实例化它。您可以使用一个 item 对象来实例化它，或者不使用，在这种情况下，Item Loader 的 `__init__` 方法将使用 `ItemLoader.default_item_class` 属性中指定的 item 类自动创建一个 item 对象。

然后，您开始将值收集到 Item Loader 中，通常使用选择器。您可以将多个值添加到同一个 item 字段；Item Loader 将知道稍后使用适当的处理函数来“连接”这些值。

> [!Note]
>
> 收集的数据在内部作为列表存储，允许将多个值添加到同一个字段。如果创建 loader 时传递了 `item` 参数，如果它已经是可迭代的，则每个 item 的值将保持原样存储；如果是单个值，则将其包装在列表中。

以下是在爬虫中典型使用 Item Loader 的示例，使用在 Items 章节中声明的 Product item：

```python
from scrapy.loader import ItemLoader
from myproject.items import Product


def parse(self, response):
    l = ItemLoader(item=Product(), response=response)
    l.add_xpath("name", '//div[@class="product_name"]')
    l.add_xpath("name", '//div[@class="product_title"]')
    l.add_xpath("price", '//p[@id="price"]')
    l.add_css("stock", "p#stock")
    l.add_value("last_updated", "today")  # you can also use literal values
    return l.load_item()
```

通过快速查看那段代码，我们可以看到 `name` 字段是从页面中的两个不同的 XPath 位置提取的：

1. `//div[@class="product_name"]`
2. `//div[@class="product_title"]`

换句话说，数据是通过使用 `add_xpath()` 方法从两个 XPath 位置提取来收集的。这是稍后将被分配给 `name` 字段的数据。

之后，对于 `price` 和 `stock` 字段（后者使用 `add_css()` 方法配合 CSS 选择器），使用了类似的调用，最后直接使用不同的方法 `add_value()` 将 `last_update` 字段填充为字面值（ `today` ）。

最后，当所有数据收集完毕后，调用 `ItemLoader.load_item()` 方法，该方法实际上返回包含先前通过 `add_xpath()` 、 `add_css()` 和 `add_value()` 调用提取和收集的数据的条目。

## 5.2 使用 dataclass Items

默认情况下，创建数据类项时需要传递所有字段。在使用数据类项与项目加载器时，这可能会成为一个问题：除非向加载器传递一个预填充的项目，否则字段将使用加载器的 `add_xpath()` 、 `add_css()` 和 `add_value()` 方法逐步填充。

一种解决方法是通过使用 `field()` 函数并带有 `default` 参数来定义项目：

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InventoryItem:
    name: Optional[str] = field(default=None)
    price: Optional[float] = field(default=None)
    stock: Optional[int] = field(default=None)
```

## 5.3 输入和输出处理器

`Item Loader`（项目加载器）会为每个 **（项目）字段 ** 分别配备一个输入处理器和一个输出处理器。输入处理器会在接收到提取的数据后（通过`add_xpath()`、`add_css()`或`add_value()`方法传入）立即进行处理，处理结果会被收集并存储在`ItemLoader`内部。待所有数据收集完毕后，调用`ItemLoader.load_item()`方法来填充并获取已填充的项目对象，此时输出处理器才会被调用，处理的数据源是此前收集的、经过输入处理器处理的数据。输出处理器的最终处理结果，将作为该字段的最终值被赋予项目对象。

下面通过一个示例，说明特定字段的输入与输出处理器是如何被调用的（该逻辑适用于所有其他字段）：

```python
l = ItemLoader(Product(), some_selector)
l.add_xpath("name", xpath1)  # (1)
l.add_xpath("name", xpath2)  # (2)
l.add_css("name", css)       # (3)
l.add_value("name", "test")  # (4)
return l.load_item()         # (5)
```

具体执行流程如下：

1. 从`xpath1`中提取数据，传入`name`字段的输入处理器进行处理，处理结果被收集并存储在`Item Loader`中（此时尚未赋值给项目对象）。
2. 从`xpath2`中提取数据，传入步骤 (1) 中使用的同一个输入处理器处理，处理结果会追加到步骤 (1) 收集的数据之后（若步骤 (1) 有数据）。
3. 此步骤与前两步逻辑类似，区别在于数据是从`css`选择器中提取，同样传入步骤 (1)、(2) 使用的输入处理器处理，处理结果追加到步骤 (1)、(2) 收集的数据之后（若有数据）。
4. 此步骤与前几步逻辑也类似，区别在于待收集的值是直接指定的，而非从 XPath 表达式或 CSS 选择器中提取，但该值仍会经过输入处理器处理。需要注意的是，由于输入处理器要求接收的参数必须是可迭代对象，若传入的值不可迭代，会先被转换为仅包含单个元素的可迭代对象，再传入输入处理器。
5. 将步骤 (1)、(2)、(3)、(4) 收集的所有数据，传入`name`字段的输出处理器处理，最终处理结果即为项目对象中`name`字段的赋值。

需要注意的是，**处理器本质上是可调用对象**：它们接收待解析的数据作为参数，返回解析后的值。因此，你可以将任意函数用作输入或输出处理器，唯一的要求是：该函数必须且只能接收一个位置参数，且该参数的类型必须是可迭代对象。

> [!note]
>
> 输入处理器与输出处理器都必须以**可迭代对象**作为其第一个参数。这些函数的输出可以是任意类型的数据。输入处理器的处理结果会被追加至加载器内部的一个列表中，该列表用于存储（对应字段的）已收集数据。输出处理器的处理结果则会作为最终值，被赋予对应的项目字段。

你还需要记住的另一点是：**输入处理器返回的值会被加载器内部收集并存放在列表中**，之后再传递给输出处理器，用于填充对应的字段。

最后同样重要的是，为了方便使用，`itemloaders` 内置了一些**常用的处理器**。

## 5.4 声明 Item Loaders

Item Loader 采用类定义的语法进行声明。以下是一个示例：

```python
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.title)
    name_out = Join()

    price_in = MapCompose(str.strip)

    # ...
```

正如你所见，输入处理器通过 **`_in`后缀**来声明，而输出处理器则通过**`_out`后缀**来声明。此外，你还可以通过`ItemLoader.default_input_processor`和`ItemLoader.default_output_processor`这两个属性，来声明**默认的输入 / 输出处理器 **。

## 5.5 声明输入和输出处理器

正如上一节所述，输入处理器与输出处理器可以在**项目加载器（Item Loader）的定义中声明**，而且这种声明输入处理器的方式十分常用。除此之外，还有一处可以指定要使用的输入 / 输出处理器，即**项目字段（Item Field）的元数据**中。以下是一个示例：

```python
import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def filter_price(value):
    if value.isdigit():
        return value


class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_price),
        output_processor=TakeFirst(),
    )
```

```shell
>>> from scrapy.loader import ItemLoader
>>> il = ItemLoader(item=Product())
>>> il.add_value("name", ["Welcome to my", "<strong>website</strong>"])
>>> il.add_value("price", ["&euro;", "<span>1000</span>"])
>>> il.load_item()
{'name': 'Welcome to my website', 'price': '1000'}
```

对于输入处理器和输出处理器，其优先级顺序如下：

1. **项目加载器（Item Loader）的字段专属属性**：`field_in` 和 `field_out`（优先级最高）
2. **字段元数据**：`input_processor` 和 `output_processor` 关键字
3. **项目加载器默认配置**：`ItemLoader.default_input_processor()` 和 `ItemLoader.default_output_processor()`（优先级最低）

另见：**复用与扩展项目加载器**

## 5.6 Item Loaders 上下文

**项目加载器上下文**（Item Loader Context）是一个存储任意键值对的字典，可供项目加载器内所有的输入处理器和输出处理器共享。你可以在**声明**、**实例化**或**使用**项目加载器时传入该上下文。它的作用是用来调整输入 / 输出处理器的行为。

例如，假设你有一个名为 `parse_length` 的函数，该函数接收一个文本值并从中提取长度信息：

```python
def parse_length(text, loader_context):
    unit = loader_context.get("unit", "m")
    # ... length parsing code goes here ...
    return parsed_length
```

该函数通过接收 `loader_context` 参数，明确告知项目加载器（Item Loader）自身能够接收项目加载器上下文。因此，项目加载器在调用该函数时会传入当前生效的上下文，而处理器函数（本例中为 `parse_length`）便可利用这些上下文信息。

修改项目加载器上下文值有以下几种方式：

1. 修改当前生效的项目加载器上下文（通过 `context` 属性）：
   ```python
   loader = ItemLoader(product)
   loader.context["unit"] = "cm"
   ```

2. 在项目加载器实例化时传入（项目加载器 `__init__` 方法的关键字参数会被存入上下文）：
   ```python
   loader = ItemLoader(product, unit="cm")
   ```

3. 在项目加载器声明时指定（适用于那些支持通过项目加载器上下文实例化的输入 / 输出处理器，`MapCompose` 便是其中之一）：
   ```python
   class ProductLoader(ItemLoader):
       length_out = MapCompose(parse_length, unit="cm")
   ```

## 5.7 ItemLoader 对象

### 5.7.1 `class scrapy.loader.ItemLoader`

```python
class scrapy.loader.ItemLoader(
    item: Any = None, 
    selector: Selector | None = None,
	response: TextResponse | None = None,
    parent: itemloaders.ItemLoader | None = None,
    **context: Any
)
```

一种便于用户使用的抽象组件，它通过对抓取的数据应用字段处理器，来完成数据项的填充工作。当传入选择器（Selector）或响应对象（Response）进行实例化时，该组件支持借助选择器从网页中提取数据。

#### 5.7.1.1 **参数说明**

- **item** (scrapy.item.Item)：待填充的数据项实例，后续可通过调用 `add_xpath()`、`add_css()` 或 `add_value()` 方法为其填充数据。
- **selector** (选择器对象)：数据提取的目标选择器，调用 `add_xpath()`、`add_css()`、`replace_xpath()` 或 `replace_css()` 方法时会用到该参数。
- **response** (响应对象)：若未传入 `selector` 参数，则会通过 `default_selector_class` 基于此响应对象构建选择器；若已传入 `selector` 参数，此参数将被忽略。

若未传入 `item` 参数，系统会自动调用 `default_item_class` 中指定的类来实例化一个数据项。

`item`、`selector`、`response` 以及其余的关键字参数，都会被存入加载器上下文（可通过 `context` 属性访问）。

#### 5.7.1.2 **属性说明**

- item
  当前由该项目加载器处理的数据项对象。该属性多作为只读属性使用，因此若你尝试修改其值，建议先查看 `default_item_class` 的相关配置。

- context
  当前生效的项目加载器上下文。

- default_item_class
  数据项类（或工厂类），当 `__init__` 方法未传入 `item` 参数时，将使用此类来实例化数据项。

- default_input_processor
  默认输入处理器，适用于所有未单独指定输入处理器的字段。

- default_output_processor
  默认输出处理器，适用于所有未单独指定输出处理器的字段。

- default_selector_class
  选择器构建类，当 `__init__` 方法仅传入 `response` 参数时，将使用此类来构建项目加载器的选择器。若 `__init__` 方法已传入 `selector` 参数，该属性将被忽略。此属性常被子类重写。

- selector
  数据提取所用的选择器对象。该对象的来源有两种：一是 `__init__` 方法传入的选择器；二是当未传入选择器时，基于 `response` 参数和 `default_selector_class` 构建的选择器。**该属性为只读属性**。\

`add_css(field_name: str | None, css: str | Iterable[str], *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `ItemLoader.add_value()` 类似，但接收 CSS 选择器而非直接值，该选择器用于从当前 ItemLoader 关联的选择器中提取 unicode 字符串列表。

更多关键字参数说明见 `get_css()`。

**参数**：

- css (str) – 用于提取数据的 CSS 选择器

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

**示例**：

```python
# HTML 片段: <p class="product-name">Color TV</p>
loader.add_css('name', 'p.product-name')
# HTML 片段: <p id="price">the price is $1200</p>
loader.add_css('price', 'p#price', re='the price is (.*)')
```

`add_jmes(field_name: str | None, jmes: str, *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `ItemLoader.add_value()` 类似，但接收 JMESPath 选择器而非直接值，该选择器用于从当前 ItemLoader 关联的选择器中提取 unicode 字符串列表。

更多关键字参数说明见 `get_jmes()`。

**参数**：

- jmes (str) – 用于提取数据的 JMESPath 选择器

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

**示例**：

```python
# 数据片段: {"name": "Color TV"}
loader.add_jmes('name', 'name')
# 数据片段: {"price": "the price is $1200"}
loader.add_jmes('price', 'price', TakeFirst(), re='the price is (.*)')
```

> 注：原示例存在语法错误（字符串未闭合），已修正；且补充了缺失的 jmes 路径参数，符合实际使用逻辑。

`add_value(field_name: str | None, value: Any, *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

对指定字段的给定值进行处理后添加至字段数据中。

处理流程：先将值传入 `get_value()`（结合指定的处理器和关键字参数），再传入该字段的输入处理器，处理结果追加到该字段已收集的数据中。若字段已有收集数据，新数据会被追加。

若传入的 `field_name` 为 None，则可同时为多个字段添加值，此时处理后的 value 需为字典（键为字段名，值为对应字段值）。

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

**示例**：

```python
loader.add_value('name', 'Color TV')
loader.add_value('colours', ['white', 'blue'])
loader.add_value('length', '100')
loader.add_value('name', 'name: foo', TakeFirst(), re='name: (.+)')
loader.add_value(None, {'name': 'foo', 'sex': 'male'})
```

`add_xpath(field_name: str | None, xpath: str | Iterable[str], *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `ItemLoader.add_value()` 类似，但接收 XPath 表达式而非直接值，该表达式用于从当前 ItemLoader 关联的选择器中提取字符串列表。

更多关键字参数说明见 `get_xpath()`。

**参数**：

- xpath (str) – 用于提取数据的 XPath 表达式

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

**示例**：

```python
# HTML 片段: <p class="product-name">Color TV</p>
loader.add_xpath('name', '//p[@class="product-name"]')
# HTML 片段: <p id="price">the price is $1200</p>
loader.add_xpath('price', '//p[@id="price"]', re='the price is (.*)')
```

`get_collected_values(field_name: str)→ List[Any]`

返回指定字段已收集的所有原始值（未经过输出处理器处理）。

`get_css(css: str | Iterable[str], *processors: Callable[[...], Any], re: str | Pattern[str] | None = None, **kw: Any)→ Any`

功能与 `ItemLoader.get_value()` 类似，但接收 CSS 选择器而非直接值，该选择器用于从当前 ItemLoader 关联的选择器中提取 unicode 字符串列表。

**参数**：

- css (str) – 用于提取数据的 CSS 选择器
- re (str 或 Pattern [str]) – 正则表达式，用于从选中的 CSS 区域中提取数据

**示例**：

```python
# HTML 片段: <p class="product-name">Color TV</p>
loader.get_css('p.product-name')
# HTML 片段: <p id="price">the price is $1200</p>
loader.get_css('p#price', TakeFirst(), re='the price is (.*)')
```

`get_jmes(jmes: str | Iterable[str], *processors: Callable[[...], Any], re: str | Pattern[str] | None = None, **kw: Any)→ Any`

功能与 `ItemLoader.get_value()` 类似，但接收 JMESPath 选择器而非直接值，该选择器用于从当前 ItemLoader 关联的选择器中提取 unicode 字符串列表。

**参数**：

- jmes (str) – 用于提取数据的 JMESPath 选择器
- re (str 或 Pattern) – 正则表达式，用于从选中的 JMESPath 结果中提取数据

**示例**：

```python
# 数据片段: {"name": "Color TV"}
loader.get_jmes('name')
# 数据片段: {"price": "the price is $1200"}
loader.get_jmes('price', TakeFirst(), re='the price is (.*)')
```

> 注：原示例存在语法错误（字符串未闭合），已修正。

get_output_value(field_name: str)→ Any[source]

返回指定字段已收集的值经输出处理器解析后的结果。该方法**不会**填充或修改 item 对象。

get_value(value: Any, *processors: Callable[[...], Any], re: str | Pattern[str] | None = None, **kw: Any)→ Any[source]

使用指定的处理器和关键字参数处理给定值。

**可用关键字参数**：

- re (str 或 Pattern [str]) – 正则表达式，会在处理器执行前通过 `extract_regex()` 方法从给定值中提取数据

**示例**：

```python
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst
loader = ItemLoader()
loader.get_value('name: foo', TakeFirst(), str.upper, re='name: (.+)')
# 输出: 'FOO'
```

get_xpath(xpath: str | Iterable[str], *processors: Callable[[...], Any], re: str | Pattern[str] | None = None, **kw: Any)→ Any[source]

功能与 `ItemLoader.get_value()` 类似，但接收 XPath 表达式而非直接值，该表达式用于从当前 ItemLoader 关联的选择器中提取 unicode 字符串列表。

**参数**：

- xpath (str) – 用于提取数据的 XPath 表达式
- re (str 或 Pattern [str]) – 正则表达式，用于从选中的 XPath 区域中提取数据

**示例**：

```python
# HTML 片段: <p class="product-name">Color TV</p>
loader.get_xpath('//p[@class="product-name"]')
# HTML 片段: <p id="price">the price is $1200</p>
loader.get_xpath('//p[@id="price"]', TakeFirst(), re='the price is (.*)')
```

`load_item()→ Any`

使用已收集的所有数据填充 item 对象并返回该对象。收集的数据会先经过输出处理器处理，最终结果将赋值给 item 的各个字段。

`nested_css(css: str, **context: Any)→ Self`

基于 CSS 选择器创建嵌套加载器。传入的选择器会相对于当前 ItemLoader 关联的选择器执行。嵌套加载器与父级 ItemLoader 共享同一个 item 对象，因此调用 `add_xpath()`、`add_value()`、`replace_value()` 等方法时行为与预期一致。

`nested_xpath(xpath: str, **context: Any)→ Self`

基于 XPath 表达式创建嵌套加载器。传入的 XPath 会相对于当前 ItemLoader 关联的选择器执行。嵌套加载器与父级 ItemLoader 共享同一个 item 对象，因此调用 `add_xpath()`、`add_value()`、`replace_value()` 等方法时行为与预期一致。

`replace_css(field_name: str | None, css: str | Iterable[str], *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `add_css()` 类似，但会替换字段已收集的数据（而非追加）。

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

`replace_jmes(field_name: str | None, jmes: str | Iterable[str], *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `add_jmes()` 类似，但会替换字段已收集的数据（而非追加）。

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

`replace_value(field_name: str | None, value: Any, *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `add_value()` 类似，但会用新值替换字段已收集的数据（而非追加）。

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

`replace_xpath(field_name: str | None, xpath: str | Iterable[str], *processors: Callable[..., Any], re: str | Pattern[str] | None = None, **kw: Any)→ Self`

功能与 `add_xpath()` 类似，但会替换字段已收集的数据（而非追加）。

**返回值**：当前 ItemLoader 实例（支持方法链式调用）。

**返回类型**：ItemLoader

## 5.8 嵌套加载器

当需要从文档的一个子区域中解析相关联的数据时，创建嵌套加载器会非常实用。假设你要从页面的页脚部分提取详情信息，该页脚的结构如下：

**示例：**

```
<footer>
    <a class="social" href="https://facebook.com/whatever">Like Us</a>
    <a class="social" href="https://twitter.com/whatever">Follow Us</a>
    <a class="email" href="mailto:whatever@example.com">Email Us</a>
</footer>
```

如果不使用嵌套加载器，你需要为每一个想要提取的值指定**完整的 XPath（或 CSS 选择器）**。

**示例：**

```python
loader = ItemLoader(item=Item())
# load stuff not in the footer
loader.add_xpath("social", '//footer/a[@class = "social"]/@href')
loader.add_xpath("email", '//footer/a[@class = "email"]/@href')
loader.load_item()
```

反之，你可以**基于页脚选择器创建一个嵌套加载器**，并添加**相对于页脚的数值**。功能完全保持一致，但可以避免重复编写页脚选择器的代码。

**示例：**

```python
loader = ItemLoader(item=Item())
# load stuff not in the footer
footer_loader = loader.nested_xpath("//footer")
footer_loader.add_xpath("social", 'a[@class = "social"]/@href')
footer_loader.add_xpath("email", 'a[@class = "email"]/@href')
# no need to call footer_loader.load_item()
loader.load_item()
```

你可以**任意嵌套加载器**，这些加载器可同时兼容 XPath 或 CSS 选择器。一个通用的使用原则是：当嵌套加载器能让代码更简洁时再使用它，但**不要过度嵌套**，否则会导致解析器的可读性变差。

## 5.9 复用与扩展 Item Loaders

随着项目规模不断扩大、爬虫数量日益增多，**维护工作会逐渐成为核心难题**。尤其是当你需要为每个爬虫编写大量差异化的解析规则、处理诸多异常情况，同时又希望复用通用处理器时，这个问题会更加突出。

项目加载器（Item Loader）的设计初衷，就是在不损失灵活性的前提下，**减轻解析规则的维护负担**，同时提供便捷的机制来扩展和重写这些规则。正因如此，项目加载器支持通过 Python 传统的类继承机制，来适配特定爬虫（或爬虫分组）的差异化需求。

举个例子，假设某网站的产品名称被三层连字符包裹（例如 `---等离子电视---`），而你不希望最终抓取的产品名称中包含这些连字符。

你可以通过**复用并扩展默认的产品项目加载器（ProductLoader）**，来移除这些连字符，具体实现方式如下：

```python
from itemloaders.processors import MapCompose
from myproject.ItemLoaders import ProductLoader


def strip_dashes(x):
    return x.strip("-")


class SiteSpecificLoader(ProductLoader):
    name_in = MapCompose(strip_dashes, ProductLoader.name_in)
```

另一种能体现**扩展项目加载器**优势的场景是：当你需要处理**多种数据源格式**（例如 XML 和 HTML）时。在处理 XML 格式的数据时，你可能需要移除其中的 CDATA 标记。具体实现示例如下：

```python
from itemloaders.processors import MapCompose
from myproject.ItemLoaders import ProductLoader
from myproject.utils.xml import remove_cdata


class XmlProductLoader(ProductLoader):
    name_in = MapCompose(remove_cdata, ProductLoader.name_in)
```

这就是**扩展输入处理器的典型方式**。

至于输出处理器，更常见的做法是在**字段元数据中声明**它们。因为输出处理器通常只依赖于字段本身，而不像输入处理器那样，需要适配每个特定网站的解析规则。另见：《声明输入与输出处理器》。

扩展、继承和重写项目加载器的方式还有很多种，不同的项目加载器层级结构，可能更适合不同的项目。Scrapy 仅提供实现这一功能的机制，并不会强制你采用某种特定的加载器组织方式 —— 具体如何设计，完全取决于你和项目的实际需求。

# 6 Scrapy Shell

Scrapy Shell 是一个交互式终端，你可以在其中快速尝试和调试爬虫代码，无需运行整个爬虫程序。它主要用于测试数据提取代码，但本质上也是一个标准的 Python 终端，因此也可用于测试任意代码。

该终端常用于测试 XPath 或 CSS 表达式：验证表达式的执行效果，以及它们能从目标网页中提取到哪些数据。在编写爬虫的过程中，你可以交互式地测试这些表达式，无需每次修改后都运行爬虫来验证。

一旦熟悉 Scrapy Shell 的使用方式，你会发现它是开发和调试爬虫时**不可或缺的工具**。

## 6.1 配置 Shell

如果你安装了 IPython，Scrapy Shell 会优先使用 IPython（而非标准 Python 控制台）。IPython 控制台功能更强大，提供智能自动补全、彩色输出等特性。

我们强烈建议你安装 IPython，尤其是在 Unix 系统下（IPython 在该系统中表现更佳）。更多信息可参考《IPython 安装指南》。

Scrapy 也支持 bpython，当系统中未安装 IPython 时，会尝试使用 bpython。

无论系统中安装了哪些终端工具，你都可以通过 Scrapy 的配置，指定使用 ipython、bpython 或标准 python 终端中的任意一种。配置方式有两种：

1. 设置 `SCRAPY_PYTHON_SHELL` 环境变量；

2. 在 `scrapy.cfg` 配置文件中定义：
   ```ini
   [settings]
   shell = bpython
   ```

## 6.2 启动 Shell

你可以通过 `shell` 命令启动 Scrapy Shell，格式如下：

```bash
scrapy shell <url>
```

其中 `<url>` 是你想要爬取的网址。

Shell 同样支持本地文件。如果你想调试某个网页的本地副本，这个功能会非常实用。Shell 支持以下本地文件路径语法：

```bash
# UNIX 风格路径
scrapy shell ./path/to/file.html
scrapy shell ../other/path/to/file.html
scrapy shell /absolute/path/to/file.html

# File URI 格式
scrapy shell file:///absolute/path/to/file.html
```

> [!Note]
>
> 使用相对文件路径时，务必显式添加 `./` 前缀（或根据需要添加 `../`）。`scrapy shell index.html` 并不会按预期执行（这是设计如此，并非 Bug）。
>
> 由于 Shell 优先处理 HTTP URL 而非 File URI，而 `index.html` 在语法上与域名（如 `example.com`）相似，因此 Shell 会将 `index.html` 当作域名处理，从而触发 DNS 查找错误：
>
> ```bash
> $ scrapy shell index.html
> [ ... scrapy shell 启动中 ... ]
> [ ... 回溯信息 ... ]
> twisted.internet.error.DNSLookupError: DNS lookup failed:
> address 'index.html' not found: [Errno -5] No address associated with hostname.
> ```
>
> Shell 不会预先检查当前目录下是否存在名为 `index.html` 的文件。再次强调，请务必显式指定路径。

## 6.3 使用 Shell

Scrapy Shell 本质上是一个标准的 Python 控制台（若安装了 IPython 则为 IPython 控制台），仅额外提供了一些便捷的快捷函数。

## 6.4 可用快捷函数

- `shelp()` - 打印帮助信息，列出所有可用的对象和快捷函数
- `fetch(url[, redirect=True])` - 从指定 URL 获取新的响应，并更新所有相关对象。可通过传入 `redirect=False` 选择不跟随 HTTP 3xx 重定向
- `fetch(request)` - 从指定 Request 对象获取新的响应，并更新所有相关对象
- `view(response)` - 在本地浏览器中打开指定响应，便于检查。该函数会在响应体中添加 `<base>` 标签，确保外部链接（如图片、样式表）能正常显示。但需注意，此操作会在本地创建一个临时文件，且不会自动删除。

## 6.5 可用的 Scrapy 对象

Scrapy Shell 会自动从下载的页面创建一些便捷对象，例如 Response 对象和 Selector 对象（适用于 HTML 和 XML 内容）。

这些对象包括：

- `crawler` - 当前的 Crawler 对象
- `spider` - 已知可处理该 URL 的 Spider 对象；若未找到适配当前 URL 的爬虫，则返回一个基础 Spider 对象
- `request` - 最后一次获取页面的 Request 对象。你可以使用 `replace()` 方法修改该请求，或通过 `fetch` 快捷函数获取新请求（无需退出 Shell）
- `response` - 包含最后一次获取页面的 Response 对象
- `settings` - 当前的 Scrapy 配置（Settings）对象

## 6.6 Shell 会话示例

以下是一个典型的 Shell 会话示例：先爬取 `https://scrapy.org` 页面，再爬取 `https://old.reddit.com/` 页面；接着将（Reddit 的）请求方法修改为 POST 并重新获取，最终得到错误响应；最后通过按下 Ctrl-D（Unix 系统）或 Ctrl-Z（Windows 系统）结束会话。

请注意，你实际测试时提取的数据可能与示例不同 —— 这些页面并非静态页面，内容可能已发生变化。本示例仅用于帮助你熟悉 Scrapy Shell 的使用方式。

### 6.6.1 步骤 1：启动 Shell

```bash
scrapy shell 'https://scrapy.org' --nolog
```

> **注意**在命令行运行 Scrapy Shell 时，务必将 URL 用引号包裹。否则，包含参数的 URL（即含 `&` 字符的 URL）将无法正常工作。
>
> Windows 系统需使用双引号：
>
> ```bash
> scrapy shell "https://scrapy.org" --nolog
> ```

### 6.6.2 步骤 2：Shell 加载 URL 并输出可用对象

Shell 会通过 Scrapy 下载器获取指定 URL，并打印可用对象和实用快捷函数列表（这些行均以 `[s]` 前缀开头）：

```plaintext
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f07395dd690>
[s]   item       {}
[s]   request    <GET https://scrapy.org>
[s]   response   <200 https://scrapy.org/>
[s]   settings   <scrapy.settings.Settings object at 0x7f07395dd710>
[s]   spider     <DefaultSpider 'default' at 0x7f0735891690>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser

>>>
```

### 6.6.3 步骤 3：操作对象

```python
# 提取页面标题
response.xpath("//title/text()").get()
'Scrapy | A Fast and Powerful Scraping and Web Crawling Framework'

# 获取 Reddit 旧版页面
fetch("https://old.reddit.com/")

# 再次提取标题
response.xpath("//title/text()").get()
'reddit: the front page of the internet'

# 修改请求方法为 POST
request = request.replace(method="POST")

# 重新发起请求
fetch(request)

# 查看响应状态码
response.status
404

# 打印响应头信息
from pprint import pprint
pprint(response.headers)
{'Accept-Ranges': ['bytes'],
'Cache-Control': ['max-age=0, must-revalidate'],
'Content-Type': ['text/html; charset=UTF-8'],
'Date': ['Thu, 08 Dec 2016 16:21:19 GMT'],
'Server': ['snooserv'],
'Set-Cookie': ['loid=KqNLou0V9SKMX4qb4n; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loidcreated=2016-12-08T16%3A21%3A19.445Z; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loid=vi0ZVe4NkxNWdlH7r7; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure',
                'loidcreated=2016-12-08T16%3A21%3A19.459Z; Domain=reddit.com; Max-Age=63071999; Path=/; expires=Sat, 08-Dec-2018 16:21:19 GMT; secure'],
'Vary': ['accept-encoding'],
'Via': ['1.1 varnish'],
'X-Cache': ['MISS'],
'X-Cache-Hits': ['0'],
'X-Content-Type-Options': ['nosniff'],
'X-Frame-Options': ['SAMEORIGIN'],
'X-Moose': ['majestic'],
'X-Served-By': ['cache-cdg8730-CDG'],
'X-Timer': ['S1481214079.394283,VS0,VE159'],
'X-Ua-Compatible': ['IE=edge'],
'X-Xss-Protection': ['1; mode=block']}
```

## 6.7 从爬虫中调用 Shell 检查响应

有时你需要检查爬虫某个处理节点的响应，仅为确认预期的响应是否正常到达。

这一需求可通过 `scrapy.shell.inspect_response` 函数实现。

以下是在爬虫中调用该函数的示例：

```python
import scrapy

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net",
    ]

    def parse(self, response):
        # 仅检查特定响应
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        # 剩余解析逻辑
```

运行该爬虫时，你会看到类似如下的输出：

```plaintext
2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.com> (referer: None)
2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.org> (referer: None)
[s] Available Scrapy objects:
[s]   crawler    <scrapy.crawler.Crawler object at 0x1e16b50>
...

>>> response.url
'http://example.org'
```

随后你可以验证数据提取代码是否生效：

```python
response.xpath('//h1[@class="fn"]')
[]
```

显然未提取到数据。此时你可以在浏览器中打开响应，确认是否是预期的页面：

```python
view(response)
True
```

最后按下 Ctrl-D（或 Windows 系统的 Ctrl-Z）退出 Shell，爬虫会继续执行：

```plaintext
^D
2014-01-23 17:50:03-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.net> (referer: None)
...
```

> [!Note]
>
> 此处无法使用 `fetch` 快捷函数 —— 因为 Scrapy 引擎已被 Shell 阻塞。但退出 Shell 后，爬虫会从暂停处继续执行，如上所示。

# 7 Item Pipeline

当爬虫抓取到一个项目（Item）后，该项目会被发送至项目管道（Item Pipeline），并由管道中的多个组件按顺序依次处理。

每个项目管道组件（有时也简称为 “项目管道”）都是一个实现了简单方法的 Python 类。这些组件接收项目对象并对其执行特定操作，同时决定该项目是继续沿管道传递，还是被丢弃（不再进行后续处理）。

项目管道的典型用途包括：

- 清理 HTML 数据
- 验证抓取的数据（检查项目是否包含特定字段）
- 检查重复项（并丢弃重复的项目）
- 将抓取的项目存储到数据库中

## 7.1 编写自定义项目管道

每个项目管道组件都必须实现以下方法：

### 7.1.1 process_item(self, item, spider)

该方法会为每个项目管道组件调用。`item` 是一个项目对象（详见《支持所有项目类型》）。

`process_item()` 方法必须执行以下操作之一：返回一个项目对象、返回一个 Deferred 对象，或抛出 `DropItem` 异常。被丢弃的项目将不再被后续管道组件处理。

**参数**：

- item（项目对象）：被抓取的项目
- spider（爬虫对象）：抓取该项目的爬虫

此外，管道组件还可选择性实现以下方法：

### 7.1.2 open_spider(self, spider)

该方法在爬虫启动时调用。

**参数**：

- spider（爬虫对象）：启动的爬虫

### 7.1.3 close_spider(self, spider)

该方法在爬虫关闭时调用。

**参数**：

- spider（爬虫对象）：关闭的爬虫

## 7.2 项目管道示例

### 7.2.1 价格验证并丢弃无价格的项目

以下是一个示例管道：它会为不含增值税的项目（带有 `price_excludes_vat` 属性）调整 `price` 字段值，并丢弃不含价格的项目：

```python
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PricePipeline:
    vat_factor = 1.15  # 增值税系数

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("price"):  # 检查是否存在价格字段
            if adapter.get("price_excludes_vat"):  # 检查是否不含增值税
                adapter["price"] = adapter["price"] * self.vat_factor  # 计算含增值税价格
            return item  # 返回处理后的项目
        else:
            raise DropItem("Missing price")  # 抛出异常，丢弃无价格的项目
```

### 7.2.2 将项目写入 JSON 行文件

以下管道会将所有抓取的项目（来自所有爬虫）存储到单个 `items.jsonl` 文件中，每行存储一个以 JSON 格式序列化的项目：

```python
import json

from itemadapter import ItemAdapter


class JsonWriterPipeline:
    def open_spider(self, spider):
        # 爬虫启动时打开文件，写入模式
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        # 爬虫关闭时关闭文件
        self.file.close()

    def process_item(self, item, spider):
        # 将项目转为字典并序列化为 JSON 字符串，添加换行符
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)  # 写入文件
        return item  # 返回项目继续传递
```

> **注意**
>
> `JsonWriterPipeline` 仅用于演示如何编写项目管道。如果需要将抓取的项目存储为 JSON 文件，建议使用 Scrapy 内置的「Feed 导出」功能。

### 7.2.3 将项目写入 MongoDB

本示例展示如何使用 `pymongo` 将项目写入 MongoDB。MongoDB 的地址和数据库名在 Scrapy 配置中指定，集合名称与项目类名一致。

该示例的核心是演示如何获取爬虫对象，以及如何正确释放资源。

```python
import pymongo
from itemadapter import ItemAdapter


class MongoPipeline:
    collection_name = "scrapy_items"  # MongoDB 集合名

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri  # MongoDB 连接地址
        self.mongo_db = mongo_db    # MongoDB 数据库名

    @classmethod
    def from_crawler(cls, crawler):
        # 从爬虫配置中获取 MongoDB 连接信息
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),  # 默认为 items 库
        )

    def open_spider(self, spider):
        # 爬虫启动时建立 MongoDB 连接
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 爬虫关闭时关闭 MongoDB 连接
        self.client.close()

    def process_item(self, item, spider):
        # 将项目插入 MongoDB 集合
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
```

### 7.2.4 为项目生成截图

本示例演示如何在 `process_item()` 方法中使用协程语法。

该管道会向本地运行的 Splash 实例发起请求，渲染项目 URL 的截图。请求响应下载完成后，管道将截图保存到文件，并将文件名添加到项目中。

```python
import hashlib
from pathlib import Path
from urllib.parse import quote

import scrapy
from itemadapter import ItemAdapter
from scrapy.http.request import NO_CALLBACK
from scrapy.utils.defer import maybe_deferred_to_future


class ScreenshotPipeline:
    """使用 Splash 为每个 Scrapy 项目生成截图的管道"""

    SPLASH_URL = "http://localhost:8050/render.png?url={}"  # Splash 截图接口

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        encoded_item_url = quote(adapter["url"])  # 对 URL 进行编码
        screenshot_url = self.SPLASH_URL.format(encoded_item_url)  # 拼接截图请求 URL
        
        # 构建请求（无回调函数）
        request = scrapy.Request(screenshot_url, callback=NO_CALLBACK)
        # 异步下载响应
        response = await maybe_deferred_to_future(
            spider.crawler.engine.download(request)
        )

        if response.status != 200:  # 响应状态码非 200，直接返回项目
            return item

        # 将截图保存到文件，文件名使用 URL 的 MD5 哈希值
        url = adapter["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = f"{url_hash}.png"
        Path(filename).write_bytes(response.body)

        # 将文件名存入项目
        adapter["screenshot_filename"] = filename
        return item
```

### 7.2.5 重复项过滤器

该过滤器用于检测重复项目，并丢弃已处理过的项目。假设我们的项目包含唯一 ID，但爬虫会返回多个相同 ID 的项目：

```python
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()  # 存储已处理的项目 ID

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:  # 检查 ID 是否已存在
            raise DropItem(f"Item ID already seen: {adapter['id']}")  # 丢弃重复项
        else:
            self.ids_seen.add(adapter["id"])  # 记录新 ID
            return item  # 返回项目继续传递
```

## 7.3 激活项目管道组件

要激活项目管道组件，需将其类添加到 `ITEM_PIPELINES` 配置中，示例如下：

```python
ITEM_PIPELINES = {
    "myproject.pipelines.PricePipeline": 300,
    "myproject.pipelines.JsonWriterPipeline": 800,
}
```

配置中为类分配的整数值决定了管道的执行顺序：项目会从数值较小的组件流向数值较大的组件。通常将这些数值定义在 0-1000 范围内。

# 8 数据导出

在实现爬虫时最常需要的功能之一是能够正确地存储爬取到的数据，通常这意味着生成一个包含爬取到的数据的“导出文件”（通常称为“导出 Feed”），以供其他系统消费。

Scrapy 通过 Feed Exports 开箱即用地提供了此功能，它允许您使用多种序列化格式和存储后端生成包含爬取到的 Item 的 Feed。

本页提供了所有 Feed 导出功能的详细文档。如果您正在寻找分步指南，请查看 [Zyte 的导出指南](https://docs.zyte.com/web-scraping/guides/export/index.html#exporting-scraped-data)。

## 8.1 序列化格式[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#serialization-formats)

为了序列化爬取到的数据，Feed Exports 使用 [Item 导出器](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#topics-exporters)。以下格式开箱即用

- [JSON](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-format-json)
- [JSON lines](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-format-jsonlines)
- [CSV](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-format-csv)
- [XML](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-format-xml)

但您也可以通过 [`FEED_EXPORTERS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORTERS) 设置扩展支持的格式。

### JSON[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#json)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`json`
- 使用的导出器：[`JsonItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.JsonItemExporter)
- 如果您将 JSON 用于大型 Feed，请参阅 [此警告](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#json-with-large-data)。



### JSON lines[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#json-lines)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`jsonlines`
- 使用的导出器：[`JsonLinesItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.JsonLinesItemExporter)



### CSV[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#csv)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`csv`
- 使用的导出器：[`CsvItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.CsvItemExporter)
- 要指定要导出的列、它们的顺序及其列名，请使用 [`FEED_EXPORT_FIELDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_FIELDS)。其他 Feed 导出器也可以使用此选项，但这对于 CSV 很重要，因为与许多其他导出格式不同，CSV 使用固定的头部。



### XML[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#xml)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`xml`
- 使用的导出器：[`XmlItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.XmlItemExporter)



### Pickle[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#pickle)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`pickle`
- 使用的导出器：[`PickleItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.PickleItemExporter)



### Marshal[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#marshal)

- 在 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中的 `format` 键的值：`marshal`
- 使用的导出器：[`MarshalItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.MarshalItemExporter)

## 8.2 存储后端[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#storages)

在使用 Feed Exports 时，您可以通过 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置定义使用一个或多个 [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) 存储 Feed 的位置。Feed Exports 支持多种存储后端类型，这些类型由 URI Scheme 定义。

开箱即用的存储后端包括

- [本地文件系统](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-fs)
- [FTP](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-ftp)
- [S3](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)（需要 [boto3](https://github.com/boto/boto3)）
- [Google Cloud Storage (GCS)](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-gcs)（需要 [google-cloud-storage](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)）
- [标准输出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-stdout)

如果所需的外部库不可用，某些存储后端可能无法使用。例如，仅当安装了 [boto3](https://github.com/boto/boto3) 库时，S3 后端才可用。

## 8.3 存储 URI 参数[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#storage-uri-parameters)

存储 URI 还可以包含在创建 Feed 时会被替换的参数。这些参数包括

- `%(time)s` - 在创建 Feed 时被替换为时间戳
- `%(name)s` - 被替换为爬虫名称

任何其他命名参数都会被同名的爬虫属性替换。例如，`%(site_id)s` 在创建 Feed 时会被替换为 `spider.site_id` 属性。

以下是一些示例说明

- 使用每个爬虫一个目录的方式存储到 FTP
  - `ftp://user:password@ftp.example.com/scraping/feeds/%(name)s/%(time)s.json`
- 使用每个爬虫一个目录的方式存储到 S3
  - `s3://mybucket/scraping/feeds/%(name)s/%(time)s.json`

注意

[爬虫参数](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#spiderargs)成为爬虫属性，因此它们也可以用作存储 URI 参数。

## 8.4 存储后端[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#storage-backends)

### 本地文件系统[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#local-filesystem)

Feed 存储在本地文件系统中。

- URI Scheme: `file`
- 示例 URI: `file:///tmp/export.csv`
- 所需外部库：无

请注意，对于本地文件系统存储（仅限），如果您指定绝对路径，例如 `/tmp/export.csv`，则可以省略 Scheme（仅限 Unix 系统）。或者，您也可以使用 [`pathlib.Path`](https://docs.pythonlang.cn/3/library/pathlib.html#pathlib.Path) 对象。

### FTP[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#ftp)

Feed 存储在 FTP 服务器中。

- URI Scheme: `ftp`
- 示例 URI: `ftp://user:pass@ftp.example.com/path/to/export.csv`
- 所需外部库：无

FTP 支持两种不同的连接模式：[主动或被动](https://stackoverflow.com/a/1699163)。Scrapy 默认使用被动连接模式。要改用主动连接模式，请将 [`FEED_STORAGE_FTP_ACTIVE`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_FTP_ACTIVE) 设置为 `True`。

对于此存储后端，[`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中 `overwrite` 键的默认值为：`True`。

注意

`overwrite` 中的 `True` 值将导致您丢失之前版本的数据。

此存储后端使用 [延迟文件传输](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#delayed-file-delivery)。

### S3[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#s3)

Feed 存储在 [Amazon S3](https://aws.amazon.com/s3/) 上。

- URI Scheme: `s3`
- 示例 URI
  - `s3://mybucket/path/to/export.csv`
  - `s3://aws_key:aws_secret@mybucket/path/to/export.csv`
- 所需外部库：[boto3](https://github.com/boto/boto3) >= 1.20.0

AWS 凭据可以通过 URI 中的用户/密码形式传递，也可以通过以下设置传递

- [`AWS_ACCESS_KEY_ID`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-AWS_ACCESS_KEY_ID)
- [`AWS_SECRET_ACCESS_KEY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-AWS_SECRET_ACCESS_KEY)
- [`AWS_SESSION_TOKEN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-AWS_SESSION_TOKEN)（仅用于 [临时安全凭据](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html)）

您还可以使用以下设置定义导出 Feed 的自定义 ACL、自定义 endpoint 和区域名称

- [`FEED_STORAGE_S3_ACL`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_S3_ACL)
- [`AWS_ENDPOINT_URL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-AWS_ENDPOINT_URL)
- [`AWS_REGION_NAME`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-AWS_REGION_NAME)

对于此存储后端，[`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中 `overwrite` 键的默认值为：`True`。

注意

`overwrite` 中的 `True` 值将导致您丢失之前版本的数据。

此存储后端使用 [延迟文件传输](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#delayed-file-delivery)。

### Google Cloud Storage (GCS)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#google-cloud-storage-gcs)

*在 2.3 版本中添加。*

Feed 存储在 [Google Cloud Storage](https://cloud.google.com/storage/) 上。

- URI Scheme: `gs`
- 示例 URI
  - `gs://mybucket/path/to/export.csv`
- 所需外部库：[google-cloud-storage](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)。

有关身份验证的更多信息，请参阅 [Google Cloud 文档](https://cloud.google.com/docs/authentication)。

您可以通过以下设置设置 *项目 ID* 和 *访问控制列表 (ACL)*

- [`FEED_STORAGE_GCS_ACL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-FEED_STORAGE_GCS_ACL)
- [`GCS_PROJECT_ID`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-GCS_PROJECT_ID)

对于此存储后端，[`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS) 设置中 `overwrite` 键的默认值为：`True`。

注意

`overwrite` 中的 `True` 值将导致您丢失之前版本的数据。

此存储后端使用 [延迟文件传输](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#delayed-file-delivery)。

### 标准输出[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#standard-output)

Feed 被写入 Scrapy 进程的标准输出。

- URI Scheme: `stdout`
- 示例 URI: `stdout:`
- 所需外部库：无

### 延迟文件传输[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#delayed-file-delivery)

如上所述，某些描述的存储后端使用延迟文件传输。

这些存储后端不会在 Item 被爬取时立即将它们上传到 Feed URI。而是，Scrapy 将 Item 写入一个临时本地文件，只有当所有文件内容都写入完毕后（即在爬取结束时），才会将该文件上传到 Feed URI。

如果您在使用这些存储后端之一时希望 Item 传输更快开始，请使用 [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT) 将输出 Item 分割到多个文件中，每个文件包含指定的 Item 最大数量。这样，一旦文件达到最大 Item 数量，该文件就会被传输到 Feed URI，从而使 Item 传输在爬取结束之前很久就开始。

## 8.5 Item 过滤[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#item-filtering)

*在 2.6.0 版本中添加。*

您可以使用 [Feed 选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options) 中的 `item_classes` 选项过滤您想允许导出到特定 Feed 的 Item。只有指定类型的 Item 会被添加到 Feed 中。

`item_filter` 选项由 [`ItemFilter`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.ItemFilter) 类实现，它是 [Feed 选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options) `item_filter` 的默认值。

您可以通过实现 [`ItemFilter`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.ItemFilter) 类的方法 `accepts` 并以 `feed_options` 作为参数来创建自己的自定义过滤类。

例如

```
class MyCustomFilter:
    def __init__(self, feed_options):
        self.feed_options = feed_options

    def accepts(self, item):
        if "field1" in item and item["field1"] == "expected_data":
            return True
        return False
```

您可以将您的自定义过滤类分配给 Feed 的 `item_filter` [选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options)。有关示例，请参阅 [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS)。

### ItemFilter[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#itemfilter)

- *class*scrapy.extensions.feedexport.ItemFilter(*feed_options: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/extensions/feedexport.html#ItemFilter)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.ItemFilter)

  FeedExporter 将使用此方法来决定是否应将 Item 导出到特定 Feed。参数:**feed_options** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – FeedExporter 传递的 Feed 特定选项accepts(*item: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*)→ [bool](https://docs.pythonlang.cn/3/library/functions.html#bool)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/extensions/feedexport.html#ItemFilter.accepts)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.ItemFilter.accepts)如果应导出 item 则返回 `True`，否则返回 `False`。参数:**item** ([Scrapy items](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items)) – 用户想要检查是否可接受的爬取到的 Item返回:True 如果被接受，False 否则返回类型:[bool](https://docs.pythonlang.cn/3/library/functions.html#bool)

## 8.6 后处理[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#post-processing)

*在 2.6.0 版本中添加。*

Scrapy 提供一个选项来激活插件，在将 Feed 导出到 Feed 存储之前对其进行后处理。除了使用 [内置插件](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#builtin-plugins)，您还可以创建自己的 [插件](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#custom-plugins)。

这些插件可以通过 Feed 的 `postprocessing` 选项激活。此选项必须传递一个后处理插件列表，顺序即为您希望处理 Feed 的顺序。这些插件可以声明为导入字符串，也可以是插件的导入类。插件的参数可以通过 Feed 选项传递。有关示例，请参阅 [Feed 选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options)。

### 内置插件[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#built-in-plugins)

- *class*scrapy.extensions.postprocessing.GzipPlugin(*file: [BinaryIO](https://docs.pythonlang.cn/3/library/typing.html#typing.BinaryIO)*, *feed_options: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)]*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/extensions/postprocessing.html#GzipPlugin)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.postprocessing.GzipPlugin)

  使用 [gzip](https://en.wikipedia.org/wiki/Gzip) 压缩接收到的数据。接受的 `feed_options` 参数gzip_compresslevelgzip_mtimegzip_filename有关参数的更多信息，请参阅 [`gzip.GzipFile`](https://docs.pythonlang.cn/3/library/gzip.html#gzip.GzipFile)。

- *class*scrapy.extensions.postprocessing.LZMAPlugin(*file: [BinaryIO](https://docs.pythonlang.cn/3/library/typing.html#typing.BinaryIO)*, *feed_options: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)]*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/extensions/postprocessing.html#LZMAPlugin)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.postprocessing.LZMAPlugin)

  使用 [lzma](https://en.wikipedia.org/wiki/Lempel–Ziv–Markov_chain_algorithm) 压缩接收到的数据。接受的 `feed_options` 参数lzma_formatlzma_checklzma_presetlzma_filters注意在 pypy 版本 7.3.1 及更旧版本中不能使用 `lzma_filters`。有关参数的更多信息，请参阅 [`lzma.LZMAFile`](https://docs.pythonlang.cn/3/library/lzma.html#lzma.LZMAFile)。

- *class*scrapy.extensions.postprocessing.Bz2Plugin(*file: [BinaryIO](https://docs.pythonlang.cn/3/library/typing.html#typing.BinaryIO)*, *feed_options: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)]*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/extensions/postprocessing.html#Bz2Plugin)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.postprocessing.Bz2Plugin)

  使用 [bz2](https://en.wikipedia.org/wiki/Bzip2) 压缩接收到的数据。接受的 `feed_options` 参数bz2_compresslevel有关参数的更多信息，请参阅 [`bz2.BZ2File`](https://docs.pythonlang.cn/3/library/bz2.html#bz2.BZ2File)。

### 自定义插件[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#custom-plugins)

每个插件都是一个类，必须实现以下方法

- __init__(*self*, *file*, *feed_options*)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#init__)

  初始化插件。参数:**file** – 文件类对象，至少实现了 write、tell 和 close 方法**feed_options** ([`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – Feed 特定 [选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options)

- write(*self*, *data*)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#write)

  处理并写入 data ([`bytes`](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) 或 [`memoryview`](https://docs.pythonlang.cn/3/library/stdtypes.html#memoryview)) 到插件的目标文件中。它必须返回写入的字节数。

- close(*self*)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#close)

  清理插件。例如，您可能需要关闭一个文件包装器，该包装器可能用于压缩写入 `__init__` 方法中接收到的文件的数据。警告不要从 `__init__` 方法中关闭文件。

要将参数传递给您的插件，请使用 [Feed 选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options)。然后您可以从您的插件的 `__init__` 方法中访问这些参数。

## 8.7 设置[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#settings)

以下是用于配置 Feed Exports 的设置

- [`FEEDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS)（强制）
- [`FEED_EXPORT_ENCODING`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_ENCODING)
- [`FEED_STORE_EMPTY`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORE_EMPTY)
- [`FEED_EXPORT_FIELDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_FIELDS)
- [`FEED_EXPORT_INDENT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_INDENT)
- [`FEED_STORAGES`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES)
- [`FEED_STORAGE_FTP_ACTIVE`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_FTP_ACTIVE)
- [`FEED_STORAGE_S3_ACL`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_S3_ACL)
- [`FEED_EXPORTERS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORTERS)
- [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT)



### FEEDS[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feeds)

*在 2.1 版本中添加。*

默认值: `{}`

一个字典，其中每个键都是一个 Feed URI（或 [`pathlib.Path`](https://docs.pythonlang.cn/3/library/pathlib.html#pathlib.Path) 对象），每个值都是一个嵌套字典，包含特定 Feed 的配置参数。

此设置是启用 Feed 导出功能所必需的。

有关支持的 URI Scheme，请参阅 [存储后端](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-backends)。

例如

```
{
    'items.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'item_classes': [MyItemClass1, 'myproject.items.MyItemClass2'],
        'fields': None,
        'indent': 4,
        'item_export_kwargs': {
           'export_empty_fields': True,
        },
    },
    '/home/user/documents/items.xml': {
        'format': 'xml',
        'fields': ['name', 'price'],
        'item_filter': MyCustomFilter1,
        'encoding': 'latin1',
        'indent': 8,
    },
    pathlib.Path('items.csv.gz'): {
        'format': 'csv',
        'fields': ['price', 'name'],
        'item_filter': 'myproject.filters.MyCustomFilter2',
        'postprocessing': [MyPlugin1, 'scrapy.extensions.postprocessing.GzipPlugin'],
        'gzip_compresslevel': 5,
    },
}
```

以下是接受的键列表以及在特定 Feed 定义未提供该键时用作回退值的设置

- `format`: [序列化格式](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-format)。

  此设置是强制的，没有回退值。

- `batch_item_count`: 回退到 [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT)。

  *在 2.3.0 版本中添加。*

- `encoding`: 回退到 [`FEED_EXPORT_ENCODING`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_ENCODING)。

- `fields`: 回退到 [`FEED_EXPORT_FIELDS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_FIELDS)。

- `item_classes`: 要导出的 [Item 类](https://docs.scrapy.net.cn/en/latest/topics/items.html#topics-items) 列表。

  如果未定义或为空，所有 Item 都会被导出。

  *在 2.6.0 版本中添加。*

- `item_filter`: 用于过滤要导出 Item 的 [过滤类](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#item-filter)。

  [`ItemFilter`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.ItemFilter) 默认使用。

  *在 2.6.0 版本中添加。*

- `indent`: 回退到 [`FEED_EXPORT_INDENT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_INDENT)。

- `item_export_kwargs`: 包含对应 [Item 导出器类](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#topics-exporters) 的关键字参数的 [`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)。

  *在 2.4.0 版本中添加。*

- `overwrite`：如果文件已存在，是覆盖文件（`True`）还是追加到其内容（`False`）。

  默认值取决于[存储后端](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-backends)

  - [本地文件系统](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-fs)：`False`

  - [FTP](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-ftp)：`True`

    注意

    一些FTP服务器可能不支持文件追加（`APPE` FTP命令）。

  - [S3](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)：`True`（不支持追加）

  - [Google Cloud Storage (GCS)](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-gcs)：`True`（不支持追加）

  - [标准输出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-stdout)：`False`（不支持覆盖）

  *在 2.4.0 版本中添加。*

- `store_empty`：回退到 [`FEED_STORE_EMPTY`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORE_EMPTY)。

- `uri_params`：回退到 [`FEED_URI_PARAMS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_URI_PARAMS)。

- `postprocessing`：用于后处理的[插件](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#post-processing)列表。

  插件将按照列表中传入的顺序使用。

  *在 2.6.0 版本中添加。*



### FEED_EXPORT_ENCODING[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-export-encoding)

默认值：`"utf-8"`（[回退](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings)：`None`）

用于导出 feed 的编码。

如果设置为 `None`，除了JSON输出外，所有都使用UTF-8。JSON输出出于历史原因使用安全的数字编码（`\uXXXX`序列）。

如果您想JSON也使用UTF-8，请使用 `"utf-8"`。

*在 2.8 版本中有所变动:* [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 命令现在会在生成的 `settings.py` 文件中将此设置设为 `"utf-8"`。



### FEED_EXPORT_FIELDS[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-export-fields)

默认值：`None`

使用 `FEED_EXPORT_FIELDS` 设置定义要导出的字段、它们的顺序和输出名称。有关更多信息，请参阅 [`BaseItemExporter.fields_to_export`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.BaseItemExporter.fields_to_export)。



### FEED_EXPORT_INDENT[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-export-indent)

默认值：`0`

在每个层级缩进输出的空格数。如果 `FEED_EXPORT_INDENT` 是一个非负整数，则数组元素和对象成员将以该缩进级别进行美观打印。缩进级别为 `0`（默认值）或负数，会将每个项目放在新行上。`None` 选择最紧凑的表示形式。

目前仅由 [`JsonItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.JsonItemExporter) 和 [`XmlItemExporter`](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#scrapy.exporters.XmlItemExporter) 实现，即当您导出到 `.json` 或 `.xml` 时。



### FEED_STORE_EMPTY[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-store-empty)

默认值：`True`

是否导出空 feed（即不包含任何 item 的 feed）。如果设置为 `False`，并且没有 item 可导出，则不会创建新文件，也不会修改现有文件，即使[覆盖 feed 选项](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-options)已启用。



### FEED_STORAGES[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-storages)

默认值: `{}`

一个字典，包含您的项目支持的其他 feed 存储后端。键是 URI 方案，值是存储类的路径。



### FEED_STORAGE_FTP_ACTIVE[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-storage-ftp-active)

默认值：`False`

导出 feed 到 FTP 服务器时，是使用主动连接模式（`True`）还是使用被动连接模式（`False`，默认值）。

有关 FTP 连接模式的信息，请参阅[主动和被动FTP有什么区别？](https://stackoverflow.com/a/1699163)。



### FEED_STORAGE_S3_ACL[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-storage-s3-acl)

默认值：`''`（空字符串）

一个字符串，包含您的项目导出到 Amazon S3 的 feed 的自定义 ACL。

有关可用值的完整列表，请访问 Amazon S3 文档中的[预设 ACL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl) 部分。



### FEED_STORAGES_BASE[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-storages-base)

默认

```
{
    "": "scrapy.extensions.feedexport.FileFeedStorage",
    "file": "scrapy.extensions.feedexport.FileFeedStorage",
    "stdout": "scrapy.extensions.feedexport.StdoutFeedStorage",
    "s3": "scrapy.extensions.feedexport.S3FeedStorage",
    "ftp": "scrapy.extensions.feedexport.FTPFeedStorage",
}
```

一个字典，包含 Scrapy 支持的内置 feed 存储后端。您可以通过在 [`FEED_STORAGES`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES) 中将它们的 URI 方案赋值为 `None` 来禁用它们中的任何一个。例如，要在不替换的情况下禁用内置的 FTP 存储后端，请将其放在您的 `settings.py` 文件中

```
FEED_STORAGES = {
    "ftp": None,
}
```



### FEED_EXPORTERS[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-exporters)

默认值: `{}`

一个字典，包含您的项目支持的其他导出器。键是序列化格式，值是 [Item exporter](https://docs.scrapy.net.cn/en/latest/topics/exporters.html#topics-exporters) 类的路径。



### FEED_EXPORTERS_BASE[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-exporters-base)

默认

```
{
    "json": "scrapy.exporters.JsonItemExporter",
    "jsonlines": "scrapy.exporters.JsonLinesItemExporter",
    "jsonl": "scrapy.exporters.JsonLinesItemExporter",
    "jl": "scrapy.exporters.JsonLinesItemExporter",
    "csv": "scrapy.exporters.CsvItemExporter",
    "xml": "scrapy.exporters.XmlItemExporter",
    "marshal": "scrapy.exporters.MarshalItemExporter",
    "pickle": "scrapy.exporters.PickleItemExporter",
}
```

一个字典，包含 Scrapy 支持的内置 feed 导出器。您可以通过在 [`FEED_EXPORTERS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORTERS) 中将它们的序列化格式赋值为 `None` 来禁用它们中的任何一个。例如，要在不替换的情况下禁用内置的 CSV 导出器，请将其放在您的 `settings.py` 文件中

```
FEED_EXPORTERS = {
    "csv": None,
}
```



### FEED_EXPORT_BATCH_ITEM_COUNT[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-export-batch-item-count)

*在 2.3.0 版本中添加。*

默认值：`0`

如果指定一个大于 `0` 的整数，Scrapy 将生成多个输出文件，每个文件最多存储指定数量的 item。

生成多个输出文件时，必须在 feed URI 中使用至少一个以下占位符来指示如何生成不同的输出文件名

- `%(batch_time)s` - 在创建 feed 时替换为时间戳（例如 `2020-03-28T14-45-08.237134`）

- `%(batch_id)d` - 替换为批次的基于 1 的序号。

  使用[printf 风格的字符串格式化](https://docs.pythonlang.cn/3/library/stdtypes.html#old-string-formatting)来改变数字格式。例如，通过根据需要添加前导零，将批次 ID 变为 5 位数字，使用 `%(batch_id)05d`（例如，`3` 变为 `00003`，`123` 变为 `00123`）。

例如，如果您的设置包含

```
FEED_EXPORT_BATCH_ITEM_COUNT = 100
```

并且您的 [`crawl`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-crawl) 命令行是

```
scrapy crawl spidername -o "dirname/%(batch_id)d-filename%(batch_time)s.json"
```

上面的命令行可以生成一个目录树，如下所示

```
->projectname
-->dirname
--->1-filename2020-03-28T14-45-08.237134.json
--->2-filename2020-03-28T14-45-09.148903.json
--->3-filename2020-03-28T14-45-10.046092.json
```

其中第一个和第二个文件都包含恰好 100 个 item。最后一个文件包含 100 个或更少的 item。



### FEED_URI_PARAMS[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#feed-uri-params)

默认值：`None`

一个字符串，包含一个函数的导入路径，用于设置使用[printf 风格的字符串格式化](https://docs.pythonlang.cn/3/library/stdtypes.html#old-string-formatting)应用于 feed URI 的参数。

函数签名应如下所示

- scrapy.extensions.feedexport.uri_params(*params*, *spider*)[](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#scrapy.extensions.feedexport.uri_params)

  返回一个[`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)，包含要使用[printf 风格的字符串格式化](https://docs.pythonlang.cn/3/library/stdtypes.html#old-string-formatting)应用于 feed URI 的键值对。参数:**params** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) –默认键值对具体如下`batch_id`：文件批次的 ID。请参阅 [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT)。如果 [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT) 是 `0`，则 `batch_id` 总是 `1`。*在 2.3.0 版本中添加。*`batch_time`：UTC 日期和时间，ISO 格式，其中 `:` 替换为 `-`。请参阅 [`FEED_EXPORT_BATCH_ITEM_COUNT`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT)。*在 2.3.0 版本中添加。*`time`：`batch_time`，微秒设置为 `0`。**spider** ([*scrapy.Spider*](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider)) – feed item 的源爬虫注意函数应该返回一个新字典，原地修改接收到的 `params` 已被弃用。

例如，要在 feed URI 中包含源爬虫的 [`name`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.name)

1. 在您的项目中的某个位置定义以下函数

   ```
   # myproject/utils.py
   def uri_params(params, spider):
       return {**params, "spider_name": spider.name}
   ```

2. 在您的设置中将 [`FEED_URI_PARAMS`](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_URI_PARAMS) 指向该函数

   ```
   # myproject/settings.py
   FEED_URI_PARAMS = "myproject.utils.uri_params"
   ```

3. 在您的 feed URI 中使用 `%(spider_name)s`

   ```
   scrapy crawl <spider_name> -o "%(spider_name)s.jsonl"
   ```

# 9 请求和响应

Scrapy 使用 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 和 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象来抓取网站。

通常，[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象在 spider 中生成，并在系统中传递，直到到达 Downloader（下载器）。Downloader 执行请求并返回一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象，该对象再返回给发出请求的 spider。

[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 和 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 类都有子类，这些子类添加了基类不需要的功能。这些内容将在下面的 [Request 子类](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-subclasses) 和 [Response 子类](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-response-subclasses) 中描述。

## 9.1 Request 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-objects)

- *class*scrapy.Request(**args: Any*, ***kwargs: Any*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#Request)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)

  表示一个 HTTP 请求，通常在 Spider 中生成并由 Downloader 执行，从而生成一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)。参数:**url** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) –此请求的 URL如果 URL 无效，则会引发 [`ValueError`](https://docs.pythonlang.cn/3/library/exceptions.html#ValueError) 异常。**callback** (*Callable**[**Concatenate**[*[*Response*](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)*,* *...**]**,* *Any**]* *|* *None*) –设置 [`callback`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.callback)，默认为 `None`。*版本 2.0 中有改动:* 指定 *errback* 参数时，不再需要 *callback* 参数。**method** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 此请求的 HTTP 方法。默认为 `'GET'`。**meta** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – [`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 属性的初始值。如果提供，此参数中传递的字典将被浅拷贝。**body** ([*bytes*](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) *或* [*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 请求体。如果传入字符串，则会使用传入的 `encoding`（默认为 `utf-8`）将其编码为字节。如果未提供 `body`，则存储一个空的字节对象。无论此参数的类型如何，最终存储的值都将是一个字节对象（绝不是字符串或 `None`）。**headers** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) –此请求的请求头。字典值可以是字符串（用于单值请求头）或列表（用于多值请求头）。如果传递 `None` 作为值，则完全不会发送该 HTTP 请求头。注意通过 `Cookie` 请求头设置的 Cookie 不会被 [CookiesMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#cookies-mw) 考虑。如果需要为请求设置 Cookie，请使用 `cookies` 参数。这是一个目前已知并在处理中的限制。**cookies** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) –请求的 Cookie。可以通过两种形式发送。使用字典`request_with_cookies = Request(    url="http://www.example.com",    cookies={"currency": "USD", "country": "UY"}, ) `使用字典列表`request_with_cookies = Request(    url="https://www.example.com",    cookies=[        {            "name": "currency",            "value": "USD",            "domain": "example.com",            "path": "/currency",            "secure": True,        },    ], ) `后一种形式允许自定义 Cookie 的 `domain` 和 `path` 属性。这仅在 Cookie 保存用于后续请求时有用。当某个网站返回 Cookie（在响应中）时，这些 Cookie 将存储在该域的 Cookie 中，并在未来的请求中再次发送。这是任何常规 Web 浏览器的典型行为。请注意，在 [`request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 中将 [`dont_merge_cookies`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-dont_merge_cookies) 键设置为 `True` 会导致自定义 Cookie 被忽略。更多信息请参阅 [CookiesMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#cookies-mw)。注意通过 `Cookie` 请求头设置的 Cookie 不会被 [CookiesMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#cookies-mw) 考虑。如果需要为请求设置 Cookie，请使用 [`scrapy.Request.cookies`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 参数。这是一个目前已知并在处理中的限制。*在版本 2.6.0 中新增:* 类型为 [`bool`](https://docs.pythonlang.cn/3/library/functions.html#bool), [`float`](https://docs.pythonlang.cn/3/library/functions.html#float) 或 [`int`](https://docs.pythonlang.cn/3/library/functions.html#int) 的 Cookie 值会被转换为 [`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str)。**encoding** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 此请求的编码（默认为 `'utf-8'`）。此编码将用于对 URL 进行百分比编码，并将请求体转换为字节（如果作为字符串提供）。**priority** ([*int*](https://docs.pythonlang.cn/3/library/functions.html#int)) – 设置 [`priority`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.priority)，默认为 `0`。**dont_filter** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 设置 [`dont_filter`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.dont_filter)，默认为 `False`。**errback** (*Callable**[**[**Failure**]**,* *Any**]* *|* *None*) –设置 [`errback`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.errback)，默认为 `None`。*版本 2.0 中有改动:* 指定 *errback* 参数时，不再需要 *callback* 参数。**flags** ([*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 发送给请求的标志，可用于日志记录或类似目的。**cb_kwargs** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 一个包含任意数据的字典，这些数据将作为关键字参数传递给 Request 的回调函数。url[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.url)一个包含此请求 URL 的字符串。请记住，此属性包含已转义的 URL，因此它可能与 `__init__()` 方法中传递的 URL 不同。此属性是只读的。要更改 Request 的 URL，请使用 [`replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace)。method[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.method)表示请求中 HTTP 方法的字符串。保证为大写。示例：`"GET"`, `"POST"`, `"PUT"` 等headers[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.headers)一个类似字典的 (`scrapy.http.headers.Headers`) 对象，包含请求头。body[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.body)作为字节的请求体。此属性是只读的。要更改 Request 的请求体，请使用 [`replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace)。callback*: CallbackT | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.callback)用于解析此请求收到后的 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 的 [`Callable`](https://docs.pythonlang.cn/3/library/collections.abc.html#collections.abc.Callable) 对象。可调用对象必须将响应作为其第一个参数，并支持通过 [`cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 设置的任何额外关键字参数。除了任意可调用对象外，还支持以下值`None` (默认值)，表示必须使用 spider 的 [`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 方法。[`NO_CALLBACK()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.request.NO_CALLBACK).如果在请求或响应处理期间发生未处理的异常，例如由 [spider 中间件](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware)、[下载器中间件](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware) 或下载处理程序 ([`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)) 引发，则会改为调用 [`errback`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.errback)。提示[`HttpErrorMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#scrapy.spidermiddlewares.httperror.HttpErrorMiddleware) 默认会针对非 2xx 响应引发异常，并将其发送到 [`errback`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.errback)。另请参阅[向回调函数传递额外数据](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments)errback*: Callable[[Failure], Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.errback)用于处理请求或响应处理期间引发的异常的 [`Callable`](https://docs.pythonlang.cn/3/library/collections.abc.html#collections.abc.Callable) 对象。可调用对象必须将 [`Failure`](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html) 作为其第一个参数。另请参阅[使用 errback 捕获请求处理中的异常](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-errbacks)priority*: [int](https://docs.pythonlang.cn/3/library/functions.html#int)*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.priority)默认值: `0`[调度器](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#topics-scheduler) 可能用于请求优先级排序的值。内置调度器会优先处理优先级值更高的请求。允许使用负值。cb_kwargs[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs)一个包含此请求的任意元数据的字典。其内容将作为关键字参数传递给 Request 的回调函数。对于新的 Request，它为空，这意味着默认情况下回调函数只接收一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象作为参数。当使用 `copy()` 或 `replace()` 方法克隆请求时，此字典会进行 [浅拷贝](https://docs.pythonlang.cn/3/library/copy.html)，并且在 spider 中，也可以通过 `response.cb_kwargs` 属性访问它。如果处理请求失败，可以在请求的 errback 中通过 `failure.request.cb_kwargs` 访问此字典。更多信息请参阅 [在 errback 函数中访问额外数据](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#errback-cb-kwargs)。meta*= {}*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta)一个包含请求的任意元数据的字典。您可以根据需要扩展请求元数据。请求元数据也可以通过响应的 [`meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.meta) 属性访问。要在不同的 spider 回调函数之间传递数据，请考虑使用 [`cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs)。然而，在某些情况下，请求元数据可能是正确的选择，例如在所有后续请求中维护一些调试数据（例如源 URL）。请求元数据的一个常见用途是为 Scrapy 组件（扩展、中间件等）定义请求特定的参数。例如，如果您将 `dont_retry` 设置为 `True`，即使请求失败，[`RetryMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.retry.RetryMiddleware) 也不会重试该请求。请参阅 [Request.meta 特殊键](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-meta)。您也可以在自定义的 Scrapy 组件中使用请求元数据，例如，保存与您的组件相关的请求状态信息。例如，[`RetryMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.retry.RetryMiddleware) 使用 `retry_times` 元数据键来跟踪请求目前已重试的次数。在 spider 回调函数中，将前一个请求的所有元数据复制到新的、后续请求中是一种不良实践，因为请求元数据可能包含由 Scrapy 组件设置的元数据，这些元数据不应该被复制到其他请求中。例如，将 `retry_times` 元数据键复制到后续请求中，可能会降低这些后续请求允许的重试次数。只有当新请求旨在替换旧请求时，才应该将一个请求的所有元数据复制到另一个请求中，这通常发生在从 [下载器中间件](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware) 方法返回请求时。另请注意，[`copy()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.copy) 和 [`replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace) 请求方法会 [浅拷贝](https://docs.pythonlang.cn/3/library/copy.html) 请求元数据。dont_filter*: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool)*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.dont_filter)此请求是否可以被支持过滤请求的 [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components) 过滤掉（`False`，默认），还是这些组件不应该过滤掉此请求（`True`）。此属性通常设置为 `True`，以防止重复请求被过滤掉。通过 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls) 定义 spider 的起始 URL 时，此属性默认启用。请参阅 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start)。attributes*: [tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), ...]**= ('url', 'callback', 'method', 'headers', 'body', 'cookies', 'meta', 'encoding', 'priority', 'dont_filter', 'errback', 'flags', 'cb_kwargs')*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.attributes)一个由 [`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str) 对象组成的元组，包含类中所有公共属性的名称，这些属性也是 `__init__()` 方法的关键字参数。目前被 [`Request.replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace), [`Request.to_dict()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.to_dict) 和 [`request_from_dict()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.request_from_dict) 使用。copy()[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#Request.copy)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.copy)返回一个新的 Request，它是此 Request 的副本。另请参阅：[向回调函数传递额外数据](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments)。replace(**[***url*, *method*, *headers*, *body*, *cookies*, *meta*, *flags*, *encoding*, *priority*, *dont_filter*, *callback*, *errback*, *cb_kwargs***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#Request.replace)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace)返回一个 Request 对象，其成员与原对象相同，但通过关键字参数指定新值的成员除外。[`cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 和 [`meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 属性默认进行浅拷贝（除非作为参数提供了新值）。另请参阅 [向回调函数传递额外数据](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments)。*classmethod*from_curl(*curl_command: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)*, *ignore_unknown_options: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = True*, ***kwargs: Any*)→ Self[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#Request.from_curl)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.from_curl)从包含 [cURL](https://curl.se/) 命令的字符串创建 Request 对象。它填充 HTTP 方法、URL、请求头、Cookie 和请求体。它接受与 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 类相同的参数，并优先使用这些参数值，覆盖 cURL 命令中包含的相同参数值。默认情况下，不识别的选项会被忽略。要在发现未知选项时引发错误，请在调用此方法时传递 `ignore_unknown_options=False`。注意使用来自 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 子类（如 [`JsonRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonRequest) 或 `XmlRpcRequest`）的 [`from_curl()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.from_curl)，以及启用 [下载器中间件](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware) 和 [spider 中间件](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware)（例如 [`DefaultHeadersMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware), [`UserAgentMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.useragent.UserAgentMiddleware) 或 [`HttpCompressionMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware)），可能会修改 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。要将 cURL 命令转换为 Scrapy 请求，您可以使用 [curl2scrapy](https://michael-shub.github.io/curl2scrapy/)。to_dict(***, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)][[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#Request.to_dict)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.to_dict)返回一个包含 Request 数据的字典。使用 [`request_from_dict()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.request_from_dict) 将其转换回一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。如果给定了爬虫，该方法将尝试找出用作回调 (callback) 和错误回调 (errback) 的爬虫方法的名称，并将它们包含在输出字典中；如果找不到，则会引发异常。

### 其他与请求相关的函数[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#other-functions-related-to-requests)

- scrapy.http.request.NO_CALLBACK(**args: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*, ***kwargs: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*)→ [NoReturn](https://docs.pythonlang.cn/3/library/typing.html#typing.NoReturn)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request.html#NO_CALLBACK)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.request.NO_CALLBACK)

  当赋值给 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 的 `callback` 参数时，它表示该请求不应该有任何爬虫回调。例如`Request("https://example.com", callback=NO_CALLBACK) `这个值应该由创建和处理自身请求的 [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components) 使用，例如通过 `scrapy.core.engine.ExecutionEngine.download()`，这样处理此类请求的下载器中间件可以将其与用于 [`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 回调的请求区分开来。

- scrapy.utils.request.request_from_dict(*d: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)]*, ***, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/utils/request.html#request_from_dict)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.request_from_dict)

  从字典创建一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。如果给定了爬虫，它将尝试通过在爬虫中查找同名方法来解析回调。



### 向回调函数传递额外数据[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#passing-additional-data-to-callback-functions)

请求的回调是一个函数，当该请求的响应被下载后将被调用。回调函数将以下载的 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象作为第一个参数被调用。

示例

```
def parse_page1(self, response):
    return scrapy.Request(
        "http://www.example.com/some_page.html", callback=self.parse_page2
    )


def parse_page2(self, response):
    # this would log http://www.example.com/some_page.html
    self.logger.info("Visited %s", response.url)
```

在某些情况下，您可能希望向这些回调函数传递参数，以便稍后在第二个回调中接收这些参数。以下示例展示了如何通过使用 [`Request.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 属性来实现这一点。

```
def parse(self, response):
    request = scrapy.Request(
        "http://www.example.com/index.html",
        callback=self.parse_page2,
        cb_kwargs=dict(main_url=response.url),
    )
    request.cb_kwargs["foo"] = "bar"  # add more arguments for the callback
    yield request


def parse_page2(self, response, main_url, foo):
    yield dict(
        main_url=main_url,
        other_url=response.url,
        foo=foo,
    )
```

注意

[`Request.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 在版本 `1.7` 中引入。在此之前，建议使用 [`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 来在回调之间传递信息。在 `1.7` 之后，[`Request.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 成为处理用户信息的首选方式，而 [`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 则保留用于与中间件 (middlewares) 和扩展 (extensions) 等组件通信。



### 使用错误回调 (errbacks) 捕获请求处理中的异常[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#using-errbacks-to-catch-exceptions-in-request-processing)

请求的错误回调是一个函数，当在处理请求时发生异常时将被调用。

它接收一个 [`Failure`](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html) 对象作为第一个参数，可用于跟踪连接建立超时、DNS 错误等。

这里有一个示例爬虫，用于记录所有错误并在需要时捕获一些特定错误。

```
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ErrbackSpider(scrapy.Spider):
    name = "errback_example"
    start_urls = [
        "http://www.httpbin.org/",  # HTTP 200 expected
        "http://www.httpbin.org/status/404",  # Not found error
        "http://www.httpbin.org/status/500",  # server issue
        "http://www.httpbin.org:12345/",  # non-responding host, timeout expected
        "https://example.invalid/",  # DNS error expected
    ]

    async def start(self):
        for u in self.start_urls:
            yield scrapy.Request(
                u,
                callback=self.parse_httpbin,
                errback=self.errback_httpbin,
                dont_filter=True,
            )

    def parse_httpbin(self, response):
        self.logger.info("Got successful response from {}".format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)
```



### 在错误回调函数中访问额外数据[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#accessing-additional-data-in-errback-functions)

如果请求处理失败，您可能需要访问回调函数的参数，以便在错误回调中根据这些参数进行进一步处理。以下示例展示了如何通过使用 `Failure.request.cb_kwargs` 来实现这一点。

```
def parse(self, response):
    request = scrapy.Request(
        "http://www.example.com/index.html",
        callback=self.parse_page2,
        errback=self.errback_page2,
        cb_kwargs=dict(main_url=response.url),
    )
    yield request


def parse_page2(self, response, main_url):
    pass


def errback_page2(self, failure):
    yield dict(
        main_url=failure.request.cb_kwargs["main_url"],
    )
```



### 请求指纹[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-fingerprints)

在爬取的一些方面，例如过滤重复请求（参见 [`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)）或缓存响应（参见 [`HTTPCACHE_POLICY`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_POLICY)），您需要能够从 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象生成一个简短、唯一的标识符：一个请求指纹。

通常您无需担心请求指纹，默认的请求指纹生成器适用于大多数项目。

然而，没有一种通用的方法可以从请求生成唯一的标识符，因为不同的情况需要以不同的方式比较请求。例如，有时您可能需要不区分大小写地比较 URL，包含 URL 片段，排除某些 URL 查询参数，包含部分或全部请求头等。

要更改请求指纹的构建方式，请使用 [`REQUEST_FINGERPRINTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-setting-REQUEST_FINGERPRINTER_CLASS) 设置。



#### REQUEST_FINGERPRINTER_CLASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-fingerprinter-class)

*在版本 2.7 中新增。*

默认值：[`scrapy.utils.request.RequestFingerprinter`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.RequestFingerprinter)

一个 [请求指纹生成器类](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#custom-request-fingerprinter) 或其导入路径。

- *class*scrapy.utils.request.RequestFingerprinter(*crawler: [Crawler](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/utils/request.html#RequestFingerprinter)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.RequestFingerprinter)

  默认的指纹生成器。它考虑了 [`request.url`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.url) 的规范化版本（[`w3lib.url.canonicalize_url()`](https://w3lib.readthedocs.io/en/latest/w3lib.html#w3lib.url.canonicalize_url)）以及 [`request.method`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.method) 和 [`request.body`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.body) 的值。然后生成一个 [SHA1](https://en.wikipedia.org/wiki/SHA-1) 哈希。



#### 编写自己的请求指纹生成器[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#writing-your-own-request-fingerprinter)

请求指纹生成器是一个 [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components)，必须实现以下方法。

- fingerprint(*self*, *request: [scrapy.Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)*)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#fingerprint)

  返回一个唯一标识 *request* 的 [`bytes`](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) 对象。另请参见 [请求指纹限制](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-fingerprint-restrictions)。

默认请求指纹生成器 [`scrapy.utils.request.RequestFingerprinter`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.RequestFingerprinter) 的 [`fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#fingerprint) 方法使用了 [`scrapy.utils.request.fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.fingerprint) 的默认参数。对于一些常见的使用场景，您也可以在自己的 [`fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#fingerprint) 方法实现中使用 [`scrapy.utils.request.fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.fingerprint)。

- scrapy.utils.request.fingerprint(*request: [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)*, ***, *include_headers: Iterable[[bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *keep_fragments: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*)→ [bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/utils/request.html#fingerprint)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.fingerprint)

  返回请求指纹。请求指纹是一个哈希值，用于唯一标识请求指向的资源。例如，考虑以下两个 URL：`http://www.example.com/query?id=111&cat=222`，`http://www.example.com/query?cat=222&id=111`。尽管这是两个不同的 URL，但它们都指向同一资源并且是等效的（即它们应该返回相同的响应）。另一个例子是用于存储会话 ID 的 cookie。假设以下页面仅供认证用户访问：`http://www.example.com/members/offers.html`。许多网站使用 cookie 来存储会话 ID，这会给 HTTP 请求添加一个随机成分，因此在计算指纹时应该忽略它。因此，在计算指纹时默认忽略请求头。如果要包含特定的请求头，请使用 include_headers 参数，它是一个要包含的 Request 请求头列表。此外，服务器在处理请求时通常会忽略 URL 中的片段，因此在计算指纹时默认也会忽略它们。如果您想包含它们，请将 keep_fragments 参数设置为 True（例如在使用无头浏览器处理请求时）。

例如，要将名为 `X-ID` 的请求头的值考虑在内。

```
# my_project/settings.py
REQUEST_FINGERPRINTER_CLASS = "my_project.utils.RequestFingerprinter"

# my_project/utils.py
from scrapy.utils.request import fingerprint


class RequestFingerprinter:
    def fingerprint(self, request):
        return fingerprint(request, include_headers=["X-ID"])
```

您也可以从头开始编写自己的指纹生成逻辑。

然而，如果您不使用 [`scrapy.utils.request.fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.fingerprint)，请确保使用 [`WeakKeyDictionary`](https://docs.pythonlang.cn/3/library/weakref.html#weakref.WeakKeyDictionary) 来缓存请求指纹。

- 缓存通过确保每个请求的指纹只计算一次，而不是每个需要请求指纹的 Scrapy 组件都计算一次，从而节省 CPU。
- 使用 [`WeakKeyDictionary`](https://docs.pythonlang.cn/3/library/weakref.html#weakref.WeakKeyDictionary) 通过确保请求对象不会仅仅因为您的缓存字典中引用了它们而永远保留在内存中，从而节省内存。

例如，仅考虑请求的 URL，而无需进行任何 URL 规范化或考虑请求方法或请求体。

```
from hashlib import sha1
from weakref import WeakKeyDictionary

from scrapy.utils.python import to_bytes


class RequestFingerprinter:
    cache = WeakKeyDictionary()

    def fingerprint(self, request):
        if request not in self.cache:
            fp = sha1()
            fp.update(to_bytes(request.url))
            self.cache[request] = fp.digest()
        return self.cache[request]
```

如果您需要能够从爬虫回调中覆盖任意请求的指纹生成，您可以实现一个请求指纹生成器，在可用时从 [`request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 中读取指纹，然后回退到 [`scrapy.utils.request.fingerprint()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.fingerprint)。例如

```
from scrapy.utils.request import fingerprint


class RequestFingerprinter:
    def fingerprint(self, request):
        if "fingerprint" in request.meta:
            return request.meta["fingerprint"]
        return fingerprint(request)
```

如果您需要重现与 Scrapy 2.6 相同的指纹算法，请使用以下请求指纹生成器。

```
from hashlib import sha1
from weakref import WeakKeyDictionary

from scrapy.utils.python import to_bytes
from w3lib.url import canonicalize_url


class RequestFingerprinter:
    cache = WeakKeyDictionary()

    def fingerprint(self, request):
        if request not in self.cache:
            fp = sha1()
            fp.update(to_bytes(request.method))
            fp.update(to_bytes(canonicalize_url(request.url)))
            fp.update(request.body or b"")
            self.cache[request] = fp.digest()
        return self.cache[request]
```



#### 请求指纹限制[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-fingerprint-restrictions)

使用请求指纹的 Scrapy 组件可能会对您的 [请求指纹生成器](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#custom-request-fingerprinter) 生成的指纹格式施加额外的限制。

以下内置的 Scrapy 组件具有此类限制。

- [`scrapy.extensions.httpcache.FilesystemCacheStorage`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.extensions.httpcache.FilesystemCacheStorage) ([`HTTPCACHE_STORAGE`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_STORAGE) 的默认值)

  请求指纹必须至少为 1 字节长。

  [`HTTPCACHE_DIR`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_DIR) 文件系统的路径和文件名长度限制也适用。在 [`HTTPCACHE_DIR`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_DIR) 内部，会创建以下目录结构：

  - [`爬虫名`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.name)
    - 请求指纹的第一个字节（十六进制表示）
      - 指纹（十六进制表示）
        - 文件名（最长 16 个字符）

  例如，如果一个请求指纹由 20 字节组成（默认），[`HTTPCACHE_DIR`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_DIR) 是 `'/home/user/project/.scrapy/httpcache'`，并且您的爬虫名称是 `'my_spider'`，则您的文件系统必须支持类似以下的文件路径：

  ```
  /home/user/project/.scrapy/httpcache/my_spider/01/0123456789abcdef0123456789abcdef01234567/response_headers
  ```

- [`scrapy.extensions.httpcache.DbmCacheStorage`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.extensions.httpcache.DbmCacheStorage)

  底层的 DBM 实现必须支持长度为请求指纹字节数的两倍加 5 的键。例如，如果一个请求指纹由 20 字节组成（默认），则必须支持长度为 45 个字符的键。



## 9.2 Request.meta 特殊键[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-meta-special-keys)

通过 [`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 属性可以包含任意数据，但有一些由 Scrapy 及其内置扩展识别的特殊键。

这些键包括：

- [`allow_offsite`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-allow_offsite)
- [`autothrottle_dont_adjust_delay`](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-reqmeta-autothrottle_dont_adjust_delay)
- [`bindaddress`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-bindaddress)
- [`cookiejar`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-cookiejar)
- [`dont_cache`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-dont_cache)
- [`dont_merge_cookies`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-dont_merge_cookies)
- [`dont_obey_robotstxt`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-dont_obey_robotstxt)
- [`dont_redirect`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-dont_redirect)
- [`dont_retry`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-dont_retry)
- [`download_fail_on_dataloss`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-download_fail_on_dataloss)
- [`download_latency`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-download_latency)
- [`download_maxsize`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-reqmeta-download_maxsize)
- [`download_warnsize`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-reqmeta-download_warnsize)
- [`download_timeout`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-download_timeout)
- `ftp_password` (参见 [`FTP_PASSWORD`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-FTP_PASSWORD) 了解更多信息)
- `ftp_user` (参见 [`FTP_USER`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-FTP_USER) 了解更多信息)
- [`handle_httpstatus_all`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-reqmeta-handle_httpstatus_all)
- [`handle_httpstatus_list`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-reqmeta-handle_httpstatus_list)
- [`is_start_request`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-reqmeta-is_start_request)
- [`max_retry_times`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-max_retry_times)
- [`proxy`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-proxy)
- [`redirect_reasons`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-redirect_reasons)
- [`redirect_urls`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-reqmeta-redirect_urls)
- [`referrer_policy`](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-reqmeta-referrer_policy)



### bindaddress[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#bindaddress)

用于执行请求的出站 IP 地址。



### download_timeout[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#download-timeout)

下载器在超时前等待的时间（秒）。另请参见：[`DOWNLOAD_TIMEOUT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_TIMEOUT)。



### download_latency[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#download-latency)

从请求开始（即 HTTP 消息通过网络发送）到获取响应所花费的时间。这个 meta 键只在响应下载完成后可用。虽然大多数其他 meta 键用于控制 Scrapy 的行为，但这个键应被视为只读。



### download_fail_on_dataloss[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#download-fail-on-dataloss)

是否在响应损坏时失败。参见：[`DOWNLOAD_FAIL_ON_DATALOSS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_FAIL_ON_DATALOSS)。



### max_retry_times[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#max-retry-times)

这个 meta 键用于设置每个请求的重试次数。初始化时，[`max_retry_times`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-max_retry_times) meta 键的优先级高于 [`RETRY_TIMES`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_TIMES) 设置。



## 9.3 停止下载响应[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#stopping-the-download-of-a-response)

从 [`bytes_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.bytes_received) 或 [`headers_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.headers_received) 信号的处理程序中引发 [`StopDownload`](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.StopDownload) 异常将停止给定响应的下载。参见以下示例：

```
import scrapy


class StopSpider(scrapy.Spider):
    name = "stop"
    start_urls = ["https://docs.scrapy.net.cn/en/latest/"]

    @classmethod
    def from_crawler(cls, crawler):
        spider = super().from_crawler(crawler)
        crawler.signals.connect(
            spider.on_bytes_received, signal=scrapy.signals.bytes_received
        )
        return spider

    def parse(self, response):
        # 'last_chars' show that the full response was not downloaded
        yield {"len": len(response.text), "last_chars": response.text[-40:]}

    def on_bytes_received(self, data, request, spider):
        raise scrapy.exceptions.StopDownload(fail=False)
```

这会产生以下输出：

```
2020-05-19 17:26:12 [scrapy.core.engine] INFO: Spider opened
2020-05-19 17:26:12 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2020-05-19 17:26:13 [scrapy.core.downloader.handlers.http11] DEBUG: Download stopped for <GET https://docs.scrapy.org/en/latest/> from signal handler StopSpider.on_bytes_received
2020-05-19 17:26:13 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://docs.scrapy.org/en/latest/> (referer: None) ['download_stopped']
2020-05-19 17:26:13 [scrapy.core.scraper] DEBUG: Scraped from <200 https://docs.scrapy.org/en/latest/>
{'len': 279, 'last_chars': 'dth, initial-scale=1.0">\n  \n  <title>Scr'}
2020-05-19 17:26:13 [scrapy.core.engine] INFO: Closing spider (finished)
```

默认情况下，结果响应由其相应的错误回调处理。要像本例一样调用其回调而不是错误回调，请将 `fail=False` 传递给 [`StopDownload`](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.StopDownload) 异常。



## 9.4 Request 子类[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-subclasses)

以下是内置的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 子类列表。您也可以继承它来实现您自己的自定义功能。

### FormRequest 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#formrequest-objects)

FormRequest 类扩展了基本的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 类，提供了处理 HTML 表单的功能。它使用 [lxml.html forms](https://lxml.de/lxmlhtml.html#forms) 根据 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象中的表单数据预填充表单字段。

- *class*scrapy.FormRequest(*url***[**, *formdata*, *...***]**)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest)

  [`FormRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest) 类为 `__init__()` 方法添加了一个新的关键字参数。其余参数与 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 类相同，在此不再赘述。参数:**formdata** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict) *or* [*collections.abc.Iterable*](https://docs.pythonlang.cn/3/library/collections.abc.html#collections.abc.Iterable)) – 是一个字典（或 (键, 值) 元组的可迭代对象），包含 HTML 表单数据，这些数据将被进行 URL 编码并赋值给请求的 body。[`FormRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest) 对象除了支持标准的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 方法外，还支持以下类方法：*classmethod*from_response(*response***[**, *formname=None*, *formid=None*, *formnumber=0*, *formdata=None*, *formxpath=None*, *formcss=None*, *clickdata=None*, *dont_click=False*, *...***]**)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest.from_response)返回一个新的 [`FormRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest) 对象，其表单字段值预填充了给定响应中包含的 HTML `<form>` 元素中的值。有关示例，请参阅 [使用 FormRequest.from_response() 模拟用户登录](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-userlogin)。默认情况下，策略是自动模拟点击任何看起来可点击的表单控件，例如 `<input type="submit">`。尽管这非常方便，并且通常是期望的行为，但有时它可能会导致难以调试的问题。例如，在使用通过 javascript 填充和/或提交的表单时，默认的 [`from_response()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest.from_response) 行为可能不是最合适的。要禁用此行为，可以将 `dont_click` 参数设置为 `True`。另外，如果您想更改被点击的控件（而不是禁用它），您也可以使用 `clickdata` 参数。注意由于 [lxml 中的一个错误](https://bugs.launchpad.net/lxml/+bug/1665241)，在选项值中包含前导或尾随空白的 select 元素上使用此方法将不起作用，该错误应在 lxml 3.8 及更高版本中修复。参数:**response** ([`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象) – 包含将用于预填充表单字段的 HTML 表单的响应**formname** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 如果给定，将使用 name 属性设置为此值的表单。**formid** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 如果给定，将使用 id 属性设置为此值的表单。**formxpath** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 如果给定，将使用第一个匹配 xpath 的表单。**formcss** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 如果给定，将使用第一个匹配 css 选择器的表单。**formnumber** ([*int*](https://docs.pythonlang.cn/3/library/functions.html#int)) – 当响应包含多个表单时要使用的表单编号。第一个（也是默认值）是 `0`。**formdata** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 要在表单数据中覆盖的字段。如果一个字段已存在于响应的 `<form>` 元素中，则其值将被此参数中传递的值覆盖。如果此参数中传递的值是 `None`，则该字段将不会包含在请求中，即使它存在于响应的 `<form>` 元素中。**clickdata** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 用于查找被点击控件的属性。如果未给定，则将模拟点击第一个可点击元素来提交表单数据。除了 html 属性外，还可以通过相对于表单内其他可提交输入的从零开始的索引（通过 `nr` 属性）来识别控件。**dont_click** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 如果为 True，将不点击任何元素直接提交表单数据。此类方法的其他参数直接传递给 [`FormRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest) 的 `__init__()` 方法。

### 请求使用示例[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#request-usage-examples)

#### 使用 FormRequest 通过 HTTP POST 发送数据[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#using-formrequest-to-send-data-via-http-post)

如果您想在爬虫中模拟 HTML 表单 POST 并发送一些键值字段，您可以像这样从爬虫中返回一个 [`FormRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest) 对象

```
return [
    FormRequest(
        url="http://www.example.com/post/action",
        formdata={"name": "John Doe", "age": "27"},
        callback=self.after_post,
    )
]
```



#### 使用 FormRequest.from_response() 模拟用户登录[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#using-formrequest-from-response-to-simulate-a-user-login)

网站通常会通过 `<input type="hidden">` 元素提供预填充的表单字段，例如会话相关数据或身份验证令牌（用于登录页面）。在抓取时，您会希望这些字段被自动预填充，并且只覆盖其中几个，例如用户名和密码。您可以使用 [`FormRequest.from_response()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.FormRequest.from_response) 方法来完成此工作。以下是使用此方法的一个爬虫示例

```
import scrapy


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class LoginSpider(scrapy.Spider):
    name = "example.com"
    start_urls = ["http://www.example.com/users/login.php"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"username": "john", "password": "secret"},
            callback=self.after_login,
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
```

### JsonRequest[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#jsonrequest)

JsonRequest 类扩展了基本的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 类，增加了处理 JSON 请求的功能。

- *class*scrapy.http.JsonRequest(*url***[**, *... data*, *dumps_kwargs***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/request/json_request.html#JsonRequest)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonRequest)

  [`JsonRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonRequest) 类在 `__init__()` 方法中增加了两个新的关键字参数。其余参数与 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 类相同，在此不再赘述。使用 [`JsonRequest`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonRequest) 将把 `Content-Type` 请求头设置为 `application/json`，将 `Accept` 请求头设置为 `application/json, text/javascript, */*; q=0.01`参数:**data** ([*object*](https://docs.pythonlang.cn/3/library/functions.html#object)) – 任何需要进行 JSON 编码并分配给 body 的可 JSON 序列化对象。如果提供了 [`body`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.body) 参数，则此参数将被忽略。如果未提供 [`body`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.body) 参数但提供了 `data` 参数，则 [`method`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.method) 将自动设置为 `'POST'`。**dumps_kwargs** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 将传递给底层 [`json.dumps()`](https://docs.pythonlang.cn/3/library/json.html#json.dumps) 方法的参数，该方法用于将数据序列化为 JSON 格式。attributes*: [tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), ...]**= ('url', 'callback', 'method', 'headers', 'body', 'cookies', 'meta', 'encoding', 'priority', 'dont_filter', 'errback', 'flags', 'cb_kwargs', 'dumps_kwargs')*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonRequest.attributes)一个由 [`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str) 对象组成的元组，包含类中所有公共属性的名称，这些属性也是 `__init__()` 方法的关键字参数。目前被 [`Request.replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.replace), [`Request.to_dict()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.to_dict) 和 [`request_from_dict()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.utils.request.request_from_dict) 使用。

### JsonRequest 使用示例[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#jsonrequest-usage-example)

发送带有 JSON 有效载荷的 JSON POST 请求

```
data = {
    "name1": "value1",
    "name2": "value2",
}
yield JsonRequest(url="http://www.example.com/post/action", data=data)
```

## 9.5 Response 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#response-objects)

- *class*scrapy.http.Response(**args: Any*, ***kwargs: Any*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)

  表示 HTTP 响应的对象，通常由下载器（Downloader）下载并提供给爬虫（Spiders）进行处理。参数:**url** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 此响应的 URL**status** ([*int*](https://docs.pythonlang.cn/3/library/functions.html#int)) – 响应的 HTTP 状态。默认为 `200`。**headers** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – 此响应的头部信息。字典值可以是字符串（对于单值头部）或列表（对于多值头部）。**body** ([*bytes*](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes)) – 响应正文。要以字符串形式访问解码后的文本，请使用具有编码感知能力的 [Response 子类](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-response-subclasses)（例如 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse)）中的 `response.text`。**flags** ([*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 一个列表，包含 [`Response.flags`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.flags) 属性的初始值。如果给定，该列表将被浅复制。**request** ([*scrapy.Request*](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)) – [`Response.request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request) 属性的初始值。这表示生成此响应的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)。**certificate** ([*twisted.internet.ssl.Certificate*](https://docs.twisted.org.cn/en/stable/api/twisted.internet.ssl.Certificate.html)) – 表示服务器 SSL 证书的对象。**ip_address** ([`ipaddress.IPv4Address`](https://docs.pythonlang.cn/3/library/ipaddress.html#ipaddress.IPv4Address) 或 [`ipaddress.IPv6Address`](https://docs.pythonlang.cn/3/library/ipaddress.html#ipaddress.IPv6Address)) – 响应来自的服务器的 IP 地址。**protocol** ([`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 用于下载响应的协议。例如：“HTTP/1.0”、“HTTP/1.1”、“h2”*2.0.0 版新增：* `certificate` 参数。*2.1.0 版新增：* `ip_address` 参数。*2.5.0 版新增：* `protocol` 参数。url[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.url)包含响应 URL 的字符串。此属性是只读的。要更改 Response 的 URL，请使用 [`replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.replace)。status[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.status)表示响应 HTTP 状态的整数。示例：`200`、`404`。headers[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.headers)一个类似字典（`scrapy.http.headers.Headers`）的对象，包含响应头部信息。可以使用 `get()` 访问值以返回具有指定名称的第一个头部值，或使用 `getlist()` 返回具有指定名称的所有头部值。例如，此调用将返回头部中的所有 cookie`response.headers.getlist('Set-Cookie') `body[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.body)响应正文（以 bytes 为单位）。如果您想要字符串形式的正文，请使用 [`TextResponse.text`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.text)（仅在 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 及其子类中可用）。此属性是只读的。要更改 Response 的正文，请使用 [`replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.replace)。request[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request)生成此响应的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。此属性在 Scrapy 引擎中分配，在响应和请求通过所有 [Downloader Middlewares](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware) 后。特别地，这意味着HTTP 重定向将从重定向之前的请求创建一个新请求。它拥有与原始请求大部分相同的元数据和属性，并被分配给重定向后的响应，而不是原始请求的传播。`Response.request.url` 并不总是等于 `Response.url`此属性仅在爬虫代码和 [Spider Middlewares](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware) 中可用，但在 Downloader Middlewares（尽管您可以通过其他方式在那里获得 Request）和 [`response_downloaded`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-response_downloaded) 信号的处理程序中不可用。meta[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.meta)[`Response.request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request) 对象的 [`meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 属性的快捷方式（即 `self.request.meta`）。与 [`Response.request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request) 属性不同，[`Response.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.meta) 属性会沿着重定向和重试传播，因此您将获得从爬虫发送的原始 [`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta)。另请参阅[`Request.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.meta) 属性cb_kwargs[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.cb_kwargs)**2.0 版新增。**[`Response.request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request) 对象的 [`cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 属性的快捷方式（即 `self.request.cb_kwargs`）。与 [`Response.request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.request) 属性不同，[`Response.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.cb_kwargs) 属性会沿着重定向和重试传播，因此您将获得从爬虫发送的原始 [`Request.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs)。另请参阅[`Request.cb_kwargs`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.cb_kwargs) 属性flags[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.flags)包含此响应标志的列表。标志是用于标记 Response 的标签。例如：`'cached'`、`'redirected`’ 等。它们显示在 Response 的字符串表示中（`__str__()` 方法），引擎使用它进行日志记录。certificate[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.certificate)**2.0.0 版新增。**一个 [`twisted.internet.ssl.Certificate`](https://docs.twisted.org.cn/en/stable/api/twisted.internet.ssl.Certificate.html) 对象，表示服务器的 SSL 证书。仅针对 `https` 响应填充，否则为 `None`。ip_address[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.ip_address)**2.1.0 版新增。**响应来自的服务器的 IP 地址。当前此属性仅由 HTTP 1.1 下载处理程序填充，即对于 `http(s)` 响应。对于其他处理程序，[`ip_address`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.ip_address) 始终为 `None`。protocol[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.protocol)**2.5.0 版新增。**用于下载响应的协议。例如：“HTTP/1.0”、“HTTP/1.1”当前此属性仅由 HTTP 下载处理程序填充，即对于 `http(s)` 响应。对于其他处理程序，[`protocol`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.protocol) 始终为 `None`。attributes*: [tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), ...]**= ('url', 'status', 'headers', 'body', 'flags', 'request', 'certificate', 'ip_address', 'protocol')*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.attributes)一个由 [`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str) 对象组成的元组，包含类中所有公共属性的名称，这些属性也是 `__init__()` 方法的关键字参数。当前由 [`Response.replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.replace) 使用。copy()[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response.copy)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.copy)返回此 Response 的一个新副本。replace(**[***url*, *status*, *headers*, *body*, *request*, *flags*, *cls***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response.replace)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.replace)返回一个 Response 对象，其成员与原对象相同，但通过指定的关键字参数赋予新值的成员除外。[`Response.meta`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.meta) 属性默认被复制。urljoin(*url*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response.urljoin)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.urljoin)通过将 Response 的 [`url`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.url) 与可能的相对 url 组合来构造一个绝对 url。这是对 [`urljoin()`](https://docs.pythonlang.cn/3/library/urllib.parse.html#urllib.parse.urljoin) 的包装，它仅仅是执行此调用的一个别名`urllib.parse.urljoin(response.url, url) `follow(*url: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [Link](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link)*, *callback: CallbackT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *method: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) = 'GET'*, *headers: Mapping[AnyStr, Any] | Iterable[[tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[AnyStr, Any]] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *body: [bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cookies: CookiesT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *meta: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *encoding: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = 'utf-8'*, *priority: [int](https://docs.pythonlang.cn/3/library/functions.html#int) = 0*, *dont_filter: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*, *errback: Callable[[Failure], Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cb_kwargs: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *flags: [list](https://docs.pythonlang.cn/3/library/stdtypes.html#list)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response.follow)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.follow)返回一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 实例，用于跟踪一个链接 `url`。它接受与 `Request.__init__()` 方法相同的参数，但 `url` 可以是相对 URL 或 [`Link`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) 对象，而不仅仅是绝对 URL。[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 提供了 [`follow()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow) 方法，除了支持绝对/相对 URL 和 Link 对象外，还支持选择器。*2.0 版本加入:* 参数 *flags*。follow_all(*urls: Iterable[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [Link](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link)]*, *callback: CallbackT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *method: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) = 'GET'*, *headers: Mapping[AnyStr, Any] | Iterable[[tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[AnyStr, Any]] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *body: [bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cookies: CookiesT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *meta: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *encoding: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = 'utf-8'*, *priority: [int](https://docs.pythonlang.cn/3/library/functions.html#int) = 0*, *dont_filter: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*, *errback: Callable[[Failure], Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cb_kwargs: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *flags: [list](https://docs.pythonlang.cn/3/library/stdtypes.html#list)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ Iterable[[Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)][[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response.html#Response.follow_all)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.follow_all)**2.0 版新增。**返回一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 实例的可迭代对象，用于跟踪 `urls` 中的所有链接。它接受与 `Request.__init__()` 方法相同的参数，但 `urls` 的元素可以是相对 URL 或 [`Link`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) 对象，而不仅仅是绝对 URL。[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 提供了 [`follow_all()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow_all) 方法，除了支持绝对/相对 URL 和 Link 对象外，还支持选择器。



## 9.6 Response 子类[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#response-subclasses)

以下是可用的内置 Response 子类列表。您也可以子类化 Response 类来实现您自己的功能。

### TextResponse 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#textresponse-objects)

- *class*scrapy.http.TextResponse(*url***[**, *encoding***[**, *...***]****]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse)

  [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 对象在基础 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 类（该类仅用于二进制数据，如图像、声音或任何媒体文件）的基础上增加了编码能力。[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 对象除了基础 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象外，还支持一个新的 `__init__()` 方法参数。其余功能与 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 类相同，此处不再赘述。参数:**encoding** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 一个字符串，包含用于此响应的编码。如果您使用字符串作为正文创建一个 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 对象，它将被转换为使用此编码编码的字节。如果 *encoding* 是 `None`（默认），编码将改为在响应头和正文中查找。[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 对象除了标准 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象外，还支持以下属性：text[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.text)响应体，作为字符串。与 `response.body.decode(response.encoding)` 相同，但结果会在首次调用后缓存，因此您可以多次访问 `response.text` 而没有额外开销。注意`str(response.body)` 不是将响应体转换为字符串的正确方法`str(b"body") "b'body'" `encoding[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.encoding)一个字符串，包含此响应的编码。编码通过尝试以下机制按顺序解析：在 `__init__()` 方法的 `encoding` 参数中传递的编码在 Content-Type HTTP 头中声明的编码。如果此编码无效（即未知），则忽略并尝试下一个解析机制。在响应体中声明的编码。`TextResponse` 类对此不提供任何特殊功能。但是，[`HtmlResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.HtmlResponse) 和 [`XmlResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.XmlResponse) 类提供了。通过查看响应体推断出的编码。这是更脆弱的方法，但也是最后尝试的方法。selector[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.selector)一个以响应为目标的 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 实例。选择器在首次访问时延迟实例化。attributes*: [tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), ...]**= ('url', 'status', 'headers', 'body', 'flags', 'request', 'certificate', 'ip_address', 'protocol', 'encoding')*[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.attributes)一个由 [`str`](https://docs.pythonlang.cn/3/library/stdtypes.html#str) 对象组成的元组，包含类中所有公共属性的名称，这些属性也是 `__init__()` 方法的关键字参数。当前由 [`Response.replace()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.replace) 使用。[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 对象除了标准 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 方法外，还支持以下方法：jmespath(*query*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.jmespath)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.jmespath)指向 `TextResponse.selector.jmespath(query)` 的快捷方式`response.jmespath('object.[*]') `xpath(*query*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.xpath)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.xpath)指向 `TextResponse.selector.xpath(query)` 的快捷方式`response.xpath('//p') `css(*query*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.css)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.css)指向 `TextResponse.selector.css(query)` 的快捷方式`response.css('p') `follow(*url: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [Link](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) | parsel.Selector*, *callback: CallbackT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *method: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) = 'GET'*, *headers: Mapping[AnyStr, Any] | Iterable[[tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[AnyStr, Any]] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *body: [bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cookies: CookiesT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *meta: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *encoding: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *priority: [int](https://docs.pythonlang.cn/3/library/functions.html#int) = 0*, *dont_filter: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*, *errback: Callable[[Failure], Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cb_kwargs: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *flags: [list](https://docs.pythonlang.cn/3/library/stdtypes.html#list)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.follow)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow)返回一个 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 实例，用于跟踪一个链接 `url`。它接受与 `Request.__init__()` 方法相同的参数，但 `url` 不仅可以是绝对 URL，还可以是相对 URL一个 [`Link`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) 对象，例如 [Link Extractors](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#topics-link-extractors) 的结果一个 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 对象，用于 `<link>` 或 `<a>` 元素，例如 `response.css('a.my_link')[0]`一个属性 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector)（不是 SelectorList），例如 `response.css('a::attr(href)')[0]` 或 `response.xpath('//img/@src')[0]`参阅 [创建请求的快捷方式](https://docs.scrapy.net.cn/en/latest/intro/tutorial.html#response-follow-example) 以获取用法示例。follow_all(*urls: Iterable[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [Link](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link)] | parsel.SelectorList | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *callback: CallbackT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *method: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) = 'GET'*, *headers: Mapping[AnyStr, Any] | Iterable[[tuple](https://docs.pythonlang.cn/3/library/stdtypes.html#tuple)[AnyStr, Any]] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *body: [bytes](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cookies: CookiesT | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *meta: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *encoding: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *priority: [int](https://docs.pythonlang.cn/3/library/functions.html#int) = 0*, *dont_filter: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*, *errback: Callable[[Failure], Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *cb_kwargs: [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str), Any] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *flags: [list](https://docs.pythonlang.cn/3/library/stdtypes.html#list)[[str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *css: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *xpath: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ Iterable[[Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)][[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.follow_all)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow_all)一个生成器，用于生成 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 实例以追踪 `urls` 中的所有链接。它接受与 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 的 `__init__()` 方法相同的参数，但每个 `urls` 元素不需要是绝对 URL，可以是以下任一类型相对 URL一个 [`Link`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) 对象，例如 [Link Extractors](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#topics-link-extractors) 的结果一个 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 对象，用于 `<link>` 或 `<a>` 元素，例如 `response.css('a.my_link')[0]`一个属性 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector)（不是 SelectorList），例如 `response.css('a::attr(href)')[0]` 或 `response.xpath('//img/@src')[0]`此外，接受 `css` 和 `xpath` 参数可在 `follow_all()` 方法内部执行链接提取（仅接受 `urls`、`css` 和 `xpath` 中的一个参数）。注意，当将 `SelectorList` 作为 `urls` 参数的实参传递，或使用 `css` 或 `xpath` 参数时，此方法不会为无法获取链接的选择器生成请求（例如，没有 `href` 属性的锚标签）。json()[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.json)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.json)*2.2 版本新增。*将 JSON 文档反序列化为 Python 对象。返回从反序列化 JSON 文档中获得的 Python 对象。结果会在首次调用后缓存。urljoin(*url*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/text.html#TextResponse.urljoin)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.urljoin)通过将 Response 的基本 URL 与可能的相对 URL 组合来构建绝对 URL。基本 URL 应从 `<base>` 标签中提取，如果没有此类标签，则使用 [`Response.url`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.url)。

### HtmlResponse 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#htmlresponse-objects)

- *class*scrapy.http.HtmlResponse(*url***[**, *...***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/html.html#HtmlResponse)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.HtmlResponse)

  [`HtmlResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.HtmlResponse) 类是 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 的子类，通过查看 HTML [meta http-equiv](https://w3schools.org.cn/TAGS/att_meta_http_equiv.asp) 属性来添加编码自动发现支持。参阅 [`TextResponse.encoding`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.encoding)。

### XmlResponse 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#xmlresponse-objects)

- *class*scrapy.http.XmlResponse(*url***[**, *...***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/xml.html#XmlResponse)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.XmlResponse)

  [`XmlResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.XmlResponse) 类是 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 的子类，通过查看 XML 声明行来添加编码自动发现支持。参阅 [`TextResponse.encoding`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.encoding)。

### JsonResponse 对象[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#jsonresponse-objects)

- *class*scrapy.http.JsonResponse(*url***[**, *...***]**)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/http/response/json.html#JsonResponse)[🔗](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonResponse)

  [`JsonResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.JsonResponse) 类是 [`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 的子类，当响应在其 Content-Type 头部中具有 [JSON MIME 类型](https://mimesniff.spec.whatwg.org/#json-mime-type)时使用。

# 10 链接提取器

链接提取器是一个从响应中提取链接的对象。

[`LxmlLinkExtractor`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor) 的 `__init__` 方法接受用于确定可提取链接的设置。[`LxmlLinkExtractor.extract_links`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor.extract_links) 从一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象返回匹配的 [`Link`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.link.Link) 对象的列表。

链接提取器在 [`CrawlSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider) 爬虫中通过一组 [`Rule`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Rule) 对象使用。

您也可以在常规爬虫中使用链接提取器。例如，您可以在爬虫中将 [`LinkExtractor`](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor) 实例化为一个类变量，并在爬虫回调函数中使用它

```
def parse(self, response):
    for link in self.link_extractor.extract_links(response):
        yield Request(link.url, callback=self.parse)
```

## 链接提取器参考[🔗](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#module-scrapy.linkextractors)

链接提取器类是 `scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor`。为方便起见，它也可以导入为 `scrapy.linkextractors.LinkExtractor`

```
from scrapy.linkextractors import LinkExtractor
```

### LxmlLinkExtractor[🔗](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#module-scrapy.linkextractors.lxmlhtml)

- *class*scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(*allow=()*, *deny=()*, *allow_domains=()*, *deny_domains=()*, *deny_extensions=None*, *restrict_xpaths=()*, *restrict_css=()*, *tags=('a', 'area')*, *attrs=('href',)*, *canonicalize=False*, *unique=True*, *process_value=None*, *strip=True*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/linkextractors/lxmlhtml.html#LxmlLinkExtractor)[🔗](https://docs.scrapy.net.cn/en/latest/topics/link-extractors.html#scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor)

  LxmlLinkExtractor 是推荐的链接提取器，具有方便的过滤选项。它使用 lxml 强大的 HTMLParser 实现。参数：**allow** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 一个正则表达式（或正则表达式列表），绝对 URL 必须匹配该表达式才能被提取。如果未给出（或为空），它将匹配所有链接。**deny** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 一个正则表达式（或正则表达式列表），绝对 URL 必须匹配该表达式才能被排除（即不提取）。它优先于 `allow` 参数。如果未给出（或为空），它将不排除任何链接。**allow_domains** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 单个值或包含将被考虑提取链接的域名的字符串列表**deny_domains** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 单个值或包含将不被考虑提取链接的域名的字符串列表**deny_extensions** ([*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) –单个值或字符串列表，包含在提取链接时应忽略的扩展名。如果未给出，它将默认为 `scrapy.linkextractors.IGNORED_EXTENSIONS`。*在 2.0 版本中更改:* `IGNORED_EXTENSIONS` 现在包含 `7z`, `7zip`, `apk`, `bz2`, `cdr`, `dmg`, `ico`, `iso`, `tar`, `tar.gz`, `webm`, 和 `xz`。**restrict_xpaths** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 是一个 XPath（或 XPath 列表），定义了响应中应从中提取链接的区域。如果给出，将仅扫描由这些 XPath 选择的文本以查找链接。**restrict_css** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 一个 CSS 选择器（或选择器列表），定义了响应中应从中提取链接的区域。其行为与 `restrict_xpaths` 相同。**restrict_text** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 一个正则表达式（或正则表达式列表），链接文本必须匹配该表达式才能被提取。如果未给出（或为空），它将匹配所有链接。如果给出了正则表达式列表，则链接将至少匹配其中一个时被提取。**tags** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *或* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 提取链接时要考虑的标签或标签列表。默认为 `('a', 'area')`。**attrs** ([*列表*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) — 在查找要提取的链接时，一个或多个应被考虑的属性 (仅适用于 `tags` 参数中指定的那些标签)。默认为 `('href',)`**canonicalize** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 对每个提取的 URL 进行规范化处理（使用 `w3lib.url.canonicalize_url`）。默认为 `False`。请注意，`canonicalize_url` 用于重复检查；它可能会改变服务器端可见的 URL，因此对于经过规范化和原始 URL 的请求，响应可能会不同。如果您使用 LinkExtractor 来跟踪链接，保持默认的 `canonicalize=False` 会更健壮。**unique** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 是否应对提取的链接应用重复过滤。**process_value** ([*collections.abc.Callable*](https://docs.pythonlang.cn/3/library/collections.abc.html#collections.abc.Callable)) –一个函数，它接收从扫描的标签和属性中提取的每个值，可以修改该值并返回一个新值，或者返回 `None` 以完全忽略该链接。如果未给出，`process_value` 默认为 `lambda x: x`。例如，要从以下代码中提取链接`<a href="javascript:goToPage('../other/page.html'); return false">Link text</a> `您可以在 `process_value` 中使用以下函数`def process_value(value):    m = re.search(r"javascript:goToPage\('(.*?)'", value)    if m:        return m.group(1) `**strip** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 是否从提取的属性中去除空白字符。根据 HTML5 标准，必须去除 ``、`` 和许多其他元素的 `href` 属性、`![img]()`、``

# 11 设置

Scrapy 设置允许您自定义所有 Scrapy 组件的行为，包括核心、扩展、pipeline 以及 Spider 本身。

设置的基础设施提供了一个全局的键值映射命名空间，代码可以使用它来获取配置值。设置可以通过不同的机制来填充，这些机制将在下面介绍。

设置也是选择当前活动的 Scrapy 项目（如果您有多个项目）的机制。

有关可用内置设置的列表，请参阅：[内置设置参考](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-ref)。



## 指定设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#designating-the-settings)

使用 Scrapy 时，您必须告诉它您正在使用哪些设置。您可以通过使用环境变量 `SCRAPY_SETTINGS_MODULE` 来实现这一点。

`SCRAPY_SETTINGS_MODULE` 的值应采用 Python 路径语法，例如 `myproject.settings`。请注意，设置模块应位于 Python 的 [导入搜索路径](https://docs.pythonlang.cn/3/tutorial/modules.html#tut-searchpath) 中。



## 填充设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#populating-the-settings)

设置可以使用不同的机制来填充，每种机制具有不同的优先级

> 1. [命令行设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#cli-settings) (最高优先级)
> 2. [Spider 设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-settings)
> 3. [项目设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#project-settings)
> 4. [Add-on 设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#addon-settings)
> 5. [命令特定的默认设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#cmd-default-settings)
> 6. [全局默认设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings) (最低优先级)



### 1. 命令行设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#command-line-settings)

命令行中设置的设置具有最高优先级，会覆盖任何其他设置。

您可以使用 `-s`（或 `--set`）命令行选项显式覆盖一个或多个设置。

示例

```
scrapy crawl myspider -s LOG_LEVEL=INFO -s LOG_FILE=scrapy.log
```



### 2. Spider 设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-settings)

[Spiders](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#topics-spiders) 可以定义自己的设置，这些设置将具有更高的优先级并覆盖项目设置。

注意

[爬虫前设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#pre-crawler-settings) 不能按 spider 定义，并且 [reactor 设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#reactor-settings) 在 [在同一进程中运行多个 spider](https://docs.scrapy.net.cn/en/latest/topics/practices.html#run-multiple-spiders) 时，不应按 spider 设置不同的值。

实现这一点的一种方法是设置它们的 [`custom_settings`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.custom_settings) 属性

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"

    custom_settings = {
        "SOME_SETTING": "some value",
    }
```

通常最好实现 [`update_settings()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.update_settings) 方法，并且在那里设置的设置应明确使用 `"spider"` 优先级

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("SOME_SETTING", "some value", priority="spider")
```

*版本 2.11 新增。*

也可以在 [`from_crawler()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.from_crawler) 方法中修改设置，例如根据 [spider 参数](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#spiderargs) 或其他逻辑

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        if "some_argument" in kwargs:
            spider.settings.set(
                "SOME_SETTING", kwargs["some_argument"], priority="spider"
            )
        return spider
```



### 3. 项目设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#project-settings)

Scrapy 项目包含一个设置模块，通常是一个名为 `settings.py` 的文件，您应该在该文件中填充适用于所有 spider 的大多数设置。

另请参阅

[指定设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-module-envvar)



### 4. Add-on 设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#add-on-settings)

[Add-ons](https://docs.scrapy.net.cn/en/latest/topics/addons.html#topics-addons) 可以修改设置。如果可能，它们应使用 `"addon"` 优先级来完成此操作。



### 5. 命令特定的默认设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#command-specific-default-settings)

每个 [Scrapy 命令](https://docs.scrapy.net.cn/en/latest/topics/commands.html#topics-commands) 都可以有自己的默认设置，这些设置会覆盖 [全局默认设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings)。

这些命令特定的默认设置在每个命令类的 `default_settings` 属性中指定。

### 6. 全局默认设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-global-settings)

`scrapy.settings.default_settings` 模块定义了一些 [内置设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-ref) 的全局默认值。

注意

[`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 会生成一个 `settings.py` 文件，该文件将一些设置设置为不同的值。

设置的参考文档会指示默认值（如果存在）。如果 [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 设置了一个值，则该值被记录为默认值，而来自 `scrapy.settings.default_settings` 的值被记录为“备用值”（fallback）。

## 与 pickle 的兼容性[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#compatibility-with-pickle)

设置值必须是 [可 pickle 化](https://docs.pythonlang.cn/3/library/pickle.html#pickle-picklable) 的。

## 导入路径和类[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#import-paths-and-classes)

*版本 2.4.0 新增。*

当设置引用 Scrapy 需要导入的可调用对象（例如类或函数）时，您可以通过两种不同的方式指定该对象

- 作为包含该对象导入路径的字符串
- 作为对象本身

例如

```
from mybot.pipelines.validate import ValidateMyItem

ITEM_PIPELINES = {
    # passing the classname...
    ValidateMyItem: 300,
    # ...equals passing the class path
    "mybot.pipelines.validate.ValidateMyItem": 300,
}
```

注意

不支持传递不可调用对象。

## 如何访问设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#how-to-access-settings)

在 spider 中，可以通过 `self.settings` 访问设置

```
class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["http://example.com"]

    def parse(self, response):
        print(f"Existing settings: {self.settings.attributes.keys()}")
```

注意

`settings` 属性在 spider 初始化后在基础 Spider 类中设置。如果您想在初始化之前使用设置（例如，在 spider 的 `__init__()` 方法中），您需要覆盖 [`from_crawler()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.from_crawler) 方法。

[组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components) 也可以 [访问设置](https://docs.scrapy.net.cn/en/latest/topics/components.html#component-settings)。

`settings` 对象可以像 [`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict) 一样使用（例如 `settings["LOG_ENABLED"]`）。但是，为了支持非字符串设置值（可能从命令行作为字符串传递），建议使用 [`Settings`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.settings.Settings) API 提供的方法之一。



## 组件优先级字典[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#component-priority-dictionaries)

一个 **组件优先级字典** 是一个 [`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)，其中键是 [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components)，值是组件优先级。例如

```
{
    "path.to.ComponentA": None,
    ComponentB: 100,
}
```

组件可以指定为类对象或通过导入路径指定。

警告

组件优先级字典是常规的 [`dict`](https://docs.pythonlang.cn/3/library/stdtypes.html#dict) 对象。请注意不要多次定义同一组件，例如使用不同的导入路径字符串或同时定义导入路径和 [`type`](https://docs.pythonlang.cn/3/library/functions.html#type) 对象。

优先级可以是 [`int`](https://docs.pythonlang.cn/3/library/functions.html#int) 或 [`None`](https://docs.pythonlang.cn/3/library/constants.html#None)。

优先级为 1 的组件会比优先级为 2 的组件 *更早* 执行。然而，更早执行的具体含义取决于对应的设置。例如，在 [`DOWNLOADER_MIDDLEWARES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES) 设置中，组件的 [`process_request()`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.DownloaderMiddleware.process_request) 方法会在后续组件的方法之前执行，但其 [`process_response()`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.DownloaderMiddleware.process_response) 方法会在后续组件的方法之后执行。

优先级为 [`None`](https://docs.pythonlang.cn/3/library/constants.html#None) 的组件会被禁用。

一些组件优先级字典会与一些内置值合并。例如，[`DOWNLOADER_MIDDLEWARES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES) 会与 [`DOWNLOADER_MIDDLEWARES_BASE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES_BASE) 合并。这就是 [`None`](https://docs.pythonlang.cn/3/library/constants.html#None) 的便利之处，它允许您在常规设置中禁用基本设置中的组件

```
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.offsite.OffsiteMiddleware": None,
}
```

## 特殊设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#special-settings)

以下设置与其他所有设置的工作方式略有不同。



### 爬虫前设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#pre-crawler-settings)

**爬虫前设置** 是在创建 [`Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 对象之前使用的设置。

这些设置不能 [从 spider 中设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-settings)。

这些设置包括 [`SPIDER_LOADER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_LOADER_CLASS) 以及相应 [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components) 使用的设置，例如默认组件的 [`SPIDER_MODULES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_MODULES) 和 [`SPIDER_LOADER_WARN_ONLY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_LOADER_WARN_ONLY)。



### Reactor 设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#reactor-settings)

**Reactor 设置** 是与 [Twisted reactor](https://docs.twisted.org.cn/en/stable/core/howto/reactor-basics.html) 相关联的设置。

这些设置可以从 spider 中定义。但是，由于每个进程只能使用 1 个 reactor，因此在 [在同一进程中运行多个 spider](https://docs.scrapy.net.cn/en/latest/topics/practices.html#run-multiple-spiders) 时，这些设置不能按 spider 使用不同的值。

一般来说，如果不同的 spider 定义了不同的值，则使用第一个定义的值。但是，如果两个 spider 请求不同的 reactor，则会引发异常。

这些设置包括

- [`ASYNCIO_EVENT_LOOP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-ASYNCIO_EVENT_LOOP)
- [`DNS_RESOLVER`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNS_RESOLVER) 以及相应组件使用的设置，例如默认组件的 [`DNSCACHE_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNSCACHE_ENABLED)、[`DNSCACHE_SIZE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNSCACHE_SIZE) 和 [`DNS_TIMEOUT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNS_TIMEOUT)。
- [`REACTOR_THREADPOOL_MAXSIZE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-REACTOR_THREADPOOL_MAXSIZE)
- [`TWISTED_REACTOR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-TWISTED_REACTOR)

[`ASYNCIO_EVENT_LOOP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-ASYNCIO_EVENT_LOOP) 和 [`TWISTED_REACTOR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-TWISTED_REACTOR) 在安装 reactor 时使用。其余设置在启动 reactor 时应用。



## 内置设置参考[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#built-in-settings-reference)

以下是所有可用 Scrapy 设置的列表，按字母顺序排列，以及它们的默认值和适用范围。

适用范围（如果可用）显示了该设置的使用位置，如果它与任何特定组件相关联。在这种情况下，将显示该组件的模块，通常是扩展、中间件或 pipeline。这也意味着必须启用该组件，设置才能生效。



### ADDONS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#addons)

默认值: `{}`

一个字典，包含项目中启用的 add-ons 的路径及其优先级。有关更多信息，请参阅 [Add-ons](https://docs.scrapy.net.cn/en/latest/topics/addons.html#topics-addons)。



### AWS_ACCESS_KEY_ID[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-access-key-id)

默认值: `None`

需要访问 [Amazon Web Services](https://aws.amazon.com/) 的代码（例如 [S3 feed 存储后端](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)）使用的 AWS 访问密钥。



### AWS_SECRET_ACCESS_KEY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-secret-access-key)

默认值: `None`

需要访问 [Amazon Web Services](https://aws.amazon.com/) 的代码（例如 [S3 feed 存储后端](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)）使用的 AWS 秘密密钥。



### AWS_SESSION_TOKEN[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-session-token)

默认值: `None`

需要访问 [Amazon Web Services](https://aws.amazon.com/) 的代码（例如 [S3 feed 存储后端](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)）在使用 [临时安全凭证](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html) 时使用的 AWS 安全令牌。



### AWS_ENDPOINT_URL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-endpoint-url)

默认值: `None`

用于 S3 兼容存储（例如 Minio 或 s3.scality）的端点 URL。



### AWS_USE_SSL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-use-ssl)

默认值: `None`

如果您想禁用与 S3 或 S3 兼容存储通信时的 SSL 连接，请使用此选项。默认情况下会使用 SSL。



### AWS_VERIFY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-verify)

默认值: `None`

验证 Scrapy 与 S3 或 S3 兼容存储之间的 SSL 连接。默认情况下会进行 SSL 验证。



### AWS_REGION_NAME[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#aws-region-name)

默认值: `None`

与 AWS 客户端关联的区域名称。



### ASYNCIO_EVENT_LOOP[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#asyncio-event-loop)

默认值: `None`

给定 `asyncio` 事件循环类的导入路径。

如果启用了 asyncio reactor（参见 [`TWISTED_REACTOR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-TWISTED_REACTOR)），则可以使用此设置指定要与之一起使用的 asyncio 事件循环。将此设置设置为所需 asyncio 事件循环类的导入路径。如果将此设置设置为 `None`，则将使用默认的 asyncio 事件循环。

如果您使用 [`install_reactor()`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.utils.reactor.install_reactor) 函数手动安装 asyncio reactor，则可以使用 `event_loop_path` 参数指示要使用的事件循环类的导入路径。

请注意，事件循环类必须继承自 [`asyncio.AbstractEventLoop`](https://docs.pythonlang.cn/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop)。

Caution

请注意，当使用非默认事件循环时（通过 [`ASYNCIO_EVENT_LOOP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-ASYNCIO_EVENT_LOOP) 定义或使用 [`install_reactor()`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.utils.reactor.install_reactor) 安装），Scrapy 会调用 [`asyncio.set_event_loop()`](https://docs.pythonlang.cn/3/library/asyncio-eventloop.html#asyncio.set_event_loop)，这将把指定的事件循环设置为当前 OS 线程的当前循环。



### BOT_NAME[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#bot-name)

默认值: `<项目名称>` ([备用值](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings): `'scrapybot'`)

此 Scrapy 项目实现的机器人的名称（也称为项目名称）。此名称也将用于日志记录。

使用 [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 命令创建项目时，此名称会自动填充为您的项目名称。



### CONCURRENT_ITEMS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#concurrent-items)

默认值: `100`

在 [item pipelines](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline) 中并行处理的最大并发 item 数（每个响应）。



### CONCURRENT_REQUESTS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#concurrent-requests)

默认值: `16`

Scrapy 下载器将执行的最大并发（即同时）请求数。



### CONCURRENT_REQUESTS_PER_DOMAIN[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#concurrent-requests-per-domain)

默认值: `8`

将对任何单个域名执行的最大并发（即同时）请求数。

另请参阅: [AutoThrottle 扩展](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#topics-autothrottle) 及其 [`AUTOTHROTTLE_TARGET_CONCURRENCY`](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_TARGET_CONCURRENCY) 选项。



### CONCURRENT_REQUESTS_PER_IP[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#concurrent-requests-per-ip)

默认值: `0`

将对任何单个 IP 执行的最大并发（即同时）请求数。如果非零，则忽略 [`CONCURRENT_REQUESTS_PER_DOMAIN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_DOMAIN) 设置，并使用此设置。换句话说，并发限制将按 IP 应用，而不是按域名应用。

此设置也影响 [`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY) 和 [AutoThrottle 扩展](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#topics-autothrottle)：如果 [`CONCURRENT_REQUESTS_PER_IP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_IP) 非零，则下载延迟将按 IP 执行，而不是按域名执行。



### DEFAULT_DROPITEM_LOG_LEVEL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-dropitem-log-level)

默认值: `"WARNING"`

关于丢弃 item 的消息的默认 [日志级别](https://docs.pythonlang.cn/3/library/logging.html#levels)。

当 item pipeline 的 [`process_item()`](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#process_item) 方法通过引发 [`scrapy.exceptions.DropItem`](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.DropItem) 来丢弃 item 时，会记录一条消息，默认情况下其日志级别为此设置中配置的级别。

您可以将此日志级别指定为整数（例如 `20`）、日志级别常量（例如 `logging.INFO`）或带有日志级别常量名称的字符串（例如 `"INFO"`）。

编写 item pipeline 时，您可以通过在 [`scrapy.exceptions.DropItem`](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.DropItem) 异常中设置 `scrapy.exceptions.DropItem.log_level` 来强制使用不同的日志级别。例如

```
from scrapy.exceptions import DropItem


class MyPipeline:
    def process_item(self, item, spider):
        if not item.get("price"):
            raise DropItem("Missing price data", log_level="INFO")
        return item
```



### DEFAULT_ITEM_CLASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-item-class)

默认值: `'scrapy.Item'`

在[Scrapy shell](https://docs.scrapy.net.cn/en/latest/topics/shell.html#topics-shell)中实例化项目的默认类。



### DEFAULT_REQUEST_HEADERS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-request-headers)

默认值

```
{
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}
```

Scrapy HTTP请求使用的默认头部。它们在[`DefaultHeadersMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware)中填充。

Caution

通过 `Cookie` 头部设置的cookie不会被[CookiesMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#cookies-mw)考虑。如果您需要为请求设置cookie，请使用[`Request.cookies`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)参数。这是一个已知且正在解决的当前限制。



### DEPTH_LIMIT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#depth-limit)

默认值: `0`

范围: `scrapy.spidermiddlewares.depth.DepthMiddleware`

允许对任何站点进行的最大爬取深度。如果为零，则不施加限制。



### DEPTH_PRIORITY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#depth-priority)

默认值: `0`

范围: `scrapy.spidermiddlewares.depth.DepthMiddleware`

一个整数，用于根据[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)的深度调整其[`priority`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request.priority)。

请求的优先级调整如下：

```
request.priority = request.priority - (depth * DEPTH_PRIORITY)
```

随着深度增加，`DEPTH_PRIORITY`的正值会降低请求优先级 (BFO)，而负值会提高请求优先级 (DFO)。另请参阅[Scrapy是按广度优先还是深度优先顺序爬取？](https://docs.scrapy.net.cn/en/latest/faq.html#faq-bfo-dfo)。

注意

与[`REDIRECT_PRIORITY_ADJUST`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-REDIRECT_PRIORITY_ADJUST)和[`RETRY_PRIORITY_ADJUST`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_PRIORITY_ADJUST)等其他优先级设置相比，此设置的优先级调整方式**恰好相反**。



### DEPTH_STATS_VERBOSE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#depth-stats-verbose)

默认值: `False`

范围: `scrapy.spidermiddlewares.depth.DepthMiddleware`

是否收集详细的深度统计信息。如果启用，将会在统计信息中收集每个深度的请求数量。



### DNSCACHE_ENABLED[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dnscache-enabled)

默认值: `True`

是否启用DNS内存缓存。



### DNSCACHE_SIZE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dnscache-size)

默认值: `10000`

DNS内存缓存大小。



### DNS_RESOLVER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dns-resolver)

*版本 2.0 中新增。*

默认值: `'scrapy.resolver.CachingThreadedResolver'`

用于解析DNS名称的类。默认的`scrapy.resolver.CachingThreadedResolver`通过[`DNS_TIMEOUT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNS_TIMEOUT)设置支持为DNS请求指定超时，但仅适用于IPv4地址。Scrapy提供了一个替代解析器`scrapy.resolver.CachingHostnameResolver`，它支持IPv4/IPv6地址，但不考虑[`DNS_TIMEOUT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DNS_TIMEOUT)设置。



### DNS_TIMEOUT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dns-timeout)

默认值: `60`

处理DNS查询的超时时间（秒）。支持浮点数。



### DOWNLOADER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader)

默认值: `'scrapy.core.downloader.Downloader'`

用于爬取的下载器。



### DOWNLOADER_HTTPCLIENTFACTORY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-httpclientfactory)

默认值: `'scrapy.core.downloader.webclient.ScrapyHTTPClientFactory'`

定义用于HTTP/1.0连接 (对于`HTTP10DownloadHandler`) 的Twisted `protocol.ClientFactory` 类。

注意

HTTP/1.0现在很少使用，其Scrapy支持已弃用，因此您可以安全地忽略此设置，除非您确实想使用HTTP/1.0并相应地为`http(s)`方案覆盖[`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)，即设置为`'scrapy.core.downloader.handlers.http.HTTP10DownloadHandler'`。



### DOWNLOADER_CLIENTCONTEXTFACTORY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-clientcontextfactory)

默认值: `'scrapy.core.downloader.contextfactory.ScrapyClientContextFactory'`

表示要使用的ContextFactory的类路径。

这里的“ContextFactory”是Twisted中用于SSL/TLS上下文的术语，定义了要使用的TLS/SSL协议版本、是否进行证书验证，甚至启用客户端认证（以及各种其他功能）。

注意

Scrapy默认的上下文工厂**不执行远程服务器证书验证**。这对于网页抓取通常是可以接受的。

如果您确实需要启用远程服务器证书验证，Scrapy还提供了另一个您可以设置的上下文工厂类：`'scrapy.core.downloader.contextfactory.BrowserLikeContextFactory'`，它使用平台的证书来验证远程端点。

如果您使用了自定义的ContextFactory，请确保其 `__init__` 方法接受一个 `method` 参数 (这是 `OpenSSL.SSL` 方法映射 [`DOWNLOADER_CLIENT_TLS_METHOD`>)，一个 `tls_verbose_logging` 参数 (`bool`) 以及一个 `tls_ciphers` 参数 (参见 ](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_CLIENT_TLS_METHOD)[`DOWNLOADER_CLIENT_TLS_CIPHERS`>)。](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_CLIENT_TLS_CIPHERS)







### [DOWNLOADER_CLIENT_TLS_CIPHERS](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_CLIENT_TLS_CIPHERS)[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-client-tls-ciphers)

默认值: `'DEFAULT'`

使用此设置自定义默认HTTP/1.1下载器使用的TLS/SSL密码套件。

此设置应包含符合[OpenSSL密码列表格式](https://docs.openssl.org/master/man1/openssl-ciphers/#cipher-list-format)的字符串，这些密码将被用作客户端密码套件。更改此设置可能对于访问某些HTTPS网站是必需的：例如，对于DH参数较弱的网站，您可能需要使用`'DEFAULT:!DH'`，或者如果网站要求，则需要启用一个不包含在`DEFAULT`中的特定密码套件。



### DOWNLOADER_CLIENT_TLS_METHOD[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-client-tls-method)

默认值: `'TLS'`

使用此设置自定义默认HTTP/1.1下载器使用的TLS/SSL方法。

此设置必须是以下字符串值之一：

- `'TLS'`: 映射到OpenSSL的`TLS_method()` (也称为`SSLv23_method()`)，允许协议协商，从平台支持的最高版本开始；**默认，推荐**
- `'TLSv1.0'`: 此值强制HTTPS连接使用TLS版本1.0；如果您想要 Scrapy<1.1 的行为，请设置此值
- `'TLSv1.1'`: 强制使用TLS版本1.1
- `'TLSv1.2'`: 强制使用TLS版本1.2



### DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-client-tls-verbose-logging)

默认值: `False`

将此设置为`True`将在建立HTTPS连接后启用关于TLS连接参数的DEBUG级别消息日志。日志信息的类型取决于OpenSSL和pyOpenSSL的版本。

此设置仅用于默认的[`DOWNLOADER_CLIENTCONTEXTFACTORY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_CLIENTCONTEXTFACTORY)。



### DOWNLOADER_MIDDLEWARES[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-middlewares)

默认值:: `{}`

一个字典，包含您的项目中启用的下载器中间件及其顺序。更多信息请参见[激活下载器中间件](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware-setting)。



### DOWNLOADER_MIDDLEWARES_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-middlewares-base)

默认值

```
{
    "scrapy.downloadermiddlewares.offsite.OffsiteMiddleware": 50,
    "scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": 100,
    "scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware": 300,
    "scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware": 350,
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": 400,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 500,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware": 560,
    "scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware": 580,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 590,
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 600,
    "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": 700,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 750,
    "scrapy.downloadermiddlewares.stats.DownloaderStats": 850,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 900,
}
```

一个字典，包含Scrapy中默认启用的下载器中间件及其顺序。较低的顺序更接近引擎，较高的顺序更接近下载器。您绝不应在项目中修改此设置，请修改[`DOWNLOADER_MIDDLEWARES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES)代替。更多信息请参见[激活下载器中间件](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-downloader-middleware-setting)。



### DOWNLOADER_STATS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#downloader-stats)

默认值: `True`

是否启用下载器统计信息收集。



### DOWNLOAD_DELAY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-delay)

默认值: `0`

对同一域名进行连续两次请求之间等待的最小秒数。

使用[`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY)来限制您的爬取速度，以避免对服务器造成过大压力。

支持小数。例如，每10秒最多发送4个请求：

```
DOWNLOAD_DELAY = 2.5
```

此设置也受[`RANDOMIZE_DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-RANDOMIZE_DOWNLOAD_DELAY)设置的影响，该设置默认启用。

当[`CONCURRENT_REQUESTS_PER_IP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_IP)非零时，延迟将按IP地址而不是按域名强制执行。

请注意，[`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY)可以降低每个域名的有效并发度，使其低于[`CONCURRENT_REQUESTS_PER_DOMAIN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_DOMAIN)。如果域名的响应时间低于[`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY)，则该域名的有效并发度为1。测试限速配置时，通常应该首先降低[`CONCURRENT_REQUESTS_PER_DOMAIN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_DOMAIN)，只有当[`CONCURRENT_REQUESTS_PER_DOMAIN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_DOMAIN)为1但希望施加更高的限制时，才增加[`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY)。

注意

可以使用`download_delay`蜘蛛属性为每个蜘蛛设置此延迟。

也可以按域名更改此设置，但这需要非平凡的代码。请参阅[AutoThrottle](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#topics-autothrottle)扩展的实现以获取示例。



### DOWNLOAD_HANDLERS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-handlers)

默认值: `{}`

一个字典，包含您的项目中启用的请求下载处理器。有关示例格式，请参见[`DOWNLOAD_HANDLERS_BASE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS_BASE)。



### DOWNLOAD_HANDLERS_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-handlers-base)

默认值

```
{
    "data": "scrapy.core.downloader.handlers.datauri.DataURIDownloadHandler",
    "file": "scrapy.core.downloader.handlers.file.FileDownloadHandler",
    "http": "scrapy.core.downloader.handlers.http.HTTPDownloadHandler",
    "https": "scrapy.core.downloader.handlers.http.HTTPDownloadHandler",
    "s3": "scrapy.core.downloader.handlers.s3.S3DownloadHandler",
    "ftp": "scrapy.core.downloader.handlers.ftp.FTPDownloadHandler",
}
```

一个字典，包含Scrapy中默认启用的请求下载处理器。您绝不应在项目中修改此设置，请修改[`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)代替。

您可以通过在[`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)中将其URI方案赋值为`None`来禁用任何这些下载处理器。例如，要禁用内置的FTP处理器（不替换），请将其放入您的`settings.py`中：

```
DOWNLOAD_HANDLERS = {
    "ftp": None,
}
```

默认的HTTPS处理器使用HTTP/1.1。要使用HTTP/2：

1. 安装`Twisted[http2]>=17.9.0`以安装在Twisted中启用HTTP/2支持所需的包。

2. 更新[`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)如下：

   ```
   DOWNLOAD_HANDLERS = {
       "https": "scrapy.core.downloader.handlers.http2.H2DownloadHandler",
   }
   ```

警告

Scrapy中的HTTP/2支持是实验性的，尚不推荐用于生产环境。未来的Scrapy版本可能会引入相关更改，恕不另行通知或弃用。

注意

当前Scrapy HTTP/2 实现的已知限制包括：

- 不支持HTTP/2 明文 (h2c)，因为没有主流浏览器支持未加密的HTTP/2 (参考[http2 faq](https://http2.github.io/faq/#does-http2-require-encryption))。
- 没有设置可以指定大于默认值16384的最大[帧大小](https://datatracker.ietf.org/doc/html/rfc7540#section-4.2)。连接到发送更大帧的服务器将失败。
- 不支持[服务器推送](https://datatracker.ietf.org/doc/html/rfc7540#section-8.2)，服务器推送将被忽略。
- 不支持[`bytes_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-bytes_received)和[`headers_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-headers_received)信号。



### DOWNLOAD_SLOTS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-slots)

默认值: `{}`

允许为每个槽 (域名) 定义并发/延迟参数

> ```
> DOWNLOAD_SLOTS = {
>     "quotes.toscrape.com": {"concurrency": 1, "delay": 2, "randomize_delay": False},
>     "books.toscrape.com": {"delay": 3, "randomize_delay": False},
> }
> ```

注意

对于其他下载器槽，将使用默认设置值：

- [`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY): `delay`
- [`CONCURRENT_REQUESTS_PER_DOMAIN`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_DOMAIN): `concurrency`
- [`RANDOMIZE_DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-RANDOMIZE_DOWNLOAD_DELAY): `randomize_delay`



### DOWNLOAD_TIMEOUT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-timeout)

默认值: `180`

下载器在超时前等待的时间（秒）。

注意

可以使用`download_timeout`蜘蛛属性为每个蜘蛛设置此超时，并使用[`download_timeout`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-download_timeout) Request.meta 键为每个请求设置。



### DOWNLOAD_MAXSIZE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-maxsize)

默认值: `1073741824` (1 GiB)

允许的最大响应体大小（字节）。大于此值的响应将被中止并忽略。

这适用于压缩前和压缩后。如果解压响应体超出此限制，解压将被中止，响应将被忽略。

使用`0`来禁用此限制。

此限制可以使用`download_maxsize`蜘蛛属性为每个蜘蛛设置，并使用[`download_maxsize`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-reqmeta-download_maxsize) Request.meta 键为每个请求设置。



### DOWNLOAD_WARNSIZE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-warnsize)

默认值: `33554432` (32 MiB)

如果响应的大小在压缩前或压缩后超过此值，将记录一条警告。

使用`0`来禁用此限制。

此限制可以使用`download_warnsize`蜘蛛属性为每个蜘蛛设置，并使用[`download_warnsize`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-reqmeta-download_warnsize) Request.meta 键为每个请求设置。



### DOWNLOAD_FAIL_ON_DATALOSS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#download-fail-on-dataloss)

默认值: `True`

是否在响应损坏时失败，即声明的 `Content-Length` 与服务器发送的内容不匹配，或者分块响应未正确结束。如果设置为 `True`，这些响应将引发 `ResponseFailed([_DataLoss])` 错误。如果设置为 `False`，这些响应将被传递，并且会将 `dataloss` 标志添加到响应中，例如：`'dataloss' in response.flags` 为 `True`。

此设置也可以通过使用[`download_fail_on_dataloss`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-reqmeta-download_fail_on_dataloss) Request.meta 键并设置为 `False` 来按请求设置。

注意

响应损坏或数据丢失错误可能发生在多种情况下，从服务器配置错误到网络错误再到数据损坏。用户需要决定处理损坏的响应是否有意义，因为它们可能包含部分或不完整的内容。如果[`RETRY_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_ENABLED)为`True`且此设置也为`True`，则`ResponseFailed([_DataLoss])`失败将像往常一样重试。

警告

此设置被`H2DownloadHandler`下载处理器忽略（参见[`DOWNLOAD_HANDLERS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_HANDLERS)）。如果发生数据丢失错误，相应的HTTP/2连接可能会损坏，影响使用同一连接的其他请求；因此，对于使用该连接的每个请求，始终会引发`ResponseFailed([InvalidBodyLengthError])`失败。



### DUPEFILTER_CLASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dupefilter-class)

默认值: `'scrapy.dupefilters.RFPDupeFilter'`

用于检测和过滤重复请求的类。

默认的[`RFPDupeFilter`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.dupefilters.RFPDupeFilter)根据[`REQUEST_FINGERPRINTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-setting-REQUEST_FINGERPRINTER_CLASS)设置进行过滤。

要更改如何检查重复项，您可以将[`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)指向[`RFPDupeFilter`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.dupefilters.RFPDupeFilter)的自定义子类，该子类覆盖其`__init__`方法以使用[不同的请求指纹生成类](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#custom-request-fingerprinter)。例如：

```
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import fingerprint


class CustomRequestFingerprinter:
    def fingerprint(self, request):
        return fingerprint(request, include_headers=["X-ID"])


class CustomDupeFilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False, *, fingerprinter=None):
        super().__init__(
            path=path, debug=debug, fingerprinter=CustomRequestFingerprinter()
        )
```

要禁用重复请求过滤，请将[`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)设置为`'scrapy.dupefilters.BaseDupeFilter'`。请注意，不过滤重复请求可能会导致爬取循环。通常最好在不应过滤的特定[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)对象的`__init__`方法中将`dont_filter`参数设置为`True`。

分配给[`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)的类必须实现以下接口：

```
class MyDupeFilter:

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance of this duplicate request filtering class
        based on the current crawl settings."""
        return cls()

    def request_seen(self, request):
        """Returns ``True`` if *request* is a duplicate of another request
        seen in a previous call to :meth:`request_seen`, or ``False``
        otherwise."""
        return False

    def open(self):
        """Called before the spider opens. It may return a deferred."""
        pass

    def close(self, reason):
        """Called before the spider closes. It may return a deferred."""
        pass

    def log(self, request, spider):
        """Logs that a request has been filtered out.

        It is called right after a call to :meth:`request_seen` that
        returns ``True``.

        If :meth:`request_seen` always returns ``False``, such as in the
        case of :class:`~scrapy.dupefilters.BaseDupeFilter`, this method
        may be omitted.
        """
        pass
```

- *class*scrapy.dupefilters.BaseDupeFilter[[源代码\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/dupefilters.html#BaseDupeFilter)[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.dupefilters.BaseDupeFilter)

  空的重复请求过滤类（[`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)），不会过滤任何请求。

- *class*scrapy.dupefilters.RFPDupeFilter(*path: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *debug: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = False*, ***, *fingerprinter: RequestFingerprinterProtocol | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)[[源代码\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/dupefilters.html#RFPDupeFilter)[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.dupefilters.RFPDupeFilter)

  重复请求过滤类（[`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS)），根据规范化（[`w3lib.url.canonicalize_url()`](https://w3lib.readthedocs.io/en/latest/w3lib.html#w3lib.url.canonicalize_url)）的`url`、`method`和`body`来过滤请求。



### DUPEFILTER_DEBUG[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#dupefilter-debug)

默认值: `False`

默认情况下，`RFPDupeFilter`只记录第一个重复请求。将[`DUPEFILTER_DEBUG`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_DEBUG)设置为`True`将使其记录所有重复请求。



### EDITOR[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#editor)

默认值: `vi` (在Unix系统上) 或 IDLE 编辑器 (在Windows上)

用于通过[`edit`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-edit)命令编辑蜘蛛的编辑器。此外，如果设置了`EDITOR`环境变量，[`edit`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-edit)命令将优先使用它而不是默认设置。



### EXTENSIONS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#extensions)

默认值:: `{}`

已启用的扩展的[组件优先级字典](https://docs.scrapy.net.cn/en/latest/topics/settings.html#component-priority-dictionaries)。参见[扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions)。



### EXTENSIONS_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#extensions-base)

默认值

```
{
    "scrapy.extensions.corestats.CoreStats": 0,
    "scrapy.extensions.telnet.TelnetConsole": 0,
    "scrapy.extensions.memusage.MemoryUsage": 0,
    "scrapy.extensions.memdebug.MemoryDebugger": 0,
    "scrapy.extensions.closespider.CloseSpider": 0,
    "scrapy.extensions.feedexport.FeedExporter": 0,
    "scrapy.extensions.logstats.LogStats": 0,
    "scrapy.extensions.spiderstate.SpiderState": 0,
    "scrapy.extensions.throttle.AutoThrottle": 0,
}
```

一个字典，包含Scrapy中默认可用的扩展及其顺序。此设置包含所有稳定的内置扩展。请记住，其中一些需要通过设置启用。

更多信息请参阅[扩展用户指南](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions)和[可用扩展列表](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref)。



### FEED_TEMPDIR[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#feed-tempdir)

Feed Temp dir 允许您设置一个自定义文件夹来保存爬虫临时文件，以便在使用[FTP feed存储](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-ftp)和[Amazon S3](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-s3)上传之前使用。



### FEED_STORAGE_GCS_ACL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#feed-storage-gcs-acl)

将项目存储到 [Google Cloud Storage](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-storage-gcs) 时使用的访问控制列表 (ACL)。有关如何设置此值的更多信息，请参阅 [Google Cloud 文档](https://cloud.google.com/storage/docs/access-control/lists)中名为 *JSON API* 的列。



### FTP_PASSIVE_MODE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#ftp-passive-mode)

默认值: `True`

在发起 FTP 传输时是否使用被动模式。



### FTP_PASSWORD[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#ftp-password)

默认值: `"guest"`

当 `Request` meta 中没有 `"ftp_password"` 时，用于 FTP 连接的密码。

注意

引用 [RFC 1635](https://datatracker.ietf.org/doc/html/rfc1635)，尽管匿名 FTP 通常使用密码 “guest” 或用户的电子邮件地址，但有些 FTP 服务器会明确要求用户的电子邮件地址，并且不允许使用 “guest” 密码登录。



### FTP_USER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#ftp-user)

默认值: `"anonymous"`

当 `Request` meta 中没有 `"ftp_user"` 时，用于 FTP 连接的用户名。



### GCS_PROJECT_ID[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#gcs-project-id)

默认值: `None`

在 [Google Cloud Storage](https://cloud.google.com/storage/) 上存储数据时将使用的项目 ID。



### ITEM_PIPELINES[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#item-pipelines)

默认值: `{}`

一个字典，包含要使用的项目管道及其顺序。顺序值是任意的，但通常定义在 0-1000 范围内。较低的顺序比较高的顺序先处理。

示例

```
ITEM_PIPELINES = {
    "mybot.pipelines.validate.ValidateMyItem": 300,
    "mybot.pipelines.validate.StoreMyItem": 800,
}
```



### ITEM_PIPELINES_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#item-pipelines-base)

默认值: `{}`

一个字典，包含 Scrapy 中默认启用的管道。您不应在项目中修改此设置，而应修改 [`ITEM_PIPELINES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-ITEM_PIPELINES)。



### JOBDIR[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#jobdir)

默认值: `None`

一个字符串，指示在 [暂停和恢复爬取](https://docs.scrapy.net.cn/en/latest/topics/jobs.html#topics-jobs) 时用于存储爬取状态的目录。



### LOG_ENABLED[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-enabled)

默认值: `True`

是否启用日志记录。



### LOG_ENCODING[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-encoding)

默认值: `'utf-8'`

用于日志记录的编码。



### LOG_FILE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-file)

默认值: `None`

用于日志输出的文件名。如果为 `None`，则将使用标准错误输出。



### LOG_FILE_APPEND[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-file-append)

默认值: `True`

如果为 `False`，则指定给 [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE) 的日志文件将被覆盖（丢弃之前运行的输出，如果有的话）。



### LOG_FORMAT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-format)

默认值: `'%(asctime)s [%(name)s] %(levelname)s: %(message)s'`

用于格式化日志消息的字符串。有关可用占位符的完整列表，请参阅 [Python 日志记录文档](https://docs.pythonlang.cn/3/library/logging.html#logrecord-attributes)。



### LOG_DATEFORMAT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-dateformat)

默认值: `'%Y-%m-%d %H:%M:%S'`

用于格式化日期/时间的字符串，是 [`LOG_FORMAT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FORMAT) 中 `%(asctime)s` 占位符的扩展。有关可用指令的完整列表，请参阅 [Python datetime 文档](https://docs.pythonlang.cn/3/library/datetime.html#strftime-strptime-behavior)。



### LOG_FORMATTER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-formatter)

默认值: [`scrapy.logformatter.LogFormatter`](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter)

用于 [格式化不同操作的日志消息](https://docs.scrapy.net.cn/en/latest/topics/logging.html#custom-log-formats) 的类。



### LOG_LEVEL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-level)

默认值: `'DEBUG'`

要记录的最低级别。可用级别为: CRITICAL, ERROR, WARNING, INFO, DEBUG。更多信息请参阅 [日志记录](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging)。



### LOG_STDOUT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-stdout)

默认值: `False`

如果为 `True`，则进程的所有标准输出（和错误）都将重定向到日志。例如，如果执行 `print('hello')`，它将出现在 Scrapy 日志中。



### LOG_SHORT_NAMES[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-short-names)

默认值: `False`

如果为 `True`，日志将只包含根路径。如果设置为 `False`，则显示负责日志输出的组件。



### LOG_VERSIONS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#log-versions)

默认值: `["lxml", "libxml2", "cssselect", "parsel", "w3lib", "Twisted", "Python", "pyOpenSSL", "cryptography", "Platform"]`

记录指定项目的已安装版本。

项目可以是任何已安装的 Python 包。

还支持以下特殊项目：

- `libxml2`
- `Platform` （[`platform.platform()`](https://docs.pythonlang.cn/3/library/platform.html#platform.platform)）
- `Python`



### LOGSTATS_INTERVAL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#logstats-interval)

默认值: `60.0`

[`LogStats`](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#scrapy.extensions.logstats.LogStats) 记录统计数据的间隔（以秒为单位）。



### MEMDEBUG_ENABLED[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memdebug-enabled)

默认值: `False`

是否启用内存调试。



### MEMDEBUG_NOTIFY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memdebug-notify)

默认值: `[]`

当内存调试启用时，如果此设置不为空，则内存报告将发送到指定的地址，否则报告将写入日志。

示例

```
MEMDEBUG_NOTIFY = ['user@example.com']
```



### MEMUSAGE_ENABLED[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memusage-enabled)

默认值: `True`

范围: `scrapy.extensions.memusage`

是否启用内存使用扩展。此扩展记录进程使用的峰值内存（并将其写入统计信息）。它还可以选择在超过内存限制时关闭 Scrapy 进程（参见 [`MEMUSAGE_LIMIT_MB`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-MEMUSAGE_LIMIT_MB)），并在发生时通过电子邮件通知（参见 [`MEMUSAGE_NOTIFY_MAIL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-MEMUSAGE_NOTIFY_MAIL)）。

参见 [内存使用扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-memusage)。



### MEMUSAGE_LIMIT_MB[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memusage-limit-mb)

默认值: `0`

范围: `scrapy.extensions.memusage`

在关闭 Scrapy 之前允许的最大内存量（以兆字节为单位）（如果 MEMUSAGE_ENABLED 为 True）。如果为零，则不执行检查。

参见 [内存使用扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-memusage)。



### MEMUSAGE_CHECK_INTERVAL_SECONDS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memusage-check-interval-seconds)

默认值: `60.0`

范围: `scrapy.extensions.memusage`

[内存使用扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-memusage) 以固定的时间间隔检查当前内存使用情况，与 [`MEMUSAGE_LIMIT_MB`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-MEMUSAGE_LIMIT_MB) 和 [`MEMUSAGE_WARNING_MB`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-MEMUSAGE_WARNING_MB) 设置的限制进行比较。

此设置这些间隔的长度，以秒为单位。

参见 [内存使用扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-memusage)。



### MEMUSAGE_NOTIFY_MAIL[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memusage-notify-mail)

默认值: `False`

范围: `scrapy.extensions.memusage`

达到内存限制时要通知的电子邮件列表。

示例

```
MEMUSAGE_NOTIFY_MAIL = ['user@example.com']
```

参见 [内存使用扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-memusage)。



### MEMUSAGE_WARNING_MB[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#memusage-warning-mb)

默认值: `0`

范围: `scrapy.extensions.memusage`

在发送警告电子邮件通知之前允许的最大内存量（以兆字节为单位）。如果为零，则不生成警告。



### NEWSPIDER_MODULE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#newspider-module)

默认值: `"<project name>.spiders"` （[回退](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings): `""`）

使用 [`genspider`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-genspider) 命令创建新爬虫的模块。

示例

```
NEWSPIDER_MODULE = 'mybot.spiders_dev'
```



### RANDOMIZE_DOWNLOAD_DELAY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#randomize-download-delay)

默认值: `True`

如果启用，Scrapy 在从同一网站抓取请求时将等待随机时间（介于 0.5 * [`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY) 和 1.5 * [`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY) 之间）。

这种随机化降低了爬虫被分析请求并查找请求之间时间统计上显着相似性的网站检测到（并随后阻止）的可能性。

随机化策略与 [wget](https://gnu.ac.cn/software/wget/manual/wget.html) 的 `--random-wait` 选项使用的策略相同。

如果 [`DOWNLOAD_DELAY`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DOWNLOAD_DELAY) 为零（默认值），则此选项无效。



### REACTOR_THREADPOOL_MAXSIZE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#reactor-threadpool-maxsize)

默认值: `10`

Twisted Reactor 线程池的最大大小限制。这是各种 Scrapy 组件使用的通用多用途线程池。例如，线程 DNS 解析器、BlockingFeedStorage、S3FilesStore。如果您在使用不足的阻塞 IO 时遇到问题，请增加此值。



### REDIRECT_PRIORITY_ADJUST[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#redirect-priority-adjust)

默认值: `+2`

范围: `scrapy.downloadermiddlewares.redirect.RedirectMiddleware`

调整重定向请求相对于原始请求的优先级。

- **正的优先级调整（默认值）意味着更高的优先级。**
- 负的优先级调整意味着更低的优先级。



### ROBOTSTXT_OBEY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#robotstxt-obey)

默认值: `True` （[回退](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings): `False`）

如果启用，Scrapy 将遵守 robots.txt 策略。更多信息请参阅 [RobotsTxtMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-dlmw-robots)。

注意

尽管出于历史原因，默认值为 `False`，但在通过 `scrapy startproject` 命令生成的 settings.py 文件中，此选项默认启用。



### ROBOTSTXT_PARSER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#robotstxt-parser)

默认值: `'scrapy.robotstxt.ProtegoRobotParser'`

用于解析 `robots.txt` 文件的解析器后端。更多信息请参阅 [RobotsTxtMiddleware](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#topics-dlmw-robots)。



#### ROBOTSTXT_USER_AGENT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#robotstxt-user-agent)

默认值: `None`

用于在 robots.txt 文件中匹配的用户代理字符串。如果为 `None`，则您在请求中发送的 User-Agent 头部或 [`USER_AGENT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-USER_AGENT) 设置（按此顺序）将用于确定在 robots.txt 文件中使用的用户代理。



### SCHEDULER[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler)

默认值: `'scrapy.core.scheduler.Scheduler'`

用于爬取的调度器类。详情请参阅 [调度器](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#topics-scheduler) 主题。



### SCHEDULER_DEBUG[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-debug)

默认值: `False`

设置为 `True` 将记录关于请求调度器的调试信息。这目前仅记录（一次）请求无法序列化到磁盘的情况。统计计数器（`scheduler/unserializable`）跟踪发生此情况的次数。

日志中的示例条目

```
1956-01-31 00:00:00+0800 [scrapy.core.scheduler] ERROR: Unable to serialize request:
<GET http://example.com> - reason: cannot serialize <Request at 0x9a7c7ec>
(type Request)> - no more unserializable requests will be logged
(see 'scheduler/unserializable' stats counter)
```



### SCHEDULER_DISK_QUEUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-disk-queue)

默认值: `'scrapy.squeues.PickleLifoDiskQueue'`

调度器将使用的磁盘队列类型。其他可用类型包括 `scrapy.squeues.PickleFifoDiskQueue`、`scrapy.squeues.MarshalFifoDiskQueue`、`scrapy.squeues.MarshalLifoDiskQueue`。



### SCHEDULER_MEMORY_QUEUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-memory-queue)

默认值: `'scrapy.squeues.LifoMemoryQueue'`

调度器使用的内存队列类型。其他可用类型为: `scrapy.squeues.FifoMemoryQueue`。



### SCHEDULER_PRIORITY_QUEUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-priority-queue)

默认值: `'scrapy.pqueues.ScrapyPriorityQueue'`

调度器使用的优先级队列类型。另一个可用类型是 `scrapy.pqueues.DownloaderAwarePriorityQueue`。`scrapy.pqueues.DownloaderAwarePriorityQueue` 在您并行爬取许多不同域名时比 `scrapy.pqueues.ScrapyPriorityQueue` 效果更好。但目前 `scrapy.pqueues.DownloaderAwarePriorityQueue` 不与 [`CONCURRENT_REQUESTS_PER_IP`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS_PER_IP) 一起工作。



### SCHEDULER_START_DISK_QUEUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-start-disk-queue)

默认值: `'scrapy.squeues.PickleFifoDiskQueue'`

[调度器](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#topics-scheduler) 用于 [start requests](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#start-requests) 的磁盘队列类型（参见 [`JOBDIR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-JOBDIR)）。

有关可用选项，请参见 [`SCHEDULER_DISK_QUEUE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SCHEDULER_DISK_QUEUE)。

使用 `None` 或 `""` 完全禁用这些单独的队列，改为让 start requests 与其他请求共享相同的队列。

注意

禁用单独的 start request 队列会使 [start request 顺序](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#start-request-order) 不直观：start requests 只会按顺序发送，直到达到 [`CONCURRENT_REQUESTS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS)，然后剩余的 start requests 将按反向顺序发送。



### SCHEDULER_START_MEMORY_QUEUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scheduler-start-memory-queue)

默认值: `'scrapy.squeues.FifoMemoryQueue'`

[调度器](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#topics-scheduler) 用于 [start requests](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#start-requests) 的内存队列类型。

有关可用选项，请参见 [`SCHEDULER_MEMORY_QUEUE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SCHEDULER_MEMORY_QUEUE)。

使用 `None` 或 `""` 完全禁用这些单独的队列，改为让 start requests 与其他请求共享相同的队列。

注意

禁用单独的 start request 队列会使 [start request 顺序](https://docs.scrapy.net.cn/en/latest/topics/scheduler.html#start-request-order) 不直观：start requests 只会按顺序发送，直到达到 [`CONCURRENT_REQUESTS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-CONCURRENT_REQUESTS)，然后剩余的 start requests 将按反向顺序发送。



### SCRAPER_SLOT_MAX_ACTIVE_SIZE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scraper-slot-max-active-size)

*版本 2.0 中新增。*

默认值: `5_000_000`

正在处理的响应数据的软限制（以字节为单位）。

当所有正在处理的响应大小总和超过此值时，Scrapy 不处理新的请求。



### SPIDER_CONTRACTS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-contracts)

默认值:: `{}`

一个字典，包含项目中启用的爬虫契约，用于测试爬虫。更多信息请参阅 [爬虫契约](https://docs.scrapy.net.cn/en/latest/topics/contracts.html#topics-contracts)。



### SPIDER_CONTRACTS_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-contracts-base)

默认值

```
{
    "scrapy.contracts.default.UrlContract": 1,
    "scrapy.contracts.default.ReturnsContract": 2,
    "scrapy.contracts.default.ScrapesContract": 3,
}
```

一个字典，包含 Scrapy 中默认启用的爬虫契约。您不应在项目中修改此设置，而应修改 [`SPIDER_CONTRACTS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_CONTRACTS)。更多信息请参阅 [爬虫契约](https://docs.scrapy.net.cn/en/latest/topics/contracts.html#topics-contracts)。

您可以通过在 [`SPIDER_CONTRACTS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_CONTRACTS) 中将其类路径设置为 `None` 来禁用这些契约中的任何一个。例如，要禁用内置的 `ScrapesContract`，请将其放入您的 `settings.py` 中：

```
SPIDER_CONTRACTS = {
    "scrapy.contracts.default.ScrapesContract": None,
}
```



### SPIDER_LOADER_CLASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-loader-class)

默认值: `'scrapy.spiderloader.SpiderLoader'`

用于加载爬虫的类，该类必须实现 [SpiderLoader API](https://docs.scrapy.net.cn/en/latest/topics/api.html#topics-api-spiderloader)。



### SPIDER_LOADER_WARN_ONLY[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-loader-warn-only)

默认值: `False`

默认情况下，当 Scrapy 尝试从 [`SPIDER_MODULES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-SPIDER_MODULES) 导入爬虫类时，如果发生任何 `ImportError` 或 `SyntaxError` 异常，它将大声失败。但您可以通过设置 `SPIDER_LOADER_WARN_ONLY = True` 来选择静默此异常，并将其转换为简单的警告。

注意

一些 [scrapy 命令](https://docs.scrapy.net.cn/en/latest/topics/commands.html#topics-commands) 已经在 `True` 的情况下运行此设置（即它们只会发出警告而不会失败），因为它们实际上不需要加载爬虫类即可工作：[`scrapy runspider`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-runspider)、[`scrapy settings`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-settings)、[`scrapy startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject)、[`scrapy version`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-version)。



### SPIDER_MIDDLEWARES[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-middlewares)

默认值:: `{}`

一个字典，包含项目中启用的爬虫中间件及其顺序。更多信息请参阅 [激活爬虫中间件](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware-setting)。



### SPIDER_MIDDLEWARES_BASE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-middlewares-base)

默认值

```
{
    "scrapy.spidermiddlewares.httperror.HttpErrorMiddleware": 50,
    "scrapy.spidermiddlewares.referer.RefererMiddleware": 700,
    "scrapy.spidermiddlewares.urllength.UrlLengthMiddleware": 800,
    "scrapy.spidermiddlewares.depth.DepthMiddleware": 900,
}
```

一个字典，包含 Scrapy 中默认启用的爬虫中间件及其顺序。较低的顺序更接近引擎，较高的顺序更接近爬虫。更多信息请参阅 [激活爬虫中间件](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#topics-spider-middleware-setting)。



### SPIDER_MODULES[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#spider-modules)

默认值: `["<project name>.spiders"]` （[回退](https://docs.scrapy.net.cn/en/latest/topics/settings.html#default-settings): `[]`）

一个列表，列出了 Scrapy 将查找爬虫的模块。

示例

```
SPIDER_MODULES = ["mybot.spiders_prod", "mybot.spiders_dev"]
```



### STATS_CLASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#stats-class)

默认值: `'scrapy.statscollectors.MemoryStatsCollector'`

用于收集统计信息的类，该类必须实现 [Stats Collector API](https://docs.scrapy.net.cn/en/latest/topics/api.html#topics-api-stats)。



### STATS_DUMP[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#stats-dump)

默认值: `True`

爬虫完成时转储 [Scrapy 统计信息](https://docs.scrapy.net.cn/en/latest/topics/stats.html#topics-stats)（到 Scrapy 日志）。

更多信息请参阅: [统计信息收集](https://docs.scrapy.net.cn/en/latest/topics/stats.html#topics-stats)。



### STATSMAILER_RCPTS[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#statsmailer-rcpts)

默认值: `[]` （空列表）

在爬虫完成爬取后发送 Scrapy 统计信息。更多信息请参阅 [`StatsMailer`](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#scrapy.extensions.statsmailer.StatsMailer)。



### TELNETCONSOLE_ENABLED[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#telnetconsole-enabled)

默认值: `True`

一个布尔值，指定是否启用 [telnet 控制台](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#topics-telnetconsole)（前提是其扩展也已启用）。



### TEMPLATES_DIR[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#templates-dir)

默认值: scrapy 模块内的 `templates` 目录

使用 [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 命令创建新项目和使用 [`genspider`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-genspider) 命令创建新爬虫时查找模板的目录。

项目名称不得与 `project` 子目录中自定义文件或目录的名称冲突。



### TWISTED_REACTOR[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#twisted-reactor)

*版本 2.0 中新增。*

默认值: `"twisted.internet.asyncioreactor.AsyncioSelectorReactor"`

给定 [`reactor`](https://docs.twisted.org.cn/en/stable/api/twisted.internet.reactor.html) 的导入路径。

如果尚未安装其他 reactor，例如在调用 `scrapy` CLI 程序或使用 [`CrawlerProcess`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerProcess) 类时，Scrapy 将安装此 reactor。

如果您正在使用 [`CrawlerRunner`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerRunner) 类，您还需要手动安装正确的 reactor。您可以使用 [`install_reactor()`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.utils.reactor.install_reactor) 来实现：

- scrapy.utils.reactor.install_reactor(*reactor_path: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str)*, *event_loop_path: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ [None](https://docs.pythonlang.cn/3/library/constants.html#None)[[源代码\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/utils/reactor.html#install_reactor)[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.utils.reactor.install_reactor)

  安装具有指定导入路径的 [`reactor`](https://docs.twisted.org.cn/en/stable/api/twisted.internet.reactor.html)。如果启用了 asyncio reactor，也会安装具有指定导入路径的 asyncio 事件循环。

如果已安装 reactor，[`install_reactor()`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#scrapy.utils.reactor.install_reactor) 无效。

`CrawlerRunner.__init__` 如果已安装的 reactor 与 [`TWISTED_REACTOR`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-TWISTED_REACTOR) 设置不匹配，则会引发 [`Exception`](https://docs.pythonlang.cn/3/library/exceptions.html#Exception)；因此，在项目文件和导入的第三方库中存在顶级 [`reactor`](https://docs.twisted.org.cn/en/stable/api/twisted.internet.reactor.html) 导入会导致 Scrapy 在检查安装的 reactor 时引发 [`Exception`](https://docs.pythonlang.cn/3/library/exceptions.html#Exception)。

为了使用 Scrapy 安装的 reactor：

```
import scrapy
from twisted.internet import reactor


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, *args, **kwargs):
        self.timeout = int(kwargs.pop("timeout", "60"))
        super(QuotesSpider, self).__init__(*args, **kwargs)

    async def start(self):
        reactor.callLater(self.timeout, self.stop)

        urls = ["https://quotes.toscrape.com/page/1"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {"text": quote.css("span.text::text").get()}

    def stop(self):
        self.crawler.engine.close_spider(self, "timeout")
```

这将引发 [`Exception`](https://docs.pythonlang.cn/3/library/exceptions.html#Exception)，变为：

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, *args, **kwargs):
        self.timeout = int(kwargs.pop("timeout", "60"))
        super(QuotesSpider, self).__init__(*args, **kwargs)

    async def start(self):
        from twisted.internet import reactor

        reactor.callLater(self.timeout, self.stop)

        urls = ["https://quotes.toscrape.com/page/1"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {"text": quote.css("span.text::text").get()}

    def stop(self):
        self.crawler.engine.close_spider(self, "timeout")
```

如果此设置设置为 `None`，则 Scrapy 将使用已安装的现有 reactor（如果存在），否则安装 Twisted 为当前平台定义的默认 reactor。

*版本 2.7 中的变化:* [`startproject`](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-command-startproject) 命令现在在生成的 `settings.py` 文件中将此设置设置为 `twisted.internet.asyncioreactor.AsyncioSelectorReactor`。

*版本 2.13 中的变化:* 默认值从 `None` 更改为 `"twisted.internet.asyncioreactor.AsyncioSelectorReactor"`。

更多信息请参阅 [选择 Reactor 和 GUI 工具包集成](https://docs.twisted.org.cn/en/stable/core/howto/choosing-reactor.html)。



### URLLENGTH_LIMIT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#urllength-limit)

默认值: `2083`

范围: `spidermiddlewares.urllength`

允许爬取 URL 的最大长度。

此设置可作为 URL 长度不断增加情况下的停止条件，这种情况可能是由于目标服务器或您的代码中的编程错误引起的。另请参阅 [`REDIRECT_MAX_TIMES`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-REDIRECT_MAX_TIMES) 和 [`DEPTH_LIMIT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DEPTH_LIMIT)。

使用 `0` 允许任何长度的 URL。

默认值复制自 [Microsoft Internet Explorer 最大 URL 长度](https://support.microsoft.com/en-us/topic/maximum-url-length-is-2-083-characters-in-internet-explorer-174e7c8a-6666-f4e0-6fd6-908b53c12246)，尽管此设置存在的原因不同。



### USER_AGENT[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#user-agent)

默认值: `"Scrapy/VERSION (+https://scrapy.net.cn)"`

爬取时使用的默认 User-Agent，除非被覆盖。如果 [`ROBOTSTXT_USER_AGENT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-ROBOTSTXT_USER_AGENT) 设置为 `None` 且请求未指定覆盖的 User-Agent 头部，则 [`RobotsTxtMiddleware`](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware) 也会使用此用户代理。



### WARN_ON_GENERATOR_RETURN_VALUE[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#warn-on-generator-return-value)

默认值: `True`

启用后，如果基于生成器的回调方法（如 `parse`）包含非 `None` 值的 return 语句，Scrapy 将发出警告。这有助于检测爬虫开发中的潜在错误。

禁用此设置可防止在运行时动态修改生成器函数源代码时可能发生的语法错误，跳过对回调函数的 AST 解析，或在自动重载开发环境中提高性能。

### 其他地方记录的设置：[🔗](https://docs.scrapy.net.cn/en/latest/topics/settings.html#settings-documented-elsewhere)

以下设置记录在其他地方，请查看每个特定情况以了解如何启用和使用它们。

- [AUTOTHROTTLE_DEBUG](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_DEBUG)
- [AUTOTHROTTLE_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_ENABLED)
- [AUTOTHROTTLE_MAX_DELAY](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_MAX_DELAY)
- [AUTOTHROTTLE_START_DELAY](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_START_DELAY)
- [AUTOTHROTTLE_TARGET_CONCURRENCY](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#std-setting-AUTOTHROTTLE_TARGET_CONCURRENCY)
- [CLOSESPIDER_ERRORCOUNT](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_ERRORCOUNT)
- [CLOSESPIDER_ITEMCOUNT](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_ITEMCOUNT)
- [CLOSESPIDER_PAGECOUNT](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_PAGECOUNT)
- [CLOSESPIDER_PAGECOUNT_NO_ITEM](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_PAGECOUNT_NO_ITEM)
- [CLOSESPIDER_TIMEOUT](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_TIMEOUT)
- [CLOSESPIDER_TIMEOUT_NO_ITEM](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-CLOSESPIDER_TIMEOUT_NO_ITEM)
- [COMMANDS_MODULE](https://docs.scrapy.net.cn/en/latest/topics/commands.html#std-setting-COMMANDS_MODULE)
- [COMPRESSION_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-COMPRESSION_ENABLED)
- [COOKIES_DEBUG](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-COOKIES_DEBUG)
- [COOKIES_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-COOKIES_ENABLED)
- [FEEDS](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEEDS)
- [FEED_EXPORTERS](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORTERS)
- [FEED_EXPORTERS_BASE](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORTERS_BASE)
- [FEED_EXPORT_BATCH_ITEM_COUNT](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_BATCH_ITEM_COUNT)
- [FEED_EXPORT_ENCODING](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_ENCODING)
- [FEED_EXPORT_FIELDS](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_FIELDS)
- [FEED_EXPORT_INDENT](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_EXPORT_INDENT)
- [FEED_STORAGES](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES)
- [FEED_STORAGES_BASE](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGES_BASE)
- [FEED_STORAGE_FTP_ACTIVE](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_FTP_ACTIVE)
- [FEED_STORAGE_S3_ACL](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORAGE_S3_ACL)
- [FEED_STORE_EMPTY](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_STORE_EMPTY)
- [FEED_URI_PARAMS](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#std-setting-FEED_URI_PARAMS)
- [FILES_EXPIRES](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_EXPIRES)
- [FILES_RESULT_FIELD](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_RESULT_FIELD)
- [FILES_STORE](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_STORE)
- [FILES_STORE_GCS_ACL](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_STORE_GCS_ACL)
- [FILES_STORE_S3_ACL](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_STORE_S3_ACL)
- [FILES_URLS_FIELD](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-FILES_URLS_FIELD)
- [HTTPCACHE_ALWAYS_STORE](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_ALWAYS_STORE)
- [HTTPCACHE_DBM_MODULE](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_DBM_MODULE)
- [HTTPCACHE_DIR](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_DIR)
- [HTTPCACHE_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_ENABLED)
- [HTTPCACHE_EXPIRATION_SECS](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_EXPIRATION_SECS)
- [HTTPCACHE_GZIP](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_GZIP)
- [HTTPCACHE_IGNORE_HTTP_CODES](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_IGNORE_HTTP_CODES)
- [HTTPCACHE_IGNORE_MISSING](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_IGNORE_MISSING)
- [HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS)
- [HTTPCACHE_IGNORE_SCHEMES](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_IGNORE_SCHEMES)
- [HTTPCACHE_POLICY](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_POLICY)
- [HTTPCACHE_STORAGE](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPCACHE_STORAGE)
- [HTTPERROR_ALLOWED_CODES](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-setting-HTTPERROR_ALLOWED_CODES)
- [HTTPERROR_ALLOW_ALL](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-setting-HTTPERROR_ALLOW_ALL)
- [HTTPPROXY_AUTH_ENCODING](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPPROXY_AUTH_ENCODING)
- [HTTPPROXY_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-HTTPPROXY_ENABLED)
- [IMAGES_EXPIRES](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_EXPIRES)
- [IMAGES_MIN_HEIGHT](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_MIN_HEIGHT)
- [IMAGES_MIN_WIDTH](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_MIN_WIDTH)
- [IMAGES_RESULT_FIELD](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_RESULT_FIELD)
- [IMAGES_STORE](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_STORE)
- [IMAGES_STORE_GCS_ACL](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_STORE_GCS_ACL)
- [IMAGES_STORE_S3_ACL](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_STORE_S3_ACL)
- [IMAGES_THUMBS](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_THUMBS)
- [IMAGES_URLS_FIELD](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-IMAGES_URLS_FIELD)
- [MAIL_FROM](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_FROM)
- [MAIL_HOST](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_HOST)
- [MAIL_PASS](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_PASS)
- [MAIL_PORT](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_PORT)
- [MAIL_SSL](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_SSL)
- [MAIL_TLS](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_TLS)
- [MAIL_USER](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_USER)
- [MEDIA_ALLOW_REDIRECTS](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#std-setting-MEDIA_ALLOW_REDIRECTS)
- [METAREFRESH_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-METAREFRESH_ENABLED)
- [METAREFRESH_IGNORE_TAGS](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-METAREFRESH_IGNORE_TAGS)
- [METAREFRESH_MAXDELAY](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-METAREFRESH_MAXDELAY)
- [PERIODIC_LOG_DELTA](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-PERIODIC_LOG_DELTA)
- [PERIODIC_LOG_STATS](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-PERIODIC_LOG_STATS)
- [PERIODIC_LOG_TIMING_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#std-setting-PERIODIC_LOG_TIMING_ENABLED)
- [REDIRECT_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-REDIRECT_ENABLED)
- [REDIRECT_MAX_TIMES](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-REDIRECT_MAX_TIMES)
- [REFERER_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-setting-REFERER_ENABLED)
- [REFERRER_POLICY](https://docs.scrapy.net.cn/en/latest/topics/spider-middleware.html#std-setting-REFERRER_POLICY)
- [REQUEST_FINGERPRINTER_CLASS](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#std-setting-REQUEST_FINGERPRINTER_CLASS)
- [RETRY_ENABLED](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_ENABLED)
- [RETRY_EXCEPTIONS](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_EXCEPTIONS)
- [RETRY_HTTP_CODES](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_HTTP_CODES)
- [RETRY_PRIORITY_ADJUST](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_PRIORITY_ADJUST)
- [RETRY_TIMES](https://docs.scrapy.net.cn/en/latest/topics/downloader-middleware.html#std-setting-RETRY_TIMES)
- [TELNETCONSOLE_HOST](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_HOST)
- [TELNETCONSOLE_PASSWORD](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_PASSWORD)
- [TELNETCONSOLE_PORT](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_PORT)
- [TELNETCONSOLE_USERNAME](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_USERNAME)

# 12 异常

## 内置异常参考[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#built-in-exceptions-reference)

以下是 Scrapy 中包含的所有异常及其用法列表。

### CloseSpider[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#closespider)

- *异常*scrapy.exceptions.CloseSpider(*reason='cancelled'*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#CloseSpider)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.CloseSpider)

  可以在爬虫回调中引发此异常，以请求关闭/停止爬虫。支持的参数参数:**reason** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 关闭原因

例如

```
def parse_page(self, response):
    if "Bandwidth exceeded" in response.body:
        raise CloseSpider("bandwidth_exceeded")
```

### DontCloseSpider[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#dontclosespider)

- *异常*scrapy.exceptions.DontCloseSpider[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#DontCloseSpider)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.DontCloseSpider)

  

可以在 [`spider_idle`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#std-signal-spider_idle) 信号处理器中引发此异常，以防止爬虫被关闭。

### DropItem[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#dropitem)

- *异常*scrapy.exceptions.DropItem[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#DropItem)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.DropItem)

  

Item Pipeline 阶段必须引发此异常，以停止处理 Item。更多信息请参阅 [Item Pipeline](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline)。

### IgnoreRequest[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#ignorerequest)

- *异常*scrapy.exceptions.IgnoreRequest[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#IgnoreRequest)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.IgnoreRequest)

  

调度器或任何 downloader middleware 都可以引发此异常，表明请求应该被忽略。

### NotConfigured[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#notconfigured)

- *异常*scrapy.exceptions.NotConfigured[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#NotConfigured)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.NotConfigured)

  

此异常可以由某些组件引发，以指示它们将保持禁用状态。这些组件包括

- 扩展
- Item pipelines
- Downloader middlewares
- Spider middlewares

必须在组件的 `__init__` 方法中引发此异常。

### NotSupported[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#notsupported)

- *异常*scrapy.exceptions.NotSupported[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#NotSupported)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.NotSupported)

  

引发此异常以指示不支持的功能。

### StopDownload[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#stopdownload)

*在版本 2.2 中添加。*

- *异常*scrapy.exceptions.StopDownload(*fail=True*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/exceptions.html#StopDownload)[🔗](https://docs.scrapy.net.cn/en/latest/topics/exceptions.html#scrapy.exceptions.StopDownload)

  

从 [`bytes_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.bytes_received) 或 [`headers_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.headers_received) 信号处理器中引发，以指示不应再为响应下载更多字节。

布尔参数 `fail` 控制哪个方法将处理生成的响应

- 如果 `fail=True` (默认)，则调用请求的 errback。响应对象可作为 `StopDownload` 异常的 `response` 属性使用，该属性又作为接收到的 [`Failure`](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html) 对象的 `value` 属性存储。这意味着在定义为 `def errback(self, failure)` 的 errback 中，可以通过 `failure.value.response` 访问响应。
- 如果 `fail=False`，则改为调用请求的回调。

在这两种情况下，响应的主体可能会被截断：主体包含直到引发异常时接收到的所有字节，包括在引发异常的信号处理器中接收到的字节。此外，响应对象在其 [`flags`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.flags) 属性中被标记为 `"download_stopped"`。

注意

`fail` 是一个仅限关键字的参数，即引发 `StopDownload(False)` 或 `StopDownload(True)` 将引发一个 [`TypeError`](https://docs.pythonlang.cn/3/library/exceptions.html#TypeError)。

有关 [`bytes_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.bytes_received) 和 [`headers_received`](https://docs.scrapy.net.cn/en/latest/topics/signals.html#scrapy.signals.headers_received) 信号以及 [Stopping the download of a Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-stop-response-download) 主题的更多信息和示例，请参阅相关文档。























































































































































































































































































