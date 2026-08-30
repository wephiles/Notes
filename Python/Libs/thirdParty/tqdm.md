---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-15 15:08:52 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">tqdm</h1>

# 1. 什么是 `tqdm`

## 1.1 基本介绍

**`tqdm`** 是一个 Python 进度条库，名称来源于阿拉伯语 “taqaddum”，意为"进步"。它为长时间运行的循环和迭代操作提供直观的进度显示，帮助用户了解任务执行情况。

## 1.2 主要特点

| 特性             | 说明                                   |
| ---------------- | -------------------------------------- |
| 📊 **可视化进度** | 显示进度条、百分比、剩余时间等信息     |
| 🚀 **极简使用**   | 只需一行代码即可添加进度条             |
| 🔄 **自动适应**   | 自动适应终端宽度，支持Jupyter Notebook |
| ⚡ **轻量高效**   | 性能开销极小，不影响运行速度           |
| 🎨 **高度可定制** | 支持自定义颜色、格式、描述等           |
| 🌐 **广泛支持**   | 支持列表、迭代器、文件处理、pandas等   |

## 1.3 应用场景

- 数据处理和清洗循环
- 机器学习模型训练
- 文件批量操作
- 网络请求批量处理
- 科学计算迭代
- 任何需要长时间运行的循环操作

# 2. 如何使用

`pip install tqdm`

## 2.1 基础用法

**直接包装可迭代对象**.

```python
from tqdm import tqdm
import time

# 基础用法 - 包装range
for i in tqdm(range(100)):
    time.sleep(0.02)  # 模拟耗时操作

```

**包装列表/可迭代对象**

```python
from tqdm import tqdm
import time

data = ['item1', 'item2', 'item3', 'item4', 'item5']

for item in tqdm(data):
    time.sleep(0.5)
    # 处理每个item

```

**手动更新进度条**

```python
from tqdm import tqdm
import time

# 创建进度条
pbar = tqdm(total=100)

# 手动更新
for i in range(10):
    time.sleep(0.2)
    pbar.update(10)  # 每次增加10

pbar.close()  # 关闭进度条

```

## 2.2 进阶用法

**添加描述信息**

```python
from tqdm import tqdm
import time

# 添加描述
for i in tqdm(range(100), desc="处理数据"):
    time.sleep(0.02)

```

**自定义单位**

```python
from tqdm import tqdm
import time

# 设置单位
for i in tqdm(range(1000), desc="下载", unit="文件", unit_scale=True):
    time.sleep(0.001)

```

输出效果:

```python
下载: 100%|██████████| 1.00k/1.00k [00:01<00:00, 638文件/s]
```

**嵌套进度条**

```python
from tqdm import tqdm
import time

# 外层循环
for i in tqdm(range(5), desc="外层循环"):
    # 内层循环
    for j in tqdm(range(10), desc=f"  内层 {i}", leave=False):
        time.sleep(0.05)


```

输出结果:

```python
外层循环:   0%|          | 0/5 [00:00<?, ?it/s]
  内层 0:   0%|          | 0/10 [00:00<?, ?it/s]
  内层 0:  20%|██        | 2/10 [00:00<00:00, 19.90it/s]
  内层 0:  40%|████      | 4/10 [00:00<00:00, 19.88it/s]
  内层 0:  60%|██████    | 6/10 [00:00<00:00, 19.85it/s]
  内层 0:  80%|████████  | 8/10 [00:00<00:00, 19.89it/s]
  内层 0: 100%|██████████| 10/10 [00:00<00:00, 19.91it/s]
外层循环:  20%|██        | 1/5 [00:00<00:02,  1.99it/s]
  内层 1:   0%|          | 0/10 [00:00<?, ?it/s]
  内层 1:  20%|██        | 2/10 [00:00<00:00, 19.77it/s]
  内层 1:  40%|████      | 4/10 [00:00<00:00, 19.85it/s]
  内层 1:  60%|██████    | 6/10 [00:00<00:00, 19.85it/s]
  内层 1:  80%|████████  | 8/10 [00:00<00:00, 19.86it/s]
  内层 1: 100%|██████████| 10/10 [00:00<00:00, 19.87it/s]
外层循环:  40%|████      | 2/5 [00:01<00:01,  1.99it/s]
  内层 2:   0%|          | 0/10 [00:00<?, ?it/s]
  内层 2:  20%|██        | 2/10 [00:00<00:00, 19.79it/s]
  内层 2:  40%|████      | 4/10 [00:00<00:00, 19.78it/s]
  内层 2:  60%|██████    | 6/10 [00:00<00:00, 19.81it/s]
  内层 2:  80%|████████  | 8/10 [00:00<00:00, 19.81it/s]
  内层 2: 100%|██████████| 10/10 [00:00<00:00, 19.83it/s]
外层循环:  60%|██████    | 3/5 [00:01<00:01,  1.98it/s]
  内层 3:   0%|          | 0/10 [00:00<?, ?it/s]
  内层 3:  20%|██        | 2/10 [00:00<00:00, 19.84it/s]
  内层 3:  40%|████      | 4/10 [00:00<00:00, 19.86it/s]
  内层 3:  60%|██████    | 6/10 [00:00<00:00, 19.85it/s]
  内层 3:  80%|████████  | 8/10 [00:00<00:00, 19.85it/s]
  内层 3: 100%|██████████| 10/10 [00:00<00:00, 19.84it/s]
外层循环:  80%|████████  | 4/5 [00:02<00:00,  1.98it/s]
  内层 4:   0%|          | 0/10 [00:00<?, ?it/s]
  内层 4:  20%|██        | 2/10 [00:00<00:00, 19.84it/s]
  内层 4:  40%|████      | 4/10 [00:00<00:00, 19.81it/s]
  内层 4:  60%|██████    | 6/10 [00:00<00:00, 19.80it/s]
  内层 4:  80%|████████  | 8/10 [00:00<00:00, 19.83it/s]
  内层 4: 100%|██████████| 10/10 [00:00<00:00, 19.80it/s]
外层循环: 100%|██████████| 5/5 [00:02<00:00,  1.98it/s]
```

**处理字典**

```python
from tqdm import tqdm
import time

data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

for key, value in tqdm(data.items(), desc="处理字典"):
    time.sleep(0.3)
    # 处理每个键值对

```

## 2.3 与常用库结合

**pandas**

```python
import pandas as pd
from tqdm import tqdm


tqdm.pandas()  # 初始化

df = pd.DataFrame({'A': range(1000), 'B': range(1000)})

# 使用 progress_apply
df['C'] = df['A'].progress_apply(lambda x: x ** 2)

```

**文件读取**

```python
from tqdm import tqdm
import time

# 读取大文件并显示进度
with open('large_file.txt', 'r') as f:
    lines = f.readlines()
    for line in tqdm(lines, desc="读取文件"):
        time.sleep(0.001)
        # 处理每一行

```

```python
读取文件:  51%|█████     | 50/98 [00:02<00:02, 19.82it/s]
```

---

```python
from tqdm import tqdm
import time

# 读取大文件并显示进度
with open('data.txt', 'r') as f:
    for line in tqdm(f, desc="读取文件"):
        time.sleep(0.05)
        # 处理每一行
```

```python
读取文件: 34it [00:01, 19.85it/s]
```

**与 requests 网络请求结合**

```python
import requests
from tqdm import tqdm

urls = ['https://example.com/1', 'https://example.com/2', 'https://example.com/3']

for url in tqdm(urls, desc="下载网页"):
    response = requests.get(url)
    # 处理响应

```

# 3. 常用参数详解

| 参数          | 说明                     | 示例值              |
| ------------- | ------------------------ | ------------------- |
| `desc`        | 进度条前缀描述           | `"处理数据"`        |
| `total`       | 总迭代次数               | `100`               |
| `unit`        | 迭代单位名称             | `"item"`, `"文件"`  |
| `unit_scale`  | 自动缩放单位（1000->1k） | `True`              |
| `leave`       | 完成后是否保留进度条     | `True/False`        |
| `ncols`       | 进度条宽度               | `100`               |
| `colour`      | 进度条颜色               | `'green'`, `'blue'` |
| `mininterval` | 最小更新间隔（秒）       | `0.1`               |
| `maxinterval` | 最大更新间隔（秒）       | `10.0`              |
| `position`    | 多进度条时的位置         | `0, 1, 2...`        |

# 4. 实用技巧

## 4.1 使用 with 语句自动关闭

```
from tqdm import tqdm
import time

with tqdm(total=100, desc="自动关闭") as pbar:
    for i in range(10):
        time.sleep(0.2)
        pbar.update(10)
# 自动调用 close()
```

## 4.2 在进度条中显示额外信息

```
from tqdm import tqdm
import time

with tqdm(total=100, desc="显示额外信息") as pbar:
    for i in range(10):
        time.sleep(0.2)
        # 添加后缀信息
        pbar.set_postfix({'loss': f'{i/10:.2f}', 'acc': f'{i*10}%'})
        pbar.update(10)
```

## 4.3 创建独立进度条（用于后台任务）

```
from tqdm import tqdm
import time

pbar = tqdm(total=100, position=0, leave=True)

# 在另一个位置创建进度条
pbar2 = tqdm(total=50, position=1, leave=False)

for i in range(10):
    time.sleep(0.2)
    pbar.update(10)
    pbar2.update(5)

pbar.close()
pbar2.close()
```

## 4.4 条件禁用进度条

```
from tqdm import tqdm
import time

# 可以通过环境变量控制是否显示
# export TQDM_DISABLE=1  # 禁用进度条
from tqdm import tqdm as tqdm_base

def get_tqdm():
    try:
        # 如果设置了禁用环境变量
        import os
        if os.environ.get('TQDM_DISABLE'):
            return lambda x: x  # 返回原始迭代器
        return tqdm_base
    except:
        return tqdm_base

tqdm = get_tqdm()

for i in tqdm(range(100)):
    time.sleep(0.01)
```

## 4.5 Jupyter Notebook 中的使用

```
# Jupyter Notebook 中使用
from tqdm.notebook import tqdm
import time

for i in tqdm(range(100), desc="Jupyter进度条"):
    time.sleep(0.02)
```

## 4.6 完整实战示例

```
from tqdm import tqdm
import time
import random

def process_data(item):
    """模拟数据处理函数"""
    time.sleep(random.uniform(0.01, 0.05))
    return item * 2

def main():
    # 准备数据
    data = list(range(100))
    results = []
    
    print("开始处理数据...")
    
    # 使用 tqdm 包装迭代
    with tqdm(
        data,
        desc="处理进度",
        unit="项",
        unit_scale=True,
        colour='blue'
    ) as pbar:
        for item in pbar:
            # 处理数据
            result = process_data(item)
            results.append(result)
            
            # 更新后缀信息
            pbar.set_postfix({
                '当前值': item,
                '结果': result
            })
    
    print(f"\n处理完成！共处理 {len(results)} 项数据")
    return results

if __name__ == "__main__":
    results = main()
```

## 4.7 注意事项

⚠️ **使用建议：**

1. **避免在极快循环中使用**：如果迭代速度太快，进度条更新反而会拖慢速度
2. **合理使用 `leave` 参数**：多进度条时设置 `leave=False` 避免屏幕混乱
3. **`Jupyter` 环境使用 `tqdm.notebook`**：获得更好的显示效果
4. **生产环境考虑禁用**：可通过环境变量控制是否显示
5. **确保调用 `close()`**：手动创建进度条时要记得关闭

# 5. 总结

`tqdm` 是一个功能强大且易用的进度条工具：

✅ **安装简单**：`pip install tqdm`
✅ **使用方便**：一行代码即可添加进度显示
✅ **功能丰富**：支持自定义样式、嵌套、多场景
✅ **性能优秀**：几乎不影响程序运行效率
