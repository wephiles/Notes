#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @CreateTime : 2026/05/15 19:55
# @Author     : wephiles@wephiles
# @IDE        : PyCharm
# @ProjectName: employee_management
# @FileName   : employee_management/pagination.py
# @Description: This is description of this script.
# @Interpreter: python 3.0+
# @Motto      : You must take your place in the circle of life!
# @AuthorSite : https://github.com/wephiles or https://gitee.com/wephiles

# Copyright (c) 2026 wephiles.
# This software is licensed under the MIT license.
# See the LICENSE file for details.

from django.utils.safestring import mark_safe


class Pagination:
    """
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ 自定义 bootstrap 分页组件                                                         │
    └─────────────────────────────────────────────────────────────────────────────────┘
    展示效果:
    ┌──────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──────┐    ┌───────────────┬────┐
    │ Prev │  1  │  2  │  3  │  4  │  5  │  6  │  7  │ Next │    │  1            │ Go │
    └──────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──────┘    └───────────────┴────┘

    如何使用:
    1. 在你的视图模块中:
        ```python
        #导入 Pagination 类
        from ... import Pagination


        def your_view(request):
            # 查询你的所有需要展示的数据
            need_show_objs = models.User.objects.all()

            # 分页
            paginator = Pagination(request, need_show_objs)

            return render(
                request,
                'your_show_html_files.html',
                {
                    'query_sets': paginator.query_sets,  # 这个值是必须的, 需要传到前端进行数据展示
                    'html_string': paginator.html,  # 这个是必须传的, 分页组件
                }
            )

        ```
    2. 在你的前端 HTML 文件中:
        ```html
        ...
        <table>
            在你想展示的地方循环展示数据.
        </table>
        ...
        <div class="row">
            {{html_string}}
        </div>
        ...

        ```
    """

    def __init__(
        self,
        request,
        query_sets,
        page_size: int = 10,
        total_page_block: int = 7,
        page_prev: int = 3,
    ):
        """初始化一些数据

        Args:
            request (): 请求对象
            query_sets (): 获取到的所有符合条件的,需要分页的数据
            page_size (): 每一页展示多少条数据,默认 10 条
            total_page_block (): 一个分页条展示多少个页码块,默认 7 块
            page_prev (): 当前页码块前面要显示几块,通过 此参数和total_page_block 可以计算出当前页码块后面需要显示几块
                默认前面显示 3 块,后面显示 3 块,总共 7 块.
        """
        self.all_nums = query_sets.count()
        self.cur_page = int(request.GET.get("page", 1))
        self.page_size = page_size
        self.total_page_block = total_page_block
        self.page_prev = page_prev
        self.page_next = self.total_page_block - self.page_prev - 1
        self.start = (self.cur_page - 1) * self.page_size
        self.end = self.start + self.page_size

        # 计算一共有几页
        count = self.all_nums // self.page_size
        if self.all_nums % page_size == 0:  # 正好全部分页都有 page_size 条数据
            self.total_pages = count
        else:  # 最后一页不足 page_size 条数据
            self.total_pages = count + 1

        if self.cur_page < self.total_pages:
            # 前面的每一页都有 page_size 条数据
            self.query_sets = query_sets[self.start : self.end]
        else:
            # 最后一页可能不足 page_size 条数据, 需要另做计算
            self.query_sets = query_sets[self.start : self.all_nums]

    @property
    def html(self):
        # 计算前面需要展示几个分页块
        total_lst = [i + 1 for i in range(self.total_pages)]

        if self.total_pages <= self.total_page_block:
            # 总页数小于用户可点击的页数 直接将其全部返回
            show_lst = total_lst
        else:
            left_page = self.cur_page - self.page_prev
            right_need_add = 0
            if left_page <= 0:
                right_need_add = -left_page + 1

            left_need_add = 0
            right_page = self.cur_page + self.page_next
            if right_page > self.total_pages:
                left_need_add = right_page - self.total_pages

            left_offset = (left_page if left_page > 0 else 1) - left_need_add
            right_offset = (
                right_page if right_page <= self.total_pages else self.total_pages
            ) + right_need_add
            show_lst = total_lst[left_offset - 1 : right_offset]

        backend_str_lst = [
            '<div class="col-2"></div> <div class="col"> <ul class="pagination justify-content-sm-end">'
        ]

        second_str = (
            '<li class="page-item disabled"><a class="page-link">Prev</a></li>'
            if self.cur_page == 1
            else f'<li class="page-item"> <a class="page-link" href="?page={self.cur_page - 1}">Prev</a> </li>'
        )
        backend_str_lst.append(second_str)
        for n in show_lst:
            if n == self.cur_page:
                cur_str = f'<li class="page-item active"><a class="page-link" href="?page={n}">{n}</a></li>'
            else:
                cur_str = f'<li class="page-item"><a class="page-link" href="?page={n}">{n}</a></li>'
            backend_str_lst.append(cur_str)
        end_str = (
            '<li class="page-item disabled"><a class="page-link">Next</a></li>'
            if self.cur_page == self.total_pages
            else f'<li class="page-item"> <a class="page-link" href="?page={self.cur_page + 1}">Next</a> </li>'
        )
        backend_str_lst.append(end_str)

        the_last_string = """</ul></div> <div class="col-2">
        <form class="d-flex" role="search" method="GET" style="margin-left: 20px;">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="page" value="1"/>
        <button class="btn btn-outline-success" type="submit">Go</button>
        </form>
        </div>"""
        backend_str_lst.append(the_last_string)
        # 将整个字符串拼接起来 传到后端
        html_string = "".join(backend_str_lst)
        return mark_safe(html_string)
