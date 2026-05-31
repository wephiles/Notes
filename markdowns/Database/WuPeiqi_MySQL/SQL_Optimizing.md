# `SQL`优化

## 1.1 查询中的JOIN优化

```
-- 普通查询
select 
  (select teacher.id from teacher where teacher.id=teacher2class.teacher_id) as tid,
  (select teacher.name from teacher where teacher.id=teacher2class.teacher_id) as tname,
  (select class.title from class where class.id=teacher2class.class_id) as ctitle
from teacher2class;

-- 连表查询 三张表相连
select 
  teacher.id as tid,
  teacher.name as tname,
  class.title as ctitle
from teacher  
left join teacher2class on teacher.id=teacher2class.teacher_id 
left join class on class.id=teacher2class.class_id;
```

这两条 SQL 语句在**逻辑结果**、**性能**和**代码规范**上都有非常大的区别。

最核心的区别在于**基表（驱动表）不同**：第一个查询以中间表 `teacher2class` 为基表，第二个查询以 `teacher` 表为基表。

以下是详细的对比分析：

### 1. 逻辑结果的区别（最重要）

- **查询一（子查询）：以 `teacher2class` 为基表**
  它遍历 `teacher2class` 表的每一行，去主表里取名字。结果集的行数**严格等于** `teacher2class` 表的行数。
  如果一个老师带了 3 个班，就会出现 3 行；如果一个老师没有带班（在 `teacher2class` 中没有记录），那么**这个老师根本不会出现在结果中**。
- **查询二（LEFT JOIN）：以 `teacher` 为基表**
  由于你使用的是 `LEFT JOIN`，且 `teacher` 在最左边，所以它以 `teacher` 表为基表。
  结果集**至少包含** `teacher` 表的所有老师。如果一个老师带了 3 个班，会出现 3 行；**如果一个老师没有带班，他依然会出现在结果中，只是对应的 `ctitle` 为 NULL**。

**举例说明：**
假设有一个老师"张三"（id=1），他没有带任何班级（`teacher2class` 表中没有 teacher_id=1 的记录）。

- 查询一的结果：**没有张三**。
- 查询二的结果：`1 | 张三 | NULL`。

> **补充：**如果你的本意是“只查询有带班的老师”，那么查询二的 `LEFT JOIN` 应该改成 `INNER JOIN`。改成 `INNER JOIN` 后，查询一和查询二在逻辑结果上就基本等价了（只要外键约束完整）。

### 2. 性能的区别

- **查询一（子查询）：性能极差**
  这种写法叫做**相关子查询**。数据库引擎在执行时，会对 `teacher2class` 的**每一行**，去执行 3 次子查询（查 tid、查 tname、查 ctitle）。
  如果 `teacher2class` 有 1000 条记录，数据库可能要额外执行 3000 次索引查找或全表扫描。这是典型的 N+1 查询问题，在数据量大时会导致严重卡顿。
- **查询二（LEFT JOIN）：性能优秀**
  `JOIN` 是数据库引擎专门为多表关联优化过的操作。数据库可以一次性评估最好的连接策略（如 Hash Join、Nested Loop Join 等），通过全表扫描或索引一次性完成结果集的拼接，效率比子查询高几个数量级。

*(注：某些现代的高级数据库优化器，如 MySQL 8.0+，可能会在底层自动将查询一优化成 JOIN 的执行计划，但从 SQL 编写意图上看，查询一依然是极度不推荐的写法。)*

### 3. 代码风格与可维护性

- **查询一：冗余且容易出错**
  你在两个子查询中重复写了 `where teacher.id=teacher2class.teacher_id` 这个关联条件。如果你还要加一个老师的字段（比如 age），你还得再写一个几乎一样的子查询，不仅代码臃肿，还容易漏改出错。
- **查询二：清晰标准**
  这是标准的 SQL 连表查询写法，逻辑清晰，关联条件集中写在 `ON` 后面，要增加查询字段只需在 `SELECT` 后补充 `teacher.age` 即可，非常易于维护。

### 总结与建议

**绝对不要在生产环境中使用查询一的写法。** 这种在 `SELECT` 列表中使用相关子查询去替代 `JOIN` 的方式是 SQL 编写的大忌。

**建议写法：**
根据你的业务需求，选择以下两种 JOIN 方式之一：

```
-- 情况 A：我想看所有的老师，即使没带班的也要列出来（带班为NULL）
SELECT 
  teacher.id AS tid,
  teacher.name AS tname,
  class.title AS ctitle
FROM teacher  
LEFT JOIN teacher2class ON teacher.id = teacher2class.teacher_id 
LEFT JOIN class ON class.id = teacher2class.class_id;

-- 情况 B：我只看有带班的老师和班级（和你的查询一逻辑一致，但性能好百倍）
SELECT 
  teacher.id AS tid,
  teacher.name AS tname,
  class.title AS ctitle
FROM teacher2class
INNER JOIN teacher ON teacher.id = teacher2class.teacher_id 
INNER JOIN class ON class.id = teacher2class.class_id;
```

*(注意情况 B 中，我把 `teacher2class` 放在了 `FROM` 后面作为驱动表，并使用了 `INNER JOIN`，这样逻辑上就和你写的第一个查询完全一致了，但性能极佳。)*

## 1.2 N+1问题

这是一个非常经典且重要的数据库/后端开发问题。

### 什么是 N+1 问题？

简单来说，**N+1 问题是由于在循环中执行数据库查询，导致原本可以用 1 次查询完成的工作，变成了 1+N 次查询，从而引发严重性能瓶颈的现象。**

这里的 `1` 指的是查询主列表的 1 次请求，`N` 指的是为了获取主列表中每条记录的关联数据，而额外发出的 N 次请求。

#### 结合你的表来举个生动例子

假设你现在要展示一个页面：**“所有老师及其所带的班级”**。数据库里有 **100 个老师**。

**写法 A：产生 N+1 问题（典型错误写法）**

1. 首先，你执行 1 次查询，获取所有老师：`SELECT * FROM teacher;` （返回 100 个老师）
2. 然后，你在代码里写了一个 for 循环，遍历这 100 个老师，每次循环都去查一次他带的班级：
   `SELECT * FROM teacher2class JOIN class ... WHERE teacher_id = 1;`
   `SELECT * FROM teacher2class JOIN class ... WHERE teacher_id = 2;`
   …
   `SELECT * FROM teacher2class JOIN class ... WHERE teacher_id = 100;`

结果：你向数据库发送了 **1 + 100 = 101 次请求**。这就是 N+1 问题。

**写法 B：使用 JOIN（正确写法）**
直接使用连表查询，一次性搞定：
`SELECT teacher.name, class.title FROM teacher JOIN teacher2class ... JOIN class ...;`
结果：你向数据库只发送了 **1 次请求**，数据库直接返回了拼装好的 100 条（或更多，看一个老师带几个班）结果。

### 为什么 N+1 问题很严重？

数据库的查询不仅消耗 CPU 和内存，更致命的是**网络往返开销**。
应用服务器和数据库服务器通常不在同一台机器上，每次查询都要经过：应用发请求 -> 网络传输 -> 数据库执行 -> 网络传回 -> 应用接收。
101 次网络交互和 1 次网络交互的延迟差距是巨大的。当数据量达到万级时，系统直接卡死是常有的事。

> ```sql
> select 
>   (select teacher.id from teacher where teacher.id=teacher2class.teacher_id) as tid,
>   (select teacher.name from teacher where teacher.id=teacher2class.teacher_id) as tname,
>   (select class.title from class where class.id=teacher2class.class_id) as ctitle
> from teacher2class;
> ```
>
> *注：上面这个SQL（在 SELECT 里写子查询），虽然看起来只有一句 SQL，但数据库引擎在底层执行时，相当于对每一行做了子查询，本质上也属于 N+1 问题的变体。*

### 如何解决 N+1 问题？

解决 N+1 问题的核心思想是：**用集合操作代替循环中的单条操作。** 主要有以下几种方案：

#### 方案 1：使用 JOIN（连表查询）—— 最直接的方案

```sql
SELECT 
  teacher.id AS tid,
  teacher.name AS tname,
  class.title AS ctitle
FROM teacher2class
INNER JOIN teacher ON teacher.id = teacher2class.teacher_id 
INNER JOIN class ON class.id = teacher2class.class_id;
```

就像上述 SQL 一样，在数据库层面直接把表连起来，一次性取出所有数据。

- **优点**：数据库一次搞定，网络交互最少。
- **缺点**：如果关联层级很深，或者是一对多/多对多关系，JOIN 会产生大量的“笛卡尔积”数据冗余（比如一个老师带 10 个班，老师的名字就会在结果里重复出现 10 次，传输数据量变大）。

#### 方案 2：使用 IN 子句（分批查询 / 批量获取）—— 最常用的方案

如果你觉得 JOIN 导致的数据冗余太大，或者因为某些原因（比如 ORM 框架的限制）不想用 JOIN，可以使用 IN 子句。

**步骤：**

1. 先查出主表：`SELECT * FROM teacher;` （拿到 100 个老师的 ID 列表：[1, 2, 3…100]）
2. 拿着这批 ID，一次性查出所有关联数据：
   `SELECT * FROM teacher2class JOIN class ... WHERE teacher_id IN (1, 2, 3 ... 100);`
3. 在应用代码（内存）中，将这 100 个老师和查出来的班级进行拼装映射。

- **优点**：避免了 JOIN 的数据冗余，查询次数从 N+1 降到了 2 次。
- **注意**：如果 ID 列表太长，IN 子句可能会超出数据库限制或导致索引失效，此时可以分批做 IN（比如每 500 个 ID 查一次）。

#### 方案 3：在 ORM 框架中使用“急切加载”

在现代 Web 开发中，很少直接手写原生 SQL，而是使用 ORM（如 Java 的 MyBatis/Hibernate，Python 的 Django ORM，Go 的 GORM 等）。ORM 默认通常是“懒加载”，极易产生 N+1 问题。

针对不同的 ORM，都有专门的语法来解决：

- **Django (Python)**: 使用 `select_related`（针对外键/一对一）或 `prefetch_related`（针对多对多/一对多）

```
    # 错误（N+1）：默认懒加载
    teachers = Teacher.objects.all()
    for t in teachers:
        print(t.classes.all()) # 每次循环都会查库
    
    # 正确：prefetch_related 会自动帮你执行 IN 查询
    teachers = Teacher.objects.prefetch_related('classes').all()
```

- **Golang (GORM)**: 使用 `Preload`

```
    // 正确：会在后台自动执行 IN 查询
    db.Preload("Classes").Find(&teachers)
```

- **Java (MyBatis)**: 使用 `<collection>` 标签的联合查询，或者手动执行两次查询并在 Service 层拼装。

### 总结

- **N+1 问题**：1 次查主表 + N 次查关联表 = 灾难级的性能问题。
- **解决思路**：
  1. 数据库层面用 **JOIN** 一次查出。
  2. 应用层面用 **IN 子句** 批量查出，然后在内存中拼装。
  3. 使用 ORM 时，务必开启 **急切加载**，避免在循环中触发懒加载查询。























































































