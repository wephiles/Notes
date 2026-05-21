[TOC]



# 这是一级标题 Title1

## 这是二级标题 Title2

### 这是三级标题 Title3

#### 这是四级标题 Title4

##### 这是五级标题 Title5

###### 这是六级标题 Title6

**滕王阁序 - 王勃**

豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。台隍枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨戟遥临；宇文新州之懿范，襜帷暂驻。十旬休假，胜友如云；千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗；紫电青霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。(豫章故郡 一作：南昌故郡；青霜 一作：清霜)

　　时维九月，序属三秋。潦水尽而寒潭清，烟光凝而暮山紫。俨骖騑于上路，访风景于崇阿。临帝子之长洲，得天人之旧馆。层峦耸翠，上出重霄；飞阁流丹，下临无地。鹤汀凫渚，穷岛屿之萦回；桂殿兰宫，即冈峦之体势。（天人 一作：仙人；层峦 一作：层台；即冈 一作：列冈；飞阁流丹 一作：飞阁翔丹）

　　...
　　滕王高阁临江渚，佩玉鸣鸾罢歌舞。
　　画栋朝飞南浦云，珠帘暮卷西山雨。
　　闲云潭影日悠悠，物换星移几度秋。
　　阁中帝子今何在？槛外长江空自流。

No human being could fail to be deeply moved by such a tribute as this [[Thayer Award](https://en.wikipedia.org/wiki/Sylvanus_Thayer_Award)]. Coming from a `profession `I have served so long, and a people I have loved so well, it fills me with an emotion I cannot express. **But this award is not intended primarily to honor a personality**, but to symbolize a great moral code -- <u>the code of conduct and chivalry</u> of those who ==guard this beloved== land of culture and ancient descent. That is the animation of this medallion. For all eyes and for all time, it is an expression of the ethics of the American soldier. That I should be integrated in this way with so noble an ideal arouses a sense of pride and yet of humility which will be with me always.

这有一段文字，我要**将他们加粗**，并且还要进行==高亮==，有些时候，我还会使用一些 `English`，另外，我还会<u>给他们加上下划线</u>；

并且我还要*给有的文字加上斜体*；

有的时候，==我会高亮并且**加粗**，有的文字会*再加一些斜体*，再加一些 `English` 来测试==。

此外，~~我还会给某些字体加上删除线~~

还有~下标~ ，也有^上标^

<!--这里面是注释，我会注释一些东西...-->

这是一个超链接，链接到 [百度](https://www.baidu.com)

下面有一条分割线

---

上面有一条分割线，下面是一张图片:

![image-20251216140630898](./assets/image-20251216140630898.png)

| 这是表头 | 这是表头 | Head |
| -------- | -------- | ---- |
| 一       | aaa      | 123  |
| 二       | bbb      | 456  |
| 三       | ccc      | 789  |

下面是公式块
$$
sin(x) + cos(x) = 1
$$
这是单行代码: `python manage.py runserver`

```python
# 这是一段代码
from pathlib import Path

import scrapy


class Test1Spider(scrapy.Spider):
    name = "test_1"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
        "https://quotes.toscrape.com/page/3/",
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                "text": quote.xpath("./span[1]/text()").get(),
                "author": quote.xpath("./span[2]/small/text()").get(),
                "tags": quote.xpath("./div/a/text()").getall(),
            }
```

> [!NOTE]
>
> 提醒 Note

> [!TIP]
>
> 建议 Tip

> [!IMPORTANT]
>
> 重要 Important

> [!WARNING]
>
> 警告 Warning

> [!CAUTION]
>
> 注意 Caution

> 这是引用内容 

1. 第一
2. 第二
    1. 巴拉巴拉
        - 哗啦哗啦
    2. balabala
3. 第三

- 项目1
- 项目2
    - 巴拉巴拉
        - 稀里哗啦
- 项目3

- [x] 任务1
- [x] 任务二
- [ ] 任务三
- [ ] job 4

