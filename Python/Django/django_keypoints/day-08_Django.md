<h1 style="text-align: center;font-size: 40px; font-family: Source Code Pro;">day-08. Django</h1>

[TOC]

今日概要：

- `ORM` 操作
  - 增删改查
  - 其他
    - 排序
    - 
- `xss攻击`
- `CSRF`

# 1. `ORM`

> 参考 https://www.cnblogs.com/wupeiqi/articles/6216618.html

## 1.1 `F、Q、extra`

```python
def home(request):
    # # 创建数据
    # models.UserType.objects.create(title='普通用户')
    # models.UserType.objects.create(title='二逼用户')
    # models.UserType.objects.create(title='牛逼用户')

    # models.UserData.objects.create(name='杰克', age=15, type_id=2)
    # models.UserData.objects.create(name='罗丝', age=14, type_id=2)
    # models.UserData.objects.create(name='小明', age=13, type_id=1)
    # models.UserData.objects.create(name='鲍斯', age=20, type_id=3)

    # # 获取数据
    # # 跨表操作
    # query_set = models.UserData.objects.all()
    # for obj in query_set:
    #     # obj.type 是 UserType object (2) 类型的数据
    #     # print(obj.name, obj.age, obj.type_id)  # 杰克 15 2
    #     print(obj.name, obj.age, obj.type.title)  # 小明 13 普通用户

    # obj = models.UserData.objects.all().first()  # obj 是一个 UserData 对象
    # print(obj.name, obj.age, obj.type.title)  # 杰克 15 二逼用户

    # # 反向查找 -- 跨表
    # obj = models.UserType.objects.all().first()
    # print(obj.id, obj.title, obj.userdata_set)  # 1 普通用户 app01.UserData.None
    # print(obj.id, obj.title, obj.userdata_set.all())  # 1 普通用户 <QuerySet [<UserData: UserData object (3)>]>
    # for user_data_obj in obj.userdata_set.all():  # obj.userdata_set.all(): 查找属于UserType类型的所有用户
    #     print(user_data_obj.id, user_data_obj.name, user_data_obj.age)  # 3 小明 13

    # res = models.UserType.objects.all()
    # for obj in res:
    #     print(obj.title, obj.userdata_set.filter(name='小明', age=13).first())
    # # # 上述运行结果入下:
    # # 普通用户 UserData object (3)
    # # 二逼用户 None
    # # 牛逼用户 None

    # # res 类型: 还是 QuerySet 类型,但是里面不再是一个个对象,而是一个个字典
    # # QuerySet[{'id': 1, 'name': 'jack'}, {'id': 2, 'rose': 'jack'},{'id': 3, 'name': 'xiaoming'}]
    # res = models.UserData.objects.all().values('id', 'name')
    #
    # # res 类型: 还是 QuerySet 类型,但是里面不再是一个个对象,而是一个个字典
    # # QuerySet[{'id': 1, 'name': 'jack'}, {'id': 2, 'rose': 'jack'},{'id': 3, 'name': 'xiaoming'}]
    # res = models.UserData.objects.values('id', 'name')

    # # <QuerySet [(1, '杰克'), (2, '罗丝'), (3, '小明'), (4, '鲍斯')]>
    # res = models.UserData.objects.values_list('id', 'name')
    # # <QuerySet [(1, '杰克'), (2, '罗丝'), (3, '小明'), (4, '鲍斯')]>
    # res = models.UserData.objects.all().values_list('id', 'name')

    # # 这里要注意: 要获取UserType, 不能用 type.title, 而是要用 type__title
    # # <QuerySet [{'id': 1, 'name': '杰克', 'type__title': '二逼用户'},
    # # {'id': 2, 'name': '罗丝', 'type__title': '二逼用户'}, ...]>
    # res = models.UserData.objects.values('id', 'name', 'type__title')

    # query_set = models.UserType.objects.all()
    # # UserType表没有定义 __str__ 方法时打印: <QuerySet [<UserType: UserType object (1)>, <UserType: UserType object (2)>, <UserType: UserType object (3)>]>
    # # UserType表定义 __str__ 方法后打印: <QuerySet [<UserType: 普通用户>, <UserType: 二逼用户>, <UserType: 牛逼用户>]>
    # print(query_set)

    # # 排序
    # query_set = models.UserType.objects.all().order_by('-id', 'title')  # order_by: 排序
    # # <QuerySet [<UserType: 牛逼用户>, <UserType: 二逼用户>, <UserType: 普通用户>]>
    # print(query_set)

    # # 分组
    # from django.db.models import Count, Sum, Max, Min
    # v = models.UserData.objects.all().values('type_id').annotate(xxxx=Count('id'))
    # print(v.query)  # 查看 Django 生成的SQL语句
    # # SELECT "app01_userdata"."type_id" AS "type_id", COUNT("app01_userdata"."id") AS "xxxx" FROM "app01_userdata" GROUP BY 1

    # 分组
    # from django.db.models import Count, Sum, Max, Min
    # v = models.UserData.objects.all().values('type_id').annotate(xxxx=Count('id')).filter(xxxx__gt=1)
    # print(v.query)  # 查看 Django 生成的SQL语句
    # # SELECT "app01_userdata"."type_id" AS "type_id", COUNT("app01_userdata"."id") AS "xxxx" FROM "app01_userdata" GROUP BY 1 HAVING COUNT("app01_userdata"."id") > 1

    # from django.db.models import Count, Sum, Max, Min
    # v = models.UserData.objects.filter(id__gt=1).values('type_id').annotate(xxxx=Count('id'))
    # print(v.query)  # 查看 Django 生成的SQL语句
    # # SELECT "app01_userdata"."type_id" AS "type_id", COUNT("app01_userdata"."id") AS "xxxx" FROM "app01_userdata" WHERE "app01_userdata"."id" > 1 GROUP BY 1
    #
    # v = models.UserData.objects.filter(id__gt=1).values('type_id').annotate(xxxx=Count('id')).filter(xxxx__gt=1)
    # # SELECT "app01_userdata"."type_id" AS "type_id", COUNT("app01_userdata"."id") AS "xxxx" FROM "app01_userdata" WHERE "app01_userdata"."id" > 1 GROUP BY 1 HAVING COUNT("app01_userdata"."id") > 1
    # print(v.query)  # 查看 Django 生成的SQL语句

    # models.UserData.objects.filter(id__gt=1)  # id > 1
    # models.UserData.objects.filter(id__lt=1)  # id < 1
    # models.UserData.objects.filter(id__gte=1)  # id >= 1
    # models.UserData.objects.filter(id__lte=1)  # id <= 1
    # models.UserData.objects.filter(id__in=[1, 2, 3])  # id in (1, 2, 3)
    # models.UserData.objects.filter(id__range=[1, 2])  # id between 1 and 2
    # models.UserData.objects.filter(name__startswith='杰')
    # models.UserData.objects.filter(name__endswith='明')
    # models.UserData.objects.filter(name__contains='小1')
    # models.UserData.objects.exclude(id=1)  # id != 1
    # # 还有其他的 --> 参考 https://www.cnblogs.com/wupeiqi/articles/6216618.html

    # F, Q, extra
    from django.db.models import F
    # # 案例1. 让每个人的年龄自增 1
    # models.UserData.objects.all().update(age=F('age') + 1)

    # models.UserData.objects.filter(id=1, name='杰克')
    # conditions = {
    #     'id': 1,
    #     'name': '杰克'
    # }
    # models.UserData.objects.filter(**conditions)

    # Q 使用有两种使用方式
    from django.db.models import Q
    # models.UserData.objects.filter(Q(id=1))
    # models.UserData.objects.filter(Q(id=1) | Q(id=2))
    # models.UserData.objects.filter(Q(id=1) & Q(name='杰克'))
    #
    # q1 = Q()
    # q1.connector = 'OR'
    # q1.children.append(('id', 1))
    # q1.children.append(('id', 10))
    # q1.children.append(('id', 9))
    #
    # q2 = Q()
    # q2.connector = 'OR'
    # q2.children.append(('age', 30))
    # q2.children.append(('age', 35))
    # q2.children.append(('age', 14))
    #
    # q3 = Q()
    # q3.connector = 'AND'
    # q3.children.append(('id', 1))
    # q3.children.append(('name', '小明'))
    #
    # q1.add(q3, 'OR')
    #
    # con = Q()
    # con.add(q1, 'AND')
    # con.add(q1, 'AND')
    # con.add(q2, 'AND')
    # # (id=1 or id=10 or id=9 or (id=1 and name='小明')) and (age=30 or age=35 or age=14)

    # 可以根据前端传入的筛选条件动态生成查询条件
    # condition = {  # 查询 id in (1 2 3 4) 且 name='杰克' 且 age=16
    #     'id': [1, 2, 3, 4],
    #     'name': ['杰克', ],
    #     'age': [16, ]
    # }
    # new_conn = Q()
    # for k, v in condition.items():
    #     q = Q()
    #     q.connector = 'OR'
    #     for i in v:
    #         q.children.append((k, i))
    #     new_conn.add(q, 'AND')
    #
    # res = models.UserData.objects.filter(new_conn)
    # print(res)  # <QuerySet [<UserData: 杰克>]>

    # # extra
    # select
    #   id,
    #   name,
    #   (select count(1) from tb) as xx
    # from
    #   tb;
    # v = models.UserData.objects.all().extra(
    #     select={
    #         'n': 'select count(1) from app01_usertype where id > %s and id < %s',
    #         'm': 'select title from app01_usertype where id > %s and id < %s',
    #     },
    #     select_params=(1, 3, 1, 3)
    # )
    # for item in v:
    #     print(item.name, item.age, item.type_id, item.n, item.m)  # 杰克 16 2 1 二逼用户

    # v = models.UserData.objects.all().extra(
    #     where=['id=%s or id%s', "name=%s"],
    #     params=(1, 2, '杰克',)
    # )
    # # SELECT "app01_userdata"."id", "app01_userdata"."name", "app01_userdata"."age", "app01_userdata"."type_id" FROM "app01_userdata" WHERE (id=1 or id2) AND (name=杰克)
    # print(v.query)

    # v = models.UserData.objects.all().extra(
    #     tables=['app01_usertype']
    # )
    # # SELECT
    # #   "app01_userdata"."id",
    # #   "app01_userdata"."name",
    # #   "app01_userdata"."age",
    # #   "app01_userdata"."type_id"
    # # FROM "app01_userdata" , "app01_usertype"
    # print(v.query)

    return HttpResponse("Hello World")
```

## 1.2 关于 `models.UserData.objects.all().extra()`

```python
extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
```

一般情况下:

1. `select + select_params` 组合使用 -- 映射

   ```sql
   select ... from 表;
   ```

2. `where + params` 组合使用 -- 条件

   ```sql
   select * from 表 where ...;
   ```

3. `tables` -- 表

   ```sql
   select * from 表, ...;
   ```

4. `order_by` -- 排序

   ```sql
   select * from 表 order by ...;
   ```

注意上述四种相互间没有影响 -- 可以一起使用.

```python
models.UserInfo.objects.extra(
    select={'newid':'select count(1) from app01_usertype where id>%s'},
    select_params=[1,],
    where = ['age>%s'],
    params=[18,],
    order_by=['-age'],
    tables=['app01_usertype']
)
"""
select 
    app01_userinfo.id,
    (select count(1) from app01_usertype where id>1) as newid
from app01_userinfo,app01_usertype
where 
    app01_userinfo.age > 18
order by 
    app01_userinfo.age desc
"""
```

## 1.3 写原生SQL语句

```python
def home(request):
    from django.db import connection, connections
    cursor = connection.cursor()  # connection 就是 default
    cursor = connections['default'].cursor()  # 可以选择使用哪个数据库 默认是 default
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     },
    #     'another': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db_1.sqlite3',
    #     }
    # }
    # 然后就正常去写SQL语句即可.
    
    return HttpResponse("Hello World")
```

## 1.4 `extra`

```python
models.UserInfo.objects.extra(
    select={'newid':'select count(1) from app01_usertype where id>%s'},
    select_params=[1,],
    where = ['age>%s'],
    params=[18,],
    order_by=['-age'],
    tables=['app01_usertype']
)
"""
select 
    app01_userinfo.id,
    (select count(1) from app01_usertype where id>1) as newid
from app01_userinfo,app01_usertype
where 
    app01_userinfo.age > 18
order by 
    app01_userinfo.age desc
"""
------------------------------------------------------------------------
result = models.UserInfo.objects.filter(id__gt=1).extra(
    where=['app01_userinfo.id < %s'],
    params=[100,],
    tables=['app01_usertype'],
    order_by=['-app01_userinfo.id'],
    select={'uid':1,'sw':"select count(1) from app01_userinfo"}
)
print(result.query)
# SELECT (1) AS "uid", (select count(1) from app01_userinfo) AS "sw", "app01_userinfo"."id", "app01_userinfo"."name", "app01_userinfo"."age", "app01_userinfo"."ut_id" FROM "app01_userinfo" , "app01_usertype" WHERE ("app01_userinfo"."id" > 1 AND (app01_userinfo.id < 100)) ORDER BY ("app01_userinfo".id) DESC

```

## 1.5 `distinct`

```python
数据源不同，distinct(去重)的参数不同：
MySQL等数据库:
	models.UserData.objects.values('nid').distinct()
	# select distinct nid from app01_userdata;
	
PostgreSQL(只有):
	models.UserData.objects.values().distinct('nid')
```

## 1.6 性能相关

### 1.6.1 N+ 1问题

```python
# # 下面的语句会导致 N + 1 查询问题
# q = models.UserData.objects.all()
# for item in q:
#     print(item.name, item.age, item.type.title)

# 解决 N + 1 问题
# 1. 连表 inner join -- 第一次查询时自动做连表 -- 可以多张表关联 -- 只做一次连表
q = models.UserData.objects.all().select_related('type')
for item in q:
    print(item.name, item.age, item.type.title)  # 杰克 16 二逼用户
# SELECT
#   "app01_userdata"."id",
#   "app01_userdata"."name",
#   "app01_userdata"."age",
#   "app01_userdata"."type_id",
#   "app01_usertype"."id",
#   "app01_usertype"."title"
# FROM
#   "app01_userdata" LEFT OUTER JOIN "app01_usertype"
#   ON ("app01_userdata"."type_id" = "app01_usertype"."id")

# 也可以关联多张表:
# q = models.UserData.objects.all().select_related('type', 'group)
```

### 1.6.2 `prefetch_related`

```python
# # 连表也会导致查询速度减慢
# prefetch_related --> 不做连表, 做多次查询 -- 只做两次查询, 每次查一张表
q = models.UserData.objects.all().prefetch_related('type')
# # select * from userdata;
# # 在 Django 内部:
# #     获取查询出来的所有的 type_id 字段进行去重(查询出来其实就是 type_id 列表) --> type_id = [1, 2, 3, 4]
# #     再查询一次: select * from usertype where id in [1, 2, 3, 4];
for i in q:
    print(i.name, i.age, i.type.title)  # 杰克 16 二逼用户
```

### 1.6.3 多对多关系

```python
class Boy(models.Model):
    name = models.CharField('姓名', max_length=20)
    # 如果不写through参数 这样的话会生成一张新的多对多表,而我们自定义的多对多表也会有
    # through_fields 代表要连的那些字段
    m = models.ManyToManyField('Girl', through='Love', through_fields=('b', 'g'))  # 多对多字段 django 会帮我们创建一个多对多关系表 app01_boy_m,里面封装了set(),clear(),add(),remove(),all()方法来快速地进行增删改查操作

    def __str__(self):
        return self.name


class Girl(models.Model):
    name = models.CharField('姓名', max_length=20)
    # m = models.ManyToManyField('Boy')


class Love(models.Model):
    """多对多表 -- 很多代码需要自己写 比较多"""
    b = models.ForeignKey('Boy', on_delete=models.SET_NULL, null=True)
    g = models.ForeignKey('Girl', on_delete=models.SET_NULL, null=True)

    class Meta:
        # 联合唯一索引
        unique_together = [
            ('b', 'g'),
        ]
```



```python
# 1. 查找 和 jack 有关系的 girl
# # 1.1
# obj = models.Boy.objects.filter(name='jack').first()
# love_list = obj.love_set.all()
# for row in love_list:
#     print(row.g.name)  # rose, fake

# # 1.2
# love_list = models.Love.objects.filter(b__name='jack').all()
# for row in love_list:
#     print(row.g.name)  # rose, fake

# 1.3 一次查询
# love_list = models.Love.objects.filter(b__name='jack').values('g__name')
# print(love_list)  # <QuerySet [{'g__name': 'rose'}, {'g__name': 'fake'}]>
# for item in love_list:
#     print(item.get('g__name'))  # rose, fake

# 1.4 一次查询
# love_list = models.Love.objects.filter(b__name='jack').select_related('g')
# print(love_list)  # <QuerySet [<Love: Love object (1)>, <Love: Love object (2)>]>
# print(love_list.query)  # SELECT "app01_love"."id", "app01_love"."b_id", "app01_love"."g_id", "app01_girl"."id", "app01_girl"."name" FROM "app01_love" INNER JOIN "app01_boy" ON ("app01_love"."b_id" = "app01_boy"."id") LEFT OUTER JOIN "app01_girl" ON ("app01_love"."g_id" = "app01_girl"."id") WHERE "app01_boy"."name" = jack
#
# for item in love_list:
#     print(item.g.name)  # rose, fake
```

```python
# ***************************************** 多对多 *****************************************
# # 创建一些信息
# b_objs = [
#     models.Boy(name='jack'),
#     models.Boy(name='jordan'),
#     models.Boy(name='kobe'),
#     models.Boy(name='liming'),
#     models.Boy(name='jenny'),
# ]
# models.Boy.objects.bulk_create(b_objs, 5)
#
# g_objs = [
#     models.Girl(name='rose'),
#     models.Girl(name='green'),
#     models.Girl(name='frank'),
#     models.Girl(name='fake'),
#     models.Girl(name='danny'),
# ]
# models.Girl.objects.bulk_create(g_objs, 5)
#
# models.Love.objects.create(b_id=1, g_id=1)
# models.Love.objects.create(b_id=1, g_id=4)
# models.Love.objects.create(b_id=2, g_id=4)
# models.Love.objects.create(b_id=3, g_id=3)
# models.Love.objects.create(b_id=4, g_id=2)
# models.Love.objects.create(b_id=5, g_id=5)

# 1. 查找 和 jack 有关系的 girl
# # 1.1
# obj = models.Boy.objects.filter(name='jack').first()
# love_list = obj.love_set.all()
# for row in love_list:
#     print(row.g.name)  # rose, fake

# # 1.2
# love_list = models.Love.objects.filter(b__name='jack').all()
# for row in love_list:
#     print(row.g.name)  # rose, fake

# 1.3 一次查询
# love_list = models.Love.objects.filter(b__name='jack').values('g__name')
# print(love_list)  # <QuerySet [{'g__name': 'rose'}, {'g__name': 'fake'}]>
# for item in love_list:
#     print(item.get('g__name'))  # rose, fake

# 1.4 一次查询
# love_list = models.Love.objects.filter(b__name='jack').select_related('g')
# print(love_list)  # <QuerySet [<Love: Love object (1)>, <Love: Love object (2)>]>
# print(love_list.query)  # SELECT "app01_love"."id", "app01_love"."b_id", "app01_love"."g_id", "app01_girl"."id", "app01_girl"."name" FROM "app01_love" INNER JOIN "app01_boy" ON ("app01_love"."b_id" = "app01_boy"."id") LEFT OUTER JOIN "app01_girl" ON ("app01_love"."g_id" = "app01_girl"."id") WHERE "app01_boy"."name" = jack
#
# for item in love_list:
#     print(item.g.name)  # rose, fake

# 多对多 2.0
boys = models.Boy.objects.filter(name='jack').first()
# print(boys.id, boys.name)  # 1 jack
# boys.m.add(3)  # 多对多表中创建一行: boy_id=jack的id(此处是1),girl=add(3)方法里面的参数(此处是3)
# boys.m.add(1, 4)  # 多对多表中创建多行
# boys.m.add(*[2,])  # 多对多表中创建多行

# 删除
# boys.m.remove(1)
# boys.m.remove(2, 3)
# boys.m.remove(*[4,])

# 修改
# boys.m.set([1])  # 重置
# boys.m.set([1, 2])

# 获取 -- 此操作获取name='jack'的boy有关的girl
# v = boys.m.all()
# print(v)  # <QuerySet [<Girl: Girl object (1)>, <Girl: Girl object (2)>]>

# # boys.m 相当于是一个 Girl 对象
# v = boys.m.filter(id=1, name='rose')
# print(v)  # <QuerySet [<Girl: Girl object (1)>]>

# boys.m.clear()  # 全部删除

obj = models.Girl.objects.filter(name='green').first()
print(obj.boy_set.all())  # <QuerySet [<Boy: Boy object (1)>]>

```



# 2. `xss攻击`

跨站脚本攻击。

> https://www.cnblogs.com/wupeiqi/p/4592637.html

`safe, mark_safe`

# 3. `CSRF` & `CBV`

## 3.1 跨站请求伪造(`CSRF(Django)/XSRF`) `FBV`

`FBV`:  `csrf_exempt`    /   `csrf_protect`

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect
```

## 3.2 `CBV`

`CBV 进行 csrf 豁免: -- 只能这样写`

```python
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class View(View):
    
    def get(self, request):
        ...

    def post(self, request):
        ...
```

对CBV的函数进行装饰:

```python
# 1. 对类中方法加装饰器

def my_wrapper(func):
    """我的装饰器"""
    pass


class View(view):
    
    @method_decorator(my_wrapper)
    def get(self, request):
        pass
    
    
# 2. 对整个类加装饰器
@method_decorator(my_wrapper, name='dispathc')
class View(view):
	
    def get(self, request):
        pass

    
@method_decorator(my_wrapper, name='get')
class View(view):
	
    def get(self, request):
        pass
    
    def post(self, request):
        pass

    
@method_decorator(my_wrapper, name='post')
class View(view):
	
    def get(self, request):
        pass
    
    def post(self, request):
        pass
    
@method_decorator(my_wrapper, name='post')
@method_decorator(my_wrapper, name='get')
class View(view):
	
    def get(self, request):
        pass
    
    def post(self, request):
        pass
```

## 3.3 `Ajax + CSRF 1`

```python
# ajax/send/
def ajax_send(request):
    if request.method == 'GET':
        return render(request, 'ajax_send.html')
    return HttpResponse("OKK")
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ajax send.</title>
</head>
<body>
<form>
    {% csrf_token %}
    姓名<input type="text" name="name" value="" id="inputName">
    密码<input type="password" name="password" value="" id="inputPassword">
    <button type="button" onclick="submitForm();">提交</button>
</form>

<script src="/static/jquery-4.0.0.min.js"></script>
<script>
    function submitForm() {
        var a = $('#inputName').val();
        var b = $('#inputPassword').val();
        var c = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/ajax/send/',
            type: 'POST',
            data: {
                'name': a,
                'password': b,
                'csrfmiddlewaretoken': c  // 注意这里，csrf的键名只能是csrfmiddlewaretoken，否则会被Django拦截
            },
            success: function (data) {
                console.log('pk');
            }
        })
    }
</script>
</body>
</html>
```

## 3.4 `Ajax + CSRF 2`

```html
<script src="/static/jquery-4.0.0.min.js"></script>
<script src="/static/jquery.cookie.min.js"></script>
<script>
    /*
    // 第一种方法 从隐藏字段中找
    function submitForm() {
        var a = $('#inputName').val();
        var b = $('#inputPassword').val();
        var c = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/ajax/send/',
            type: 'POST',
            data: {
                'name': a,
                'password': b,
                'csrfmiddlewaretoken': c  // 注意这里，csrf的键名只能是csrfmiddlewaretoken，否则会被Django拦截
            },
            success: function (data) {
                console.log('pk');
            }
        })
    }
    */
	
    function submitForm() {
        var a = $('#inputName').val();
        var b = $('#inputPassword').val();

        // // 获取 cookie 的值 -- jquery cookie 太老了，应当是已经无法使用了
        // var c = $.cookie('csrftoken');
        // console.log(c);

        // // 使用原生 JS 获取名为 csrftoken 的 Cookie
        var c = getCookie('csrftoken');
        // console.log(c); // 你可以打印看看是否成功获取到了 token

        $.ajax({
            url: '/ajax/send/',
            type: 'POST',
            headers: {
                'X-CSRFToken': c
            },
            data: {
                'name': a,
                'password': b,
            },
            success: function (data) {
                console.log('pk');
            }
        })
    }

    // Django 官方提供的获取 Cookie 的函数
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // 判断该 cookie 是否以我们想要的 name 开头
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

</script>
```

# 4. 模板引擎

















































































