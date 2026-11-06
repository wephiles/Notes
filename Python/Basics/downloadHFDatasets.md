---
tags:
  - type/tutorial
  - lang/
  - lange/YouLang/
  - domain/computer-science
  - domain/computer-science/basic
  - topic/
  - status/draft
  - source/
aliases:
description:
datetime: " 2026-10-17 15:10:85 周六"
author:
rating:
introduction:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
---
<h1 style="text-align: center;">downloadHFDatasets</h1>

----

```python
# ==============================================================
# # 落盘后再转换成 json
# ==============================================================

# from datasets import load_dataset
#
# # 下载数据集并保存到本地(Arrow 格式)
# dataset = load_dataset(path='Bithubs/PerceptionBench')
# dataset.save_to_disk('./datasets/PerceptionBench')
#
# # 从本地加载数据集(Arrow 格式), 处理三个子集
# dataset = load_dataset('./datasets/PerceptionBench')
# for split in dataset:  # train validation test
#     dataset[split].to_json(f'./data/PerceptionBench_{split}.json')
#
# print('保存完成')

# ==============================================================
# # 下载某些指定的文件，防止下载太多
# ==============================================================

import os

from huggingface_hub import hf_hub_download, snapshot_download

# 1. 设置仓库信息和本地保存路径
repo_id = "comma-project/deep-jsonl"
# 指定一个本地文件夹，例如在当前目录下创建 "./data"
local_dir = "./data"
os.makedirs(local_dir, exist_ok=True)

# 2. 指定要下载的文件名 (根据数据集页面，文件名如 parts_0000.jsonl)
# 这里以下载前三个文件为例
files_to_download = [
    "parts_0000.jsonl",
    "parts_0001.jsonl",
    "parts_0002.jsonl",
    "parts_0003.jsonl",
    "parts_0004.jsonl",
    "parts_0005.jsonl",
    "parts_0006.jsonl",
    "parts_0007.jsonl",
    "parts_0008.jsonl",
    "parts_0009.jsonl",
    "parts_0010.jsonl",
    "parts_0011.jsonl",
    "parts_0013.jsonl",
    "parts_0014.jsonl",
    "parts_0015.jsonl",
]

for filename in files_to_download:
    print(f"正在下载: {filename}")
    file_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",  # 关键参数，指定这是数据集
        local_dir=local_dir,  # 文件将保存到此目录
        # local_dir_use_symlinks=False # 如需直接复制文件而非创建符号链接，可设置为 False
    )
    print(f"文件已保存至: {file_path}")

# ==============================================================
# # 下载某些指定的文件，防止下载太多
# ==============================================================
# local_dir = "./comma-project-deep-jsonl"
#
# # 下载整个仓库的全部文件（确保磁盘空间充足）
# snapshot_download(
#     repo_id="comma-project/deep-jsonl",
#     repo_type="dataset",
#     local_dir=local_dir,
#     max_workers=8  # 可调整并发下载的线程数，加快速度
# )

```

