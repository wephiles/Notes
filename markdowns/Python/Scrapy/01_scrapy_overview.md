<h1 style="text-align: center;">Scrapy 概览</h1>

---

[TOC]

# 1 一个小示例

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/tag/humor/",  # 开始 url，Scrapy爬虫从此url开始
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            # yield一个字典，引擎会认识这个字典 -- 这个字典是已经获取到的数据，于是可以在后续保存或者处理
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            # yield 一个Requests对象，引擎会知道，这些Requests对象是需要进一步交给调度器，再交由下载器下载的
            yield response.follow(next_page, self.parse)
```

使用下面的命令运行上述代码，那么爬虫程序将会进行爬虫，获取到一个字典数据就向 `data.jsonl` 这个 `JSONLines` 文件中写入一条字典数据。

```python
scrapy runspider .\quick_start.py -o data.jsonl
```

爬虫完毕后，获取到的数据就像下面这样:

```json
{"author": "Jane Austen", "text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d"}
{"author": "Steve Martin", "text": "\u201cA day without sunshine is like, you know, night.\u201d"}
```

## 1.1 刚才发生了什么

当您运行命令 `scrapy runspider quotes_spider.py` 时，Scrapy 会在其中查找 Spider 定义，并通过其爬虫引擎运行它。

爬取过程始于对 `start_urls` 属性中定义的 URL（在此例中，仅是“幽默”类别的引言 URL）发起请求，并调用默认的回调方法 `parse`，将响应对象作为参数传递。在 `parse` 回调中，我们使用 CSS 选择器遍历引言元素，生成一个包含提取的引言文本和作者的 Python 字典，然后查找指向下一页的链接，并使用相同的 `parse` 方法作为回调来调度另一个请求。

在这里您会注意到 Scrapy 的主要优势之一：请求是[异步调度和处理](https://docs.scrapy.net.cn/en/latest/topics/architecture.html#topics-architecture)的。这意味着 Scrapy 不需要等待一个请求完成并处理完毕，它可以在此期间发送另一个请求或执行其他操作。这也意味着即使某个请求失败或在处理过程中发生错误，其他请求仍然可以继续进行。

虽然这使得您可以进行非常快速的爬取（以容错的方式同时发送多个并发请求），但 Scrapy 也允许您通过[一些设置](https://docs.scrapy.net.cn/en/latest/topics/settings.html#topics-settings-ref)来控制爬取的礼貌性。您可以设置每个请求之间的下载延迟，限制每个域名或每个 IP 的并发请求数量，甚至[使用自动限速扩展](https://docs.scrapy.net.cn/en/latest/topics/autothrottle.html#topics-autothrottle)来尝试自动确定这些设置。

> [!Note]
>
> 这使用了[feed 导出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-exports)来生成 JSON 文件，您可以轻松更改导出格式（例如 XML 或 CSV）或存储后端（例如 FTP 或 [Amazon S3](https://aws.amazon.com/s3/)）。您还可以编写一个[Item Pipeline](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline) 将 item 存储到数据库中。

## 1.2 还有什么

您已经了解了如何使用 Scrapy 从网站提取和存储 item，但这只是冰山一角。Scrapy 提供了许多强大功能，使抓取变得简单高效，例如：

- 内置支持使用扩展的 CSS 选择器和 XPath 表达式从 HTML/XML 源[选择和提取](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#topics-selectors)数据，并提供使用正则表达式进行提取的辅助方法。
- 提供一个[交互式 shell 控制台](https://docs.scrapy.net.cn/en/latest/topics/shell.html#topics-shell)（支持 `IPython`），用于尝试 CSS 和 XPath 表达式来抓取数据，这在编写或调试 Spider 时非常有用。
- 内置支持以多种格式（JSON、CSV、XML）[生成 feed 导出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-exports)，并将其存储到多个后端（FTP、S3、本地文件系统）。
- 强大的编码支持和自动检测，用于处理外部、非标准和损坏的编码声明。
- [强大的扩展性支持](https://docs.scrapy.net.cn/en/latest/index.html#extending-scrapy)，允许您使用[信号](https://docs.scrapy.net.cn/en/latest/topics/signals.html#topics-signals)和定义良好的 API（中间件、[扩展](https://docs.scrapy.net.cn/en/latest/topics/extensions.html#topics-extensions)和[管道](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline)）插入自己的功能。
- 广泛的内置扩展和中间件，用于处理：
  - cookies 和会话处理
  - HTTP 功能，如压缩、认证、缓存
  - 模拟用户代理
  - robots.txt
  - 爬取深度限制
  - 等等
- 一个 [Telnet 控制台](https://docs.scrapy.net.cn/en/latest/topics/telnetconsole.html#topics-telnetconsole)，用于连接到在 Scrapy 进程中运行的 Python 控制台，以便内省和调试爬虫。
- 此外还有其他好东西，例如可重用的 Spider，用于从 [Sitemaps](https://www.sitemaps.org/index.html) 和 XML/CSV feed 爬取站点；一个媒体管道，用于[自动下载](https://docs.scrapy.net.cn/en/latest/topics/media-pipeline.html#topics-media-pipeline)与抓取到的 item 相关的图片（或任何其他媒体）；一个缓存 DNS 解析器；以及更多！

# 2 安装指南

> 详细的安装细节参考 Scrapy官方文档 [Scrapy安装指南(中文版)](https://docs.scrapy.net.cn/en/latest/intro/install.html)

# 3 Scrapy 教程

本教程假设您的系统上已经安装了 Scrapy。如果还没有安装，请参阅[安装指南](https://docs.scrapy.net.cn/en/latest/intro/install.html#intro-install)。

我们将要抓取[quotes.toscrape.com](https://quotes.toscrape.com/)，这是一个列出著名作者引言的网站。

本教程将引导您完成以下任务

1. 创建新的 Scrapy 项目
2. 编写一个[spider](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#topics-spiders) 来抓取网站并提取数据
3. 使用命令行导出抓取到的数据
4. 修改 spider 以递归跟踪链接
5. 使用 spider 参数

Scrapy 是用[Python](https://pythonlang.cn/)编写的。您对 Python 了解得越多，Scrapy 的作用就越大。

如果您已经熟悉其他语言并想快速学习 Python，[Python 教程](https://docs.pythonlang.cn/3/tutorial)是一个很好的资源。

如果您是编程新手并想从 Python 开始，以下书籍可能对您有用

- [利用 Python 自动化无聊的工作](https://automatetheboringstuff.com/)
- [像计算机科学家一样思考](http://openbookproject.net/thinkcs/python/english3e/)
- [笨方法学 Python 3](https://learnpythonthehardway.org/python3/)

您还可以查看[这份面向非程序员的 Python 资源列表](https://wiki.python.org/moin/BeginnersGuide/NonProgrammers)，以及 [learnpython-subreddit 中推荐的资源](https://www.reddit.com/r/learnpython/wiki/index#wiki_new_to_python.3F)。

## 3.1 创建项目

在开始抓取之前，您需要设置一个新的 Scrapy 项目。进入您想要存储代码的目录并运行

```
scrapy startproject tutorial
```

这将创建一个名为`tutorial` 的目录，其内容如下

```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

## 3.2 第一个 spider

Spider 是您定义的类，Scrapy 使用它们从网站（或一组网站）抓取信息。它们必须继承自[`Spider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider)，并定义初始请求，以及（可选地）如何跟踪页面中的链接和解析下载的页面内容以提取数据。

这是我们第一个 Spider 的代码。将其保存在项目目录 `tutorial/spiders` 下名为 `quotes_spider.py` 的文件中

```
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
```

正如您所看到的，我们的 Spider 继承自[`scrapy.Spider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider)，并定义了一些属性和方法

- [`name`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.name)：用于标识 Spider。它在项目内必须是唯一的，也就是说，您不能为不同的 Spider 设置相同的名称。

- [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start)：必须是一个异步生成器，用于产生供 spider 开始抓取的请求（以及可选的 item）。后续请求将从这些初始请求中连续生成。

- [`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse)：一个将被调用的方法，用于处理每个请求下载的响应。response 参数是[`TextResponse`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse) 的一个实例，它包含页面内容并具有其他有用的方法来处理它。

  [`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 方法通常会解析响应，将抓取到的数据提取为字典，并找到要跟踪的新 URL 并从中创建新的请求（[`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)）。

### 3.2.1 如何运行

要运行我们的 spider，请进入项目的顶层目录并运行

```
scrapy crawl quotes
```

此命令会运行我们刚刚添加的名为 `quotes` 的 spider，它将向 `quotes.toscrape.com` 域发送一些请求。您将获得类似于以下的输出

```
... (omitted for brevity)
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Spider opened
2016-12-16 21:24:05 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-12-16 21:24:05 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://quotes.toscrape.com/robots.txt> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/2/> (referer: None)
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-1.html
2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-2.html
2016-12-16 21:24:05 [scrapy.core.engine] INFO: Closing spider (finished)
...
```

现在，检查当前目录中的文件。您应该注意到已创建了两个新文件：*quotes-1.html* 和 *quotes-2.html*，包含相应 URL 的内容，正如我们的 `parse` 方法所指示的。

> 注意：
>
> 如果您想知道为什么我们还没有解析 HTML，请稍等，我们很快就会介绍。

### 3.2.2 背后发生了什么

Scrapy 发送由 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) spider 方法产生的第一个 [`scrapy.Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象。在收到每个请求的响应后，Scrapy 会调用与请求关联的回调方法（在本例中是 `parse` 方法），并传入一个 [`Response`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response) 对象。

### 3.2.3 start 方法的快捷方式

您可以不实现一个产生来自 URL 的 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request) 对象的 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 方法，而是定义一个带有 URL 列表的 [`start_urls`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start_urls) 类属性。然后，这个列表将由 [`start()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.start) 的默认实现用来创建您的 spider 的初始请求。

```
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
```

即使我们没有明确告诉 Scrapy 这样做，[`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 方法也会被调用来处理这些 URL 的每个请求。发生这种情况是因为 <u>[`parse()`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.Spider.parse) 是 Scrapy 的默认回调方法，它会被用于没有明确指定回调的请求。</u>

### 3.2.4 提取数据

学习如何使用 Scrapy 提取数据的最好方法是使用[Scrapy shell](https://docs.scrapy.net.cn/en/latest/topics/shell.html#topics-shell)尝试选择器。运行

```
scrapy shell 'https://quotes.toscrape.com/page/1/'
```

注意

请记住，从命令行运行 Scrapy shell 时，务必将 URL 用引号括起来，否则包含参数（即 `&` 字符）的 URL 将无法工作。

在 Windows 上，请使用双引号

```
scrapy shell "https://quotes.toscrape.com/page/1/"
```

您将看到类似以下的内容

```bash
2025-12-17 10:29:09 [scrapy.utils.log] INFO: Scrapy 2.13.4 started (bot: Demo)
2025-12-17 10:29:09 [scrapy.utils.log] INFO: Versions:
{'lxml': '6.0.2',
 'libxml2': '2.11.9',
 'cssselect': '1.3.0',
 'parsel': '1.10.0',
 'w3lib': '2.3.1',
 'Twisted': '25.5.0',
 'Python': '3.13.4 (tags/v3.13.4:8a526ec, Jun  3 2025, 17:46:04) [MSC v.1943 '
           '64 bit (AMD64)]',
 'pyOpenSSL': '25.3.0 (OpenSSL 3.5.4 30 Sep 2025)',
 'cryptography': '46.0.3',
 'Platform': 'Windows-11-10.0.26200-SP0'}
2025-12-17 10:29:09 [scrapy.addons] INFO: Enabled addons:
[]
2025-12-17 10:29:09 [asyncio] DEBUG: Using selector: SelectSelector
2025-12-17 10:29:09 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.asyncioreactor.AsyncioSelectorReactor
2025-12-17 10:29:09 [scrapy.utils.log] DEBUG: Using asyncio event loop: asyncio.windows_events._WindowsSelectorEventLoop
2025-12-17 10:29:09 [scrapy.extensions.telnet] INFO: Telnet Password: af38f4a1859f96d7
2025-12-17 10:29:09 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole']
2025-12-17 10:29:09 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'Demo',
 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
 'DOWNLOAD_DELAY': 1,
 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
 'FEED_EXPORT_ENCODING': 'utf-8',
 'LOGSTATS_INTERVAL': 0,
 'NEWSPIDER_MODULE': 'Demo.spiders',
 'SPIDER_MODULES': ['Demo.spiders']}
2025-12-17 10:29:10 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2025-12-17 10:29:10 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.start.StartSpiderMiddleware',
 'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2025-12-17 10:29:10 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2025-12-17 10:29:10 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2025-12-17 10:29:10 [scrapy.core.engine] INFO: Spider opened
2025-12-17 10:29:11 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x000001A397150590>
[s]   item       {}
[s]   request    <GET https://quotes.toscrape.com/page/1/>
[s]   response   <200 https://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x000001A39709AD50>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
>>>
```

使用 shell，您可以使用响应对象尝试使用[CSS](https://www.w3.org/TR/selectors)选择元素

```
response.css("title")
[<Selector query='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```

运行 `response.css('title')` 的结果是一个类似列表的对象，称为 [`SelectorList`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList)，它代表一个 [`Selector`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.Selector) 对象的列表，这些对象包装了 XML/HTML 元素，并允许您运行进一步的查询来细化选择或提取数据。

要提取上面标题的文本，您可以这样做

```
response.css("title::text").getall()
['Quotes to Scrape']
```

这里有两点需要注意：一是我们在 CSS 查询中添加了 `::text`，这意味着我们只想选择 `<title>` 元素内部的文本元素。如果我们不指定 `::text`，我们将获得完整的标题元素，包括其标签

```
response.css("title").getall()
['<title>Quotes to Scrape</title>']
```

另一点是调用 `.getall()` 的结果是一个列表：选择器可能返回多个结果，因此我们提取所有结果。当您知道只需要第一个结果时（就像在本例中），您可以这样做

```
response.css("title::text").get()
'Quotes to Scrape'
```

作为替代方案，您可以这样写

```
response.css("title::text")[0].get()
'Quotes to Scrape'
```

访问 [`SelectorList`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList) 实例上的索引，如果没有结果，将引发 [`IndexError`](https://docs.pythonlang.cn/3/library/exceptions.html#IndexError) 异常

```
response.css("noelement")[0].get()
Traceback (most recent call last):
...
IndexError: list index out of range
```

您可能希望直接在 [`SelectorList`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList) 实例上使用 `.get()`，这样在没有结果时会返回 `None`

```
response.css("noelement").get()
```

这里的经验是：对于大多数抓取代码，您希望它对页面上找不到内容导致的错误具有弹性，这样即使某些部分抓取失败，您至少也能获得**部分**数据。

除了 [`getall()`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList.getall) 和 [`get()`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList.get) 方法外，您还可以使用 [`re()`](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#scrapy.selector.SelectorList.re) 方法使用[正则表达式](https://docs.pythonlang.cn/3/library/re.html)进行提取

```
response.css("title::text").re(r"Quotes.*")
['Quotes to Scrape']
response.css("title::text").re(r"Q\w+")
['Quotes']
response.css("title::text").re(r"(\w+) to (\w+)")
['Quotes', 'Scrape']
```

为了找到合适的 CSS 选择器，您可能会发现在 shell 中使用 `view(response)` 在 Web 浏览器中打开响应页面很有用。您可以使用浏览器的开发者工具检查 HTML 并找出选择器（参阅[使用浏览器的开发者工具进行抓取](https://docs.scrapy.net.cn/en/latest/topics/developer-tools.html#topics-developer-tools)）。

[Selector Gadget](https://selectorgadget.com/) 也是一个很好的工具，可以快速查找视觉选择元素的 CSS 选择器，它在许多浏览器中都能工作。

自己动手操作的示例：

```bash
>>> response.css('title')
[<Selector query='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
>>>
>>>
>>> response.css('title::text').getall()
['Quotes to Scrape']
>>> response.css('title::text').get()
'Quotes to Scrape'
>>>
>>>
>>> response.css('title::text')[0].get()
'Quotes to Scrape'
>>>
>>>
>>> response.css('noelement')
[]
>>>
>>> response.css('noelement').get()
>>>
>>> response.css('title::text').re(r'Quotes.*')
['Quotes to Scrape']
>>>
>>>
>>> response.css('title::text').re(r'Q\w+')
['Quotes']
```

### 3.2.5 XPath 简介

除了[CSS](https://www.w3.org/TR/selectors)，Scrapy 选择器还支持使用[XPath](https://www.w3.org/TR/xpath-10/)表达式

```
response.xpath("//title")
[<Selector query='//title' data='<title>Quotes to Scrape</title>'>]
response.xpath("//title/text()").get()
'Quotes to Scrape'
```

XPath 表达式非常强大，是 Scrapy 选择器的基础。实际上，CSS 选择器在底层会被转换为 XPath。如果您仔细阅读 shell 中选择器对象的文本表示，就可以看到这一点。

虽然可能不如 CSS 选择器流行，但 XPath 表达式提供了更多功能，因为它除了导航结构外，还可以查看内容。使用 XPath，您可以选择诸如：*包含文本“下一页”的链接*之类的内容。这使得 XPath 非常适合抓取任务，我们鼓励您即使已经知道如何构建 CSS 选择器，也学习 XPath，这将使抓取变得容易得多。

我们在这里不会过多介绍 XPath，但您可以在[此处阅读更多关于将 XPath 与 Scrapy 选择器一起使用](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#topics-selectors)的内容。要了解更多关于 XPath 的信息，我们推荐[这个通过示例学习 XPath 的教程](http://zvon.org/comp/r/tut-XPath_1.html)，以及[这个学习“如何用 XPath 思考”的教程](http://plasmasturm.org/log/xpath101/)。

自己操作的示例：

```bash
>>> # 也支持 xpath 解析
>>> response.xpath('//title')
[<Selector query='//title' data='<title>Quotes to Scrape</title>'>]
>>>
>>>
>>> response.xpath('//title/text()').getall()
['Quotes to Scrape']
>>>
>>>
>>> response.xpath('//title/text()').get()
'Quotes to Scrape'
```

### 3.2.6 提取引言和作者

现在您对选择和提取有了一些了解，让我们通过编写代码从网页中提取引言来完成我们的 spider。

[https://quotes.toscrape.com](https://quotes.toscrape.com/) 中的每个引言都由看起来像这样的 HTML 元素表示

```
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```

让我们打开 scrapy shell 并尝试一下，找出如何提取我们需要的数据

```
scrapy shell 'https://quotes.toscrape.com'
```

我们使用以下方法获取引言 HTML 元素的选择器列表

```
response.css("div.quote")
[<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
<Selector query="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data='<div class="quote" itemscope itemtype...'>,
...]
```

上面查询返回的每个选择器都允许我们对其子元素运行进一步的查询。让我们将第一个选择器分配给一个变量，以便我们可以直接在特定的引言上运行我们的 CSS 选择器

```
quote = response.css("div.quote")[0]
```

现在，让我们使用刚刚创建的 `quote` 对象提取该引言的 `text`、`author` 和 `tags`

```
text = quote.css("span.text::text").get()
text
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
author = quote.css("small.author::text").get()
author
'Albert Einstein'
```

鉴于标签是一个字符串列表，我们可以使用 `.getall()` 方法获取所有标签

```
tags = quote.css("div.tags a.tag::text").getall()
tags
['change', 'deep-thoughts', 'thinking', 'world']
```

弄清楚如何提取每个部分后，我们现在可以遍历所有引言元素并将它们组合成一个 Python 字典

```
for quote in response.css("div.quote"):
    text = quote.css("span.text::text").get()
    author = quote.css("small.author::text").get()
    tags = quote.css("div.tags a.tag::text").getall()
    print(dict(text=text, author=author, tags=tags))

{'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', 'author': 'Albert Einstein', 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
{'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', 'author': 'J.K. Rowling', 'tags': ['abilities', 'choices']}
...
```

### 3.2.7 在我们的 spider 中提取数据

让我们回到我们的 spider。到目前为止，它还没有特别提取任何数据，只是将整个 HTML 页面保存到本地文件。让我们将上面的提取逻辑集成到我们的 spider 中。

Scrapy spider 通常会生成许多包含从页面提取的数据的字典。为此，我们在回调中使用 Python 关键字 `yield`，如下所示

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
```

要运行此 spider，请通过输入以下内容退出 scrapy shell

```
quit()
```

然后，运行

```
scrapy crawl quotes
```

现在，它应该会输出提取的数据以及日志

```
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com/page/1/>
{'tags': ['life', 'love'], 'author': 'André Gide', 'text': '“It is better to be hated for what you are than to be loved for what you are not.”'}
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com/page/1/>
{'tags': ['edison', 'failure', 'inspirational', 'paraphrased'], 'author': 'Thomas A. Edison', 'text': "“I have not failed. I've just found 10,000 ways that won't work.”"}
```

## 3.3 存储抓取到的数据

存储抓取到的数据的最简单方法是使用[Feed 导出](https://docs.scrapy.net.cn/en/latest/topics/feed-exports.html#topics-feed-exports)，使用以下命令

```
scrapy crawl quotes -O quotes.json
```

这将生成一个 `quotes.json` 文件，其中包含所有抓取到的 item，以[JSON](https://en.wikipedia.org/wiki/JSON)格式序列化。

命令行选项 `-O` 会覆盖任何现有文件；请改用 `-o` 将新内容追加到现有文件中。但是，追加到 JSON 文件会使文件内容无效 JSON。追加文件时，请考虑使用不同的序列化格式，例如[JSON Lines](https://jsonlines.org/)

```
scrapy crawl quotes -o quotes.jsonl
```

[JSON Lines](https://jsonlines.org/) 格式很有用，因为它像流一样，因此您可以轻松地向其中追加新记录。当您运行两次时，它不会像 JSON 那样出现问题。此外，由于每个记录都是单独一行，您可以处理大文件而无需将所有内容都放入内存，有一些工具如[JQ](https://stedolan.github.io/jq)可以在命令行中帮助完成此操作。

在小型项目（例如本教程中的项目）中，这应该足够了。但是，如果您想对抓取到的 item 执行更复杂的操作，您可以编写一个[Item Pipeline](https://docs.scrapy.net.cn/en/latest/topics/item-pipeline.html#topics-item-pipeline)。创建项目时，已经在 `tutorial/pipelines.py` 中为您设置了一个 Item Pipelines 的占位文件。尽管如果您只想存储抓取到的 item，则无需实现任何 Item Pipeline。

## 3.4 跟踪链接

假设您不仅想抓取 [https://quotes.toscrape.com](https://quotes.toscrape.com/) 前两页的内容，还想抓取网站中所有页面的引言。

现在您知道如何从页面中提取数据了，让我们看看如何从页面中跟踪链接。

首先要做的是提取我们要跟踪的页面的链接。检查我们的页面，我们可以看到有一个指向下一页的链接，其标记如下

```
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```

我们可以在 shell 中尝试提取它

```
response.css('li.next a').get()
'<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
```

这获取了 anchor 元素，但我们想要属性 `href`。为此，Scrapy 支持一个 CSS 扩展，允许您选择属性内容，如下所示

```
response.css("li.next a::attr(href)").get()
'/page/2/'
```

还有一个 `attrib` 属性可用（更多信息请参阅[选择元素属性](https://docs.scrapy.net.cn/en/latest/topics/selectors.html#selecting-attributes)）

```
response.css("li.next a").attrib["href"]
'/page/2/'
```

现在让我们看看我们的 spider，修改后它可以递归跟踪指向下一页的链接，并从中提取数据

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
		
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

现在，提取数据后，`parse()` 方法会查找指向下一页的链接，使用 [`urljoin()`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.Response.urljoin) 方法构建完整的绝对 URL（因为链接可能是相对的），并生成一个指向下一页的新请求，将自身注册为回调以处理下一页的数据提取，并使抓取继续遍历所有页面。

您在这里看到的是 Scrapy 跟踪链接的机制：当您在回调方法中 yield 一个 Request 时，Scrapy 会安排发送该请求，并注册一个回调方法以便在请求完成后执行。

通过这种方式，您可以构建复杂的爬虫，根据您定义的规则跟踪链接，并根据正在访问的页面提取不同类型的数据。

在我们的示例中，它创建了一种循环，跟踪所有指向下一页的链接，直到找不到为止——这对于抓取博客、论坛和其他带分页的网站非常方便。

### 3.4.1 创建 Requests 的快捷方式

作为创建 Request 对象的快捷方式，您可以使用 [`response.follow`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow)

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

与 scrapy.Request 不同，`response.follow` 直接支持相对 URL - 无需调用 urljoin。请注意，`response.follow` 仅返回一个 Request 实例；您仍然需要 yield 这个 Request。

您还可以将选择器而不是字符串传递给 `response.follow`；此选择器应提取必要的属性

```
for href in response.css("ul.pager a::attr(href)"):
    yield response.follow(href, callback=self.parse)
```

对于 `<a>` 元素有一个快捷方式：`response.follow` 会自动使用它们的 href 属性。因此代码可以进一步缩短

```
for a in response.css("ul.pager a"):
    yield response.follow(a, callback=self.parse)
```

补充示例：

```python
import scrapy


class Test1Spider(scrapy.Spider):
    name = "test_1"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                "text": quote.xpath("./span[1]/text()").get(),
                "author": quote.xpath("./span[2]/small/text()").get(),
                "tags": quote.xpath("./div/a/text()").getall(),
            }

        next_page = response.xpath('//li[@class="next"]/a').getall()
        if next_page is not None:
            yield response.follow(next_page[0], callback=self.parse)
```

要从一个可迭代对象创建多个请求，您可以改用 [`response.follow_all`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow_all)

```
anchors = response.css("ul.pager a")
yield from response.follow_all(anchors, callback=self.parse)
```

或者，进一步缩短

```
yield from response.follow_all(css="ul.pager a", callback=self.parse)
```

### 3.4.2 更多示例和模式

这里是另一个演示回调和跟踪链接的 spider，这次用于抓取作者信息

```
import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
```

我自己写的 xpath 版本：

```python
import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        author_pages = response.xpath('//div[@class="quote"]/span[2]/a')
        yield from response.follow_all(author_pages, callback=self.parse_author)

        pagination_pages = response.xpath('//li[@class="next"]/a')
        yield from response.follow_all(pagination_pages, callback=self.parse)

    def parse_author(self, response):
        yield {
            "name": response.xpath('//h3[@class="author-title"]/text()').get(
                default=""
            ),
            "birthday": response.xpath(
                '//div[@class="author-details"]/p[1]/span[1]/text()'
            ).get(default=""),
            "description": response.xpath(
                '//div[@class="author-description"]/text()'
            ).get(default=""),
        }
```

这个 spider 将从主页开始，它将跟踪所有指向作者页面的链接，并为每个链接调用 `parse_author` 回调，同时也会像我们之前看到的那样，使用 `parse` 回调跟踪分页链接。

这里我们将回调作为位置参数传递给 [`response.follow_all`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.http.TextResponse.follow_all)，以使代码更短；这也适用于 [`Request`](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#scrapy.Request)。

`parse_author` 回调定义了一个辅助函数，用于从 CSS 查询中提取和清理数据，并生成包含作者数据的 Python 字典。

这个 spider 演示的另一个有趣的事情是，即使同一作者有许多引言，我们也不必担心多次访问同一作者页面。默认情况下，Scrapy 会过滤掉已访问过的 URL 的重复请求，从而避免因编程错误而过度访问服务器的问题。这可以在 [`DUPEFILTER_CLASS`](https://docs.scrapy.net.cn/en/latest/topics/settings.html#std-setting-DUPEFILTER_CLASS) 设置中配置。

希望到目前为止，您已经对如何使用 Scrapy 的跟踪链接和回调机制有了很好的理解。

作为另一个利用跟踪链接机制的 spider 示例，请查看 [`CrawlSpider`](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider) 类，它是一个通用的 spider，实现了一个小型规则引擎，您可以在其之上编写爬虫。

此外，一种常见模式是使用[传递额外数据给回调函数的方法](https://docs.scrapy.net.cn/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments)，从多个页面构建一个 item。

## 3.5 使用 spider 参数

您可以在运行 spider 时使用 `-a` 选项为它们提供命令行参数

```
scrapy crawl quotes -O quotes-humor.json -a tag=humor
```

这些参数默认会传递给 Spider 的 `__init__` 方法，并成为 spider 的属性。

在此示例中，为 `tag` 参数提供的值将通过 `self.tag` 获取。您可以使用此方法让您的 spider 仅抓取具有特定标签的引言，并根据参数构建 URL

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

如果您向此 spider 传递 `tag=humor` 参数，您会注意到它将仅访问来自 `humor` 标签的 URL，例如 `https://quotes.toscrape.com/tag/humor`。

您可以[在此处了解更多关于处理 spider 参数的信息](https://docs.scrapy.net.cn/en/latest/topics/spiders.html#spiderargs)。

## 3.6 示例

学习的最佳方式是通过示例，Scrapy 也不例外。因此，有一个名为 [quotesbot](https://github.com/scrapy/quotesbot) 的示例 Scrapy 项目，您可以使用它来尝试并学习更多关于 Scrapy 的知识。它包含两个用于 [https://quotes.toscrape.com](https://quotes.toscrape.com/) 的 spider，一个使用 CSS 选择器，另一个使用 XPath 表达式。

The [quotesbot](https://github.com/scrapy/quotesbot) 项目可在以下地址获取：https://github.com/scrapy/quotesbot。您可以在项目的 README 中找到更多信息。

如果您熟悉 git，可以检出代码。否则，您可以通过点击[这里](https://github.com/scrapy/quotesbot/archive/master.zip)将项目下载为 zip 文件。