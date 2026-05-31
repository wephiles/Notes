<h1 style="text-align: center;font-size: 40px; font-family: Source Code Pro;">day-05.Django</h1>

今日内容：

- Bootstrap
  - 响应式
  - 栅格系统
- 后台管理布局
- cookie
- Django知识
  - 母版
  - 路由系统

# 1. Bootstrap

## 1.1 响应式

```html
...

<style>
    原来的标签属性 {
        background-color: green;
        height: 48px;
    }
    
    @media(max-width: 700px){  // 当页面宽度小于 700px 时执行下面的样式
		background-color: blue;
        height: 48px;
    }
</style>

...
```

# 2. 后台管理布局

![image-20260531194107163](./assets/image-20260531194107163.png)

```html
stule="min-width: 1190px;" -- 当缩小到 一定宽度时，下面会出现滚动条
```

---

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <style>
        body {
            margin: 0;
        }

        .page-header {
            height: 48px;
            min-width: 1190px;
            background-color: #6ea8fe;
        }

        .menus {
            width: 200px;
            position: absolute;
            left: 0;
            bottom: 0;
            top: 48px;
            background-color: red;
        }

        .content {
            position: absolute;
            left: 200px;
            top: 48px;
            bottom: 0;
            right: 0;
            min-width: 990px;
            background-color: yellow;
        }
    </style>
</head>
<body>
<div class="page-header"></div>
<div class="page-body">
    <div class="menus">菜单</div>
    <div class="content">内容</div>
</div>

</body>
</html>
```

![image-20260531195952615](./assets/image-20260531195952615.png)

但是像上面这样写有问题：如果主页面部分有很多数据，那么会出现问题。

![image-20260531200150472](./assets/image-20260531200150472.png)如果将黄色块的颜色变成白色，又将左边导航的高度定死 -- 这是一类布局是这样写的。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <style>
        body {
            margin: 0;
        }

        .page-header {
            height: 48px;
            min-width: 1190px;
            background-color: #6ea8fe;
        }

        .menus {
            width: 200px;
            position: absolute;
            left: 0;
        {#bottom: 0;#} height: 500px;
            top: 48px;
            background-color: red;
        }

        .content {
            position: absolute;
            left: 200px;
            top: 48px;
            bottom: 0;
            right: 0;
            min-width: 990px;

        }
    </style>
</head>
<body>
<div class="page-header"></div>
<div class="page-body">
    <div class="menus">菜单</div>
    <div class="content">
        <p>sdadas</p>
        ...
        <p>sdadas</p>
    </div>
</div>

</body>
</html>
```

![image-20260531200519880](./assets/image-20260531200519880.png)

----

但我们觉得这样不好，我们想让左侧菜单永远存在，右边正文部分超过长度可以向下滚动。

```html
overflow: scroll; -- 溢出的时候出现滚轮
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <style>
        body {
            margin: 0;
        }

        .page-header {
            height: 48px;
            min-width: 1190px;
            background-color: #6ea8fe;
        }

        .menus {
            width: 200px;
            position: absolute;
            left: 0;
            bottom: 0;
            top: 48px;
            background-color: red;
        }

        .content {
            position: absolute;
            left: 200px;
            top: 48px;
            bottom: 0;
            right: 0;
            min-width: 990px;
            background-color: gray;
            overflow: scroll;
        }
    </style>
</head>
<body>
<div class="page-header"></div>
<div class="page-body">
    <div class="menus">菜单</div>
    <div class="content">
        <p>sdadas</p>
        ...
        <p>f</p>
        <p>e</p>
        <p>d</p>
        <p>sdadas</p>
        <p>b</p>
        <p>a</p>
    </div>
</div>

</body>
</html>
```



![image-20260531200903687](./assets/image-20260531200903687.png)

## 2.1 模板

下面就是主页面滚动 但是菜单永远在那个位置不变，以后自定义你的各部分内容即可。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <style>
        body {
            margin: 0;
        }

        .page-header {
            height: 48px;
            min-width: 1190px;
            background-color: #6ea8fe;
        }

        .menus {
            width: 200px;
            position: absolute;
            left: 0;
            bottom: 0;
            top: 48px;
            background-color: red;
        }

        .content {
            position: absolute;
            left: 200px;
            top: 48px;
            bottom: 0;
            right: 0;
            min-width: 990px;
            background-color: gray;
            overflow: scroll;
        }
    </style>
</head>
<body>
<div class="page-header"></div>
<div class="page-body">
    <div class="menus">这里写你的菜单</div>
    <div class="content">
        <p>这里写你的主页面内容</p>
    </div>
</div>

</body>
</html>
```

![image-20260531201217975](./assets/image-20260531201217975.png)

## 2.2 完成模板

```html
logo 要上下居中：给他的父标签加 line-height: 多少px;
logo 要左右居中：给自己加属性： text-align: center;
```

```css
/*layout.css*/

body {
    margin: 0;
}

.hide {
    display: none;
}

.left {
    float: left;
}

.right {
    float: right;
}

.page-header {
    height: 48px;
    min-width: 1190px;
    background-color: purple;
    line-height: 48px;
}

.page-header .logo {
    color: white;
    font-size: 18px;
    width: 200px;
    text-align: center;
    border-right: 1px solid #dddddd;
}

.page-header .rheaders a {
    display: inline-block;
    padding: 0 10px;
    color: white;
}

.page-header .rheaders a:hover {
    background-color: #0d6efd;
}

.page-header .avatar {
    padding: 0 20px;
}


.page-header .avatar img {
    border-radius: 50%;
}

.page-header .avatar .user-info {
    display: none;
    position: absolute;
    width: 150px;
    top: 48px;
    right: 0;
    border: 1px solid #dddddd;
    background-color: white;
    z-index: 100;
}

.page-header .avatar:hover .user-info {
    display: block;
}

.page-header .avatar .user-info a {
    display: block;
    margin-left: 10px;
}

.menus {
    width: 200px;
    position: absolute;
    left: 0;
    bottom: 0;
    top: 48px;
    background-color: #9eeaf9;
    border-right: 1px solid #dddddd;
}

.page-body .menus a {
    display: block;
    padding: 10px 10px;
    border-bottom: 2px solid #ffffff;
}

.content {
    position: absolute;
    left: 200px;
    top: 48px;
    bottom: 0;
    right: 0;
    min-width: 990px;
    overflow: scroll;
    z-index: 99;
}
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <link rel="stylesheet" href="/static/plugins/fontawesome-free-7.2.0-web/css/all.css">
</head>
<body>
<div class="page-header">
    <div class="logo left">这是logo</div>
	
    <div class="left">工具1</div>
    <div class="left">工具2</div>
    <div class="left">工具3</div>

    <div class="avatar right" style="position: relative;">
        <img style="width: 40px; height: 40px;" src="/static/imgs/avatar.png" alt="">
        <div class="user-info hide">
            <a>个人资料</a>
            <a>注销</a>
        </div>
    </div>
    <div class="rheaders right">
        <a><i class="fa-solid fa-comment-dots"></i> 消息</a>
        <a><i class="fa-solid fa-envelope"></i> 邮件</a>
    </div>

</div>

<div class="page-body">
    <div class="menus">
        <a><i class="fa-solid fa-school"></i> 班级管理 </a>
        <a><i class="fa-solid fa-chalkboard-user"></i> 教师管理</a>
        <a><i class="fa-solid fa-user-graduate"></i> 学生管理</a>
    </div>
    <div class="content">
        <div aria-label="breadcrumb" class="container-fluid navbar-light bg-light">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="#">首页</a></li>
                <li class="breadcrumb-item"><a href="#">班级管理</a></li>
                <li class="breadcrumb-item active" aria-current="page">添加班级</li>
            </ol>
        </div>
    </div>
</div>

</body>
</html>
```

另外也要注意：shadow、modal这种类属性值、id属性值可能会与bootstrap里面的属性冲突，所以最好不要用这些。

经过修改后，以班级列表为例：只改了表面，内部还没改，看见样子即可。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <style>
        .hide {
            display: none;
        }

        .shadowAdd {
            position: fixed;
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            background-color: black;
            opacity: 0.4;
            z-index: 999;
        }

        .modalAdd {
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


    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <link rel="stylesheet" href="/static/plugins/fontawesome-free-7.2.0-web/css/all.css">

</head>
<body>
<div class="page-header">
    <div class="logo left">这是logo</div>

    <div class="left">工具1</div>
    <div class="left">工具2</div>
    <div class="left">工具3</div>

    <div class="avatar right" style="position: relative;">
        <img style="width: 40px; height: 40px;" src="/static/imgs/avatar.png" alt="">
        <div class="user-info hide">
            <a>个人资料</a>
            <a>注销</a>
        </div>
    </div>
    <div class="rheaders right">
        <a><i class="fa-solid fa-comment-dots"></i> 消息</a>
        <a><i class="fa-solid fa-envelope"></i> 邮件</a>
    </div>

</div>

<div class="page-body">
    <div class="menus">
        <a><i class="fa-solid fa-school"></i> 班级管理 </a>
        <a><i class="fa-solid fa-chalkboard-user"></i> 教师管理</a>
        <a><i class="fa-solid fa-user-graduate"></i> 学生管理</a>
    </div>
    <div class="content">
        <div aria-label="breadcrumb" class="container-fluid navbar-light bg-light">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="#">首页</a></li>
                <li class="breadcrumb-item"><a href="#">班级管理</a></li>
                {# <li class="breadcrumb-item active" aria-current="page">添加班级</li>#}
            </ol>
        </div>

        <div class="container-fluid">

            <a type="button" class="btn btn-primary btn-sm" href="/add/class/">添 加</a>
            <button type="button" class="btn btn-primary btn-sm" onclick="showModal();">模态框添加</button>

            <table class="table table-striped table-hover table-bordered border-primary" style="margin-top: 10px;">
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
                            <a type="button" class="btn btn-primary btn-sm">详情</a>
                            <a type="button" class="btn btn-primary btn-sm"
                               href="/update/class?cid={{ item.id }}">编辑</a>
                            <a cid="{{ item.id }}" class="btn btn-primary btn-sm" type="button"
                               onclick="showUpdateModal(this);">模态编辑</a>
                            <a type="button" class="btn btn-primary btn-sm"
                               href="/delete/class?cid={{ item.id }}">删除</a>
                            <a cid="{{ item.id }}" class="btn btn-primary btn-sm" type="button"
                               onclick="ShowDeleteModal(this);" id="delete-modal">模态删除
                            </a>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>


<!-- 新增数据 -- 遮罩层 模态框 -->
<div id="shadowAdd" class="shadowAdd hide">
</div>
<div id="modalAdd" class="modalAdd hide">
    <p>
        <label>
            班级名<input type="text" placeholder="班级名" name="title" id="title"/>
            <span id="error-text" style="color: red;"></span>
        </label>
    </p>

    <p>
        <button type="button" onclick="AjaxSend();">提 交</button>
        <button type="button" onclick="cancelModal();">取 消</button>
    </p>

</div>

<!-- 删除数据 -- 遮罩层 模态框 -->
<div id="shadow-delete" class="shadow hide">
</div>
<div id="modal-delete" class="modal hide">
    <p>
        {# <label>#}
        {# 班级名<input type="text" placeholder="班级名" name="title" id="title-delete"/>#}
        {# <span id="error-text-delete" style="color: red;"></span>#}
        {# </label>#}
        您正在执行删除操作，是否确认删除？
    </p>

    <p>
        <button type="button" onclick="DeleteAjaxSend();">提 交</button>
        <button type="button" onclick="DeleteCancelModal();">取 消</button>
    </p>

</div>

<!-- 编辑数据 -- 遮罩层 模态框 -->
<div id="shadow-update" class="shadow hide"></div>
<div id="modal-update" class="modal hide">
    <p>编辑班级信息</p>
    <p>
        <label>
            班级名<input type="text" placeholder="班级名" name="title" id="title-update"/>
            <input type="text" placeholder="班级名" name="title" id="title-update-id" style="display: none;"/>
            <span id="error-text-update" style="color: red;"></span>
        </label>
    </p>
    <p>
        <button type="button" onclick="updateAjaxSend();">提 交</button>
        <button type="button" onclick="updateCancelModal();">取 消</button>
    </p>
</div>

<script src="/static/js/jquery-4.0.0.min.js"></script>
<script>
    var DELETE_ID;

    /**
     * 新增班级
     */
    function showModal() {
        document.getElementById('shadowAdd').classList.remove('hide');
        document.getElementById('modalAdd').classList.remove('hide');
    }

    function AjaxSend() {
        $.ajax({
            url: '/modal/add/class/',
            type: 'post',
            data: {'title': $('#title').val()},
            success: function (response_data) {
                // 当服务端处理完毕，将数据返回到前端时该函数自动调用 response_data 是服务端返回的值
                // response_data = {status: true, code: 200, msg: 'Successfully insert data to trainee.class.'}
                // { 'status': false, 'code': 400, 'errors': '这个字段不能为空', }
                if (response_data.status) {
                    // 新增数据成功
                    // 跳转到 /class/list/
                    location.href = '/class/list/';
                } else {
                    // 新增数据失败
                    $("#error-text").text(response_data.errors)
                }
            }
        })
    }

    function cancelModal() {
        document.getElementById('shadowAdd').classList.add('hide');
        document.getElementById('modalAdd').classList.add('hide');
    }

    /**
     * 删除班级
     */
    function ShowDeleteModal(ths) {
        document.getElementById('shadow-delete').classList.remove('hide');
        document.getElementById('modal-delete').classList.remove('hide');
        DELETE_ID = $(ths).attr('cid');
    }


    function DeleteAjaxSend() {
        $.ajax({
            url: '/modal/delete/class?cid=' + DELETE_ID,
            type: 'get',
            data: {},
            success: function (response_data) {
                if (response_data.status) {
                    // 成功
                    location.reload();
                } else {
                    // 失败
                    alert(response_data.errors);
                }
            }
        })
    }

    function DeleteCancelModal() {
        document.getElementById('shadow-delete').classList.add('hide');
        document.getElementById('modal-delete').classList.add('hide');
    }

    /**
     * 编辑班级
     */
    function showUpdateModal(ths) {
        document.getElementById('shadow-update').classList.remove('hide');
        document.getElementById('modal-update').classList.remove('hide');

        /**
         * 获取当前标签
         * 获取当前标签的父标签
         * 获取当前标签的父标签的两个兄弟标签
         * <tr>
         *   <td>1</td> ---------------------------------------------------------------> 要找这两个标签
         *   <td>全栈一期</td> ---------------------------------------------------------> 要找这两个标签
         *   <td> ---------------------------------------------------------------------> 这是点击标签的父标签
         *       <button type="button">详情</button>                                             ^
         *       <button type="button" href="/update/class?cid=1">编辑</button>                  |
         *       <button cid="1" type="button" onclick="showUpdateModal();">模态编辑</button> -- 这是我们点击的那个标签
         *       <button type="button" href="/delete/class?cid=1">删除</button>
         *       <button cid="1" type="button" onclick="ShowDeleteModal();" id="delete-modal">模态删除
         *       </button>
         *   </td>
         * </tr>
         * 获取班级当前行的 id 当前班级名称 赋值给对话框中
         */

            // 当前标签 $(ths); 当前标签的父标签 $(ths).parent(); 前两个 $(ths).parent().prevAll();
            // 注意不能用$(ths).parent().siblings(),因为如果 $(ths).parent() 后面还有标签的话也会获取到，那就不对了.
            // 另外要注意 $(ths).parent().prevAll(); 获取到的 td 标签是从下往上的吗，即先获取了 <td>全栈一期</td> 再获取了 <td>1</td>
        var v = $(ths).parent().prevAll();
        var content = $(v[0]).text();
        $('#title-update').val(content);

        // 获取到班级ID
        var contentID = $(v[1]).text();
        $('#title-update-id').val(contentID);
    }

    function updateAjaxSend() {
        var cid = $('#title-update-id').val();
        var ctitle = $('#title-update').val();

        $.ajax({
            url: '/modal/update/class/',
            type: 'post',
            data: {'cid': cid, 'ctitle': ctitle},
            dataType: 'json',
            success: function (response_data) {
                if (response_data.status) {
                    // 成功
                    // JSON.parse('字符串'); // 将json字符串转换成对象
                    // JSON.stringify(json对象); // 将json对象转换成json串
                    // location.href = '/class/list/';
                    location.reload();  // 刷新当前页面
                } else {
                    // 失败
                    $('#error-text-update').text(response_data.errors);
                }
            }
        })
    }

    function updateCancelModal() {
        document.getElementById('shadow-update').classList.add('hide');
        document.getElementById('modal-update').classList.add('hide');
    }
</script>

</body>
</html>

```

![image-20260531215611352](./assets/image-20260531215611352.png)

---

这样做，如果要应用到别的地方，那么如果这样写，每次都要手动复制过去，很麻烦。

## 2.3 模板的优化 -- 可继承

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>

    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <link rel="stylesheet" href="/static/plugins/fontawesome-free-7.2.0-web/css/all.css">
    {% block css %}{% endblock %}
</head>
<body>
<div class="page-header">
    <div class="logo left">这是logo</div>

    <div class="left">工具1</div>
    <div class="left">工具2</div>
    <div class="left">工具3</div>

    <div class="avatar right" style="position: relative;">
        <img style="width: 40px; height: 40px;" src="/static/imgs/avatar.png" alt="">
        <div class="user-info hide">
            <a>个人资料</a>
            <a>注销</a>
        </div>
    </div>
    <div class="rheaders right">
        <a><i class="fa-solid fa-comment-dots"></i> 消息</a>
        <a><i class="fa-solid fa-envelope"></i> 邮件</a>
    </div>

</div>

<div class="page-body">
    <div class="menus">
        <a><i class="fa-solid fa-school"></i> 班级管理 </a>
        <a><i class="fa-solid fa-chalkboard-user"></i> 教师管理</a>
        <a><i class="fa-solid fa-user-graduate"></i> 学生管理</a>
    </div>
    <div class="content">
        <div aria-label="breadcrumb" class="container-fluid navbar-light bg-light myBrandNav">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="#">首页</a></li>
                <li class="breadcrumb-item"><a href="#">班级管理</a></li>
                <li class="breadcrumb-item active" aria-current="page">添加班级</li>
            </ol>
        </div>

        <div class="container-fluid">
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>


{% block js %}{% endblock %}
</body>
</html>
```

```html
body {
    margin: 0;
}

.hide {
    display: none;
}

.left {
    float: left;
}

.right {
    float: right;
}

.page-header {
    height: 48px;
    min-width: 1190px;
    background-color: purple;
    line-height: 48px;
}

.page-header .logo {
    color: white;
    font-size: 18px;
    width: 200px;
    text-align: center;
    border-right: 1px solid #dddddd;
}

.page-header .rheaders a {
    display: inline-block;
    padding: 0 10px;
    color: white;
}

.page-header .rheaders a:hover {
    background-color: #0d6efd;
}

.page-header .avatar {
    padding: 0 20px;
}


.page-header .avatar img {
    border-radius: 50%;
}

.page-header .avatar .user-info {
    display: none;
    position: absolute;
    width: 150px;
    top: 48px;
    right: 0;
    border: 1px solid #dddddd;
    background-color: white;
    z-index: 100;
}

.page-header .avatar:hover .user-info {
    display: block;
}

.page-header .avatar .user-info a {
    display: block;
    margin-left: 10px;
}

.menus {
    width: 200px;
    position: absolute;
    left: 0;
    bottom: 0;
    top: 48px;
    background-color: #9eeaf9;
    border-right: 1px solid #dddddd;
}

.page-body .menus a {
    display: block;
    padding: 10px 10px;
    border-bottom: 2px solid #ffffff;
}

.content {
    position: absolute;
    left: 200px;
    top: 48px;
    bottom: 0;
    right: 0;
    min-width: 990px;
    overflow: scroll;
    z-index: 99;
}

.page-body .content .myBrandNav {
    height: 35px;
}

.page-body .content .myBrandNav ol {
    line-height: 35px;
}
```

```html
{% extends 'layout.html' %}

{% block css %}
    <style>
        .hide {
            display: none;
        }

        .shadow {
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
            position: fixed;
            background-color: black;
            opacity: 0.4;
            z-index: 999;
        }

        .modal {
            z-index: 1000;
            width: 400px;
            height: 300px;
            position: fixed;
            left: 50%;
            top: 50%;
            margin-left: -200px;
            margin-top: -250px;
            background-color: white;
        }
    </style>
{% endblock %}

{% block content %}
    <a href="/add/student/">添 加</a>
    <button type="button" id="add-modal-student">模态框添加</button>

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
                    <a href="/update/student?sid={{ item.id }}">编辑</a>
                    <a class="updateButtonUpdate" cid="{{ item.class_id }}" sname="{{ item.name }}" sid="{{ item.id }}">模态框编辑</a>
                    <a href="/delete/student?sid={{ item.id }}">删除</a>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>

    {# 新增学生 模态框 #}
    <div id="shadow" class="shadow hide"></div>
    <div id="modalAdd" class="modal hide">
        <h3>添加学生</h3>
        <p>
            <label for="addNameInput">姓 名</label>
            <input type="text" id="addNameInput" name="addName">
        </p>
        <span style="color: red;" id="errorInName"></span>

        <p>
            <label for="addClassChoice">班级</label>
            <select id="addClassChoice" name="selectClass">
                <option selected style="text-align: center;">---</option>
                {% for item in class_list %}
                    <option style="text-align: center;" value="{{ item.id }}">{{ item.title }}</option>
                {% endfor %}
            </select>
            <span style="color: red;" id="errorInClassSelected"></span>
        </p>

        <p>
            <button type="button" id="addStudentSubmit">提 交</button>
            <button type="button" id="addStudentCancel">取 消</button>
        </p>
    </div>

    {# 编辑学生信息 模态框 #}
    <div id="shadowUpdate" class="shadow hide"></div>
    <div id="modalUpdate" class="modal hide">
        <h3>编辑学生信息</h3>
        <p>
            <label for="updateNameInput">姓 名</label>
            <input type="text" id="updateNameInput" name="updateName">
            <input type="text" id="updateNameInputId" name="updateNameId" style="display: none;">
        </p>
        <span style="color: red;" id="errorInNameUpdate"></span>

        <p>
            <label for="updateClassChoice">班级</label>
            <select id="updateClassChoice" name="selectClass">
                {% for item in class_list %}
                    <option style="text-align: center;" value="{{ item.id }}">{{ item.title }}</option>
                {% endfor %}
            </select>
            <span style="color: red;" id="errorInClassSelectedUpdate"></span>
        </p>

        <p>
            <button type="button" id="updateStudentSubmit">提 交</button>
            <button type="button" id="updateStudentCancel">取 消</button>
        </p>
    </div>

{% endblock %}

{% block js %}
    <script src="/static/js/jquery-4.0.0.min.js"></script>

    <script>
        // 当页面框架加载完毕执行
        $(function () {
            // 给 模态框新增学生绑定一个事件
            clickAddModalNewEvent();

            // 给 模态框编辑学生信息绑定一个事件
            clickUpdateModalNewEvent();
        })

        function clickAddModalNewEvent() {
            $('#add-modal-student').click(function () {
                // 只要点击相关标签就执行此函数体里面的内容
                $('#shadow,#modalAdd').removeClass('hide');
            });
            $('#addStudentSubmit').click(function () {
                // 点击模态框的提交按钮后执行此函数体内的代码
                $.ajax({
                    url: '/modal/add/student/',
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'name': $('#addNameInput').val(),
                        'class_id': $('#addClassChoice').val(),
                    },
                    success: function (res) {
                        if (res.status) {
                            // 成功添加
                            location.reload();
                        } else {
                            // 添加失败
                            if (res.code == 400) {
                                $('#errorInName').text(res.errors);
                            } else {
                                $('#errorInClassSelected').text(res.errors);
                            }
                        }
                    }
                })
            });

            $('#addStudentCancel').click(function () {
                // 点击模态框的取消按钮后执行此函数体内的代码
                document.getElementById('shadow').classList.add('hide');
                document.getElementById('modalAdd').classList.add('hide');
            });
        }

        function clickUpdateModalNewEvent() {
            // 弹出模态框
            $('.updateButtonUpdate').click(function () {
                $('#shadowUpdate,#modalUpdate').removeClass('hide');

                // 将残留的错误信息删掉
                $('#errorInNameUpdate').empty();
                $('errorInClassSelectedUpdate').text('');

                // 给输入框赋值
                // 当前标签
                var cid = $(this).attr('cid');
                var sname = $(this).attr('sname');
                var sid = $(this).attr('sid');

                $('#updateNameInputId').val(sid);
                $('#updateNameInput').val(sname);
                $('#updateClassChoice').val(cid);

            })

            // 点击取消让模态框消失
            $('#updateStudentCancel').click(function () {
                $('#shadowUpdate,#modalUpdate').addClass('hide');
            })

            $('#updateStudentSubmit').click(function () {
                // 输入好信息后发送Ajax请求到后端
                $.ajax({
                    url: '/modal/update/student/',
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'sname': $('#updateNameInput').val(),
                        'sid': $('#updateNameInputId').val(),
                        'cid': $('#updateClassChoice').val(),
                    },
                    success: function (data) {
                        if (data.status) {
                            location.reload();
                        } else {
                            $('#errorInNameUpdate').text(data.msg);
                        }
                    }
                })
            })

        }
    </script>
{% endblock %}

```

![image-20260531221253020](./assets/image-20260531221253020.png)

---

最后再修改一下：

`layout.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>


    <link rel="stylesheet" href="/static/css/bootstrap-5.3.8-dist/css/bootstrap.css">
    <link rel="stylesheet" href="/static/plugins/fontawesome-free-7.2.0-web/css/all.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    {% block css %}{% endblock %}
</head>
<body>

<div class="my-page-header">
    <div class="my-logo my-left">
        <a class="navbar-brand" href="#">
            <img src="/static/imgs/avatar.png" alt="Bootstrap"> 啥啥啥有限公司
        </a>
    </div>

    <div class="my-left my-tools-li">
        <a><i class="fa-solid fa-file"></i> 文件</a>
    </div>
    <div class="my-left my-tools-li">
        <a><i class="fa-solid fa-screwdriver-wrench"></i> 工具2</a>
    </div>
    <div class="my-left my-tools-li">
        <a><i class="fa-solid fa-calculator"></i> 工具3</a>
    </div>

    <div class="my-avatar my-right" style="position: relative;">
        <img src="/static/imgs/avatar.png" alt="">
        <div class="my-user-info my-hide">
            <a type="button" class="btn my-before-hr-info" href="#">个人资料</a>
            <a type="button" class="btn my-before-hr-info" href="#">设置中心</a>
            <hr class="my-hr-user-info">
            <a class="btn my-below-hr-info">注销</a>
        </div>
    </div>
    <div class="my-rheaders my-right">
        <a><i class="fa-solid fa-comment-dots"></i> 消息</a>
        <a><i class="fa-solid fa-envelope"></i> 邮件</a>
    </div>

</div>

<div class="my-page-body">
    <div class="my-menus">
        <a class="btn"><i class="fa-solid fa-school"></i> 班级管理 </a>
        <a class="btn"><i class="fa-solid fa-chalkboard-user"></i> 教师管理</a>
        <a class="btn"><i class="fa-solid fa-user-graduate"></i> 学生管理</a>
    </div>
    <div class="my-content">
        <div aria-label="breadcrumb" class="container-fluid navbar-light bg-light myBrandNav">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="#">首页</a></li>
                <li class="breadcrumb-item"><a href="#">班级管理</a></li>
                <li class="breadcrumb-item active" aria-current="page">添加班级</li>
            </ol>
        </div>

        <div class="container-fluid">
            {% block content %}
            {% endblock %}
        </div>
    </div>
</div>


{% block js %}{% endblock %}
</body>
</html>
```

`layout.css`:

```css
body {
    margin: 0;
}

.my-hide {
    display: none;
}

.my-left {
    float: left;
}

.my-right {
    float: right;
}

.my-page-header {
    height: 48px;
    min-width: 1190px;
    background-color: purple;
    /*background-color: rgb(13,202,250);*/
    line-height: 48px;
}

.my-page-header .my-logo {
    color: white;
    font-size: 18px;
    width: 200px;
    text-align: center;
    border-right: 1px solid gray;
}

.my-page-header .my-rheaders a {
    display: inline-block;
    padding: 0 10px;
    color: white;
    border-radius: 5px;
}

.my-page-header .my-rheaders a:hover {
    background-color: #0d6efd;
}

.my-page-header .my-avatar {
    padding: 0 20px;
}


.my-page-header .my-avatar img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-bottom: 4px;
}

.my-page-header .my-avatar .my-user-info {
    display: none;
    position: absolute;
    width: 150px;
    top: 50px;
    right: 18px;
    border: 1px solid #dddddd;
    background-color: white;
    z-index: 100;
    border-radius: 5px;
}

.my-page-header .my-avatar:hover .my-user-info {
    display: block;
}

.my-page-header .my-avatar .my-user-info .my-before-hr-info {
    display: block;
    height: 36px;
}

.my-page-header .my-avatar .my-user-info .my-hr-user-info {
    height: 1px;
    margin-top: 8px;
    margin-bottom: 1px;
}

.my-page-header .my-avatar .my-user-info .my-below-hr-info {
    display: block;
    margin-top: 1px;
}

.my-menus {
    width: 200px;
    position: absolute;
    left: 0;
    bottom: 0;
    top: 48px;
    background-color: #9eeaf9;
    border-right: 1px solid #dddddd;
}

.my-page-body .my-menus a {
    display: block;
    padding: 10px 10px;
    border-bottom: 2px solid #ffffff;
}

.my-content {
    position: absolute;
    left: 200px;
    top: 48px;
    bottom: 0;
    right: 0;
    min-width: 990px;
    overflow: scroll;
    z-index: 99;
}

.my-page-body .my-content .my-myBrandNav {
    height: 35px;
}

.my-page-body .my-content .myBrandNav ol {
    line-height: 35px;
}


.my-page-header .my-logo a img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
    margin-bottom: 4px;
}

.my-page-header .my-logo a {
    color: #31d2f2;
    font-size: 15px;
}

.my-page-header .my-tools-li a {
    display: inline-block;
    color: white;
    padding: 0 15px;
    border-radius: 5px;
}

.my-page-header .my-tools-li a:hover {

    background-color: #0d6efd;
}
```

![image-20260531233046342](./assets/image-20260531233046342.png)

![image-20260531233055130](./assets/image-20260531233055130.png)

![image-20260531233103219](./assets/image-20260531233103219.png)

# 3. cookie













































































































