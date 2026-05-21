# 基础

NumPy 的主要对象是同质的多元数组。它是一个由元素（通常是数字）组成的表格，所有元素类型相同，并由非负整数元组索引。在 NumPy 中，维度被称为轴。

例如，3D 空间中一个点的坐标数组 [1, 2, 1] 有一个轴。这个轴包含 3 个元素，所以我们称它的长度为 3。在下面的示例中，数组有 2 个轴。第一个轴的长度为 2，第二个轴的长度为 3。

```python
[[1., 0., 0.],
 [0., 1., 2.]]
```

NumPy的数组类称为ndarray。它也被称为别名array。请注意，numpy.array与标准Python库中的类array.array不同，后者仅处理一维数组并提供较少的功能。

ndarray对象更重要的属性是：

```
ndarray.ndim
数组的轴数（维度）。

ndarray.shape
数组的维度。这是一个整数元组，表示数组在每个维度的大小。对于一个有 n 行和 m 列的矩阵，shape 将是 (n,m)。因此，shape 元组的长度就是轴数，ndim。

ndarray.size
数组的元素总数。这等于 shape 中元素的乘积。

ndarray.dtype
一个描述数组中元素类型的对象。可以使用标准的 Python 类型创建或指定 dtype。此外，NumPy 还提供了自己的类型。numpy.int32、numpy.int16 和 numpy.float64 是一些例子。

ndarray.itemsize
数组中每个元素的字节大小。例如，一个由 float64 类型元素组成的数组，其 itemsize 为 8 (=64/8)，而一个由 complex32 类型元素组成的数组，其 itemsize 为 4 (=32/8)。它等同于 ndarray.dtype.itemsize。

ndarray.data
包含数组实际元素的缓冲区。通常，我们不需要使用这个属性，因为我们会使用索引功能来访问数组中的元素。
```

示例：

```python
import numpy as np

a = np.arange(15)
print(a)  # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14]

a = a.reshape(3, 5)
print(a)
# a = [[ 0  1  2  3  4]
#      [ 5  6  7  8  9]
#      [10 11 12 13 14]]

print(a.shape)  # (3, 5)
print(a.ndim)  # 2
print(a.dtype.name)  # int64
print(a.itemsize)  # 8
print(a.size)  # 15
print(type(a))  # <class 'numpy.ndarray'>

b = np.array([1, 2, 3])  # [1 2 3]
print(b)  # [1 2 3]
print(type(b))  # <class 'numpy.ndarray'>
```

# 创建数组

有多种方法可以创建数组。
例如，您可以使用array函数从一个普通的Python列表或元组创建一个数组。结果数组的类型是根据序列中元素的类型推断出来的。

```python
arr = np.array([1, 2, 3])
print(arr)  # [1 2 3]
print(arr.dtype)  # int64

b_arr = np.array([1.5, 2.3, 0.7])
print(b_arr)  # [1.5 2.3 0.7]
print(b_arr.dtype)  # float64
```

















































































































































































