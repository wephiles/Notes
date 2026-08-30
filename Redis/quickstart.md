# 1 下载安装redis -- ubunt



下面按「从零开始」的思路，把在 Ubuntu 上安装和配置 Redis 的主流做法讲清楚，并给你一份可以直接照抄的配置示例。

## 一、先选一种安装方式

推荐优先级：

1. **官方 APT 源安装（推荐）**：版本新、更新方便，适合生产/长期使用。
2. **Ubuntu 默认源安装**：最简单，但版本偏旧（Ubuntu 22.04 通常是 Redis 6.x）。tencent.com+1
3. **源码编译安装**：需要特定版本或深度定制时使用。csdn.net

下面分别给出步骤。

## 二、方式一：官方 APT 源安装（Redis 7.x，推荐）

这是 Redis 官方推荐的 Linux 安装方式，在 Ubuntu 18.04 / 20.04 / 22.04 都适用。csdn.net+2

### 1. 安装依赖 & 添加官方源

```
# 1）安装必要工具
sudo apt update
sudo apt install -y lsb-release curl gpg

# 2）导入 Redis 官方 GPG 密钥
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

# 3）添加 Redis APT 源
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/redis.list

# 4）更新包索引
sudo apt update
```

### 2. 安装 Redis

```
sudo apt install -y redis
```

> 注意：包名是 `redis`，不是 `redis-server`；这是官方源的包名，装完后会有 `redis-server` / `redis-cli` 等命令。csdn.net+1

### 3. 启动 & 开机自启

```
# 启动服务
sudo systemctl enable --now redis-server

# 查看状态
sudo systemctl status redis-server
```

正常会看到 `active (running)` 字样。csdn.net+1

### 4. 快速验证

```
redis-cli ping
# 返回 PONG 就表示 OK
```

## 三、方式二：Ubuntu 默认源安装（最简单）

如果你只是本地开发/测试，对版本没有要求，可以直接用 Ubuntu 自带源：

```
sudo apt update
sudo apt install -y redis-server

# 启动并设置开机自启
sudo systemctl enable --now redis-server

# 验证
redis-cli ping
```

默认配置文件在 `/etc/redis/redis.conf`，版本一般是 Redis 6.x 左右（视 Ubuntu 版本而定）。tencent.com+1

## 四、方式三：源码编译安装（自定义版本）

当你需要 Redis 7.x/8.x 或特定编译参数时，用源码安装。csdn.net

### 1. 安装编译依赖

```
sudo apt update
sudo apt install -y build-essential tcl
```

### 2. 下载 & 编译安装（以 Redis 7.2 为例）

```
cd /opt
sudo wget https://download.redis.io/releases/redis-7.2.0.tar.gz
sudo tar xzf redis-7.2.0.tar.gz
cd redis-7.2.0

sudo make
sudo make install
```

默认会把 `redis-server` / `redis-cli` 安装到 `/usr/local/bin`。csdn.net

### 3. 手工创建配置和服务（可选但推荐）

简单示意：

```
# 配置文件目录
sudo mkdir -p /etc/redis
sudo cp redis.conf /etc/redis/redis.conf

# 数据目录
sudo mkdir -p /var/lib/redis
sudo chown redis:redis /var/lib/redis   # 如果有 redis 用户的话
```

如果需要注册为 systemd 服务，可参考后文「systemd 服务配置」一节的模板。

## 五、核心配置（redis.conf）

无论哪种安装方式，配置文件通常都在：

- 官方源 / Ubuntu 源：`/etc/redis/redis.conf`tencent.com+1
- 源码安装：你拷贝到哪里就是哪里，常见 `/etc/redis/redis.conf`

下面用 `sudo nano /etc/redis/redis.conf`（或 vim）来改。

### 1. 网络与访问控制（关键）

#### 1.1 绑定地址：bind

默认只允许本机访问：

```
bind 127.0.0.1 -::1
```

- **只本机访问**：保持默认即可。
- **允许远程访问**（开发环境/内网）：

```
  # bind 127.0.0.1 -::1   # 注释掉或改成：
  bind 0.0.0.0
```

  注意：`0.0.0.0` 表示所有网卡，公网暴露非常危险，一定要配合防火墙 + 密码。

#### 1.2 保护模式：protected-mode

Redis 3.2+ 引入的安全机制：csdn.net+2

- 默认：`protected-mode yes`

- 含义：当没有 bind 也没有密码时，只允许本机访问（兜底安全）。

- 典型组合：

  1）只本机访问（最安全）：

```
  bind 127.0.0.1 -::1
  protected-mode yes
  # requirepass 可以不设，本机直接用
```

  2）允许远程访问，且设置密码（推荐）：

```
  bind 0.0.0.0   # 或具体内网 IP
  protected-mode yes
  requirepass 你的强密码
```

  3）允许远程访问，但不设密码（极不推荐）：

```
  bind 0.0.0.0
  protected-mode no
  # 无密码，任何能连上端口的人都能操作 Redis
```

> 生产环境：**不要**关闭 `protected-mode`，一定要设 `requirepass`，并尽量 bind 内网 IP。

#### 1.3 端口：port

默认：

```
port 6379
```

建议生产环境改为非标准端口，例如：

```
port 6380
```

### 2. 进程模式与 systemd 配合

#### 2.1 daemonize / supervised

- 传统用法（6.x 及之前）：

```
  daemonize yes
  supervised no
```

- Redis 7 + systemd 时，官方推荐组合：php.cn+1

```
  daemonize no
  supervised systemd
```

  原因：当使用 systemd 管理时，`daemonize yes` 会导致二次 fork，systemd 无法正确追踪主进程，表现为 `systemctl status` 显示 `inactive (dead)` 但进程还在跑。php.cn

如果你是通过 APT 安装，Ubuntu 的包通常已经按 systemd 方式配置，你可以检查一下：

```
grep -E '^daemonize|^supervised' /etc/redis/redis.conf
```

#### 2.2 systemd 服务文件示例（源码安装时用）

如果你是 `make install` 到 `/usr/local/bin`，可以自己写一个 systemd 服务：

```
sudo nano /etc/systemd/system/redis.service
```

内容示例（适配 Redis 7 + `daemonize no`）：csdn.net+1

```
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

然后：

```
sudo systemctl daemon-reload
sudo systemctl enable --now redis
```

### 3. 密码认证：requirepass

在 `/etc/redis/redis.conf` 中找到 `requirepass`，取消注释并设置强密码：tencent.com+1

```
requirepass 你的强密码
```

客户端连接时：

```
redis-cli -a 你的强密码
# 或进入 CLI 后：
AUTH 你的强密码
```

### 4. 内存与持久化（常用项）

#### 4.1 最大内存：maxmemory

建议生产环境限制 Redis 最大使用内存，避免把系统内存吃光：csdn.net+1

```
maxmemory 2gb        # 根据机器内存调整，比如 4GB 机器可以给 2~3GB
maxmemory-policy allkeys-lru
```

`maxmemory-policy` 常用值：

- `noeviction`：不淘汰，写入报错（默认）
- `allkeys-lru`：所有键中，最近最少使用淘汰（做缓存常用）
- `volatile-lru`：只淘汰设置了过期时间的键中 LRU

#### 4.2 持久化：RDB / AOF

默认只开启 RDB（快照），AOF 是关闭的：csdn.net

- RDB 示例：

```
  save 900 1
  save 300 10
  save 60 10000
```

- 启用 AOF（更安全，但性能略降）：

```
  appendonly yes
  appendfsync everysec
  aof-use-rdb-preamble yes
```

如果你只把 Redis 当缓存，也可以完全关闭持久化：

```
save ""
appendonly no
```

### 5. 日志与数据目录

常见配置：csdn.net+1

```
logfile /var/log/redis/redis-server.log
dir /var/lib/redis
```

确保目录存在并赋权（如果用 redis 用户运行）：

```
sudo mkdir -p /var/log/redis
sudo mkdir -p /var/lib/redis
sudo chown -R redis:redis /var/log/redis /var/lib/redis
```

## 六、配置完成后重启 & 验证

### 1. 重启 Redis

```
sudo systemctl restart redis-server
# 或源码安装时用你自己的服务名：sudo systemctl restart redis
```

### 2. 检查监听地址和端口

```
sudo ss -lntp | grep 6379
# 或
sudo ss -lntp | grep 6380  # 如果你改了端口
```

确认监听在你期望的 IP：端口上。

### 3. 本地连接测试

```
redis-cli -h 127.0.0.1 -p 6379 -a 你的强密码 ping
# 返回 PONG 即正常
```

### 4. 远程连接测试（在另一台机器上）

```
redis-cli -h Redis服务器IP -p 6379 -a 你的强密码 ping
```

如果连不上，排查：

1. Redis 是否监听正确 IP：0.0.0.0 或具体内网 IP；
2. 防火墙是否放行 6379/6380 端口（UFW/云安全组）；tencent.com
3. `protected-mode` 和 `requirepass` 是否配置合理。

## 七、一份可直接照抄的 redis.conf 示例（Redis 7 + systemd）

假设你用官方 APT 源安装 Redis 7，并希望：

- 允许内网访问（bind 内网 IP 或 0.0.0.0）
- 设置密码
- 配合 systemd
- 内存限制 + 淘汰策略
- 开启 AOF 持久化

可以在 `/etc/redis/redis.conf` 中修改/确认这些行：

```
# 网络
bind 0.0.0.0               # 或内网 IP，如 192.168.1.100
protected-mode yes
port 6379                  # 或 6380

# 进程模式（Redis 7 + systemd）
daemonize no
supervised systemd

# 密码
requirepass 你的强密码

# 内存
maxmemory 2gb
maxmemory-policy allkeys-lru

# 持久化（按需选择）
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes

# 日志与数据
logfile /var/log/redis/redis-server.log
dir /var/lib/redis
```

然后：

```
sudo systemctl restart redis-server
sudo systemctl status redis-server
redis-cli -a 你的强密码 ping
```

## 八、安全小建议（生产环境必读）

1. **不要把 Redis 直接暴露在公网**，尤其不要：
   - `bind 0.0.0.0` + `protected-mode no` + 无密码
2. **务必设置强密码**（`requirepass`），并定期更换。apiref.com+1
3. **尽量改掉默认端口** 6379，减少被扫描到的概率。csdn.net
4. **用防火墙限制来源 IP**，只允许应用服务器所在网段访问 6379/6380。tencent.com
5. **定期更新 Redis 版本**，避免已知漏洞。

# 2. 修改密码

### 第一步：在 Ubuntu 上为 Redis 设置密码

你需要修改 Redis 的配置文件 `redis.conf`。

1. **打开配置文件**：

```
   sudo nano /etc/redis/redis.conf
```

  *(如果用的是 vim，把 nano 换成 vim)*

1. **找到 `requirepass` 配置项**：
   在文件中搜索（nano 编辑器下按 `Ctrl+W`，输入 `requirepass` 回车），你会看到类似这样的内容：

```
   # requirepass foobared
```

1. **设置你的密码**：
   去掉前面的 `#` 号，并在后面写上你想设置的强密码。例如，设置密码为 `MyStrongRedisPassword123`：

```
   requirepass MyStrongRedisPassword123
```

  \> ⚠️ **注意**：因为 Redis 速度极快，如果暴露在公网，每秒可以被尝试十几万次密码，所以**密码一定要足够长和复杂**，不要用简单的数字或字母。

1. **保存并退出**：
   nano 编辑器下按 `Ctrl+O` 保存，回车确认，然后按 `Ctrl+X` 退出。
2. **重启 Redis 服务使配置生效**：

```
   sudo systemctl restart redis-server
```

### 第二步：在你的代码中填入密码

把刚才设置的密码填入你的 `REDIS_CONN_PARAMS` 字典中：

```
REDIS_CONN_PARAMS = {
    'host': 'localhost',
    'password': 'MyStrongRedisPassword123',  # 填入刚才设置的密码
    'port': 6379,
    'encoding': 'utf-8',
}
```

### 第三步：验证是否成功

在运行你的 Python 代码之前，你可以先用命令行验证一下密码是否设置成功：

1. 在终端输入 `redis-cli` 进入命令行：

```
   redis-cli
```

1. 直接输入 `ping`，如果设置了密码，此时会返回错误：`(error) NOAUTH Authentication required.`
2. 输入密码进行认证：

```
   AUTH MyStrongRedisPassword123
```

1. 再次输入 `ping`，如果返回 `PONG`，说明密码设置和验证都成功了！
2. 输入 `exit` 退出。

或者直接带密码登录：

```
redis-cli -a MyStrongRedisPassword123 ping
# 返回 PONG 即成功
```

### 💡 补充：如果我只是本地开发，不想设密码怎么办？

如果你只是在本地自己电脑上开发，觉得每次填密码很麻烦，可以**取消密码验证**，但必须确保安全：

1. 打开 `redis.conf`，确保 `requirepass` 被注释掉（前面有 `#`）或留空。
2. 确保配置文件中有这两行（默认就是这样的）：

```
   bind 127.0.0.1 -::1
   protected-mode yes
```

  *`bind 127.0.0.1` 保证了只有本机可以连接，`protected-mode yes` 保证了在没有密码且非本机连接时拒绝访问。这是不设密码情况下的安全底线。*

3. 重启 Redis：`sudo systemctl restart redis-server`
4. 你的代码中 `password` 保持为空字符串 `''` 即可。

























