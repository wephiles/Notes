#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @CreateTime : 2026/07/15 19:50
# @Author     : wephiles@wephiles
# @IDE        : PyCharm
# @ProjectName: practice
# @FileName   : practice/split_big_file.py
# @Description: This is description of this script.
# @Interpreter: python 3.0+
# @Motto      : You must take your place in the circle of life!
# @AuthorSite : https://github.com/wephiles or https://gitee.com/wephiles

# Copyright (c) 2026 wephiles.
# This software is licensed under the MIT license.
# See the LICENSE file for details.

"""
将一个大文件拆分成几个小文件
"""

import os


def split_jsonl_by_lines(input_file, lines_per_file, output_prefix):
    file_count = 1
    line_count = 0

    # 打开第一个输出文件
    out_file = open(f"{output_prefix}_{file_count}.jsonl", 'w', encoding='utf-8')

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            out_file.write(line)
            line_count += 1

            # 达到指定行数，关闭当前文件，打开新文件
            if line_count >= lines_per_file:
                out_file.close()
                file_count += 1
                line_count = 0
                out_file = open(f"{output_prefix}_{file_count}.jsonl", 'w', encoding='utf-8')

    out_file.close()
    print(f"拆分完成，共生成 {file_count} 个文件。")


# 使用示例：每个文件 50000 行
split_jsonl_by_lines("./data/fact_content_daily_performance.jsonl", 50000, "part")
