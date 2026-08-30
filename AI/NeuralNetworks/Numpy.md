---
aliases:
  - 列表
  - 数组
tags:
  - lang/python
  - lang/python/Numpy
  - type/tutorial
  - status/draft
datetime: " 2026-08-23 13:08:01 周日"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">Numpy</h1>  

----

# 1. `Quickstart`

本章节参考 Numpy 官方文档：

> https://numpy.org/doc/stable/user/quickstart.html

To work the examples, you’ll need `matplotlib` installed in addition to NumPy.

This is a quick overview of arrays in NumPy. It demonstrates(演示) how n-dimensional () arrays are represented and can be manipulated. In particular, if you don’t know how to apply common functions to n-dimensional arrays (without using for-loops), or if you want to understand axis and shape properties for n-dimensional arrays, this article might be of help.

阅读后，你应该能够：

- 了解 NumPy 中一维、二维和 n 维数组之间的区别；
- 了解如何在不使用 for 循环的情况下，对 n 维数组应用一些线性代数运算；
- 理解n维数组的轴和形状属性。

## 1.1 基础知识

NumPy 的主要对象是同质多维数组。它是一个元素表（通常是数字），所有元素类型相同，并由一个非负整数元组进行索引。在 NumPy 中，维度被称为*轴*。

例如，表示三维空间中某一点坐标的数组 `[1, 2, 1]` 只有一个轴。该轴包含 3 个元素，因此我们说它的长度为 3。在下图所示的示例中，该数组有两个轴。第一个轴的长度为 2，第二个轴的长度为 3。

```python
[[1., 0., 0.],
 [0., 1., 2.]]
```

NumPy 的数组类名为 ndarray，也称为 array。请注意，numpy.array 与标准 Python 库中的 array.array 类不同，后者仅处理一维数组，功能也较少。

ndarray 对象的主要属性包括：

- `ndarray.ndim`
  数组的轴数（维度）。

- `ndarray.shape`
  数组的维度。这是一个整数元组，分别表示数组在每个维度上的大小。例如，对于一个 n 行 m 列的矩阵，其形状为 (n, m)。因此，形状元组的长度就是轴数，即 `ndim`。

- `ndarray.size`
  数组元素的总数。它等于形状元素的乘积。

- `ndarray.dtype`
  描述数组元素类型的对象。可以使用标准的 Python 类型创建或指定 `dtype`。此外，NumPy 也提供了自己的类型。例如，`numpy.int32`、`numpy.int16` 和 `numpy.float64`。

- `ndarray.itemsize`
  数组中每个元素的大小（以字节为单位）。例如，一个 float64 类型数组的元素大小为 8 (=64/8)，而一个 complex32 类型数组的元素大小为 4 (=32/8)。这等价于 `ndarray.dtype.itemsize`。

- `ndarray.data`
  包含数组实际元素的缓冲区。通常情况下，我们不需要使用此属性，因为我们会使用索引来访问数组中的元素。

示例：

```python
import numpy as np

a = np.arange(15).reshape(3, 5)
print(a)
print(a.shape)
print(a.ndim)
print(a.size)
print(a.dtype)
print(a.dtype.name)
print(a.itemsize)
print(a.size)
print(type(a))
```

输出结果：

```python
a = [[ 0  1  2  3  4]
     [ 5  6  7  8  9]
     [10 11 12 13 14]]
```

```python
(3, 5)
2
15
int64
int64
8
15
<class 'numpy.ndarray'>
```

```python
b = np.array([6,7,8])
print(trype(b))  # <class 'numpy.ndarray'>
```

### 1.1.1 创建数组

创建数组的方法有很多种。

例如，你可以使用 `array` 函数从普通的 Python 列表或元组创建数组。生成的数组类型取决于序列中元素的类型。

```python
import numpy as np

a = np.array([2, 3, 4])
print(a)
print(a.dtype)

b = np.array([1.1, 2.3, 6, 3])
print(b)
print(b.dtype)
```

输出结果:

```python
[2 3 4]
int64
[1.1 2.3 6.  3. ]
float64
```

---

```python
c = np.array(range(5))
print(c)
print(c.dtype)
```

输出结果:

```python
[0 1 2 3 4]
int64
```

常见的错误是使用多个参数调用数组，而不是提供单个序列作为参数。

```python
>>> a = np.array(1, 2, 3)
Traceback (most recent call last):
  File "E:\Code\PyProjects\Demos\exercise\src\science_cal\demo_01.py", line 19, in <module>
    a = np.array(1, 2, 3)
TypeError: array() takes from 1 to 2 positional arguments but 3 were given
```

array 将序列的序列转换为二维数组，将序列的序列的序列转换为三维数组，依此类推。

```python
d = np.array([(1.5, 5, 6.8), (4, 5, 6)])
print(d)
```

```python
[[1.5 5.  6.8]
 [4.  5.  6. ]]
```

数组的类型也可以在创建时显式指定：

```python
e = np.array([[1, 2], [3, 4]], dtype=np.complex64)

print(e)
print(e.dtype)
print(e.shape)
print(e.itemsize)
print(e.size)
```

```python
[[1.+0.j 2.+0.j]
 [3.+0.j 4.+0.j]]
complex64
(2, 2)
8
4
```

通常情况下，数组的元素最初是未知的，但数组的大小是已知的。因此，NumPy 提供了一些函数来创建带有初始占位符内容的数组。这些函数最大限度地减少了数组增长的必要性，而数组增长是一项开销很大的操作。

`zeros` 函数创建一个全为零的数组，`ones` 函数创建一个全为一的数组，而 `empty` 函数创建一个初始内容随机且取决于内存状态的数组。默认情况下，创建的数组的数据类型为 `float64`，但可以通过关键字参数 `dtype` 指定。

```python
a = np.zeros((3, 4))
print(a)
print('=' * 20)

b = np.ones((2, 3, 4), dtype=np.int64)
print(b)
print('=' * 20)

c = np.empty((2, 3))
print(c)
```

```python
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
====================
[[[1 1 1 1]
  [1 1 1 1]
  [1 1 1 1]]

 [[1 1 1 1]
  [1 1 1 1]
  [1 1 1 1]]]
====================
[[1.20563116e-311 1.20563128e-311 1.20563116e-311]
 [1.20563116e-311 1.20563128e-311 1.20563128e-311]]
```

为了创建数字序列，NumPy 提供了 arange 函数，它类似于 Python 内置的 range 函数，但返回的是一个数组。

```python
a = np.arange(10, 30, 5)
print(a)

b = np.arange(0, 2, 0.3)
print(b)
```

```python
[10 15 20 25]
[0.  0.3 0.6 0.9 1.2 1.5 1.8]
```

当 arange 函数与浮点参数一起使用时，由于浮点精度有限，通常无法预测获取到的元素数量。因此，通常最好使用 linspace 函数，该函数接受所需的元素数量作为参数，而不是使用 step 函数。

```python
import numpy as np
from numpy import pi

c = np.linspace(0, 2 * pi, 100)
print(c)
```

```python
[0.         0.06346652 0.12693304 0.19039955 0.25386607 0.31733259
 0.38079911 0.44426563 0.50773215 0.57119866 0.63466518 0.6981317
 0.76159822 0.82506474 0.88853126 0.95199777 1.01546429 1.07893081
 1.14239733 1.20586385 1.26933037 1.33279688 1.3962634  1.45972992
 1.52319644 1.58666296 1.65012947 1.71359599 1.77706251 1.84052903
 1.90399555 1.96746207 2.03092858 2.0943951  2.15786162 2.22132814
 2.28479466 2.34826118 2.41172769 2.47519421 2.53866073 2.60212725
 2.66559377 2.72906028 2.7925268  2.85599332 2.91945984 2.98292636
 3.04639288 3.10985939 3.17332591 3.23679243 3.30025895 3.36372547
 3.42719199 3.4906585  3.55412502 3.61759154 3.68105806 3.74452458
 3.8079911  3.87145761 3.93492413 3.99839065 4.06185717 4.12532369
 4.1887902  4.25225672 4.31572324 4.37918976 4.44265628 4.5061228
 4.56958931 4.63305583 4.69652235 4.75998887 4.82345539 4.88692191
 4.95038842 5.01385494 5.07732146 5.14078798 5.2042545  5.26772102
 5.33118753 5.39465405 5.45812057 5.52158709 5.58505361 5.64852012
 5.71198664 5.77545316 5.83891968 5.9023862  5.96585272 6.02931923
 6.09278575 6.15625227 6.21971879 6.28318531]
```

```python
import numpy as np
from numpy import pi

c = np.linspace(0, 2 * pi, 10)
print(c)
```

```python
[0.         0.6981317  1.3962634  2.0943951  2.7925268  3.4906585
 4.1887902  4.88692191 5.58505361 6.28318531]
```

### 1.1.2 打印数组

打印数组时，NumPy 的显示方式与嵌套列表类似，但布局如下：

- 最后一个轴从左到右打印，
- 倒数第二个轴从上到下打印，
- 其余轴也从上到下打印，每个切片之间用空行分隔。

一维数组打印为行，二维数组打印为矩阵，三维数组打印为矩阵列表。

```python
a = np.arange(6)  # 1d array
print(a)
print('=' * 20)

b = np.arange(12).reshape(4, 3)  # 2d array
print(b)
print('=' * 20)

c = np.arange(24).reshape(2, 3, 4)  # 3d array
print(c)
```

```python
[0 1 2 3 4 5]
====================
[[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
====================
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
```

请参阅下文了解更多关于 reshape 函数的详细信息。

如果数组过大而无法全部打印，NumPy 会自动跳过数组的中心部分，只打印数组的四个角：

```python
>>> print(np.arange(10000))
[   0    1    2 ... 9997 9998 9999]
>>> print(np.arange(10000).reshape(100, 100))
[[   0    1    2 ...   97   98   99]
 [ 100  101  102 ...  197  198  199]
 [ 200  201  202 ...  297  298  299]
 ...
 [9700 9701 9702 ... 9797 9798 9799]
 [9800 9801 9802 ... 9897 9898 9899]
 [9900 9901 9902 ... 9997 9998 9999]]
```

要禁用此行为并强制 NumPy 打印整个数组，您可以使用 set_printoptions 更改打印选项。

```python
np.set_printoptions(threshold=sys.maxsize)  # sys module should be imported
```

### 1.1.3 基本运算

数组上的算术运算符逐元素应用。运算结果将存储在一个新的数组中。

```python
a = np.array([20, 30, 40, 50])
b = np.arange(4)

c = a + b
d = a - b
e = b ** 2
f = 10 * np.sin(a)
g = a > 35

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
print(a)
```

```python
[20 30 40 50]
[0 1 2 3]
[20 31 42 53]
[20 29 38 47]
[0 1 4 9]
[ 9.12945251 -9.88031624  7.4511316  -2.62374854]
[False False  True  True]
[20 30 40 50]
```

与许多矩阵语言不同，NumPy 数组中的乘积运算符 * 是逐元素运算的。矩阵乘法可以使用 @ 运算符（在 Python 3.5 及更高版本中）或点函数或方法来实现：

```python
a = np.array([[1, 1], [0, 1]])
b = np.array([[2, 0], [3, 4]])

print(a * b)  # 逐元素相乘
print()
print(a @ b)  # 矩阵乘法
print()
print(a.dot(b))  # 矩阵乘法
```

```python
[[2 0]
 [0 4]]

[[5 4]
 [3 4]]

[[5 4]
 [3 4]]
```

有些操作，例如 += 和 *=，会就地修改现有数组，而不是创建新数组。

```python
rg = np.random.default_rng(1)  # 创建默认随机数生成器的实例
a = np.ones((2, 3), dtype=np.int_)
b = rg.random((2, 3))

print(a)
a *= 3
print(a)

print(b)
b += a
print(b)

a += b
```

```python
[[1 1 1]
 [1 1 1]]
[[3 3 3]
 [3 3 3]]
[[0.51182162 0.9504637  0.14415961]
 [0.94864945 0.31183145 0.42332645]]
[[3.51182162 3.9504637  3.14415961]
 [3.94864945 3.31183145 3.42332645]]
Traceback (most recent call last):
  File "E:\Code\PyProjects\Demos\exercise\src\science_cal\demo_01.py", line 31, in <module>
    a += b
numpy._core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```

当操作不同类型的数组时，结果数组的类型与更通用或更精确的类型相对应（这种行为称为向上转型）。

```python
import numpy as np
from numpy import pi

a = np.ones(3, dtype=np.int32)
b = np.linspace(0, pi, 3)
print(b.dtype.name)

c = a + b
print(c)
print(c.dtype.name)

print(c * 1j)

d = np.exp(c * 1j)  # np.exp: 通用函数, 输入复数时就按欧拉公式计算
print(d)
print(d.dtype.name)
```

```python
float64
[1.         2.57079633 4.14159265]
float64
[0.+1.j         0.+2.57079633j 0.+4.14159265j]
[ 0.54030231+0.84147098j -0.84147098+0.54030231j -0.54030231-0.84147098j]
complex128
```

> 关于上述代码中的 `d = np.exp(c * 1j)`, 可以参考 [keypoints](keypoints.md#1. `np.exp(c * 1j)`)

许多一元运算，例如计算数组中所有元素的总和，都是通过 ndarray 类的方法实现的。

```python
rg = np.random.default_rng(seed=1)

a = rg.random((2, 3))
print(a)

print(a.sum())
print(a.min())
print(a.max())
```

```python
[[0.51182162 0.9504637  0.14415961]
 [0.94864945 0.31183145 0.42332645]]
3.290252281866131
0.14415961271963373
0.9504636963259353
```

---

```python
a = np.array([[2, 9, 0], [-3, 2, 99], [3, 52, 1]])
print(a)

print(a.sum())
print(a.min())
print(a.max())
```

```python
[[ 2  9  0]
 [-3  2 99]
 [ 3 52  1]]
165
-3
99
```

默认情况下，这些操作会像处理数字列表一样处理数组，而忽略其形状。但是，通过指定 axis 参数，您可以沿数组的指定轴执行操作：

```python
print(a)
print("***************")
print(a.sum(axis=0))  # 每列的和
print("***************")
print(a.min(axis=1))  # 每行的和
print("***************")
print(a.cumsum(axis=0))  # 每列的累计和
print("***************")
print(a.cumsum(axis=1))  # 每行的累计和
```

```python
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
***************
[12 15 18 21]
***************
[0 4 8]
***************
[[ 0  1  2  3]
 [ 4  6  8 10]
 [12 15 18 21]]
***************
[[ 0  1  3  6]
 [ 4  9 15 22]
 [ 8 17 27 38]]
```

### 1.1.4 通用函数

NumPy 提供了一些常用的数学函数，例如 sin、cos 和 exp。在 NumPy 中，这些函数被称为“通用函数”（ufunc）。在 NumPy 中，这些函数逐元素地对数组进行运算，并输出一个数组。

```python
b = np.arange(3)
print(b)
print('******************************************')

print(np.exp(b))
print('******************************************')

print(np.sqrt(b))
print('******************************************')

c = np.array([2., -1., 4.])
print(c)
print('******************************************')

print(np.add(b, c))
print('******************************************')

print(np.add(c, b))
```

```python
[0 1 2]
******************************************
[1.         2.71828183 7.3890561 ]
******************************************
[0.         1.         1.41421356]
******************************************
[ 2. -1.  4.]
******************************************
[2. 0. 6.]
******************************************
[2. 0. 6.]
```

### 1.1.5 索引、切片和迭代

**One-dimensional** arrays can be indexed, sliced and iterated over, much like [lists](https://docs.python.org/tutorial/introduction.html#lists) and other Python sequences.

```python
a = np.arange(10) ** 3
print(a)

print(a[2])

print(a[2: 5])

# a[0:6:2]
print(a[:6:2])

a[:6:2] = 1000
print(a)

print(a[::-1])

for i in a:
    print(i ** (1 / 3.))
```

```python
[  0   1   8  27  64 125 216 343 512 729]
8
[ 8 27 64]
[ 0  8 64]
[1000    1 1000   27 1000  125  216  343  512  729]
[ 729  512  343  216  125 1000   27 1000    1 1000]
9.999999999999998
1.0
9.999999999999998
3.0
9.999999999999998
4.999999999999999
5.999999999999999
6.999999999999999
7.999999999999999
8.999999999999998
```

多维数组每个轴可以有一个索引。这些索引以元组的形式给出，并用逗号分隔：

```python
def f(x, y):
    return x * 10 + y


b = np.fromfunction(f, (5, 4), dtype=np.int_)
print(b)
print('************************')
print(b[2, 3])
print('************************')
print(b[:5, 1])
print('************************')
print(b[:, 1])
print('************************')
print(b[1:3, :])
```

```python
[[ 0  1  2  3]
 [10 11 12 13]
 [20 21 22 23]
 [30 31 32 33]
 [40 41 42 43]]
************************
23
************************
[ 1 11 21 31 41]
************************
[ 1 11 21 31 41]
************************
[[10 11 12 13]
 [20 21 22 23]]
```

> 关于 `np.fromfunction`，参考：[np.fromfunction](keypoints.md#2. `np.fromfunction`)

当提供的索引数量少于坐标轴数量时，缺失的索引将被视为完整的切片：

```python
>>> b[-1]   # the last row. Equivalent to b[-1, :]
array([40, 41, 42, 43])
```

b[i] 中方括号内的表达式被视为一个 i，后面跟着足够多的冒号 (:)，以表示剩余的坐标轴。NumPy 也允许你使用点号 (...) 来表示，例如 b[i, ...]。

点号 (...) 表示足够多的冒号，以生成完整的索引元组。例如，如果 x 是一个包含 5 个坐标轴的数组，那么

- `x[1, 2, ...]` 等价于 `x[1, 2, :, :, :]`

- `x[..., 3]` 等价于 `x[:, :, :, :, 3]`

- `x[4, ..., 5, :]` 等价于 `x[4, :, :, 5, :]`

```python
c = np.array([[[0, 1, 2],  # a 3D array (two stacked 2D arrays)
               [10, 12, 13]],
              [[100, 101, 102],
               [110, 112, 113]]])
print(c.shape)
print(c[1, ...])  # same as c[1, :, :] or c[1]
print(c[..., 2])  # same as c[:, :, 2]
```

```python
(2, 2, 3)
[[100 101 102]
 [110 112 113]]
[[  2  13]
 [102 113]]
```

对多维数组进行迭代是相对于第一个轴进行的：

```python
>>> b = np.array([[ 0,  1,  2,  3], [10, 11, 12, 13], [20, 21, 22, 23], [30, 31, 32, 33], [40, 41, 42, 43]])
>>> for row in b:
...     print(row)
[0 1 2 3]
[10 11 12 13]
[20 21 22 23]
[30 31 32 33]
[40 41 42 43]
```

但是，如果想要对数组中的每个元素执行操作，可以使用 flat 属性，它是一个遍历数组所有元素的迭代器：

```python
b = np.array([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23], [30, 31, 32, 33], [40, 41, 42, 43]])
for item in b.flat:
    print(item)
```

```python
0
1
2
3
10
11
12
13
20
21
22
23
30
31
32
33
40
41
42
43
```

## 1.2 形状操作

### 1.2.1 改变数组形状

数组的形状由每个轴上的元素数量决定：

```
rg = np.random.default_rng(seed=1)

a = np.floor(10 * rg.random((3, 4)))
print(a)
print(a.shape)
```

```
[[5. 9. 1. 9.]
 [3. 4. 8. 4.]
 [5. 0. 7. 5.]]
(3, 4)
```

可以使用各种命令来改变数组的形状。请注意，以下三个命令都会返回一个修改后的数组，但不会改变原始数组：

```
rg = np.random.default_rng(seed=1)

a = np.floor(10 * rg.random((3, 4)))
print(a)
print('=' * 60)

b = a.ravel()  # 返回扁平化的数组
print(b)
print('=' * 60)

c = a.reshape(6, 2)
print(c)
print('=' * 60)

d = a.T  # 返回转置后的数组
print(d)
print('=' * 60)

print('shape a:', a.shape)
print('shape a.T', d.shape)
```

```
[[5. 9. 1. 9.]
 [3. 4. 8. 4.]
 [5. 0. 7. 5.]]
============================================================
[5. 9. 1. 9. 3. 4. 8. 4. 5. 0. 7. 5.]
============================================================
[[5. 9.]
 [1. 9.]
 [3. 4.]
 [8. 4.]
 [5. 0.]
 [7. 5.]]
============================================================
[[5. 3. 5.]
 [9. 4. 0.]
 [1. 8. 7.]
 [9. 4. 5.]]
============================================================
shape a: (3, 4)
shape a.T (4, 3)
```

使用 `ravel` 函数生成的数组元素顺序通常是“C 风格”，也就是说，最右边的索引“变化最快”，因此 `a[0, 0]` 之后的元素是 `a[0, 1]`。如果数组被重塑为其他形状，它仍然会被视为“C 风格”。NumPy 通常创建按此顺序存储的数组，因此 `ravel` 通常不需要复制其参数。但是，如果数组是通过对另一个数组进行切片或使用特殊选项创建的，则可能需要复制它。`ravel` 和 `reshape` 函数也可以通过可选参数指示其使用 `FORTRAN` 风格的数组，其中最左边的索引变化最快。

`reshape` 函数返回形状修改后的参数，而 `ndarray.resize` 方法则修改数组本身。

```python
rg = np.random.default_rng(seed=1)

a = np.floor(10 * rg.random((3, 4)))
print(a)
print('=' * 60)

a.resize((2, 6))  # 在 numpy 2.5 + 已被弃用，应该使用 np.resize(a, (2, 6)) 返回一个新数组
print(a)
```

```python
[[5. 9. 1. 9.]
 [3. 4. 8. 4.]
 [5. 0. 7. 5.]]
============================================================
[[5. 9. 1. 9. 3. 4.]
 [8. 4. 5. 0. 7. 5.]]
```

如果在重塑操作中某个尺寸被指定为 -1，则其他尺寸将自动计算：

```python
>>> a.reshape(3, -1)
array([[3., 7., 3., 4.],
       [1., 4., 2., 2.],
       [7., 2., 4., 9.]])
```

### 1.2.2 堆叠不同的数组

多个数组可以沿不同轴堆叠在一起：

```python
rg = np.random.default_rng(seed=1)

a = np.floor(10 * rg.random((2, 2)))
print(a)
print('=' * 60)

b = np.floor(10 * rg.random((2, 2)))
print(b)
print('=' * 60)

c = np.vstack((a, b))
print(c)
print('=' * 60)

d = np.hstack((a, b))
print(d)
```

```python
[[5. 9.]
 [1. 9.]]
============================================================
[[3. 4.]
 [8. 4.]]
============================================================
[[5. 9.]
 [1. 9.]
 [3. 4.]
 [8. 4.]]
============================================================
[[5. 9. 3. 4.]
 [1. 9. 8. 4.]]
```

函数 column_stack 将一维数组堆叠成一个二维数组，每列代表一个二维数组。它等价于 hstack，但仅适用于二维数组：

```python
https://numpy.org/doc/stable/user/quickstart.html#stacking-together-different-arrays
```





















































