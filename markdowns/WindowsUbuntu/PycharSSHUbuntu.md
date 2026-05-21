在Windows上的PyCharm通过SSH连接VMware虚拟机，主要分为**三个阶段**：配置虚拟机网络、在虚拟机内开启SSH服务、在PyCharm中配置连接。

以下是详细的图文级步骤：

### 第一阶段：确保网络互通（最关键的一步）

1. **获取虚拟机的IP地址**
   - 打开你的VMware虚拟机，进入Linux系统。
   - 打开终端，输入命令：

```
     ip addr
```

   或者

```
     ifconfig
```

  \* 找到你的网卡（通常叫 `ens33` 或 `eth0`），记住里面的 `inet` 后面的IP地址（例如 `192.168.xx.xx`）。

1. **测试Windows与虚拟机是否互通**
   - 在Windows上按 `Win + R`，输入 `cmd` 回车。
   - 在命令行输入：`ping 你刚刚记下的IP地址`（例如 `ping 192.168.1.100`）。
   - **如果显示“请求超时”**：说明网络不通。请检查VMware右下角的网络适配器设置，建议改成**NAT模式**（最不容易出错），或者确保你的虚拟机Linux系统内网络服务已启动。
   - **如果显示“来自…的回复”**：说明网络通了，进入下一步。

### 第二阶段：在虚拟机上安装并启动SSH服务

大多数Linux发行版默认没有开启SSH，需要手动开启：

- **对于 Ubuntu / Debian 系统：**

```
  sudo apt update
  sudo apt install openssh-server
  sudo systemctl start ssh
  sudo systemctl enable ssh  # 设置为开机自启
```

- **对于 CentOS / RedHat 系统：**

```
  sudo yum install openssh-server
  sudo systemctl start sshd
  sudo systemctl enable sshd
```

- **检查防火墙（非常重要）：**
  如果是Ubuntu，通常默认放行了；如果是CentOS，可能需要放行22端口：

```
  sudo firewall-cmd --permanent --add-port=22/tcp
  sudo firewall-cmd --reload
```

### 第三阶段：在PyCharm中配置SSH连接

1. **打开解释器设置**
   - 打开PyCharm项目，点击左上角 `File` -> `Settings`（如果是Mac则是 `PyCharm` -> `Preferences`）。
   - 在左侧找到 `Project: 你的项目名` -> `Python Interpreter`。
2. **添加SSH解释器**
   - 点击右侧的齿轮图标 ⚙️（或者 `Add Interpreter` -> `Add Local Interpreter`… 取决于PyCharm版本，新版本通常直接点 `Add Interpreter`）。
   - 在弹出的窗口左侧，选择 **SSH**（不要选System Interpreter，也不要选Virtualenv）。
3. **填写连接信息**
   - **Host（主机）**：填入虚拟机的IP地址（如 `192.168.1.100`）。
   - **Port（端口）**：填 `22`（默认端口）。
   - **Username（用户名）**：填虚拟机的登录用户名（比如 `root` 或者你自建的普通用户）。
   - **Auth type（认证类型）**：选择 `Password`（密码登录）。
   - **Password（密码）**：填入该用户对应的密码。
   - 点击 **Next**。
4. **等待连接并配置环境**
   - 第一次连接时，PyCharm可能会弹出提示“Host key is not recognized…”，点击 **Yes** 信任并保存。
   - 接着PyCharm会检测虚拟机上的Python环境。
   - 在 `Interpreter` 下拉菜单中，选择虚拟机上的Python路径（通常默认的就是 `/usr/bin/python3`，如果你装了Anaconda，路径可能在 `/home/你的用户名/anaconda3/bin/python`）。
   - 点击 **Next**，然后点击 **Create** 或 **Finish**。
5. **同步文件（可选但推荐）**
   - 连接成功后，PyCharm会自动将你Windows上的项目文件上传到虚拟机的一个临时目录（通常在 `~/PyCharmProjects/项目名`）。
   - 你可以在 `Tools` -> `Deployment` -> `Browse Remote Host` 中查看和管理虚拟机上的文件。

### 💡 常见问题排查：

1. **PyCharm提示 “Connection refused”（连接被拒绝）**
   - 说明虚拟机的SSH服务没开，或者端口不是22，回到第二阶段检查。
2. **PyCharm提示 “Connection timed out”（连接超时）**
   - 纯网络问题。检查VMware网络模式，尝试将虚拟机网络模式从“桥接”改为“NAT”，或者反过来。确保Windows的防火墙没有拦截PyCharm。
3. **能连上，但是找不到Python解释器（列表为空）**
   - 说明虚拟机上没装Python。在虚拟机终端输入 `python3 --version` 检查，如果没有，需要用 `sudo apt install python3` 安装。
4. **每次重启虚拟机，IP地址变了怎么办？**
   - 如果是NAT模式，可以在VMware的 `编辑 -> 虚拟网络编辑器` 中，把NAT模式的子网IP固定下来，然后在虚拟机内部设置静态IP。