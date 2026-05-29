<h1 style="text-align: center;font-size: 40px; font-family: 'Source Code Pro';">day-03.Django</h1>

今日内容概要

1. 学生管理
2. 模态对话框
3. Ajax

# 1. 学生管理

## 1.1 学生列表

```python
def student_list(request):
    """学生列表

    Args:
        request (): django.core.handlers.wsgi.WSGIRequest 对象，封装了请求相关的所有信息

    Returns:

    """
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='study',
        password='123456',
        database='trainee',
        charset='utf8',
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # # 下面两条语句都可以成功获取到连表的数据
    # cursor.execute("select id, name, (select title from class where class.id=student.class_id) as title from student")
    cursor.execute(
        "select student.id,student.name,class.title from student left join class on student.class_id=class.id")
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'student_list.html', {'data_list': data_list})
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>学生信息</title>
</head>
<body>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>学生信息</h1>

<a href="/add/student/">添 加</a>

<table border="1">
    <thead>
    <tr>
        <th>编号</th>
        <th>姓名</th>
        <th>所属班级</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    {% for item in data_list %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.title }}</td>
            <td>
                <a href="">详情</a>
                <a href="/update/?tid={{ item.id }}">编辑</a>
                <a href="/delete/?tid={{ item.id }}">删除</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>

</table>
</body>
</html>
</body>
</html>
```

## 1.2 添加学生

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>新增学生</title>
</head>
<body>

<h1>新增学生</h1>
<form method="POST" action="/add/student/">
    <p>姓名<input type="text" placeholder="姓名" name="name"/></p>

    <p>所在班级
        <!-- 后台根据 select 的name属性拿用户选择的东西，用户选择后提交到后台的东西是 option 标签的 value 属性的值 -->
        <!-- 后端最终拿到的是: { 'class_id': '{{ item.id }}' } -->
        <select name="class_id">
            {% for item in all_class %}
                <option value="{{ item.id }}">{{ item.title }}</option>
            {% endfor %}
        </select>
    </p>

    <button type="submit" value="提交">提 交</button>
</form>

</body>
</html>
```

```python
def add_student(request):
    if request.method == 'GET':
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='study',
            password='123456',
            database='trainee',
            charset='utf8',
        )
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select * from class')
        all_class = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'add_student.html', {'all_class': all_class})
    name = request.POST.get('name')
    class_id = request.POST.get('class_id')
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='study',
        password='123456',
        database='trainee',
        charset='utf8',
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('insert into student (name, class_id) values (%s, %s)', (name, class_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect('/student/list/')
```

## 1.3 删除班级

```
def delete_student(request):
    sid = request.GET.get('sid')
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='study',
        password='123456',
        database='trainee',
        charset='utf8',
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from student where id=%s', (sid,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect('/student/list/')
```

## 1.4 编辑学生信息

```python
from utils import MysqlConnector

def update_student(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        with MysqlConnector() as connect:
            cursor = connect.cursor
            cursor.execute('select * from class')
            all_class = cursor.fetchall()
            cursor.execute('select * from student where id=%s', (sid,))
            data = cursor.fetchone()
        return render(request, 'update_student.html', {'data': data, 'all_class': all_class})

    name = request.POST.get('name')
    sid = request.GET.get('sid')
    cid = request.POST.get('class_id')
    print('student_id=', sid, 'class id=', cid, 'new_name=', name)
    with MysqlConnector() as connect:
        cursor = connect.cursor
        cursor.execute('update student set name=%s,class_id=%s where id=%s', (name, cid, sid,))
        connect.conn.commit()

    return redirect('/student/list/')
```

```python
# utils.py

import pymysql


class MysqlConnector:
    def __init__(
            self,
            host='localhost',
            user='study',
            password='123456',
            database='trainee',
            charset='utf8',
            port=33.6
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.port = port

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset,
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>修改学生信息</title>
</head>
<body>

<h1>修改学生信息</h1>
<form method="POST" action="/update/student/?sid={{ data.id }}">
    <p>姓名<input type="text" value="{{ data.name }}" name="name"/></p>

    <p>所在班级
        <!-- 后台根据 select 的name属性拿用户选择的东西，用户选择后提交的东西是 option标签的value属性的值 -->
        <select name="class_id">
            {% for item in all_class %}
                {% if item.id == data.class_id %}
                    <option value="{{ item.id }}" selected>{{ item.title }}</option>
                {% else %}
                    <option value="{{ item.id }}">{{ item.title }}</option>
                {% endif %}
            {% endfor %}
        </select>
    </p>
    <button type="submit" value="提交">提 交</button>
</form>

</body>
</html>
```

# 2. 模态对话框

以班级列表为例

```python
def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        with MysqlConnector() as connect:
            conn = connect.conn
            cursor = connect.cursor
            cursor.execute('insert into class(title) values(%s)', (title,))
            conn.commit()
        return redirect('/class/list/')  # form表单提交，页面会刷新 -- form表单的特性，redirect后页面又会刷新一次
    else:
        # 如果传入的数据是空 则不要让对话框消失 提示错误信息
        #   这种需求永远不会成功 -- 页面永远会刷新 -- 因为用了 form 表单，页面一定会刷新 -- 换种方式 -- Ajax
        return redirect('/class/list/')
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .hide {
            display: none;
        }

        .shadow {
            position: fixed;
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            background-color: black;
            opacity: 0.4;
            z-index: 999;
        }

        .modal {
            z-index: 1000;
            position: fixed;
            left: 50%;
            top: 50%;
            height: 300px;
            width: 500px;
            background-color: white;
            margin-left: -250px;
            margin-top: -150px;
        }
    </style>
</head>
<body>
<h1>班级列表</h1>

<a href="/add/class/">添 加</a>
<button type="button" onclick="showModal();">模态框添加</button>

<table border="1">
    <thead>
    <tr>
        <th>id</th>
        <th>title</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    {% for item in data %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.title }}</td>
            <td>
                <a href="">详情</a>
                <a href="/update/class?cid={{ item.id }}">编辑</a>
                <a href="/delete/class?cid={{ item.id }}">删除</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>

</table>

<!-- 遮罩层 模态框 -->
<div id="shadow" class="shadow hide">
</div>
<div id="modal" class="modal hide">
    <form action="/modal/add/class/" method="POST">
        <p>
            <label>班级名<input type="text" placeholder="班级名" name="title"/></label>
        </p>
		
        <p>
            <button type="submit">提 交</button>
        </p>
    </form>
</div>

<script>
    function showModal() {
        document.getElementById('shadow').classList.remove('hide');
        document.getElementById('modal').classList.remove('hide');
    }
</script>

</body>
</html>

```

---

```python
# 如果传入的数据是空 则不要让对话框消失 提示错误信息
#   这种需求永远不会成功 -- 页面永远会刷新 -- 因为用了 form 表单，页面一定会刷新 -- 换种方式 -- Ajax
```

对于上述问题问题的修改方式：`Ajax`

# 3. Ajax

```python
# TODO: 学员管理之用Ajax创建班级 -- 要引入 jQuery
```































