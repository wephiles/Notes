---
tags:
  - type/note
  - domain/
  - topic/
  - status
  - source/
aliases:
  - ImgToBase64
rating:
datetime: " 2026-10-17 10:10:26 周六"
author:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
introduction:
---
<h1 align="center">ImgToBase64</h1>

---

将一个图片文件转换成 base64 格式：

```python
import base64
import os
import sys


def image_to_base64(image_path, output_path=None):
    """
    将图片转换为 Base64 编码并保存到 txt 文件

    参数:
        image_path: 图片文件路径
        output_path: 输出的 txt 文件路径（默认为 图片名_base64.txt）
    """
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：文件 '{image_path}' 不存在！")
        return

    # 生成默认输出文件名
    if output_path is None:
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = file_name + "_base64.txt"

    try:
        # 读取图片文件
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # 编码为 Base64
        base64_data = base64.b64encode(image_data).decode("utf-8")

        # 获取图片格式（用于生成 data URI）
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        mime_type = mime_types.get(ext, "image/png")

        # 生成完整的 Data URI 格式
        data_uri = f"data:{mime_type};base64,{base64_data}"

        # 保存到 txt 文件
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(data_uri)

        print(f"转换成功！")
        print(f"图片文件：{image_path}")
        print(f"输出文件：{output_path}")
        print(f"文件大小：{os.path.getsize(output_path)} 字节")

    except Exception as e:
        print(f"转换失败：{e}")
		

if __name__ == "__main__":
    # 方式一：通过命令行参数传入图片路径
    if len(sys.argv) > 1:
        image_to_base64(sys.argv[1])
    else:
        # 方式二：直接指定图片路径
        image_path = './JSON解析-F.png'
        save_path = 'JSON解析_图标_base64.txt'
        image_to_base64(image_path, save_path)
```

