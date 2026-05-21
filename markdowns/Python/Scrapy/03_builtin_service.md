<h1 style="text-align: center;">内置服务</h1>

# 1 日志

注意

`scrapy.log` 及其函数已被弃用，取而代之的是显式调用 Python 标准库的日志记录。继续阅读以了解新的日志记录系统。

Scrapy 使用 [`logging`](https://docs.pythonlang.cn/3/library/logging.html#module-logging) 进行事件日志记录。我们将提供一些简单的示例供您入门，但对于更高级的用例，强烈建议您仔细阅读其文档。

日志记录即开即用，并且可以在一定程度上通过 [日志设置](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-settings) 中列出的 Scrapy 设置进行配置。

Scrapy 在运行命令时会调用 [`scrapy.utils.log.configure_logging()`](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.utils.log.configure_logging) 来设置一些合理的默认值并处理 [日志设置](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-settings) 中的那些配置，因此如果您按照 [从脚本运行 Scrapy](https://docs.scrapy.net.cn/en/latest/topics/practices.html#run-from-script) 中所述从脚本运行 Scrapy，建议手动调用它。



## 日志级别[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#log-levels)

Python 内置的日志记录定义了 5 个不同的级别来指示给定日志消息的严重程度。以下是标准级别，按严重程度递减顺序列出：

1. `logging.CRITICAL` - 用于严重错误（最高严重程度）
2. `logging.ERROR` - 用于常规错误
3. `logging.WARNING` - 用于警告消息
4. `logging.INFO` - 用于信息性消息
5. `logging.DEBUG` - 用于调试消息（最低严重程度）

## 如何记录日志消息[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#how-to-log-messages)

以下是如何使用 `logging.WARNING` 级别记录消息的快速示例

```
import logging

logging.warning("This is a warning")
```

有用于发出标准 5 个级别中任何一个的日志消息的快捷方式，还有一个通用的 `logging.log` 方法，它接受给定的级别作为参数。如果需要，上一个示例可以改写为

```
import logging

logging.log(logging.WARNING, "This is a warning")
```

除此之外，您可以创建不同的“日志记录器”（loggers）来封装消息。（例如，一种常见做法是为每个模块创建不同的日志记录器）。这些日志记录器可以独立配置，并允许分层构造。

前面的示例在后台使用了根日志记录器，这是一个顶层日志记录器，所有消息都会传播到它（除非另有说明）。使用 `logging` 助手只是显式获取根日志记录器的一种快捷方式，因此这也与上一个代码片段等效

```
import logging

logger = logging.getLogger()
logger.warning("This is a warning")
```

您只需使用 `logging.getLogger` 函数获取其名称即可使用不同的日志记录器

```
import logging

logger = logging.getLogger("mycustomlogger")
logger.warning("This is a warning")
```

最后，您可以通过使用 `__name__` 变量，确保为您正在处理的任何模块拥有一个自定义日志记录器，该变量填充有当前模块的路径

```
import logging

logger = logging.getLogger(__name__)
logger.warning("This is a warning")
```

另请参阅

- logging 模块，[HowTo（操作指南）](https://docs.pythonlang.cn/3/howto/logging.html)

  基本日志记录教程

- logging 模块，[日志记录器（Loggers）](https://docs.pythonlang.cn/3/library/logging.html#logger)

  日志记录器的更多文档



## 从 Spiders 中记录日志[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#logging-from-spiders)

Scrapy 在每个 Spider 实例中提供了一个 [`logger`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.logger)，可以这样访问和使用它

```
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://scrapy.net.cn"]

    def parse(self, response):
        self.logger.info("Parse function called on %s", response.url)
```

该日志记录器是使用 Spider 的名称创建的，但您可以使用任何自定义 Python 日志记录器。例如

```
import logging
import scrapy

logger = logging.getLogger("mycustomlogger")


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://scrapy.net.cn"]

    def parse(self, response):
        logger.info("Parse function called on %s", response.url)
```



## 日志配置[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#logging-configuration)

日志记录器本身不管理通过它们发送的消息如何显示。对于此任务，可以将不同的“处理程序”（handlers）附加到任何日志记录器实例，它们会将这些消息重定向到适当的目标，例如标准输出、文件、电子邮件等。

默认情况下，Scrapy 根据以下设置，为根日志记录器设置和配置一个处理程序。



### 日志设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#logging-settings)

这些设置可用于配置日志记录

- [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE)
- [`LOG_FILE_APPEND`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE_APPEND)
- [`LOG_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENABLED)
- [`LOG_ENCODING`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENCODING)
- [`LOG_LEVEL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
- [`LOG_FORMAT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FORMAT)
- [`LOG_DATEFORMAT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_DATEFORMAT)
- [`LOG_STDOUT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_STDOUT)
- [`LOG_SHORT_NAMES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_SHORT_NAMES)

前几个设置定义了日志消息的目标。如果设置了 [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE)，通过根日志记录器发送的消息将被重定向到名为 [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE) 的文件，编码为 [`LOG_ENCODING`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENCODING)。如果未设置且 [`LOG_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENABLED) 为 `True`，日志消息将显示在标准错误输出。如果设置了 [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE) 且 [`LOG_FILE_APPEND`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE_APPEND) 为 `False`，文件将被覆盖（如果存在，则丢弃之前运行的输出）。最后，如果 [`LOG_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENABLED) 为 `False`，将不会有任何可见的日志输出。

[`LOG_LEVEL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_LEVEL) 确定要显示的最低严重级别，那些严重性较低的消息将被过滤掉。它涵盖了 [日志级别](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-levels) 中列出的所有可能级别。

[`LOG_FORMAT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FORMAT) 和 [`LOG_DATEFORMAT`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_DATEFORMAT) 分别指定用作所有消息布局的格式化字符串。这些字符串可以包含 [logging 的 logrecord 属性文档](https://docs.pythonlang.cn/3/library/logging.html#logrecord-attributes) 和 [datetime 的 strftime 和 strptime 指令](https://docs.pythonlang.cn/3/library/datetime.html#strftime-strptime-behavior) 中列出的任何占位符。

如果设置了 [`LOG_SHORT_NAMES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_SHORT_NAMES)，则日志不会显示打印日志的 Scrapy 组件。默认情况下未设置此项，因此日志包含负责该日志输出的 Scrapy 组件。

### 命令行选项[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#command-line-options)

有一些命令行参数可用于所有命令，您可以使用它们来覆盖一些与日志记录相关的 Scrapy 设置。

- - `--logfile FILE`

    覆盖 [`LOG_FILE`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FILE)

- - `--loglevel/-L LEVEL`

    覆盖 [`LOG_LEVEL`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_LEVEL)

- - `--nolog`

    将 [`LOG_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_ENABLED) 设置为 `False`

另请参阅

- 模块 [`logging.handlers`](https://docs.pythonlang.cn/3/library/logging.handlers.html#module-logging.handlers)

  可用处理程序的更多文档



### 自定义日志格式[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#custom-log-formats)

通过扩展 [`LogFormatter`](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter) 类并使 [`LOG_FORMATTER`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_FORMATTER) 指向您的新类，可以为不同的操作设置自定义日志格式。

- *class*scrapy.logformatter.LogFormatter[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter)

  用于为不同操作生成日志消息的类。所有方法必须返回一个字典，列出将用于在调用 `logging.log` 时构建日志消息的参数 `level`、`msg` 和 `args`。方法输出的字典键`level` 是该操作的日志级别，您可以使用 [python logging 库](https://docs.pythonlang.cn/3/library/logging.html) 中的级别：`logging.DEBUG`、`logging.INFO`、`logging.WARNING`、`logging.ERROR` 和 `logging.CRITICAL`。`msg` 应该是一个字符串，可以包含不同的格式化占位符。这个字符串，用提供的 `args` 格式化后，将成为该操作的长消息。`args` 应该是一个元组或字典，包含 `msg` 的格式化占位符。最终的日志消息计算为 `msg % args`。如果用户想自定义每个操作如何记录日志，或者想完全省略某个操作，可以定义自己的 `LogFormatter` 类。要省略记录某个操作，方法必须返回 `None`。以下是创建一个自定义日志格式化器的示例，该格式化器在项目从管道中丢弃时降低日志消息的严重级别`class PoliteLogFormatter(logformatter.LogFormatter):    def dropped(self, item, exception, response, spider):        return {            'level': logging.INFO, # lowering the level from logging.WARNING            'msg': "Dropped: %(exception)s" + os.linesep + "%(item)s",            'args': {                'exception': exception,                'item': item,            }        } `crawled(*request: [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)*, *response: [Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.crawled)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.crawled)当爬虫找到一个网页时记录消息。download_error(*failure: [Failure](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html)*, *request: [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*, *errmsg: [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.download_error)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.download_error)记录来自 spider 的下载错误消息（通常来自引擎）。*在 2.0 版本中新增。*dropped(*item: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*, *exception: [BaseException](https://docs.pythonlang.cn/3/library/exceptions.html#BaseException)*, *response: [Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.dropped)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.dropped)当项目在通过项目管道时被丢弃时记录消息。item_error(*item: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*, *exception: [BaseException](https://docs.pythonlang.cn/3/library/exceptions.html#BaseException)*, *response: [Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.item_error)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.item_error)当项目在通过项目管道时导致错误时记录消息。*在 2.0 版本中新增。*scraped(*item: [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)*, *response: [Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) | [Failure](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html) | [None](https://docs.pythonlang.cn/3/library/constants.html#None)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.scraped)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.scraped)当一个项目被 spider 抓取时记录消息。spider_error(*failure: [Failure](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html)*, *request: [Request](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)*, *response: [Response](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) | [Failure](https://docs.twisted.org.cn/en/stable/api/twisted.python.failure.Failure.html)*, *spider: [Spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.Spider)*)→ LogFormatterResult[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/logformatter.html#LogFormatter.spider_error)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.logformatter.LogFormatter.spider_error)记录来自 spider 的错误消息。*在 2.0 版本中新增。*



### 高级自定义[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#advanced-customization)

因为 Scrapy 使用 stdlib logging 模块，所以您可以使用 stdlib logging 的所有功能来自定义日志记录。

例如，假设您正在抓取一个返回大量 HTTP 404 和 500 响应的网站，并且您想隐藏所有类似这样的消息

```
2016-12-16 22:00:06 [scrapy.spidermiddlewares.httperror] INFO: Ignoring
response <500 https://quotes.toscrape.com/page/1-34/>: HTTP status code
is not handled or not allowed
```

首先要注意的是日志记录器名称——它在方括号中：`[scrapy.spidermiddlewares.httperror]`。如果您只看到 `[scrapy]`，那很可能是 [`LOG_SHORT_NAMES`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-LOG_SHORT_NAMES) 设置为 True；将其设置为 False 并重新运行爬取。

接下来，我们可以看到消息的级别是 INFO。要隐藏它，我们应该将 `scrapy.spidermiddlewares.httperror` 的日志级别设置为高于 INFO；INFO 之后的下一个级别是 WARNING。这可以在 spider 的 `__init__` 方法中完成，例如

```
import logging
import scrapy


class MySpider(scrapy.Spider):
    # ...
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("scrapy.spidermiddlewares.httperror")
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)
```

如果您再次运行此 spider，则来自 `scrapy.spidermiddlewares.httperror` 日志记录器的 INFO 消息将不再出现。

您还可以通过 [`LogRecord`](https://docs.pythonlang.cn/3/library/logging.html#logging.LogRecord) 数据过滤日志记录。例如，您可以使用子字符串或正则表达式按消息内容过滤日志记录。创建一个 [`logging.Filter`](https://docs.pythonlang.cn/3/library/logging.html#logging.Filter) 子类，并为其配备一个正则表达式模式来过滤掉不需要的消息

```
import logging
import re


class ContentFilter(logging.Filter):
    def filter(self, record):
        match = re.search(r"\d{3} [Ee]rror, retrying", record.message)
        if match:
            return False
```

可以将项目级别的过滤器附加到 Scrapy 创建的根处理程序，这是过滤项目不同部分（中间件、spider 等）中所有日志记录器的便捷方法。

```
import logging
import scrapy


class MySpider(scrapy.Spider):
    # ...
    def __init__(self, *args, **kwargs):
        for handler in logging.root.handlers:
            handler.addFilter(ContentFilter())
```

或者，您可以选择一个特定的日志记录器并将其隐藏，而不会影响其他日志记录器

```
import logging
import scrapy


class MySpider(scrapy.Spider):
    # ...
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("my_logger")
        logger.addFilter(ContentFilter())
```



## scrapy.utils.log 模块[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#module-scrapy.utils.log)

- scrapy.utils.log.configure_logging(*settings: [Settings](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.settings.Settings) | [dict](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)[[bool](https://docs.pythonlang.cn/3/library/functions.html#bool) | [float](https://docs.pythonlang.cn/3/library/functions.html#float) | [int](https://docs.pythonlang.cn/3/library/functions.html#int) | [str](https://docs.pythonlang.cn/3/library/stdtypes.html#str) | [None](https://docs.pythonlang.cn/3/library/constants.html#None), [Any](https://docs.pythonlang.cn/3/library/typing.html#typing.Any)] | [None](https://docs.pythonlang.cn/3/library/constants.html#None) = None*, *install_root_handler: [bool](https://docs.pythonlang.cn/3/library/functions.html#bool) = True*)→ [None](https://docs.pythonlang.cn/3/library/constants.html#None)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/utils/log.html#configure_logging)[🔗](https://docs.scrapy.net.cn/en/latest/topics/logging.html#scrapy.utils.log.configure_logging)

  为 Scrapy 初始化日志记录默认值。参数：**settings** (dict, [`Settings`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.settings.Settings) 对象或 `None`) – 用于为根日志记录器创建和配置处理程序的设置（默认值：None）。**install_root_handler** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 是否安装根日志处理程序（默认值：True）此函数执行以下操作：通过 Python 标准日志记录路由警告和 Twisted 日志分别将 DEBUG 和 ERROR 级别分配给 Scrapy 和 Twisted 日志记录器如果 LOG_STDOUT 设置为 True，则将 stdout 路由到日志当 `install_root_handler` 为 True（默认值）时，此函数还会根据给定设置（参见 [日志设置](https://docs.scrapy.net.cn/en/latest/topics/logging.html#topics-logging-settings)）为根日志记录器创建一个处理程序。您可以使用 `settings` 参数覆盖默认选项。当 `settings` 为空或 None 时，将使用默认值。使用 Scrapy 命令或 [`CrawlerProcess`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerProcess) 时会自动调用 `configure_logging`，但使用 [`CrawlerRunner`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerRunner) 运行自定义脚本时需要显式调用它。在这种情况下，不强制要求使用它，但建议使用。运行自定义脚本时的另一个选项是手动配置日志记录。为此，您可以使用 [`logging.basicConfig()`](https://docs.pythonlang.cn/3/library/logging.html#logging.basicConfig) 设置一个基本的根处理程序。请注意，[`CrawlerProcess`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerProcess) 会自动调用 `configure_logging`，因此建议仅与 [`CrawlerRunner`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.CrawlerRunner) 一起使用 [`logging.basicConfig()`](https://docs.pythonlang.cn/3/library/logging.html#logging.basicConfig)。以下是如何将 `INFO` 或更高级别的消息重定向到文件的示例`import logging logging.basicConfig(    filename="log.txt", format="%(levelname)s: %(message)s", level=logging.INFO ) `有关以这种方式使用 Scrapy 的更多详细信息，请参阅 [从脚本运行 Scrapy](https://docs.scrapy.net.cn/en/latest/topics/practices.html#run-from-script)。

# 2 统计收集

Scrapy 提供了一个方便的工具，用于以键/值对的形式收集统计数据，其中值通常是计数器。这个工具称为 Stats Collector，可以通过 [Crawler API](https://docs.scrapy.net.cn/en/latest/topics/api.html#topics-api-crawler) 的 [`stats`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler.stats) 属性访问，具体示例见下方的[Stats Collector 的常见用法](https://docs.scrapy.net.cn/en/latest/topics/stats.html#topics-stats-usecases)部分。

但是，Stats Collector 始终可用，因此无论是否启用统计数据收集，您都可以随时在模块中导入并使用其 API（递增或设置新的统计键）。如果它被禁用，API 仍然有效，但不会收集任何数据。这样做的目的是简化 Stats Collector 用法：在爬虫、Scrapy 扩展或任何使用 Stats Collector 的代码中，您只需一行代码即可进行统计收集。

Stats Collector 的另一个特点是，它在启用时效率很高，在禁用时效率极高（几乎不会引起注意）。

Stats Collector 为每个开启的爬虫维护一个统计表，该表在爬虫开启时自动开启，在爬虫关闭时自动关闭。



## Stats Collector 的常见用法[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#common-stats-collector-uses)

通过 [`stats`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler.stats) 属性访问统计收集器。这是一个访问统计数据的扩展示例：

```
class ExtensionThatAccessStats:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
```

设置统计值

```
stats.set_value("hostname", socket.gethostname())
```

递增统计值

```
stats.inc_value("custom_count")
```

仅当值大于前一个值时设置

```
stats.max_value("max_items_scraped", value)
```

仅当值小于前一个值时设置

```
stats.min_value("min_free_memory_percent", value)
```

获取统计值

```
stats.get_value("custom_count")
1
```

获取所有统计数据

```
stats.get_stats()
{'custom_count': 1, 'start_time': datetime.datetime(2009, 7, 14, 21, 47, 28, 977139)}
```

## 可用的 Stats Collector[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#available-stats-collectors)

除了基本的 `StatsCollector`，Scrapy 中还有其他继承了基础 Stats Collector 的可用 Stats Collector。您可以通过 [`STATS_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-STATS_CLASS) 设置来选择使用的 Stats Collector。默认使用的 Stats Collector 是 `MemoryStatsCollector`。

### MemoryStatsCollector[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#memorystatscollector)

- *class*scrapy.statscollectors.MemoryStatsCollector[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/statscollectors.html#MemoryStatsCollector)[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#scrapy.statscollectors.MemoryStatsCollector)

  一个简单的统计收集器，它在爬虫关闭后将上次运行（针对每个爬虫）的统计数据保存在内存中。这些统计数据可以通过 [`spider_stats`](https://docs.scrapy.net.cn/en/latest/topics/stats.html#scrapy.statscollectors.MemoryStatsCollector.spider_stats) 属性访问，该属性是一个以爬虫域名为键的字典。这是 Scrapy 中默认使用的 Stats Collector。spider_stats[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#scrapy.statscollectors.MemoryStatsCollector.spider_stats)一个字典的字典（以爬虫名称为键），包含每个爬虫上次抓取运行的统计数据。

### DummyStatsCollector[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#dummystatscollector)

- *class*scrapy.statscollectors.DummyStatsCollector[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/statscollectors.html#DummyStatsCollector)[🔗](https://docs.scrapy.net.cn/en/latest/topics/stats.html#scrapy.statscollectors.DummyStatsCollector)

  一个不做任何事情但效率极高（因为它什么都不做）的统计收集器。可以通过 [`STATS_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-STATS_CLASS) 设置此收集器，以禁用统计数据收集，从而提高性能。然而，与页面解析等其他 Scrapy 工作负载相比，统计收集的性能损失通常微不足道。

# 3 发送电子邮件

尽管 Python 通过 [`smtplib`](https://docs.pythonlang.cn/3/library/smtplib.html#module-smtplib) 库发送电子邮件相对容易，但 Scrapy 提供了自己的电子邮件发送功能，该功能非常易于使用，并且使用 [Twisted 非阻塞 IO](https://docs.twisted.org.cn/en/stable/core/howto/defer-intro.html) 实现，以避免干扰爬虫的非阻塞 IO。它还提供了一个简单的 API 用于发送附件，并且配置非常简单，只需几个[设置](https://docs.scrapy.net.cn/en/latest/topics/email.html#topics-email-settings)即可。

## 快速示例[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#quick-example)

有两种方法实例化邮件发送器。你可以使用标准的 `__init__` 方法进行实例化

```
from scrapy.mail import MailSender

mailer = MailSender()
```

或者，你可以传递一个 `scrapy.Crawler` 实例进行实例化，这将遵循[设置](https://docs.scrapy.net.cn/en/latest/topics/email.html#topics-email-settings)

```
mailer = MailSender.from_crawler(crawler)
```

以下是如何使用它发送电子邮件（不带附件）

```
mailer.send(
    to=["someone@example.com"],
    subject="Some subject",
    body="Some body",
    cc=["another@example.com"],
)
```

## MailSender 类参考[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mailsender-class-reference)

MailSender [组件](https://docs.scrapy.net.cn/en/latest/topics/components.html#topics-components) 是从 Scrapy 发送电子邮件的首选类，因为它像框架的其他部分一样使用 [Twisted 非阻塞 IO](https://docs.twisted.org.cn/en/stable/core/howto/defer-intro.html)。

- *class*scrapy.mail.MailSender(*smtphost=None*, *mailfrom=None*, *smtpuser=None*, *smtppass=None*, *smtpport=None*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/mail.html#MailSender)[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#scrapy.mail.MailSender)

  参数:**smtphost** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *or* [*bytes*](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes)) – 用于发送电子邮件的 SMTP 主机。如果省略，将使用 [`MAIL_HOST`](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_HOST) 设置。**mailfrom** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 用于发送电子邮件的地址（在 `From:` 头部）。如果省略，将使用 [`MAIL_FROM`](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_FROM) 设置。**smtpuser** – SMTP 用户名。如果省略，将使用 [`MAIL_USER`](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_USER) 设置。如果未给出，将不执行 SMTP 认证。**smtppass** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *or* [*bytes*](https://docs.pythonlang.cn/3/library/stdtypes.html#bytes)) – 用于认证的 SMTP 密码。**smtpport** ([*int*](https://docs.pythonlang.cn/3/library/functions.html#int)) – 要连接的 SMTP 端口。**smtptls** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 强制使用 SMTP STARTTLS。**smtpssl** ([*bool*](https://docs.pythonlang.cn/3/library/functions.html#bool)) – 强制使用安全的 SSL 连接。send(*to*, *subject*, *body*, *cc=None*, *attachs=()*, *mimetype='text/plain'*, *charset=None*)[[source\]](https://docs.scrapy.net.cn/en/latest/_modules/scrapy/mail.html#MailSender.send)[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#scrapy.mail.MailSender.send)向指定的收件人发送电子邮件。参数:**to** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *or* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 电子邮件收件人，可以是字符串或字符串列表。**subject** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 电子邮件的主题。**cc** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str) *or* [*list*](https://docs.pythonlang.cn/3/library/stdtypes.html#list)) – 抄送的电子邮件地址，可以是字符串或字符串列表。**body** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 电子邮件正文。**attachs** ([*collections.abc.Iterable*](https://docs.pythonlang.cn/3/library/collections.abc.html#collections.abc.Iterable)) – 一个包含元组 `(attach_name, mimetype, file_object)` 的可迭代对象，其中 `attach_name` 是一个字符串，表示电子邮件附件中显示的名称，`mimetype` 是附件的 mimetype，`file_object` 是一个可读的文件对象，包含附件的内容。**mimetype** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 电子邮件的 MIME 类型。**charset** ([*str*](https://docs.pythonlang.cn/3/library/stdtypes.html#str)) – 电子邮件内容使用的字符编码。



## 邮件设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-settings)

这些设置定义了 [`MailSender`](https://docs.scrapy.net.cn/en/latest/topics/email.html#scrapy.mail.MailSender) 类的默认 `__init__` 方法值，可用于在项目中配置电子邮件通知，而无需编写任何代码（对于使用 [`MailSender`](https://docs.scrapy.net.cn/en/latest/topics/email.html#scrapy.mail.MailSender) 的扩展和代码）。



### MAIL_FROM[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-from)

默认值：`'scrapy@localhost'`

发送电子邮件时使用的发件人电子邮件地址（`From:` 头部）。



### MAIL_HOST[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-host)

默认值：`'localhost'`

用于发送电子邮件的 SMTP 主机。



### MAIL_PORT[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-port)

默认值：`25`

用于发送电子邮件的 SMTP 端口。



### MAIL_USER[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-user)

默认值：`None`

用于 SMTP 认证的用户名。如果禁用，将不执行 SMTP 认证。



### MAIL_PASS[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-pass)

默认值：`None`

用于 SMTP 认证的密码，与 [`MAIL_USER`](https://docs.scrapy.net.cn/en/latest/topics/email.html#std-setting-MAIL_USER) 一起使用。



### MAIL_TLS[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-tls)

默认值：`False`

强制使用 STARTTLS。STARTTLS 是一种将现有非安全连接升级为使用 SSL/TLS 的安全连接的方式。



### MAIL_SSL[🔗](https://docs.scrapy.net.cn/en/latest/topics/email.html#mail-ssl)

默认值：`False`

强制使用 SSL 加密连接进行连接。

# 4 Telnet 控制台

Scrapy 内置了一个 telnet 控制台，用于检查和控制正在运行的 Scrapy 进程。telnet 控制台只是运行在 Scrapy 进程内部的一个普通 python shell，因此您可以在其中执行任何操作。

telnet 控制台是一个[内置的 Scrapy 扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref)，默认启用，但您也可以根据需要禁用它。有关此扩展本身的更多信息，请参阅[Telnet 控制台扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions-ref-telnetconsole)。

警告

通过公共网络使用 telnet 控制台是不安全的，因为 telnet 不提供任何传输层安全性。即使有用户名/密码认证也无法改变这一点。

预期用途是本地连接到正在运行的 Scrapy 爬虫（爬虫进程和 telnet 客户端在同一台机器上）或通过安全连接（VPN、SSH 隧道）。请避免通过不安全的连接使用 telnet 控制台，或者通过使用 [`TELNETCONSOLE_ENABLED`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-TELNETCONSOLE_ENABLED) 选项完全禁用它。

## 如何访问 telnet 控制台[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#how-to-access-the-telnet-console)

telnet 控制台侦听在 [`TELNETCONSOLE_PORT`](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_PORT) 设置中定义的 TCP 端口，默认为 `6023`。要访问控制台，您需要输入

```
telnet localhost 6023
Trying localhost...
Connected to localhost.
Escape character is '^]'.
Username:
Password:
>>>
```

默认情况下，用户名是 `scrapy`，密码是自动生成的。自动生成的密码可以在 Scrapy 日志中看到，例如以下示例

```
2018-10-16 14:35:21 [scrapy.extensions.telnet] INFO: Telnet Password: 16f92501e8a59326
```

默认用户名和密码可以通过设置 [`TELNETCONSOLE_USERNAME`](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_USERNAME) 和 [`TELNETCONSOLE_PASSWORD`](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#std-setting-TELNETCONSOLE_PASSWORD) 进行覆盖。

警告

用户名和密码只提供有限的保护，因为 telnet 不使用安全传输 - 即使设置了用户名和密码，流量默认也是未加密的。

您需要 telnet 程序，它在 Windows 和大多数 Linux 发行版中默认安装。



## telnet 控制台中可用的变量[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#available-variables-in-the-telnet-console)

telnet 控制台就像运行在 Scrapy 进程内部的一个普通 Python shell，因此您可以在其中执行任何操作，包括导入新模块等。

然而，telnet 控制台提供了一些为方便起见而定义的默认变量

| 快捷方式     | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| `crawler`    | Scrapy Crawler ([`scrapy.crawler.Crawler`](https://docs.scrapy.net.cn/en/latest/topics/api.html#scrapy.crawler.Crawler) 对象) |
| `engine`     | Crawler.engine 属性                                          |
| `spider`     | 当前活跃的爬虫                                               |
| `extensions` | 扩展管理器 (Crawler.extensions 属性)                         |
| `stats`      | 统计信息收集器 (Crawler.stats 属性)                          |
| `settings`   | Scrapy 设置对象 (Crawler.settings 属性)                      |
| `est`        | 打印引擎状态报告                                             |
| `prefs`      | 用于内存调试 (参见 [调试内存泄漏](https://docs.scrapy.net.cn/en/latest/topics/leaks.html#topics-leaks)) |
| `p`          | [`pprint.pprint()`](https://docs.pythonlang.cn/3/library/pprint.html#pprint.pprint) 函数的快捷方式 |
| `hpy`        | 用于内存调试 (参见 [调试内存泄漏](https://docs.scrapy.net.cn/en/latest/topics/leaks.html#topics-leaks)) |

## telnet 控制台使用示例[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnet-console-usage-examples)

以下是一些可以使用 telnet 控制台完成的示例任务

### 查看引擎状态[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#view-engine-status)

您可以使用 Scrapy 引擎的 `est()` 方法通过 telnet 控制台快速显示其状态

```
telnet localhost 6023
>>> est()
Execution engine status

time()-engine.start_time                        : 8.62972998619
len(engine.downloader.active)                   : 16
engine.scraper.is_idle()                        : False
engine.spider.name                              : followall
engine.spider_is_idle()                         : False
engine._slot.closing                            : False
len(engine._slot.inprogress)                    : 16
len(engine._slot.scheduler.dqs or [])           : 0
len(engine._slot.scheduler.mqs)                 : 92
len(engine.scraper.slot.queue)                  : 0
len(engine.scraper.slot.active)                 : 0
engine.scraper.slot.active_size                 : 0
engine.scraper.slot.itemproc_size               : 0
engine.scraper.slot.needs_backout()             : False
```

### 暂停、恢复和停止 Scrapy 引擎[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#pause-resume-and-stop-the-scrapy-engine)

暂停

```
telnet localhost 6023
>>> engine.pause()
>>>
```

恢复

```
telnet localhost 6023
>>> engine.unpause()
>>>
```

停止

```
telnet localhost 6023
>>> engine.stop()
Connection closed by foreign host.
```

## Telnet 控制台信号[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnet-console-signals)

- scrapy.extensions.telnet.update_telnet_vars(*telnet_vars*)[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#scrapy.extensions.telnet.update_telnet_vars)

  在 telnet 控制台打开之前发送。您可以连接到此信号以添加、删除或更新将在 telnet 本地命名空间中可用的变量。为此，您需要在处理程序中更新 `telnet_vars` dict。参数:**telnet_vars** ([*dict*](https://docs.pythonlang.cn/3/library/stdtypes.html#dict)) – telnet 变量的字典

## Telnet 设置[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnet-settings)

这些设置控制 telnet 控制台的行为



### TELNETCONSOLE_PORT[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnetconsole-port)

默认值: `[6023, 6073]`

telnet 控制台使用的端口范围。如果设置为 `None`，则使用动态分配的端口。



### TELNETCONSOLE_HOST[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnetconsole-host)

默认值: `'127.0.0.1'`

telnet 控制台应该监听的接口



### TELNETCONSOLE_USERNAME[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnetconsole-username)

默认值: `'scrapy'`

用于 telnet 控制台的用户名



### TELNETCONSOLE_PASSWORD[🔗](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#telnetconsole-password)

默认值: `None`

用于 telnet 控制台的密码，默认行为是自动生成









