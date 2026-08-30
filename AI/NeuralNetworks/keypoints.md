# 1. `np.exp(c * 1j)`

```python
c = np.array([1, 2.57079633, 4.14159265])
d = np.exp(c * 1j)
```

这段代码是在用**欧拉公式**生成复平面单位圆上的点。先拆解语法，再跑一遍看结果：
再看一张图，直观展示这三个点在复平面上的位置：
这是 **Python 复数字面量 + 欧拉公式** 的组合写法，核心是 `1j` 这个虚数单位。逐层拆开看：

## 1.1 `1j` 是什么

Python 用后缀 `j` 表示虚数单位（遵循电气工程惯例，因为 `i` 太常被用作变量名）：
```python
1j            # 虚数单位 i，即 √-1
3 + 4j        # 复数 3+4i
1j * 1j       # 结果 (-1+0j)，即 i² = -1
```
## 1.2 `c * 1j` 发生了什么
实数数组乘以虚数单位，**dtype 自动提升为 `complex128`**：
```
c * 1j = [0.+1.j  0.+2.57079633j  0.+4.14159265j]
```
原本的实数值变成了纯虚数：`1 → i·1`。
## 1.3 `np.exp` 作用在复数上：欧拉公式
`np.exp` 是个通用函数，输入复数时就按**欧拉公式**计算：
$$e^{i\theta} = \cos\theta + i\sin\theta$$
所以：

```python
d = np.exp(c * 1j)
d.real  # = [0.540, -0.841, -0.540]  ← 正好是 cos(c)
d.imag  # = [0.841,  0.540, -0.841]  ← 正好是 sin(c)
np.abs(d)   # = [1, 1, 1]  模长全为 1 → 都在单位圆上
```
上面的图也验证了：三个点全落在单位圆上，向量与 x 轴正方向的夹角正好是 `c` 里的弧度值。
## 1.4 一个小彩蛋
你选的三个角度其实是 `1`、`1+π/2`、`1+π`，每次增加 90°，所以三个点恰好是**同一个点逆时针旋转 90°、180° 的结果**——因为 $e^{i(\theta+\pi/2)} = i \cdot e^{i\theta}$。顺带一提，著名的欧拉恒等式就是它的特例：`np.exp(1j*np.pi)` ≈ `-1`（浮点误差 1e-16 左右）。
## 1.5 为什么要这么写
这是科学计算中的常见技巧：
| 用途 | 写法 |
|---|---|
| **一次算出 cos 和 sin** | `d.real`、`d.imag`，比分别调用两次三角函数更方便打包处理 |
| **相位旋转** | 信号乘 `np.exp(1j * phi)` 就是在复平面上旋转 φ 弧度，通信/信号处理里非常常用 |
| **生成复指数信号** | `np.exp(1j * 2*np.pi*f*t)` 是 FFT/DFT 的基函数 |
| **极坐标 ↔ 直角坐标** | 配合 `np.abs()`（半径）和 `np.angle()`（角度）来回转换 |

配套的常用操作记住这几个就够了：`d.real`、`d.imag`、`np.abs(d)`、`np.angle(d)`、`np.conj(d)`。

# 2. `np.fromfunction`

## 2.1 核心

函数签名：

```python
np.fromfunction(function, shape, *, dtype=float)
```

作用：生成一个形状为 `shape` 的数组，其中每个元素的值由**它的下标坐标**经过 `function` 计算得出。

最核心的原理：函数只被调用一次。

很多人以为它是“对每个元素调用一次函数”，**其实不是**。

函数收到的参数是**和输出同形状的“坐标数组”**：

```python
np.fromfunction(lambda i, j: i + j, (3, 4))
# 实际传给函数的是：
# i = [[0,0,0,0],      j = [[0,1,2,3],
#      [1,1,1,1],           [0,1,2,3],
#      [2,2,2,2]]           [0,1,2,3]]
# i + j 一次性广播算出整个结果
```

- 数组有几个维度，函数就要接收几个参数（`shape` 是 `(3,4)` → 函数签名是 `(i, j)`）
- 函数内部必须写**向量化**的运算（NumPy 的运算天然满足）
- 本质上 `np.fromfunction(f, shape)` ≈ `i, j = np.indices(shape); f(i, j)`

## 2.2 典型用法

```python
np.fromfunction(lambda i, j: i + j, (3, 4))              # 加法表
np.fromfunction(lambda i, j: i * j, (4, 4), dtype=np.int_)  # 乘法表
np.fromfunction(lambda i, j: (i + j) % 2, (5, 5))        # 棋盘格
np.fromfunction(lambda i, j: i == j, (4, 4))             # 对角线掩码
np.fromfunction(lambda i, j: i > j, (4, 4))              # 下三角掩码
np.fromfunction(lambda i, j: (i-2)**2 + (j-2)**2, (5,5)) # 抛物面/距离场
```

规律：**凡是“元素值是下标的函数”的数组，都适合用 fromfunction 一行写出来**。

## 2.3 三个常见的坑

### 2.3.1 函数里写了 Python 普通的 `if/else`

```python
np.fromfunction(lambda i, j: 1 if i > j else 0, (3, 3))
# ValueError: The truth value of an array is ambiguous...
```

因为 `i > j` 收到的是整个数组，Python 的 `if` 无法判断数组的真假。改用向量化写法：

```python
np.fromfunction(lambda i, j: np.where(i > j, 1, 0), (3, 3), dtype=np.int_)
# 或直接利用比较运算返回布尔: (i > j).astype(int)
```

### 2.3.2 `dtype` 参数控制的是坐标，不是输出

`dtype` 指的是**传给函数的坐标数组**的类型。不指定时坐标是 `float64`，所以 `lambda i, j: i + j` 的结果是浮点数组 `[[0., 1., ...]]`；想要整数输出就传 `dtype=np.int_`。输出数组本身的 dtype 由函数返回值决定。

### 2.3.3 三维别忘了多加参数

```python
np.fromfunction(lambda i, j, k: i*100 + j*10 + k, (2, 3, 4), dtype=np.int_)
# shape 有几个维度，函数就要有几个参数
```

























