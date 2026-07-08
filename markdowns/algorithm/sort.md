# 1. 冒泡排序

```python
from typing import Callable, TypeVar, List

T = TypeVar('T')


def bubble_sort(nums: List[T], key: Callable = None, reverse: bool = False, inplace: bool = False) -> List[T] | None:
    """冒泡排序 -- 加入 key 参数, 本算法是稳定的

    Args:
        nums (List[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    if not nums:
        return None if inplace else []
    # 下面是一个小坑, 记得给 lambda 表达式加括号
    # 否则会变成:
    #   如果 key is not None: key_fun = lambda x: key
    #   如果 key is Non: key_func = lambda x: x
    # 这样 就会导致我们的程序运行出错！
    key_func: Callable = (lambda x: x) if key is None else key
    # lambda x, y: x[0] > y[0] 和 lambda x, y: x[0] < y[0] 保证了本函数的排序是稳定的
    need_swap: Callable = (lambda x, y: x[0] > y[0]) if reverse else (lambda x, y: x[0] < y[0])

    # # 装饰阶段
    # nums = [A, B, C]
    # 冒泡排序的过程中, 我们要根据 key 这个 Callable 来处理 nums 的每一个值
    # 但是这样有一个问题: 这样会导致多次计算同一个值, 白白浪费时间:
    # 尤其在 key 函数计算较为复杂较为复杂的情况下, 这会大大增加排序时间, 降低排序效率.
    # 
    # 例如: 第一轮需要比较 key(A) 和 key(B), 将 A 和 B 交换, 得到 [B, A, C]
    #   此时还要继续比较 key(A) 和 key(C), key(A) 又被计算了一次，白白浪费了时间
    # 可以将key(A)、key(B)、key(C) 先缓存起来, 减少不必要的计算
    decorated: List[tuple] = [(key_func(num), num) for num in nums]

    n: int = len(decorated)
    last_swap_idx: int = n - 1
    for i in range(n - 1):
        flag: bool = False
        cur_swap_idx = 0
        for j in range(last_swap_idx):
            if need_swap(decorated[j], decorated[j + 1]):
                decorated[j], decorated[j + 1] = decorated[j + 1], decorated[j]
                flag = True
                cur_swap_idx = j
        last_swap_idx = cur_swap_idx
        if not flag:
            break
    # 去装饰
    sorted_array = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_array
        return None
    else:
        return sorted_array
```

# 2. 鸡尾酒排序

```python
from typing import Callable, TypeVar, List

T = TypeVar('T')


def cocktails_sort(nums: List[T], key: Callable = None, reverse: bool = False, inplace: bool = False) -> List[T] | None:
    """鸡尾酒排序

    Args:
        nums (List[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    if not nums:
        return None if inplace else []
    key_func: Callable = (lambda x: x) if key is None else key
    need_swap: Callable = (lambda x, y: x[0] > y[0]) if reverse else (lambda x, y: x[0] < y[0])

    # 装饰阶段 (空间换时间，避免 key 重复计算)
    decorated: List[tuple] = [(key_func(num), num) for num in nums]
	
    n: int = len(nums)

    # 使用左右两个指针来控制边界范围
    left_border: int = 0
    right_border: int = n - 1

    # 只要左边界 < 右边界, 就继续左右来回排序
    while left_border < right_border:
        swapped: bool = False
        new_right_border: int = left_border

        # 从左向右冒泡
        for i in range(left_border, right_border):
            if need_swap(decorated[i], decorated[i + 1]):
                decorated[i], decorated[i + 1] = decorated[i + 1], decorated[i]
                swapped = True
                new_right_border = i
        right_border = new_right_border
        if not swapped:
            break

        # 从右向左冒泡
        swapped = False
        new_left_border: int = right_border
        for i in range(right_border, left_border, -1):
            if need_swap(decorated[i - 1], decorated[i]):
                decorated[i - 1], decorated[i] = decorated[i], decorated[i - 1]
                swapped = True
                new_left_border = i
        left_border = new_left_border
        if not swapped:
            break
    # 去装饰阶段
    sorted_array = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_array
        return None
    else:
        return sorted_array
```

# 3. 选择排序

```python
def select_sort(
    nums: List[T],
    key: Callable = None,
    reverse: bool = False,
    inplace: bool = False,
) -> List[T] | None:
    """选择排序

    Args:
        nums (List[T): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []
    # 按照哪个关键词进行排序
    key_func: Callable[[T], T] = (lambda x: x) if key is None else key

    # 装饰阶段
    decorated: List[tuple] = [(key_func(item), item) for item in nums]

    # 对于 reverse 参数, 如果 reverse == True, 那么每次都找最大的值放在前面, 否则找最小的值放在最前面即可
    should_swap: Callable[[T, T], bool] = (
        (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]
    )
    n = len(nums)

    for i in range(n):
        swap_idx = i
        for j in range(i + 1, n):
            if should_swap(decorated[swap_idx], decorated[j]):
                swap_idx = j
        if swap_idx != i:  # 只有当 最值索引不是当前位置时才进行交换
            decorated[swap_idx], decorated[i] = decorated[i], decorated[swap_idx]
    sorted_nums = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_nums
        return None
    else:
        return sorted_nums
```

# 4. 普通插入排序

```python
def insertion_sort(
        nums: List[T],
        key: Callable = None,
        reverse: bool = False,
        inplace: bool = False,
) -> List[T] | None:
    """插入排序

    Args:
        nums (List[T): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []

    key_func: Callable = (lambda x: x) if key is None else key

    # 装饰阶段
    decorated = [(key_func(item), item) for item in nums]

    # 正倒序逻辑处理
    need_swap = (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]

    # 排序核心代码
    n = len(decorated)
    for i in range(1, n):
        key_first = decorated[i]  # 未排序序列的第一个元素
        j = i - 1
        while j >= 0 and need_swap(decorated[j], key_first):
            # 注意此处比较的对象是 key_first, 不能是 decorated[i], 因为 decorated[i] 可能会被覆盖(当 j + 1 == i 的时候)
            decorated[j + 1] = decorated[j]
            j -= 1
        decorated[j + 1] = key_first
    sorted_decorated = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_decorated
        return None
    else:
        return sorted_decorated
```

# 5. 二分插入排序

```python
def insertion_sort_binary(
        nums: List[T],
        key: Callable = None,
        reverse: bool = False,
        inplace: bool = False,
) -> List[T] | None:
    """二分插入排序

    Args:
        nums (List[T): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []

    key_func: Callable = (lambda x: x) if key is None else key

    # 装饰阶段
    decorated = [(key_func(item), item) for item in nums]

    # 正倒序逻辑处理
    need_swap = (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]

    # 排序核心代码
    n = len(decorated)
    for i in range(1, n):
        ele_first = decorated[i]
        left = 0
        right = i - 1
        while left <= right:
            mid = (right - left) // 2 + left
            if need_swap(decorated[mid], ele_first):
                right = mid - 1
            else:
                left = mid + 1
        # left 就是插入位置
        j = i - 1
        while j >= left:
            decorated[j + 1] = decorated[j]
            j -= 1
        decorated[j + 1] = ele_first
    sorted_arras = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_arras
        return None
    else:
        return sorted_arras
```

# 6. 希尔排序

```python
def shell_sort(
        nums: List[T],
        key: Callable = None,
        reverse: bool = False,
        inplace: bool = False,
) -> List[T] | None:
    """希尔排序
	
    Args:
        nums (List[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        List[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []

    key_func: Callable = (lambda x: x) if key is None else key

    # 装饰阶段 -- 此处可能有 bug, 因为 如果 key_func(item) 是不可比较大小的对象的话, 会报 TypeError
    decorated = [(key_func(item), item) for item in nums]

    # 正倒序逻辑处理
    need_swap = (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]

    # 排序核心代码
    n = len(decorated)

    # 普通的 gap 序列求法 -- 时间复杂度还是达到了 N 方
    #   gap = n // 2

    # Knuth 序列，由计算机科学鼻祖高德纳提出
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1  # 1, 4, 13, 40, 121, ...

    while gap > 0:
        for i in range(gap, n):
            temp = decorated[i]
            j = i
            while j >= gap and need_swap(decorated[j - gap], temp):
                decorated[j] = decorated[j - gap]
                j -= gap
            decorated[j] = temp
        # gap //= 2  # 减小增量 -- 普通 gap 序列
        gap //= 3
    sorted_decorated = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_decorated
        return None
    else:
        return sorted_decorated
```

# 7. 归并排序

```python
from typing import Callable, List, TypeVar, Any

T = TypeVar("T")


def merge_1(left: List[T], right: List[T], compare: Callable[[tuple, tuple], bool], key: Callable[[T], Any]) -> List[T]:
    """对两个列表 left 和 right 进行归并操作
    两个列表都是经过装饰后的列表 -- 即 decorated 列表

    Args:
        left (List[tuple]): 经过装饰后的列表
        right (List[tuple]): 经过装饰后的列表
        compare (Callable): 比较的操作逻辑
        key (Callable): 要按照哪个关键字排序

    Returns:
        List[tuple]
    """
    # 用于返回的结果数组
    merged_lst: List[tuple] = []

    # 装饰阶段
    # FIXME: 虽然这里使用了 装饰-排序-去装饰
    #   但是, 在 merge 函数内部进行装饰和去装饰会导致额外的计算
    #   比如下面的递归树:
    #                 [25, 19, 10, 20, 31, 22]
    #                 /                    \
    #           [25, 19, 10]          [20, 31, 22]
    #          /          \             /       \
    #         [25]    [19, 10]      [20]     [31, 22]
    #                 /    \                 /       \
    #               [19]   [10]            [31]      [22]
    #   我们首先 将 [19] 和 [10] 装饰一遍后再进行合并为 [10, 19]
    #   合并完毕后 又需要将 [10, 19] 和 [25] 合并, 此时又需要装饰一遍 [10, 19], 白白浪费时间!!!
    #   而这与 通过 "装饰-排序-去装饰" 来减少运算次数相悖
    #   ！！！关于这个 问题 的修复见 merge_sort 和 merge 两个函数

    decorated_l: List[tuple] = [(key(item), item) for item in left]
    decorated_r: List[tuple] = [(key(item), item) for item in right]

    i: int = 0
    j: int = 0
    while i < len(decorated_l) and j < len(decorated_r):
        if compare(decorated_l[i], decorated_r[j]):
            merged_lst.append(decorated_r[j])
            j += 1
        else:
            merged_lst.append(decorated_l[i])
            i += 1
    merged_lst.extend(decorated_l[i:])
    merged_lst.extend(decorated_r[j:])

    # # 上面两行代码也可以写成下面这样:
    # while i < len(decorated_l):
    #     merged_lst.append(decorated_l[i])
    #     i += 1
    # while j < len(decorated_r):
    #     merged_lst.append(decorated_r[j])
    #     j += 1
    return [item[1] for item in merged_lst]


def merge_sort_1(
        nums: List[T],
        key: Callable = None,
        reverse: bool = False,
) -> List[T]:
    """归并排序

    Args:
        nums (List[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大

    Returns:
        List[T] | None
    """
    # 特殊值处理
    if not nums:
        return []
    if len(nums) == 1:
        return nums[:]

    key_func: Callable[[T], Any] = (lambda x: x) if key is None else key
    # 正倒序逻辑处理
    need_swap: Callable[[tuple, tuple], bool] = (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]

    mid: int = len(nums) // 2
    left_lst: List[T] = merge_sort_1(nums[:mid], key=key_func, reverse=reverse)
    right_lst: List[T] = merge_sort_1(nums[mid:], key=key_func, reverse=reverse)
    return merge_1(left_lst, right_lst, need_swap, key=key_func)


# =====================================================================================================================
# 对于 merge_sort_1 的优化
# =====================================================================================================================

def merge(left: List[tuple], right: List[tuple], compare: Callable[[tuple, tuple], bool]) -> List[tuple]:
    """merge 函数只负责对传入的两个列表进行归并, 而这两个列表是经过装饰的

    Args:
        left (List[tuple]):
        right (List[tuple]):
        compare (Callable[[tuple, tuple], bool]):

    Returns:
        List[tuple]
    """
    merged_lst: List[tuple] = []

    i: int = 0
    j: int = 0

    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            merged_lst.append(right[j])
            j += 1
        else:
            merged_lst.append(left[i])
            i += 1
    merged_lst.extend(left[i:])
    merged_lst.extend(right[j:])

    return merged_lst


def merge_sort(
        nums: List[T],
        key: Callable = None,
        reverse: bool = False,
) -> List[T]:
    """归并排序

    Args:
        nums (List[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大

    Returns:
        List[T] | None
    """
    if not nums:
        return []
    if len(nums) == 1:
        return nums[:]
    key_func: Callable[[T], Any] = (lambda x: x) if key is None else key

    # 只在外层进行一遍装饰
    decorated = [(key_func(item), item) for item in nums]

    # 比较逻辑
    compare: Callable[[tuple, tuple], bool] = (lambda x, y: x[0] < y[0]) if reverse else lambda x, y: x[0] > y[0]

    # 内部归并函数
    def _recursive_merge_sort(decorated_lst: List[tuple]) -> List[tuple]:
        # 内部递归函数 只处理经过装饰的列表 返回的也是经过装饰的列表
        if len(decorated_lst) == 1:
            return decorated_lst[:]
        mid = len(decorated_lst) // 2
        l = _recursive_merge_sort(decorated_lst[:mid])
        r = _recursive_merge_sort(decorated_lst[mid:])

        return merge(l, r, compare)

    sorted_decorated_lst: List[tuple] = _recursive_merge_sort(decorated)
    return [item[1] for item in sorted_decorated_lst]
```

# 8. 快速排序

```python
from typing import Callable, TypeVar, Any, Optional

T = TypeVar("T")


def partition(decorated_lst: list[tuple], left: int, right: int, should_move: Callable[[tuple, tuple], bool]) -> int:
    """划分区间 [old_left, left) 和 [left, right]

    Args:
        decorated_lst (list[tuple]): 经过装饰的列表
        left (int): 起始位置 闭
        right (int): 终止位置 闭
        should_move (Callable[[tuple, tuple], bool]): 判断是否倒序排列的函数

    Returns:
        int
    """
    pivot: tuple = decorated_lst[left]
    while left < right:
        while left < right and should_move(decorated_lst[right], pivot):
            right -= 1
        decorated_lst[left] = decorated_lst[right]
        while left < right and should_move(pivot, decorated_lst[left]):
            left += 1
        decorated_lst[right] = decorated_lst[left]
    decorated_lst[left] = pivot
    return left


def quick_sort(
        nums: list[T],
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
        inplace: bool = False
) -> list[T] | None:
    """快速排序

    Args:
        nums (list[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        list[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []
    if len(nums) == 1:
        return None if inplace else nums[:]
    # 按照哪个关键词进行排序
    key_func: Callable[[T], Any] = (lambda x: x) if key is None else key

    # 装饰阶段
    decorated: list[tuple] = [(key_func(item), item) for item in nums]

    # 对于 reverse 参数, 如果 reverse == True, 那么每次都找最大的值放在前面, 否则找最小的值放在最前面即可
    # 注意: 为了能够正确地移动 left 和 right, 比较方式应该是 大于等于 或者 小于等于, 否则会导致无限循环
    should_move: Callable[[tuple, tuple], bool] = (
        (lambda x, y: x[0] <= y[0]) if reverse else lambda x, y: x[0] >= y[0]
    )
    n = len(nums)

    def _sort(decorated_lst: list[tuple], left: int, right: int) -> None:
        # 内部排序函数 排序列表是经过装饰的列表 返回值 None 直接在原地排序
        if left >= right:
            return
        mid = partition(decorated_lst, left, right, should_move)

        _sort(decorated_lst, left, mid - 1)
        _sort(decorated_lst, mid + 1, right)

    _sort(decorated, 0, n - 1)
    sorted_lst = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_lst
        return None
    return sorted_lst


if __name__ == '__main__':
    nums: list[dict[str, int | str]] = [{'age': 25, 'name': 'jack'},
                                        {'age': 19, 'name': 'donk'},
                                        {'age': 10, 'name': 'james'},
                                        {'age': 20, 'name': 'jackson'},
                                        {'age': 31, 'name': 'jordan'},
                                        {'age': 22, 'name': 'LongChen'}]

    res = quick_sort(nums, key=lambda x: x['age'])
    print(nums)
    print(res)
```

> [!Note]
>
> 在写代码的过程中有些错误
>
> | 问题                      | 现象                   | 你的修复                        |
> | ------------------------- | ---------------------- | ------------------------------- |
> | 递归参数写死              | `RecursionError`       | ✅ 传入 `left, right`            |
> | 缺少递归出口              | `RecursionError`       | ✅ 加 `if left >= right: return` |
> | 相同元素比较用 `>` `<`    | 死循环                 | ✅ 改为 `>=` `<=`                |
> | `len(nums)==1` 返回原引用 | 违反"不修改原数组"承诺 | ✅ 改为 `nums[:]`                |
> | `TypeVar T` 用于具体变量  | `PyCharm` 报 `Unbound` | ✅ 改为具体类型                  |

# 9. 堆排序

```python
from typing import Callable, TypeVar, Any, Optional

T = TypeVar("T")


def heapify(array: list[tuple], heap_size: int, root_idx: int, is_better: Callable[[tuple, tuple], bool]) -> None:
    """调整大顶堆 / 小顶堆, 直接在原数组上进行修改

    Args:
        array (list[tuple]): 经过装饰后的列表对象
        heap_size (int): 当前要处理的堆的大小
        root_idx (int): 当前处理的根结点的索引
        is_better (Callable[[tuple, tuple], bool]): 决定是大顶堆还是小顶堆

    Returns:
        None
    """
    best_idx: int = root_idx  # 首先假设当前的索引就是最优的
    left: int = 2 * root_idx + 1
    right: int = 2 * root_idx + 2

    # Note: 下面两个判断条件共同做了一件事: 找到 root_idx、left 和 right 三者所指中的 最大值 / 最小值
    if left < heap_size and is_better(array[left], array[best_idx]):
        # 假设最开始时 reverse = False, 此时需要调整为大根堆
        # is_better(array[left], array[best_idx]):
        #   if array[left] >= array[best_idx]: return True
        #   else: return False
        # 如果 array[left] >= array[best_idx]
        #   说明 当前索引的左儿子索引指向的结点 大于等于 当前的最好索引
        #   此时应该更新 best_idx 的值
        best_idx = left
    if right < heap_size and is_better(array[right], array[best_idx]):
        # 同 if left < heap_size and is_better(array[left], array[best_idx]): 的判断逻辑
        best_idx = right
    if best_idx != root_idx:
        # 最优索引改变了 此时要调整堆 向下调整
        array[best_idx], array[root_idx] = array[root_idx], array[best_idx]
        heapify(array, heap_size, best_idx, is_better)


def heap_sort(
        nums: list[T],
        key: Optional[Callable[[T], Any]] = None,
        reverse: bool = False,
        inplace: bool = False
) -> list[T] | None:
    """堆排序
    1. 建堆: 将无序数组调整为大顶堆 / 小顶堆
    2. 排序: 每次将堆顶元素与末尾元素交换, 将堆的规模 - 1, 调整剩余元素为大顶堆/小顶堆, 重复这个过程直到只剩一个元素为止

    Args:
        nums (list[T]): 要排序的对象 -- 应该是一个列表对象
        key (Callable): 要按照哪个关键字排序
        reverse (bool): 是否 倒序, 默认为 False -- 从小到大
        inplace (bool): 是否在原数组的基础上修改, 默认为 False -- 不修改原数组, 返回排好序的新数组

    Returns:
        list[T] | None
    """
    # 特殊值处理
    if not nums:
        return None if inplace else []
    if len(nums) == 1:
        return None if inplace else nums[:]

    # 按照哪个关键词进行排序
    key_func: Callable[[T], Any] = (lambda x: x) if key is None else key

    # 装饰阶段
    decorated: list[tuple] = [(key_func(item), item) for item in nums]

    # 对于 reverse 参数, 如果 reverse == True, 那么每次都找最大的值放在前面, 否则找最小的值放在最前面即可
    # 定义比较逻辑：判断父节点是否 "优于" 子节点 (即不需要交换)
    # 升序用最大堆 (父 >= 子)，降序用最小堆 (父 <= 子)
    # 注意：只能比较 tuple[0]，防止 key 相等时去比较后面的 dict 导致 TypeError
    # 为了和以前的排序算法保持相同的变量命名规则, 就不写 parent 和 child 了,可以这样理解: x = parent, y = child
    is_better: Callable[[tuple, tuple], bool] = (
        (lambda x, y: x[0] <= y[0]) if reverse else lambda x, y: x[0] >= y[0]
    )

    # 排序核心逻辑
    n = len(nums)

    # # 建立堆
    # 从 最后一个非叶子结点开始对堆进行调整 直到整个堆的根节点
    for i in range(n // 2 - 1, -1, -1):
        heapify(decorated, n, i, is_better)

    # # 排序
    # 每次都将当前堆的根和当前堆的最后一个结点交换
    for i in range(n - 1, 0, -1):  # 要进行 n - 1轮
        # 交换 把 最大值/最小值 放到末尾
        decorated[i], decorated[0] = decorated[0], decorated[i]
        # 交换完毕后可能会导致堆不满足 大顶堆/小顶堆
        # 还需要继续调整, 注意此时的 heap_size 应该是 i
        heapify(decorated, i, 0, is_better)

    # 去装饰
    sorted_lst = [item[1] for item in decorated]
    if inplace:
        nums[:] = sorted_lst
        return None
    return sorted_lst
```









































































