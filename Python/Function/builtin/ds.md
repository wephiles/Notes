---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-22 14:08:79 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">ds</h1>  

----
# 1. `str`

```python
a_string = "python 是一个十分强大的语言. 很多人都喜爱 Python. hello, world!\t20260801"  
b_string = '3.14'  
c_string = '123'  
  
d_string = 'name'  
e_string = 'age'  
  
# 首字母大写  
print(a_string.capitalize())  
  
# 返回一个指定宽度居中的字符串，'_' 为填充字符  
print(a_string.center(70, '_'))  
  
# 计算第一个参数在整个字符串中出现的次数  
print(a_string.count("on"))  #  
  
# 字符串只包含数字返回 True 否则返回 Falseprint(b_string.isdigit())  
print(c_string.isdigit())  
  
# 如果字符串中只包含数字字符，则返回 True，否则返回 Falseprint(b_string.isnumeric())  
print(c_string.isnumeric())  
  
# 返回一个原字符串左对齐,并使用 fillchar 填充至长度 width 的新字符串，fillchar 默认为空格。  
print(d_string.ljust(5, ' '), 'james')  
print(e_string.ljust(5, ' '), 21)  
  
# 返回一个原字符串右对齐,并使用fillchar(默认空格）填充至长度 width 的新字符串  
print(d_string.rjust(5, ' '), 'james')  
print(e_string.rjust(5, ' '), 21)  
  
# 返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写  
print(a_string.title())  
  
# 返回长度为 width 的字符串，原字符串右对齐，前面填充0  
print(d_string.zfill(6))  
print(e_string.zfill(6))  
  
# 检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false。  
print(b_string.isdecimal())  
print(c_string.isdecimal())
```

```plaintext
Python 是一个十分强大的语言. 很多人都喜爱 python. hello, world!	20260801
_______python 是一个十分强大的语言. 很多人都喜爱 Python. hello, world!	20260801_______
2
False
True
False
True
name  james
age   21
 name james
  age 21
Python 是一个十分强大的语言. 很多人都喜爱 Python. Hello, World!	20260801
00name
000age
False
True
```

# 2. `list`

```python
a_list = [5, 8, 6, 12, 5, 9, 7, 1, 3, 6, 5, 8, 10]  
print(a_list)  
  
a_list.append(100)  
print(a_list)  
  
print(a_list.count(5))  
  
a_list.extend([5, 8, 1])  
print(a_list)  
  
print(a_list.index(6))  
  
a_list.insert(666, 2)  
print(a_list)  
  
deleted_data = a_list.pop(3)  
print(deleted_data)  
print(a_list)  
  
a_list.remove(8)  
print(a_list)  
  
a_list.reverse()  
print(a_list)  
  
a_list.sort()  
print(a_list)  
  
new_list = a_list.copy()  
print(new_list)  
print(id(a_list))  
print(id(new_list))  
  
a_list.clear()  
print(a_list)  
print(new_list)
```

```plaintext
[5, 8, 6, 12, 5, 9, 7, 1, 3, 6, 5, 8, 10]
[5, 8, 6, 12, 5, 9, 7, 1, 3, 6, 5, 8, 10, 100]
3
[5, 8, 6, 12, 5, 9, 7, 1, 3, 6, 5, 8, 10, 100, 5, 8, 1]
2
[5, 8, 6, 12, 5, 9, 7, 1, 3, 6, 5, 8, 10, 100, 5, 8, 1, 2]
12
[5, 8, 6, 5, 9, 7, 1, 3, 6, 5, 8, 10, 100, 5, 8, 1, 2]
[5, 6, 5, 9, 7, 1, 3, 6, 5, 8, 10, 100, 5, 8, 1, 2]
[2, 1, 8, 5, 100, 10, 8, 5, 6, 3, 1, 7, 9, 5, 6, 5]
[1, 1, 2, 3, 5, 5, 5, 5, 6, 6, 7, 8, 8, 9, 10, 100]
[1, 1, 2, 3, 5, 5, 5, 5, 6, 6, 7, 8, 8, 9, 10, 100]
1763509408064
1763509696384
[]
[1, 1, 2, 3, 5, 5, 5, 5, 6, 6, 7, 8, 8, 9, 10, 100]
```

# 3. `tuple`

```python
data_info = {  
    'a': 1,  
    'b': 2,  
    'c': 3,  
    'd': 4,  
}  
  
print(tuple(data_info))  
print(tuple(data_info.keys()))  
print(tuple(data_info.values()))  
print('*' * 52)  
print(data_info.items())  
print(tuple(data_info.items()))
```

输出结果：

```plaintext
('a', 'b', 'c', 'd')
('a', 'b', 'c', 'd')
(1, 2, 3, 4)
****************************************************
dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
(('a', 1), ('b', 2), ('c', 3), ('d', 4))
```

# 4. `int`

![image.png](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260801192828238.png)

# 5. `dict`

![image.png](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260801192431923.png)

# 6. `set`

![image.png](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260801192547915.png)

```python
a = {1, 5, 9, 6, 3}  
print(a)  
  
a.remove(5)  
print(a)  
  
a.add(15)  
print(a)  
  
a.update([1, 2, 3, 999])  
print(a)
```

```plaintext
{1, 3, 5, 6, 9}
{1, 3, 6, 9}
{1, 3, 6, 9, 15}
{1, 2, 3, 6, 999, 9, 15}
```

