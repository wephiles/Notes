#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @CreateTime : 2026/07/15 19:06
# @Author     : wephiles@wephiles
# @IDE        : PyCharm
# @ProjectName: practice
# @FileName   : practice/download_hugging_face_ds.py
# @Description: This is description of this script.
# @Interpreter: python 3.0+
# @Motto      : You must take your place in the circle of life!
# @AuthorSite : https://github.com/wephiles or https://gitee.com/wephiles

# Copyright (c) 2026 wephiles.
# This software is licensed under the MIT license.
# See the LICENSE file for details.

import json
import datetime

from tqdm import tqdm
from datasets import load_dataset
from huggingface_hub import login

OUTPUT_FILE_PATH = './data/fact_content_daily_performance.jsonl'

FLUSH_SIZE = 5000


def json_default(obj):
    """处理 json 无法序列化的类型（如 date, datetime, Decimal 等）"""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()  # 转成 "2024-01-01" 这样的字符串
    if isinstance(obj, datetime.time):
        return obj.isoformat()
    # 其他未知类型，兜底转字符串
    return str(obj)


login(token='这里写你的token')

# 1. 以 streaming 模式加载数据集（不占内存，不落盘）
ds = load_dataset("FlyRank/internship-warehouse", "fact_content_daily_performance", streaming=True, split="train")

total = 0
with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as fp:
    pbar = tqdm(ds, desc='转换 jsonl', unit='行')

    for item in pbar:
        fp.write(json.dumps(item, ensure_ascii=False, default=json_default) + '\n')
        total += 1

        # 每 FLUSH_SIZE 行刷新一次附加信息
        if total % FLUSH_SIZE == 0:
            pbar.set_postfix({'已写入:': f'{total:,} 行数据'})
    pbar.close()

print(f"\n✅ 完成！共写入 {total:,} 行 → {OUTPUT_JSONL}")
