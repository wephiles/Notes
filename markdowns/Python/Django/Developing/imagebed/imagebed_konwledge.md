# 1. 关于DRF 中的 序列化 -- 简单理解

### 一、 序列化器是怎么用的？有哪些特性？有什么作用？

**1. 怎么用？**
通常在应用的 `serializers.py` 中定义一个类，继承自 `Serializer` 或 `ModelSerializer`，然后在视图中引入并实例化：

- **序列化（查）：** 将模型对象或 QuerySet 转换为 JSON 等格式。`serializer = MySerializer(instance=obj)`
- **反序列化（改/增）：** 将前端传来的 JSON 转换为 Python 字典，并校验、保存。`serializer = MySerializer(data=request.data)`

**2. 特性：**

- **数据转换：** 复杂的数据库模型对象 <-> 简单的字典/JSON。
- **强大的校验能力：** 类似于 Django 的 Form，可以自动校验字段类型、必填项，并支持自定义校验。
- **错误处理：** 校验失败时，自动聚合并返回友好的错误信息（如 `{"password": ["密码不能少于8位"]}`）。
- **嵌套关系：** 轻松处理外键、多对多关系的序列化输出。

**3. 写了序列化器有什么作用？**

- **解耦：** 将数据校验、数据结构定义从视图中剥离，视图只负责业务逻辑流转，代码更清晰。
- **安全保障：** 充当模型和前端之间的“防火墙”，防止前端恶意提交不该修改的字段（如 `is_superuser`）。

### 二、 序列化器中的类变量(字段)有啥用？类型必须和 Model 一致吗？写 Model 没有的字段会怎样？

**1. 类变量(字段)的作用：**
定义了前端可以交互的数据结构，以及这些数据应该符合什么格式（如字符串最大长度、整数最小值等）。

**2. 类型必须和 Model 一模一样吗？**
**不需要。** 它们只是“逻辑上”需要兼容。

- Model 里的 `CharField`，在序列化器里可以写成 `CharField`，也可以写成 `ChoiceField`（限制输入选项），甚至 `EmailField`（进一步收紧格式）。
- Model 里的 `DateTimeField`，序列化器里可以写成 `DateField`（前端只需要日期，不需要时间）。

**3. 写了一个 Model 中没有的字段，会发生什么？有什么作用？**
这叫做**虚拟字段**，非常有用！

- **序列化时（返回给前端）：** 通常配合 `SerializerMethodField` 使用，用于返回计算出来的数据。例如 Model 里只有 `birthday`，你可以写一个 `age` 字段返回计算后的年龄。
- **反序列化时（前端传过来）：** 例如注册时，Model 里只有 `password`，但你可以写一个 `password2` 字段接收前端的“确认密码”。这个字段不进数据库，但可以在校验阶段用来和 `password` 比对，比对完就丢弃了。
- *注意：如果不加特殊处理（如 `write_only=True`），反序列化时传入 Model 没有的字段会导致校验报错（抛出 `unknown field` 异常）。*

### 三、 create 和 update 方法的作用及参数

**1. 作用：**
这两个方法是真正与数据库打交道的。当调用 `serializer.save()` 时，DRF 会根据实例化时是否传入了 `instance` 参数，自动决定调用 `create` 还是 `update`。

**2. 参数解析：**

- `validated_data`：**是一个 Python 字典**。它包含了经过所有校验规则清洗后、绝对合法的数据。你从这里面取值去入库是 100% 安全的。
- `instance`：**是一个 ORM 模型对象**（仅在 `update` 方法中存在）。代表当前要修改的是数据库里的哪一条具体记录。

**3. 必须手动重写吗？不重写会怎样？**

- **如果你用 `ModelSerializer`：不需要。** DRF 会自动根据 `Meta.model` 帮你实现这两个方法，直接调用 `Model.objects.create()` 和 `obj.save()`。
- **如果你用普通的 `Serializer`：必须重写。** 不重写的话，调用 `save()` 会直接抛出 `NotImplementedError` 异常。因为 DRF 不知道你要把数据存到哪个表、怎么存（可能存 Redis、可能调外部 API）。

### 四、 save 方法有什么作用？什么时候需要重写？

**1. 作用：**
`save()` 是一个入口方法。它的内部逻辑大致是：

1. 检查数据是否已经校验过（没校验会自动调 `is_valid()`）。
2. 判断实例化时有没有传 `instance`（有就调 `update()`，无就调 `create()`）。
3. 将额外的关键字参数注入到 `validated_data` 中，一并传给 `create` 或 `update`。

**2. 什么样的情况下需要重写 save 方法？**
**极少需要重写。** DRF 的官方设计原则是把数据库操作放在 `create` 和 `update` 里。
但在某些特殊场景下会重写，例如：在保存前后需要执行一些**跨越增/改**的共享逻辑，比如无论新增还是修改，都需要记录操作日志，或者需要在保存前动态向 `validated_data` 塞入当前请求的用户信息（其实这步在视图层 `serializer.save(owner=request.user)` 更好，但有人喜欢写在序列化器里）。

### 五、 validate_<字段> 方法的作用及参数

**1. 作用：**
用于对**单个特定字段**进行自定义校验。方法名必须严格遵循 `validate_字段名` 的格式。如果校验失败，抛出 `serializers.ValidationError`，错误信息会绑定在这个字段上。

**2. 参数 `value` 是什么？**
`value` 是**前端传过来的该字段的单个原始值**（可能是字符串、整数、列表等）。它已经经过了字段类型的初步校验（比如你定义了 `IntegerField`，那 `value` 到这里肯定是个合法整数，不会是字母），但还没经过这里的业务逻辑校验。

### 六、 validate 方法的作用及参数

**1. 作用：**
用于**对象级别（多字段联合）**的校验。当需要同时对比多个字段的值时使用。

**2. 参数代表什么？是什么类型？**
参数通常命名为 `attrs`（或 `data`），它是一个 **Python 字典**。包含了所有单字段校验通过后的数据（包括 Model 里没有的虚拟字段）。
*例如：注册时校验“密码”和“确认密码”是否一致，就必须在这里取 `attrs.get('password')` 和 `attrs.get('password2')` 进行对比。*
*注意：该方法必须返回清洗后的 `attrs` 字典。*

### 七、 Meta 类有什么用？还能写什么？前端效果如何？

**1. 作用：**
`Meta` 是配置类，专门用来给 `ModelSerializer` 提供元数据，告诉 DRF 怎么自动生成字段和方法。

**2. 除了 model、fields、read_only_fields 还能写什么？**

- `exclude = ('id',)`：与 `fields` 互斥，指定排除哪些字段，剩下的全要。
- `extra_kwargs`：**非常重要！** 用于给自动生成的字段追加或覆盖属性。
  - 例如：`{'password': {'write_only': True, 'min_length': 8}}`
- `depth = 1`：控制外键关联对象的嵌套深度。写了 `depth=1`，外键字段就不会只返回一个 ID，而是会把关联表的数据全查出来嵌套返回。
- `validators`：附加模型级别的校验器（通常是 `UniqueTogetherValidator` 等确保联合唯一的校验器）。

**3. 前端效果/数据改变：**

- **`read_only_fields = ('created_time',)`**：前端 POST 提交时，就算传了 `created_time` 也会被自动丢弃（防止伪造创建时间）；GET 请求时正常返回该字段。
- **`extra_kwargs` 里写 `write_only: True`**：前端 GET 请求时，JSON 里绝对不会出现这个字段（最常用于密码，防止被抓包泄露）；但前端 POST 时必须传。
- **`depth = 1`**：前端拿到的数据从扁平的 `{"author_id": 1}` 变成了有层级的 `{"author": {"id": 1, "name": "张三"}}`。

### 八、 ModelSerializer 和 Serializer 的区别？

这是选型的核心，区别如下：



| 维度              | Serializer (基础序列化器)                                    | ModelSerializer (模型序列化器)                               |
| :---------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **字段生成**      | 完全手动一个个写。                                           | 根据 `Meta.model` 自动推断并生成对应字段。                   |
| **create/update** | **必须**手动重写 `create` 和 `update` 方法。                 | 自动实现，直接调 `save()` 就能入库。                         |
| **Model校验**     | 不包含模型层的校验（如 `blank=True`, `null=True` 的约束需要自己写）。 | 自动将 Model 字段上的约束（如 `max_length`, `unique`）转化为序列化器的校验规则。 |
| **使用场景**      | **非数据库场景**（如调用第三方API、组合多个Model的数据返回）、**极其复杂的自定义入库逻辑**（如一次请求保存多张表）。 | **标准的单表 CRUD**、90% 的日常业务开发。                    |

**总结建议：**
日常开发中，**优先使用 `ModelSerializer`**，能省去大量样板代码。只有当你的数据根本不对应某个具体的数据库表，或者保存逻辑极其特殊（比如一个接口要同时创建用户、创建角色、还要发邮件，走不到默认的 `Model.objects.create`），才去使用基础的 `Serializer`。

# 2. DRF中的序列化 通俗易懂理解

在Django REST Framework (DRF) 中，**序列化器** 是最核心的组件之一。为了让你彻底理解，我们用一个**“开发一个用户注册和发文章功能”**的通俗例子来贯穿全文。

### 一、 序列化器是怎么用的？有哪些特性？有什么作用？

**通俗理解：**
数据库里存的是Python对象（比如一个User对象），但前端只认JSON格式（比如 `{"username": "张三"}`）。序列化器就是**“翻译官”**。

- **怎么用？**
  1. 定义一个类继承自 `serializers.Serializer` 或 `serializers.ModelSerializer`。
  2. 在里面写字段。
  3. 在视图 中把对象传给它：`serializer = UserSerializer(user)` -> 变成JSON（序列化）。
  4. 把前端传来的JSON传给它：`serializer = UserSerializer(data=request.data)` -> 变成Python对象并存入数据库（反序列化）。
- **特性：**
  1. 数据转换（JSON <-> Python对象）。
  2. **强大的数据校验**（自动帮你检查必填项、字段类型、长度等，省去大量手写 `if else`）。
- **作用：**
  解耦！如果不写序列化器，你需要在视图里写几十行代码来提取JSON、校验数据、创建模型。有了它，视图里只需要一句话：`serializer.save()`。

### 二、 序列化器中的类变量（字段）有啥用？类型必须和Model一样吗？写了Model中没有的字段会怎样？

**1. 有啥用？**
字段相当于给“翻译官”制定了**词汇表**。你声明了什么字段，前端就能提交什么字段，也能看到什么字段。没声明的字段，前端既不能传，也看不到（默认情况下）。

**2. 类型必须和Model一模一样吗？**
**不需要！** 虽然通常是对应的（Model里是`CharField`，Serializer里也是`CharField`），但你可以灵活改变。
*例子：* Model里存的是 `DateTimeField`（包含具体时分秒），但前端只需要显示日期，你可以写成 `serializers.DateField()`。

**3. 写了Model中没有的字段，会发生什么？有什么作用？**
**不会报错，反而非常实用！** 这种字段叫“附加字段”，通常用于：

- **仅用于接收前端数据（不存数据库）：** 比如注册时的“确认密码”字段。
- **仅用于返回给前端（不存数据库）：** 比如计算出来的字段。

**代码举例：**

python

复制

```
class UserRegisterSerializer(serializers.Serializer):
    # Model中有的字段
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    # Model中没有的字段1：确认密码（只用来接收前端数据，校验完后不存库）
    password2 = serializers.CharField(max_length=20, write_only=True) 

    # Model中没有的字段2：是否是VIP（只用来返回给前端，是从其他地方算出来的）
    is_vip = serializers.BooleanField(read_only=True) 
```

*效果：前端提交时必须带 `password2`，但数据库不会有这个字段；前端获取数据时能看到 `is_vip`，但提交时不需要（也提交不了）传它。*

### 三、 create 和 update 方法有什么作用？参数是什么？必须手动重写吗？

**1. 作用：**
当调用 `serializer.save()` 时，底层其实就是在调用 `create()` 或 `update()` 方法。它们的作用是**真正地把数据写入数据库**。

**2. 参数是什么对象？**

- `validated_data`：是一个**字典**。里面装的是经过序列化器各种校验通过后的、干干净净的数据。比如：`{"username": "jack", "password": "123"}`。
- `instance`：是一个**Model对象实例**。它**只存在于 update 方法中**，代表“数据库里那条正在被修改的旧数据”。

**3. 必须手动重写吗？**

- 如果你继承的是 **`Serializer`**：**必须重写！** 否则调用 `save()` 会直接报错。因为你没告诉它怎么存数据。
- 如果你继承的是 **`ModelSerializer`**：**不需要重写！** 它会自动根据 `Meta` 里写的模型，帮你生成 `create` 和 `update` 代码。

**什么时候需要在 ModelSerializer 中重写它们？**
当默认的保存逻辑满足不了你时。
*例子：创建用户时，密码不能明文存入数据库，必须调用 `User.objects.create_user()` 来加密密码。*

python

复制

```
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # 重写create，因为默认的save()是明文存密码
    def create(self, validated_data):
        # validated_data 此时是一个字典 {'username':'jack', 'password':'123'}
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
```

### 四、 save 方法有什么作用？什么情况下需要重写？

**1. 作用：**
`save()` 是触发保存动作的“开关”。如果序列化器初始化时传了 `instance`，它就调 `update()`；没传 `instance`，它就调 `create()`。

**2. 什么情况下需要重写？**
当你需要**在保存前后，偷偷塞一些额外数据**时。
*例子：发布文章时，前端不需要（也不安全）传“作者是谁”，作者应该从登录态中自动获取。*

python

复制

```
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']

    # 重写save方法，强行把 request.user 塞进数据里
    def save(self, **kwargs):
        # self.context['request'] 是视图通过 context 传进来的 request 对象
        user = self.context['request'].user 
        # 把作者塞入 validated_data
        self.validated_data['author'] = user 
        # 继续执行真正的保存
        return super().save(**kwargs) 
```

### 五、 validate_字段 方法的作用是什么？参数 value 是什么？

**1. 作用：**
用于**单个字段级别的校验**。方法名必须固定格式：`validate_字段名`。

**2. 参数 value 是什么？**
`value` 是前端传过来的**该字段的原始值**（已经是Python类型，比如字符串、整数）。

**例子：校验用户名不能包含敏感词。**

python

复制

```
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        # value 就是前端传过来的用户名字符串，比如 "傻逼123"
        if '傻逼' in value:
            # 校验失败必须抛出 ValidationError，前端会收到错误提示
            raise serializers.ValidationError("用户名包含敏感词汇，请重试！")
        # 校验成功必须返回 value
        return value
```

### 六、 validate 方法有什么作用？参数代表什么？是什么类型？

**1. 作用：**
用于**全局/跨字段级别的校验**。当需要同时对比两个或多个字段时使用。

**2. 参数是什么类型？**
参数通常命名为 `attrs`（也可以叫 `data`），它是一个**字典**，里面包含了前面所有 `validate_字段` 校验通过后的数据。

**例子：注册时校验“密码”和“确认密码”必须一致。**

python

复制

```
class UserRegisterSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        # attrs 是一个字典: {'password': '123', 'password2': '456'}
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password2": "两次密码不一致！"})
        
        # 如果不一致，后面就不执行了。如果一致，把多余的确认密码删掉，免得影响存库
        attrs.pop('password2') 
        return attrs
```

### 七、 Meta类有什么用？还能写什么？前端效果是什么？

**1. 作用：**
`Meta` 是“元数据类”，专门用来给 `ModelSerializer` 提供配置信息，告诉它怎么跟数据库模型打交道。

**2. 除了基础三个，还能写什么？**

- `exclude = ('id',)`：排除哪些字段（和 `fields` 二选一）。
- **`extra_kwargs`（工业开发极常用）**：在不重新声明字段的前提下，给字段加属性。
- `validators`：添加模型级别的校验器。
- `read_only_fields` 的进阶用法。

**3. 代码举例与前端效果：**

python

复制

```
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'views', 'created_at']
        read_only_fields = ['views', 'created_at'] # 这俩只读
        
        # extra_kwargs 深度定制
        extra_kwargs = {
            'title': {
                'min_length': 2,
                'error_messages': {
                    'min_length': '标题太短了，至少2个字！' # 改变前端收到的错误提示语
                }
            },
            'content': {
                'write_only': True  # 前端提交时必须传，但返回列表时不给前端看（防爬虫）
            }
        }
```

![img](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAPLSURBVHgBzZi/UxNBFMffW35EIZGkQLlIQQpsQfwDiDXqYAcMhRboUCEz0gL5A5RQMQIzYiNY0UjHDNgLgy0UxBmGY0KRSE4U8Hbdd5BALpdkE0KST5Pc7dvZ773dffv2IRSJfpgICuCdwLEbQHQCohcEeK1GhLgQIoKAEQHiB2NsXWv2rEMRYCHGu7vCe8ttjMjB36TEqBMRCOvMrAtp2u2IaiclgSTM1WhMAAkrAVLogqrQvAIPosYIBz5ZhMfyEeEIoda7dxZyGeUUuB9NTJXKa1lhGPY3e0azNTsKPJ/SxLL0WhDKgNxIW6fH/HEg4Ivb25hTh/oGY61c4gi52ztdjTXLTm0ZAmlakcJGuZEO2T+US8pG2hTvRY9eMAEfoZIIMepvaQonH1MCdf1Pm2Bna/JvG1SW+MmxGUiux8sprjmbgMqLI7wud+1E8sHy4IX3dqGKkF70kRdrrSfynlDvvLG5AYtLX2B7exv2dd16t7a6Ch6PJ8M2kUhI2yXZZxO2d3as56c9PTAxPp5zjPoGRvF30hIoCggp76amrAHtGAkjQyAJejs2lvqIQpChZ4QEMl1PBEFx7c3OzTmKc0KXoooVd4GXMqZazngQFXIGmpqvKysZ7x91dYFf08Dtcae9/y6n1C6OPPxETm+wuxtUECbvrJXiOlSMNxwGfNDeDh9mZhzt7Z6mjyBbTf6qIrdFUIYZbFMxpg1hJ5cn7PYkrBBxBCJ2MEDRpmKsO6ylbAPScigRXnadPO99OAwDg4PW5rmKYRgZtrREnvX2wuvhYcePzS7wGpCnKJTMzs8reY3WMAn9vLgIqjC64EAJoDiobGso28Zpiksi8EZAEaEp3oIqRXD4KT0ovkG1grDFULCq9SBd+JmmyRu/wkZxO2Qq6e2XR53b7c5tm6f9HBGhaoQVZoQppvOZD/T1WceVHTpfXw0NpWUyyXdO0PE40N8PeeUhrtOvlSXsxmJe12lNDKoI5GZA03zWLoaAzxfnIr8XywWVRkgc/U+dJGcuWd7AaoiJMvaZZij5lBJIXoR/IgQVhnMMJb1HpJ3Ffn9TuJJTTWO3aunFJMdUej96VNbSB0H1mfv3mh7a3ztmMyd15nPZpXwBXBY2qXjk3JSDvYNfYYbW7erGsKa1pSlriS9nPkgdkcNL2llQalDEqQ6TSxyRN2HV5KJFTu4Xn6BEkNdOfvPA1SJRNgoqout6TJZI2KT826162bocScSFCdOnf3nYqVCZtRsUCV34L+7U8toqL14oL/8CvUkx54kwblE6RxmTlZQUwX9+F568K5L+eAAAAABJRU5ErkJggg==)

引用

- **前端数据改变效果：**
  - 当前端提交标题为 `"A"` 时，不会收到默认的英文报错，而是收到 `"标题太短了，至少2个字！"`。
  - 当前端请求文章列表时，返回的JSON里**没有** `content` 字段（因为 `write_only`），保护了数据不被随意抓取。
  - 当前端尝试提交 `views=999` 时，后端会直接忽略这个值（因为 `read_only`），防止恶意刷阅读量。

### 八、 ModelSerializer 和 Serializer 的区别？怎么选？



| 维度         | `Serializer` (基础序列化器)           | `ModelSerializer` (模型序列化器)                            |
| :----------- | :------------------------------------ | :---------------------------------------------------------- |
| **字段定义** | 必须手动一个个写                      | 根据 `Meta.model` 自动生成                                  |
| **校验规则** | 只能手动写 `validate` 等              | 自动继承 Model 里的规则（如 `blank`, `null`, `max_length`） |
| **保存逻辑** | **必须**手动重写 `create` 和 `update` | **自动拥有** `create` 和 `update`                           |
| **灵活性**   | 极高，完全白纸一张                    | 较高，但在 Model 绑定上有些隐式魔法                         |

**什么时候用 `Serializer`？（30%场景）**

1. **不与数据库直接交互的接口：** 比如登录接口（只校验账号密码，返回Token，不需要创建Model）、发送短信验证码接口。
2. **聚合数据的接口：** 比如首页仪表盘，返回的数据是从 `User`、`Article`、`Comment` 三个表里查出来拼在一起的，没有一个单独的 Model 对应它。
3. **极其复杂的自定义逻辑：** 当使用 `ModelSerializer` 的 `extra_kwargs` 和重写方法让你觉得代码变得混乱、难以维护时，退回 `Serializer` 全部手写反而更清晰。

**什么时候用 `ModelSerializer`？（70%场景）**
**标准的增删改查（CRUD）！** 只要是针对某一张表的直接操作（比如文章的发布、修改、列表展示、详情），无脑用 `ModelSerializer`。它能帮你省去至少 50% 的样板代码，是工业开发中提升效率的神器。

**总结口诀：**
有表对应增删改查，用 `ModelSerializer`；
无表对应或者逻辑奇葩，用 `Serializer`。

# 3. 关于序列化器类的补充

### 一、 如果要设计一个仪表盘，从 User、Article、Comment 查数据，怎么实现？

**核心思路：放弃 `ModelSerializer`，使用原生 `Serializer`！**

因为仪表盘返回的数据（比如：总用户数100、总文章数500、总评论数2000）**在数据库里并没有一张对应的“仪表盘表”**。`ModelSerializer` 是必须绑定 Model 的，所以这里只能用白纸一张的 `Serializer`。

在工业开发中，处理这种聚合数据通常有**两种流派**，我推荐第一种（职责分离原则）：

#### 推荐流派：在视图 里查好数据，序列化器只管“排版”

让视图负责去数据库跑SQL查数字，然后把算好的字典丢给序列化器，序列化器只负责定义前端长什么样。

python

复制

```
# serializers.py
from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    # 仪表盘不需要存数据库，只需要返回给前端，所以全加上 read_only=True
    total_users = serializers.IntegerField(help_text="总用户数")
    total_articles = serializers.IntegerField(help_text="总文章数")
    total_comments = serializers.IntegerField(help_text="总评论数")
    # 甚至可以加个非数据库的衍生字段
    activity_rate = serializers.FloatField(help_text="活跃率(%)")

# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from myapp.models import Article, Comment

@api_view(['GET'])
def get_dashboard(request):
    # 1. 视图层去各个表里查数据 (工业中会用 Django 的 annotate 或缓存来优化性能)
    data = {
        "total_users": User.objects.count(),
        "total_articles": Article.objects.count(),
        "total_comments": Comment.objects.count(),
        "activity_rate": 85.5 # 假设这是算出来的
    }
    
    # 2. 把字典传给序列化器
    serializer = DashboardSerializer(data)
    
    # 3. 返回 (注意：这里不需要调用 is_valid()，因为我们不是在接收前端数据，只是在做纯序列化输出)
    return Response(serializer.data)
```

**前端收到的JSON：**

json

复制

```
{
    "total_users": 100,
    "total_articles": 500,
    "total_comments": 2000,
    "activity_rate": 85.5
}
```

### 二、 序列化器类中的 `self.xxx` 属性大揭秘

在序列化器的方法（如 `validate`、`create`）中，`self` 绑定了非常多有用的属性。

#### 1. `self.context` (上下文字典)

- **是什么对象：** 一个普通的 Python 字典 (`dict`)。
- **有什么用：** **“走私通道”**。序列化器本来只负责处理数据字段，但有时候在 `create` 或 `validate` 里需要知道“当前是谁在请求”、“当前是哪个视图”，这些信息不能通过前端数据传，只能通过 `context` 偷偷运进来。
- **怎么用：**
  - 在视图里塞进去：`serializer = ArticleSerializer(data=request.data, context={'request': request})`
  - 在序列化器里拿出来：`request = self.context.get('request')`
- **经典场景：** 前端提交文章，不传作者ID，后端在 `create` 里通过 `self.context['request'].user` 自动拿到当前登录用户，存为作者。

#### 2. `self.validated_data` (干净的数据字典)

- **是什么对象：** 一个普通的 Python 字典 (`dict`)。
- **有什么用：** 保存**所有校验都通过后**的最终数据。前端传来的脏数据、多余的字段，在这里都被洗掉了或处理好了。
- **怎么用：** 只能在 `create(self, validated_data)` 和 `update(self, instance, validated_data)` 里使用。**注意：** 在 `validate` 方法执行期间，它还不存在！
- **经典场景：** `user = User.objects.create_user(**self.validated_data)` 直接把字典炸开存库。

#### 3. `self.instance` (数据库旧对象实例)

- **是什么对象：** 一个 Django Model 实例对象（比如 `<User: admin>`），或者是 `None`。
- **有什么用：** 序列化器的“分水岭”。它决定了你调用 `save()` 时，底层是走 `create()` 还是 `update()`。
  - 如果 `self.instance is None` -> 说明是新增，`save()` 调用 `create()`。
  - 如果 `self.instance` 有值 -> 说明是修改，`save()` 调用 `update()`。
- **怎么用：** 在 `update` 方法中使用。

python

复制

```
    def update(self, instance, validated_data):
        # 这里的 instance 其实就是 self.instance
        # validated_data 是前端传来的新数据
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
```

![img](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAPLSURBVHgBzZi/UxNBFMffW35EIZGkQLlIQQpsQfwDiDXqYAcMhRboUCEz0gL5A5RQMQIzYiNY0UjHDNgLgy0UxBmGY0KRSE4U8Hbdd5BALpdkE0KST5Pc7dvZ773dffv2IRSJfpgICuCdwLEbQHQCohcEeK1GhLgQIoKAEQHiB2NsXWv2rEMRYCHGu7vCe8ttjMjB36TEqBMRCOvMrAtp2u2IaiclgSTM1WhMAAkrAVLogqrQvAIPosYIBz5ZhMfyEeEIoda7dxZyGeUUuB9NTJXKa1lhGPY3e0azNTsKPJ/SxLL0WhDKgNxIW6fH/HEg4Ivb25hTh/oGY61c4gi52ztdjTXLTm0ZAmlakcJGuZEO2T+US8pG2hTvRY9eMAEfoZIIMepvaQonH1MCdf1Pm2Bna/JvG1SW+MmxGUiux8sprjmbgMqLI7wud+1E8sHy4IX3dqGKkF70kRdrrSfynlDvvLG5AYtLX2B7exv2dd16t7a6Ch6PJ8M2kUhI2yXZZxO2d3as56c9PTAxPp5zjPoGRvF30hIoCggp76amrAHtGAkjQyAJejs2lvqIQpChZ4QEMl1PBEFx7c3OzTmKc0KXoooVd4GXMqZazngQFXIGmpqvKysZ7x91dYFf08Dtcae9/y6n1C6OPPxETm+wuxtUECbvrJXiOlSMNxwGfNDeDh9mZhzt7Z6mjyBbTf6qIrdFUIYZbFMxpg1hJ5cn7PYkrBBxBCJ2MEDRpmKsO6ylbAPScigRXnadPO99OAwDg4PW5rmKYRgZtrREnvX2wuvhYcePzS7wGpCnKJTMzs8reY3WMAn9vLgIqjC64EAJoDiobGso28Zpiksi8EZAEaEp3oIqRXD4KT0ovkG1grDFULCq9SBd+JmmyRu/wkZxO2Qq6e2XR53b7c5tm6f9HBGhaoQVZoQppvOZD/T1WceVHTpfXw0NpWUyyXdO0PE40N8PeeUhrtOvlSXsxmJe12lNDKoI5GZA03zWLoaAzxfnIr8XywWVRkgc/U+dJGcuWd7AaoiJMvaZZij5lBJIXoR/IgQVhnMMJb1HpJ3Ffn9TuJJTTWO3aunFJMdUej96VNbSB0H1mfv3mh7a3ztmMyd15nPZpXwBXBY2qXjk3JSDvYNfYYbW7erGsKa1pSlriS9nPkgdkcNL2llQalDEqQ6TSxyRN2HV5KJFTu4Xn6BEkNdOfvPA1SJRNgoqout6TJZI2KT826162bocScSFCdOnf3nYqVCZtRsUCV34L+7U8toqL14oL/8CvUkx54kwblE6RxmTlZQUwX9+F568K5L+eAAAAABJRU5ErkJggg==)

引用

#### 4. 其他非常有用的隐藏属性：

- **`self.initial_data`：** 前端传过来的**最原始、未经过任何校验**的字典（相当于 `request.data`）。只在反序列化（有 `data=` 参数）时存在。有时你在 `validate` 里想看看前端原始传了什么脏东西，就看它。
- **`self.fields`：** 一个有序字典，包含了当前序列化器里定义的所有字段对象。**高级用法：** 动态修改字段（比如根据用户权限，在 `__init__` 里把某个字段设为 `read_only`）。
- **`self.errors`：** 调用 `is_valid()` 后，如果失败，错误信息就存在这里。

### 三、 序列化器 vs Django的 Form / ModelForm

很多初学者觉得这俩东西长得太像了（都有 `CharField`，都有 `validate`），其实它们的**出身和核心目标完全不同**。

#### 1. 本质区别：单向 vs 双向

- **Django Form 是“单向”的（只进不出）：** 它的职责是把前端提交的表单数据（`request.POST`）**转换并校验**成 Python 字典。它**绝对不负责**把模型转换成 JSON 返回给前端。返回渲染好的 HTML 是 Template（模板）干的。
- **DRF 序列化器是“双向”的（能进能出）：**
  - 进：把 JSON 转成 Python 字典并校验（反序列化）。
  - 出：把 Python 模型对象转成 JSON（序列化）。

#### 2. 应用场景区别

- **Form / ModelForm：** 用于**传统的服务端渲染网页**。比如你用 Django 模板写一个后台管理系统，点击提交按钮，页面刷新，Form 负责处理这个提交，如果出错，Form 还能帮你生成带错误提示的 HTML 输入框。
- **序列化器：** 用于**前后端分离 / API 接口开发**。前端是 Vue/React，后端只吐 JSON，绝不碰 HTML。

#### 3. 共同点（为什么长得像）

DRF 的作者在设计序列化器时，**几乎完全照搬了 Django Form 的优秀架构**：

- 都有字段类型声明（`CharField`, `BooleanField`）。
- 都有校验机制（`clean_<field>` 等价于 `validate_<field>`，`clean()` 等价于 `validate()`）。
- 都有 `is_valid()` 方法。
- `ModelForm` 自动根据 Model 生成字段，`ModelSerializer` 也是一样。

#### 4. 工业开发对比总结表



| 维度           | Django Form / ModelForm                        | DRF Serializer / ModelSerializer                             |
| :------------- | :--------------------------------------------- | :----------------------------------------------------------- |
| **输入数据源** | `request.POST`, `request.GET` (URLencoded)     | `request.data` (通常是 JSON)                                 |
| **输出格式**   | Python 字典 (通常交给 Template 生成 HTML)      | JSON 字符串 (直接返回给前端 Vue/React)                       |
| **渲染 HTML**  | 能！(如 `{{ form.as_p }}` 生成 `<input>` 标签) | 绝对不能，跟 HTML 彻底无关                                   |
| **嵌套能力**   | 极弱（处理一对多、多对多非常痛苦）             | **极强！** 可以在序列化器里嵌套另一个序列化器（工业开发杀手级特性） |
| **保存逻辑**   | `form.save()` 直接存库                         | `serializer.save()` 需要重写 `create/update` (ModelSerializer除外) |

**一句话总结：**
如果你在写 Django 模板页面，用 Form；如果你在写接口给 App 或前端页面调，用 Serializer。现在工业界绝大多数新项目都是前后端分离，所以 **Serializer 的使用频率远远大于 Form**。

# 总结 -- Django REST Framework (DRF) 序列化器核心指南

在 Django REST Framework 中，**序列化器** 是最核心的组件。

## 一、 序列化器是什么？怎么用？有什么用？

### 1. 通俗理解：数据界的“翻译官”

数据库里存的是 Python 对象（如 `User` 实例），但前端只认 JSON 格式（如 `{"username": "张三"}`）。序列化器就是干翻译的：

- **序列化（查）：** 把 Python 对象翻译成 JSON 返回给前端。
- **反序列化（改/增）：** 把前端传来的 JSON 翻译成 Python 字典，校验后存入数据库。

### 2. 基本用法

通常在 `serializers.py` 中定义类，在视图（`views.py`）中引入实例化：

```
# 序列化（查）：将模型对象转为 JSON
serializer = MySerializer(instance=obj)

# 反序列化（增/改）：将前端 JSON 转为字典并校验
serializer = MySerializer(data=request.data)
```

### 3. 核心特性与作用

- **数据转换：** 复杂的 ORM 对象 <-> 简单的字典/JSON。
- **强大的自动校验：** 类似 Django 的 Form，自动校验字段类型、必填项，省去大量 `if else`。
- **错误聚合：** 校验失败自动返回友好错误（如 `{"password": ["密码不能少于8位"]}`）。
- **解耦与安全：** 将数据校验从视图剥离；充当“防火墙”，防止前端恶意提交不该改的字段（如 `is_superuser`）。

## 二、 序列化器的“词汇表”：字段机制

类中定义的变量（字段）相当于给“翻译官”制定的词汇表，决定了前端能提交什么、能看到什么。

### 1. 字段类型必须和 Model 一模一样吗？

**不需要！** 它们只需“逻辑上”兼容，你可以灵活转换：

- Model 里是 `DateTimeField`，序列化器里可写成 `DateField`（前端只需日期，不要时间）。
- Model 里是 `CharField`，可写成 `EmailField`（收紧格式校验）或 `ChoiceField`（限制选项）。

### 2. 写 Model 中没有的字段会怎样？（虚拟字段）

不仅不报错，而且**非常实用**！这叫“虚拟字段”或“附加字段”：

```
class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    
    # Model中没有的字段1：仅用于接收前端数据（不存库），如“确认密码”
    password2 = serializers.CharField(max_length=20, write_only=True)
    
    # Model中没有的字段2：仅用于返回给前端（不存库），如计算得出的VIP状态
    is_vip = serializers.BooleanField(read_only=True)
```

*注意：反序列化时传入未定义且未做处理的字段，会导致 `unknown field` 校验报错。*

## 三、 分层的数据校验机制

DRF 提供了非常严谨的分层校验：字段类型校验 -> 单字段业务校验 -> 多字段联合校验。

### 1. 单字段校验：`validate_<字段名>`

用于对**单个特定字段**进行业务逻辑校验。参数 `value` 是前端传来的该字段的原始值（已通过类型校验）。

python

复制

```
def validate_username(self, value):
    # value 就是前端传过来的用户名字符串
    if '敏感词' in value:
        raise serializers.ValidationError("用户名包含敏感词汇！")
    return value  # 校验成功必须返回 value
```

### 2. 多字段联合校验：`validate`

用于**对象级别**的校验，需要同时对比多个字段。参数 `attrs` 是一个包含所有单字段校验通过后数据的**字典**。**必须返回 `attrs`**。

python

复制

```
def validate(self, attrs):
    # attrs 例如: {'password': '123', 'password2': '456'}
    if attrs.get('password') != attrs.get('password2'):
        raise serializers.ValidationError({"password2": "两次密码不一致！"})
    # 校验通过后，把不需要入库的虚拟字段删掉
    attrs.pop('password2')
    return attrs
```

## 四、 数据入库机制：save、create 与 update

### 1. `save()` 方法：触发保存的“开关”

内部逻辑：检查是否校验过 -> 判断有无 `instance`（有调 `update`，无调 `create`） -> 执行入库。
**极少需要重写 `save()`**，如果要在保存前塞额外数据（如作者），通常在视图层这样写更优雅：
`serializer.save(owner=request.user)`

### 2. `create` 和 `update` 方法

- **`create(self, validated_data)`**：`validated_data` 是经过所有校验后绝对合法的**字典**，用于新增数据。
- **`update(self, instance, validated_data)`**：`instance` 是数据库里正在被修改的**旧 ORM 对象**，用于修改数据。

**必须手动重写吗？**

- **如果用 `Serializer`：必须重写！** 否则调用 `save()` 会报 `NotImplementedError`。
- **如果用 `ModelSerializer`：不需要重写！** 会自动根据 `Meta.model` 实现。
  - *例外场景：* 比如创建用户时密码需要加密，默认的 `save()` 是明文存密码，此时需要重写 `create` 调用 `User.objects.create_user()`。

## 五、 Meta 类与字段深度定制 (`ModelSerializer`专属)

`Meta` 是配置类，告诉 DRF 怎么自动生成字段和方法。

### 1. 基础配置

- `model = Article`：绑定模型。
- `fields = ['id', 'title']` 或 `fields = '__all__'`：指定要展示的字段。
- `exclude = ('id',)`：排除指定字段（与 `fields` 互斥）。
- `read_only_fields = ('created_time',)`：前端提交时会被丢弃（防伪造），GET 时正常返回。
- `depth = 1`：控制外键嵌套深度，从扁平的 `{"author_id": 1}` 变成有层级的 `{"author": {"id": 1, "name": "张三"}}`。

### 2. 进阶神器：`extra_kwargs`

在不重新声明字段的前提下，给自动生成的字段追加或覆盖属性（**工业开发极常用**）：

python

复制

```
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'views', 'created_at']
        read_only_fields = ['views', 'created_at']
        
        extra_kwargs = {
            'title': {
                'min_length': 2,
                'error_messages': {'min_length': '标题太短了，至少2个字！'} # 自定义报错
            },
            'content': {
                'write_only': True # 前端必须传，但返回列表时不给看（防爬虫）
            }
        }
```

**前端效果：** 提交标题 `"A"` 会收到中文报错；获取列表时 JSON 里没有 `content`；尝试提交 `views=999` 会被后端直接忽略。

## 六、 选型指南：Serializer vs ModelSerializer



| 维度         | `Serializer` (基础序列化器)           | `ModelSerializer` (模型序列化器)                    |
| :----------- | :------------------------------------ | :-------------------------------------------------- |
| **字段定义** | 完全手动一个个写                      | 根据 `Meta.model` 自动生成                          |
| **校验规则** | 只能手动写 `validate` 等              | 自动继承 Model 里的规则（如 `blank`, `max_length`） |
| **保存逻辑** | **必须**手动重写 `create` 和 `update` | **自动拥有**，直接调 `save()` 即可入库              |
| **灵活性**   | 极高，完全白纸一张                    | 较高，但在 Model 绑定上有隐式魔法                   |

### 什么时候用 `ModelSerializer`？（70%场景）

**标准的单表增删改查（CRUD）！** 只要是针对某一张表的直接操作，无脑用它，省去 50% 样板代码。

### 什么时候用 `Serializer`？（30%场景）

1. **无表对应的聚合数据**（如仪表盘接口）：

```
   # 视图层查好数据，序列化器只管“排版”
   class DashboardSerializer(serializers.Serializer):
       total_users = serializers.IntegerField(help_text="总用户数")
       total_articles = serializers.IntegerField(help_text="总文章数")
       
   @api_view(['GET'])
   def get_dashboard(request):
       data = {"total_users": User.objects.count(), "total_articles": Article.objects.count()}
       serializer = DashboardSerializer(data) # 纯序列化输出，不需要 is_valid()
       return Response(serializer.data)
```



1. **非数据库交互接口**（如登录校验返回Token、发短信验证码）。
2. **极其复杂的自定义逻辑**（如一个接口同时创建用户、角色、发邮件）。

## 七、 进阶补充：序列化器中的 `self` 与 Django Form 对比

### 1. `self` 常用属性大揭秘

在 `validate`、`create` 等方法中，`self` 绑定了极有用的上下文：

- **`self.context`（走私通道）：** 一个字典。在视图里通过 `context={'request': request}` 塞进去，在序列化器里通过 `self.context.get('request')` 拿出来，常用于获取当前登录用户。
- **`self.validated_data`（干净数据）：** 所有校验通过后的最终字典。**注意：只能在 `create/update` 里用，`validate` 执行期间它还不存在！**
- **`self.instance`（分水岭）：** 当前操作的 ORM 对象。如果为 `None`，`save()` 走 `create()`；如果有值，走 `update()`。
- **`self.initial_data`（原始脏数据）：** 前端传来的最原始字典（等同于 `request.data`），未经任何校验。

### 2. 序列化器 vs Django Form / ModelForm

虽然长得像（都有 `CharField`、`validate`），但出身不同：

- **本质区别：** Django Form 是**单向**的（只负责把前端数据转成字典并校验，不负责输出JSON）；DRF 序列化器是**双向**的（能进能出）。
- **应用场景：** Form 用于传统的**服务端渲染网页**（能渲染 HTML `<input>` 标签）；序列化器用于**前后端分离 / API 接口**（只吐 JSON）。
- **嵌套能力：** Form 处理外键、多对多非常痛苦；序列化器可以轻松嵌套另一个序列化器，这是杀手级特性。
- **一句话总结：** 写 Django 模板页面用 Form；写接口给 Vue/React/App 调用，用 Serializer。



















