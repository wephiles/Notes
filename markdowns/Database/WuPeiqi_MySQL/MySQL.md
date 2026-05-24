<h1 style="text-align: center;font-size: 40px; font-family: '楷体';">MySQL</h1>

[TOC]

以前，在开发程序时，我们会把很多数据和信息存储到某个文件夹中的文件中，例如：`users.txt`，`db.xlsx` 等。

现在，有一个名叫数据库管理系统(DBMS, Database Management System) 的软件，可以帮助我们实现对文件夹中的文件进行操作，而我们只要学习DBMS能够识别的指令，就能控制它去帮助我们实现对文件和文件夹的处理，例如：

![image-20260523231942094](./assets/image-20260523231942094.png)

![image-20260523232447975](./assets/image-20260523232447975.png)

数据库管理系统（DBMS）专注于帮助开发者解决数据存储的问题，这样开发者就可以将主要精力放在实现业务功能上了。

业内有很多的DBMS产品，例如：

- MySQL： 原来是sun公司，后来被甲骨文收购 现在互联网企业几乎都在用 【免费 + 收费】
- Oracle： 甲骨文 收费 一般国企、事业单位居多 【收费】
- Microsoft SQLServer： 微软 【收费】
- DB2： IBM 【免费 + 收费】
- Access：微软 【收费】
- PostgreSQL：加州大学伯克利分校 【免费】
- ...

我们主要使用MySQL

![image-20260523233011165](./assets/image-20260523233011165.png)

![image-20260523233048785](./assets/image-20260523233048785.png)

# day-01 MySQL入门

目标：学习安装和快速应用`Python`实现数据库的操作。

课程概要：

- 安装 & 配置 & 启动
  - `win`
  - `mac`
- 数据库  管理 (类比文件夹)
- 表 管理 (类比文件夹下面的 `Excel` 文件)
- 数据行管理 (类比 `Excel` 文件中的数据行)
- `Python` 操作 `MySQL` 及相关安全问题

## 1.1 安装 & 配置 & 启动

MySQL现在的版本主要分为：

- 5.x 版本，现在互联网企业中的主流版本 包括 头条 美团 百度 腾讯等公司主流版本
- 8.x 版本 新增了一些窗口函数。持久化配置、隐藏索引等其他功能

所以，我们课程会以常用大版本中最新的版本为例来讲解 - 5.7.31

### 1.1.1 Windows 系统

省略，去网上查。

`my.ini`:

```txt
[mysqld]

# 设置端口
port=3306

# MySQL 安装目录
basedir=E:\\Software\\mysql-8.4.9-winx64

# 数据存储目录
datadir=E:\\Software\\mysql-8.4.9-winx64\\data

# 最大连接数
max_connections=200

# 默认字符集
character-set-server=utf8mb4

# 默认存储引擎
default-storage-engine=INNODB

[mysql]
# 客户端默认字符集
default-character-set=utf8mb4

[client]

# 客户端连接端口和字符集
port=3306
default-character-set=utf8mb4
```

初始化：

```bash
>>>mysqld.exe --initialize-insecure
```

- 临时启动：
  ```bash
  >>>mysqld.exe
  ```

  只要关闭黑窗口就会将MySQL关闭，但是这样每次都要手动启动 很麻烦.

- 制作 Windows 服务 基于 Windows服务管理器
  ```bash
  >>>mysqld.exe --install mysql(可以自己定义)
  ```

  创建好服务后，可以通过命里给你 启动和关闭服务
  ```bash
  >>>net start mysql(你自定义的服务名)
  >>>net stop mysql(你自定义的服务名)
  ```

  以后不想使用Windows服务了，也可以将制作的这个MySQL服务删除
  ```bash
  >>>mysqld.exe --remove mysql(你自定义的服务名)
  ```

测试连接（命令行）：

```python
>>>mysql -h 127.0.0.1 -P 3306 -u root -p
```

此时还没有设置密码，要输密码的时候直接回车即可。

![image-20260524000958251](./assets/image-20260524000958251.png)

![image-20260524001054519](./assets/image-20260524001054519.png)

修改自己的密码：

```bash
>>>mysql -u root -p
>>>ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密码';
# 如果上面的代码报错 使用下面的代码
>>>ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
```

![image-20260524001735776](./assets/image-20260524001735776.png)

### 1.1.2 Mac 系统

省略，去网上查。

## 1.2 数据库管理

安装上`MySQL`后，就需要开始学习指令了，通过指令让`MySQL`去做出一些文件操作。

![image-20260523233011165](./assets/image-20260523233011165.png)

如果将数据库管理系统与之前的文件管理做类比的话：

| 数据库管理系统 | 文件管理            |
| -------------- | ------------------- |
| 数据库         | 文件夹              |
| 数据表         | 文件夹下的Excel文件 |

接下来，我们先学习数据库（文件夹）相关操作的指令。

![image-20260524084729201](./assets/image-20260524084729201.png)

### 1.2.1 内置客户端操作

当连接上`MySQL`后，执行如下命令（一般称为`SQL`语句），就可以对`MySQL`的数据进行操作。

- 查看当前的所有数据库
  ```sql
  show databases;
  ```

- 创建数据库
  ```sql
  create database 数据库名 default charset utf8 collate utf8_general_ci;
  create database 数据库名;
  ```

- 删除数据库
  ```sql
  drop database 数据库名;
  ```

- 进入数据库（进入文件夹）
  ```sql
  use 数据库名;
  ```

示例：

```bash
# 登录MySQL
C:\Users\wephiles>mysql -u root -p
Enter password: ******
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.4.9 MySQL Community Server - GPL

Copyright (c) 2000, 2026, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

# 查看当前数据库
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.02 sec)

# 创建数据库 create database 数据库名 default charset 编码 collate 排序规则;
mysql> create database day01db default charset utf8 collate utf8_general_ci;
Query OK, 1 row affected, 2 warnings (0.18 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| day01db            |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

# 删除数据库
mysql> drop database day01db;
Query OK, 0 rows affected (0.22 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

# 进入数据库里面
mysql> use mysql;
Database changed

# 查看当前数据库下面有哪些表
mysql> show tables;
+------------------------------------------------------+
| Tables_in_mysql                                      |
+------------------------------------------------------+
| columns_priv                                         |
| component                                            |
| db                                                   |
| ...                                                  |
+------------------------------------------------------+
38 rows in set (0.00 sec)

```

### 1.2.2 Python代码操作

无论通过何种方式连接MySQL，本质上发送的指令都是相同的，只是连接的方式和操作形式不同而已。

当连上MySQL后，执行如下指令，就可以对MySQL的数据进行操作。（同上述过程）

- 查看当前所有的数据库 `show databases;`
- 创建数据库 `create database 数据库名 default charset utf8 collate utf8_general_ci;`
- 删除数据库 `drop database 数据库名;`
- 进入数据库 `use 数据库名;`



想要使用Python操作MySQL需要安装第三方模块：

```bash
pip install pymysql
```



![image-20260524084729201](./assets/image-20260524084729201.png)

安装完成后，就可以编写代码：

```python
import pymysql

# 连接 MySQL (Socket)
conn = pymysql.connect(
	host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    charset='utf8',
)
cursor = conn.cursor()

# 1. 查看数据库
# 发送指令
cursor.execute('show databases;')
# 获取指令的结果
result = cursor.fetchall()
print(result)  # (('information_schema',), ('mysql',), ('performance_schema',), ('sys',))

# 2. 创建数据库
# 发送指令
cursor.execute('create database study01 default charset utf8 collate utf8_general_ci;')
conn.commit()

# 3. 查看数据库
# 发送指令
cursor.execute('show databases;')
# 获取指令的结果
result = cursor.fetchall()
print(result)  # (('information_schema',), ('mysql',), ('performance_schema',), ('study01',), ('sys',))

# 4. 查看数据库
# 发送指令
cursor.execute('drop database study01;')
conn.commit()  # 新增 修改 删除 操作需要 commit

# 5. 查看数据库
# 发送指令
cursor.execute('show databases;')
# 获取指令的结果
result = cursor.fetchall()  # 一般查询需要获取结果I
print(result)  # (('information_schema',), ('mysql',), ('performance_schema',), ('sys',))

# 6. 进入数据库 查看表
# 发送指令
cursor.execute('use mysql;')
cursor.execute('show tables;')
result = cursor.fetchall()
print(result)  # (('columns_priv',), ('component',), ('db',), ...)

# 关闭连接
cursor.close()
conn.close()
```

> [!Note]
>
> 注意一个小问题：我们通过命令行操作数据库和数据库表以及数据行的时候，每条语句结束都要加一个分号表示当签命令结束，但是python操作数据库数据表数据行就不用加，当然加了也没有问题。

## 1.3 数据表管理

![image-20260523231942094](./assets/image-20260523231942094.png)

如果将数据库管理系统与之前的文件管理做类比的话：

| 数据库管理系统 | 文件管理            |
| -------------- | ------------------- |
| 数据库         | 文件夹              |
| 数据表         | 文件夹下的Excel文件 |

接下来，我们先学习数据表相关操作的指令。

![image-20260524084729201](./assets/image-20260524084729201.png)



在数据库中创建数据表和创建Excel文件非常类似，需要指定：`表名`、`列名称`、`列类型（整形、字符串类型或其他）`

### 1.3.1 客户端内置操作

> [!Note]
>
> 补充：在命令行中，执行 `system clear;` 或者 `system cls;` 清屏.

数据表常见的操作指令：

- 进入数据库 `use 数据库;`, 查看当前所有表 `show tables;`

- 创建表结构

  ![image-20260524093200604](./assets/image-20260524093200604.png)

  ```sql
  create table 表名(
  	列名 类型,
      列名 类型,
      列名 类型
  ) default charset=utf8;
  ```

  ```sql
  create table tb1(
  	id int,
      name varchar(16)
  ) default charset=utf8;
  ```

  ![image-20260524093718825](./assets/image-20260524093718825.png)

  ```sql
  create table tb2(
  	id int,
      name varchar(16) not null, --> 不允许为空
      email varchar(32) null, --> 允许为空(默认)
      age int
  ) default charset=utf8;
  ```

  ![image-20260524094526347](./assets/image-20260524094526347.png)

```sql
create table tb3(
	id int,
    name varchar(16) not null, --> 不允许为空
    email varchar(32) null, --> 允许为空(默认)
    age int default 3  --> 插入数据时，如果不给 age 列设置值，默认为 3
) default charset=utf8;
```

![image-20260524095010944](./assets/image-20260524095010944.png)

```sql
create table tb4(
	id int primary key,  --> 主键（不允许为空，不能重复）
    name varchar(16) not null, --> 不允许为空
    email varchar(32) null, --> 允许为空(默认)
    age int default 3  --> 插入数据时，如果不给 age 列设置值，默认为 3
) default charset=utf8;
```

主键一般用于表示当前这条数据的ID编号，需要我们自己来维护一个不重复的值，比较繁琐，所以，在数据库中一般会讲主键和自增组合；

```sql
create table tb4(
	id int not null auto_increment primary key,  -- 这是注释 `--`后面的会被注释
    name varchar(16) not null,
    email varchar(32) null,
    age int default 3
) default charset=utf8;
```

![image-20260524095457759](./assets/image-20260524095457759.png)

> [!Note]
>
> 注意：一张表中只能有一个自增列 【自增列，一般都是主键】

- 删除表 `drop table 表名;`
  ![image-20260524095941788](./assets/image-20260524095941788.png)

- 清空表 `delete from 表名;`  或者 `truncate table 表名;`(速度快，无法回滚撤销等)

  ![image-20260524100415005](./assets/image-20260524100415005.png)

- 修改表

  - 添加列
    ```
    alter table 表名 add 列名 类型;
    alter table 表名 add 列名 类型 default 默认值;
    alter table 表名 add 列名 类型 not null default 默认值;
    alter table 表名 add 列名 类型 not null primary key auto_increment;
    ```

    ![image-20260524101327808](./assets/image-20260524101327808.png)

  - 删除列
    ```
    alter table 表名 drop column 列名;
    ```

  - 修改列 类型
    ```
    alter table 表名 modify column 列名 类型;
    ```

  - 修改列 类型 + 名称
    ```
    alter table 表名 change 原列名 新列名 新类型;
    ```

    ```
    alter table tb change id nid int not null;
    alter table tb change id id int not null default 5;
    alter table tb change id id int not null primary key auto_increment;
    alter table tb change id id int; -- 如果以前已经设置为不允许为空，有默认值，是自增，此命令：让其允许为空，删除默认值，删除自增
    ```

  - 修改列 默认值
    ```
    alter table 表名 alter 列名 set default 1000;
    ```

  - 删除列 默认值
    ```
    alter table 表名 alter 列名 drop default;
    ```

  - 添加主键
    ```
    alter table 表名 add primary key(列名);
    ```

  - 删除主键
    ```
    alter table 表名 drop primary key;
    ```

- 常见列的类型
  ```
  create table tb1(
  	id int,
      name varchar(16)
  ) default charset=utf8;
  ```

  - `int[(m)][unsigned][zerofill]`

    ![image-20260524113038891](./assets/image-20260524113038891.png)

    ```
    int              表示有符号，取值范围 -21477483648 ~ 21477483647
    int unsigned     表示无符号，取值范围 0 ~ 42954967295
    int(5)zerofill   仅用于显示，当不足 5 位时，左边补 0，例如： 00002，当有 5 位时，正常显示
    ```

    ```
    mysql> create table L1 (id int, uid int unsigned, zid int(5)zerofill)default charset=utf8;
    Query OK, 0 rows affected, 3 warnings (0.45 sec)
    
    mysql> show tables;
    +-------------------+
    | Tables_in_study01 |
    +-------------------+
    | l1                |
    | tb2               |
    | tb3               |
    | tb4               |
    +-------------------+
    4 rows in set (0.00 sec)
    
    mysql> desc l1;
    +-------+--------------------------+------+-----+---------+-------+
    | Field | Type                     | Null | Key | Default | Extra |
    +-------+--------------------------+------+-----+---------+-------+
    | id    | int                      | YES  |     | NULL    |       |
    | uid   | int unsigned             | YES  |     | NULL    |       |
    | zid   | int(5) unsigned zerofill | YES  |     | NULL    |       |
    +-------+--------------------------+------+-----+---------+-------+
    3 rows in set (0.00 sec)
    
    mysql> insert into l1 (id,uid,zid) values (-123,10,2), (0,0,20000),(12,100,1234567);
    Query OK, 3 rows affected (0.14 sec)
    Records: 3  Duplicates: 0  Warnings: 0
    
    mysql> select * from l1;
    +------+------+---------+
    | id   | uid  | zid     |
    +------+------+---------+
    | -123 |   10 |   00002 |
    |    0 |    0 |   20000 |
    |   12 |  100 | 1234567 |
    +------+------+---------+
    3 rows in set (0.00 sec)
    
    mysql>
    ```

    ![image-20260524102511478](./assets/image-20260524102511478.png)

  - `tinyint[(m)][unsigned][zerofill]`

    ```
    tinyint              表示有符号，取值范围 -128 ~ 127
    tinyint unsigned     表示无符号，取值范围 0 ~ 255
    ```

  - `bigint[(m)][unsigned][zerofill]`

    ```
    bigint              表示有符号，取值范围 -.... ~ ....
    bigint unsigned     表示无符号，取值范围 0 ~ ........
    ```

  - `decimal[(m[,d])][unsigned][zerofill]`

    ```
    精确的小数值，m是数字总个数（负号不算），d 是小数点后位数，m 最大值为 65，d 最大值为 30。
    注意：小数部分位数超过后会自动四舍五入，但是整数部分超位数后会直接报错插不进去.
    
    例如：
    create table l2(
    	id int not null primary key auto_increment,
    	salary decimal(8, 2)
    ) default charset=utf8;
    ```

    ![image-20260524103537209](./assets/image-20260524103537209.png)

    ![image-20260524103759537](./assets/image-20260524103759537.png)

  - `float[(m,d)][unsigned][zerofill]` 32 bit

    ```
    单精度浮点数，非准确小数值，m是数字总个数，d是小数点后个数.
    ```

  - `double[(m,d)][unsigned][zerofill]` 64 bit

    ```
    双精度浮点数（非准确小数值），m是数字总个数，d是小数点后个数.
    ```

  - `char(m)`

    ```
    定长字符串，m代表字符串的长度，最多可容纳255刚和字符
    
    定长的体现：即使内容长度小于m，也会占用m长度，例如：char(5),数据是 yes，底层也会 占用 5 个字符，如果超出 m 长度限制，（默认MySQL是严格模式，会报错）。
    
    	如果在配置文件中加入如下配置：
    		sql-mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
        保存并重启，此时MySQL是非严格模式，此时超过长度会自动截断（不报错）.
        
    注意：默认底层存储是固定长度（不够则用空格补齐），但是查询数据时，会自动将空白去除，如果想要保留空白，在sql-mod中加入 PAD_CHAR_TO_FULL_LENGTH 即可。
    
    查看模式sql-mode：show variables like 'sql-mode';
    
    一般适用于：固定长度的内容。
    
    例如：
    create table l3(
    	id int not null auto_increment primary key,
        name varchar(5) not null,
        depart char(3)
    ) default charset=utf8;
    ```

    ![image-20260524104715512](./assets/image-20260524104715512.png)

  - `varchar(m)`

    ```
    变长字符串，m代表字符串的长度，最多可容纳65535个字节。
    
    变长的体现：内容小于 m 时，会按照真实数据长度存储，如果超出m长度限制，（默认MySQL是严格模式，所以会报错）。
    	如果在配置中加入如下配置：
    		sql-mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
        保存并重启，此时MySQL是非严格模式，此时超过长度会自动截断（不报错）.
        
    例如：
    create table l3(
    	id int not null auto_increment primary key,
        name varchar(5) not null,
        depart char(3)
    ) default charset=utf8;
    ```

  - `text`

    ```
    text数据类型用于保存变长的大字符串，可以最多到 65535（2 ** 16 - 1）个字符
    
    一般情况下，长文本会用text类型，比如文章、新闻等。
    ```

    ```
    create table l4(
    	id int not null auto_increment primary key,
    	title varchar(128),
    	context text
    )default charset=utf8;
    ```

  - `mediumtext`

    ```
    最多可容纳16,777,215(2 ** 24 - 1)个字符
    ```

  - `longtext`

    ```
    最多可容纳4,294,967,295 or 4GB(2 ** 32 - 1) 个字符
    ```

  - `datetime`

    ```
    YYYY-MM-DD HH:MM:SS(1000-01-01 00:00:00 ~ 9999-12-31 23:59:59)
    ```

  - `timestamp`

    ```
    YYYY-MM-DD HH:MM:SS(1970-01-01 00:00:00 ~ 2037年)
    ```

    ```
    对于 timestamp，它把客户端插入的时间从当前时区转换为UTC(世界标准时间)进行存储，查询时，又将其转换为客户端当前时区进行返回。
    
    对于 datetime，不做任何改变，原样输入和输出。
    ```

    ```
    mysql> create table l5 (
        ->  id int not null auto_increment primary key,
        ->  dt datetime,
        ->  tt timestamp
        -> ) default charset=utf8;
    Query OK, 0 rows affected, 1 warning (1.00 sec)
    
    mysql> show tables;
    +-------------------+
    | Tables_in_study01 |
    +-------------------+
    | l1                |
    | l2                |
    | l5                |
    | tb2               |
    | tb3               |
    | tb4               |
    +-------------------+
    6 rows in set (0.00 sec)
    
    mysql> desc l5;
    +-------+-----------+------+-----+---------+----------------+
    | Field | Type      | Null | Key | Default | Extra          |
    +-------+-----------+------+-----+---------+----------------+
    | id    | int       | NO   | PRI | NULL    | auto_increment |
    | dt    | datetime  | YES  |     | NULL    |                |
    | tt    | timestamp | YES  |     | NULL    |                |
    +-------+-----------+------+-----+---------+----------------+
    3 rows in set (0.00 sec)
    
    mysql> insert into l5 (dt,tt) values ("2026-5-24 11:19:48", "2026-5-24 11:19:48"),("2000-01-01 00:00:00", "2000-01-01 00:00:00");
    Query OK, 2 rows affected (0.14 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    
    mysql> select * from l5;
    +----+---------------------+---------------------+
    | id | dt                  | tt                  |
    +----+---------------------+---------------------+
    |  1 | 2026-05-24 11:19:48 | 2026-05-24 11:19:48 |
    |  2 | 2000-01-01 00:00:00 | 2000-01-01 00:00:00 |
    +----+---------------------+---------------------+
    2 rows in set (0.00 sec)
    
    mysql> show variables like '%time_zone%';
    +------------------+--------+
    | Variable_name    | Value  |
    +------------------+--------+
    | system_time_zone |        |
    | time_zone        | SYSTEM |
    +------------------+--------+
    2 rows in set, 1 warning (0.00 sec)
    -- "CST" 是指MySQL所在主机的系统时间，是中国标准时间的缩写，China Standard Time UT+8:00
    
    mysql> set time_zone='+0.00';
    Query OK, 0 rows affected (0.00 sec)
    ```

    ![image-20260524112113634](./assets/image-20260524112113634.png)

  - `date`

    ```
    YYYY-MM-DD(1000-01-01 ~ 9999-12-31)
    ```

  - `time`

    ```
    HH:MM:SS('-838:59:59' ~ '838:59:59')
    ```

上述就是关于数据表的一些基本操作。

`MySQL`还有很多其他的数据类型，例如 `set`，`enum`，`TinyBlob`，`MediumBlob`，`LongBlob`等，详见官方文档：

> `MySQL`数据类型参考： [Chapter 11 Data Types](https://dev.mysql.com/doc/refman/5.7/en/data-types.html)

![image-20260524113101250](./assets/image-20260524113101250.png)

...

### 1.3.2 Python代码操作

基于python去连接MySQL以后，想要进行数据库表的管理的话，发送的指令其实都是相同的。

![image-20260524113357479](./assets/image-20260524113357479.png)

![image-20260524113659346](./assets/image-20260524113659346.png)

## 1.4 数据行管理

当数据库和数据表创建完成后，就需要对数据表中的内容进行增删改查了。

![image-20260524093200604](./assets/image-20260524093200604.png)

### 1.4.1 内置客户端操作

下面的命令需要记住！！！

数据行操作的相关`SQL`语句（指令）如下：

- 新增数据
  ```sql
  insert into 表名 (列名, 列名, 列名) values (对应的值, 对应的值, 对应的值);
  ```

  ```sql
  insert into tb1 (name, password) values ('jack', '123456');
  insert into tb1 (name, password) values ('jack', '123456'),('rose', '654321');
  insert into tb1 values ('jack', '123456'),('rose', '654321'); -- 如果数据表只有两列
  ```

- 删除数据
  ```sql
  delete from 表名; -- 删除表里的所有数据，但是不删除表
  delete from 表名 where 条件;
  ```

  ```sql
  delete from tb1; -- 删除表里的所有数据，但是不删除表
  delete from tb1 where name="jack";
  delete from tb1 where name="jack" and password="123456";
  delete from tb1 where id>9;
  ```

- 修改数据
  ```sql
  update 表名 set 列名=值;
  update 表名 set 列名=值 where 条件;
  ```

  ```sql
  update tb1 set name="Jordan";
  update tb1 set name="Jordan" where id=1;
  update tb1 set age=age+1 where id=2;  -- 整形
  update users set name=concat(name, "123") where id=2; -- concat，一个函数，用于拼接字符串
  ```

- 查询数据
  ```
  select * from 表名; -- 查询表中所有数据
  select 列名,列名 from 表名;
  select 列名,列名 as 别名,别名 from 表名; // 别名是查询出来的表头显示啥样
  select * from 表名 where 条件;
  ```

  ```
  select * from tb1;
  select id,name,age from tb1;
  select name,age as n,a from tb1;
  select name,age as n,a 111 from tb1;
  
  select * from tb1 where id=1;
  select * from tb1 where id>1;
  select * from tb1 where id!=1;
  select * from tb1 where id=1 and name="jack";
  ```

### 1.4.2 Python代码操作

![image-20260524093200604](./assets/image-20260524093200604.png)

![image-20260524123047690](./assets/image-20260524123047690.png)

真正在做项目开发时，流程如下：

- 第一步：根据项目的功能设计相应的数据库和表结构（不会经常变动，在项目设计之初就确定好了）
- 第二步：操作表结构中 的数据，以达到实现业务逻辑的目的

例如：实现一个用户管理系统

先使用MySQL自带的客户端创建香瓜数据库和表结构（相当于先创建好Excel结构）

```
create database userdb default charset utf8 collate utf8_general_ci;
```

```sql
create table users(
	id int not null auto_increment primary key,
    name varchar(16),
    password varchar(16)
)default charset=utf8;
```

再在程序中执行编写相应的功能实现 注册、登录等功能。

```python
import pymysql


def register():
    user = input('请输入用户名')
    password = input('请输入密码')

    # 连接指定数据库
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        charset="utf8",
        database='userdb'
    )
    cursor = conn.cursor()

    # 执行SQL语句（有SQL注入风险，稍后讲解）
    sql = 'insert into users (name, password) values ("{}", "{}")'.format(user, password)
    cursor.execute(sql)
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()
	

def login():
    user = input('请输入用户名')
    password = input('请输入密码')

    # 连接指定数据库
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        charset="utf8",
        database='userdb'
    )
    cursor = conn.cursor()

    # 查询
    sql = 'select * from users where name="{}" and password="{}"'.format(user, password)
    cursor.execute(sql)
    
    result = cursor.fetchone()  # 如果没查到返回None 如果查到了，只返回第一条数据(1, 'jack', '123456')
    # result = cursor.fetchall()
    # print(result, type(result))  # 查到了：((1, 'jack', '123456'), ...) <class 'tuple'> 没查到：返回None
    
    # 关闭数据库连接
    cursor.close()
    conn.close()
    
    if result:
        print('登录成功')
    else:
        print('用户名或密码错误!')


def run():
    choice = input('1. 注册 2. 登录')
    if choice == '1':
        register()
    elif choice == '2':
        login()
    else:
        print('输入错误, 程序终止！')


if __name__ == '__main__':
    run()

```

```python
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| study01            |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> create database userdb default charset utf8 collate utf8_general_ci;
Query OK, 1 row affected, 2 warnings (0.15 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| study01            |
| sys                |
| userdb             |
+--------------------+
6 rows in set (0.00 sec)

mysql> use userdb;
Database changed
mysql> show tables;
Empty set (0.00 sec)

mysql> create table users(
    ->  id int not null auto_increment primary key,
    ->     name varchar(16),
    ->     password varchar(16)
    -> )default charset=utf8;
Query OK, 0 rows affected, 1 warning (0.58 sec)

mysql> show tables;
+------------------+
| Tables_in_userdb |
+------------------+
| users            |
+------------------+
1 row in set (0.00 sec)

mysql> select * from users;
Empty set (0.00 sec)

mysql> select * from users;
Empty set (0.00 sec)

mysql> select * from users;
Empty set (0.00 sec)

mysql> select * from users;
+----+------+----------+
| id | name | password |
+----+------+----------+
|  1 | jack | 123456   |
+----+------+----------+
1 row in set (0.00 sec)

mysql> select * from users;
+----+------+----------+
| id | name | password |
+----+------+----------+
|  1 | jack | 123456   |
|  2 | rose | 654321   |
+----+------+----------+
2 rows in set (0.00 sec)

mysql>
```

在项目开发时，数据库建库和数据表建表的操作只需做一次，最最常写的还是对数据行的操作。

## 1.5 关于SQL注入

加入你开发了一个用户认证系统，应该用户登录成功才能正确的返回相应的用户结果。

```python
user = input('请输入用户名')
password = input('请输入密码')

# 连接指定数据库
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    charset="utf8",
    database='userdb'
)
cursor = conn.cursor()

# 查询
sql = "select * from users where name='{}' and password='{}'".format(user, password)
cursor.execute(sql)

result = cursor.fetchone()  # 如果没查到返回None 如果查到了，只返回第一条数据(1, 'jack', '123456')
# result = cursor.fetchall()
# print(result, type(result))  # 查到了：((1, 'jack', '123456'), ...) <class 'tuple'> 没查到：返回None

# 关闭数据库连接
cursor.close()
conn.close()

if result:
    print('登录成功')
else:
    print('用户名或密码错误!')
```

> [!Warning] 
>
> ⚠️ 如果此时用户输入 `" or 1=1 -- `，这样即使用户输入的密码不正确，也可以通过验证
>
> 因为在SQL拼接时，拼接后的结果为：
>
> ```python
> select * from users where name='' or 1=1 -- ' and password="随便输的密码"
> ```
>
> 注意：在MySQL中，`--` 表示注释
>
> ![image-20260524131701977](./assets/image-20260524131701977.png)
>
> ![image-20260524131841185](./assets/image-20260524131841185.png)

那么如何在python开发中避免`SQL`注入呢？

> [!Important]
>
> ⚠️ 切记：`SQL`语句不要在使用`Python`中的字符串格式化，而是使用`pymysql`的`execute`方法.
>
> ```python
> user = input('请输入用户名')
> password = input('请输入密码')
> 
> # 连接指定数据库
> conn = pymysql.connect(
>     host='127.0.0.1',
>     port=3306,
>     user='root',
>     password='123456',
>     charset="utf8",
>     database='userdb'
> )
> cursor = conn.cursor()
> 
> # 查询
> sql = "select * from users where name=%s and password=%s"
> cursor.execute(sql, (name, password))
> 
> result = cursor.fetchone()  # 如果没查到返回None 如果查到了，只返回第一条数据(1, 'jack', '123456')
> # result = cursor.fetchall()
> # print(result, type(result))  # 查到了：((1, 'jack', '123456'), ...) <class 'tuple'> 没查到：返回None
> 
> # 关闭数据库连接
> cursor.close()
> conn.close()
> 
> if result:
>     print('登录成功')
> else:
>     print('用户名或密码错误!')
> ```
>
> ![image-20260524132828359](./assets/image-20260524132828359.png)![image-20260524132852550](./assets/image-20260524132852550.png)

## 1.6 总结

![image-20260524133058720](./assets/image-20260524133058720.png)









































































