# 启动流程概述
开机 → /etc/rc.local → start1.sh → main.py
1. 触发点（开机后）：系统进入 multi-user 运行级别末尾时，/etc/rc.local 由 root 执行。

  ```bash
  pi@raspberrypi:~ $ cat /etc/rc.local | grep -v '^#'
  
  _IP=$(hostname -I) || true
  if [ "$_IP" ]; then
    printf "My IP address is %s\n" "$_IP"
  fi
  
  su pi -c 'bash /home/pi/start1.sh'
  exit 0
  ```

1. 切换工作目录到项目根：cd /home/pi/RaspberryPi-CM4-main/

2. 由remix.py代理启动main.py，根据/home/pi/RaspberryPi-CM4-main/language/language.ini文件选择语言cn/en。

  ```bash
  pi@raspberrypi:~/RaspberryPi-CM4-main $ cat remix.py
  from uiutils import *
  
  lang=language()
  print(lang)
  if lang=='cn':
          print('lang = cn')
          os.system('sudo python3 main.py')
           
  else:
       print('lang = en')
       os.system('sudo -E python3 main.py')
  
  ```

# 服务

```
开机 → 系统内核加载 → systemd 启动服务
│
├─ ① 系统基础服务（建议保留）
│   ├─ networking.service       # 网络初始化（有线/无线）
│   ├─ wpa_supplicant.service   # Wi-Fi 驱动与连接
│   ├─ dhcpcd.service           # DHCP 获取 IP
│   ├─ systemd-timesyncd.service# 网络时间同步
│   ├─ rsyslog.service          # 系统日志
│   ├─ cron.service             # 定时任务
│
├─ ② 远程访问/管理
│   ├─ ssh.service              # SSH 远程登录
│   ├─ vncserver-x11-serviced   # VNC 远程桌面
│   ├─ avahi-daemon.service     # 局域网设备发现（Bonjour/mDNS）
│
├─ ③ 硬件驱动/功能模块
│   ├─ wm8960-soundcard.service # 声卡驱动
│   ├─ rpi-display-backlight    # 屏幕背光控制
│   ├─ hciuart.service          # 蓝牙串口
│
├─ ④ 应用级服务（你自己安装/业务相关）
│   ├─ jupyter.service          # Jupyter Notebook/Lab
│   ├─ mihomo.service           # 代理/网络加速内核
│   ├─ /etc/rc.local            # 调用 start1.sh → main.py（业务主程序）
│
├─ ⑤ 额外功能
│   ├─ cups.service / cups-browsed.service # 打印服务
│   ├─ rsync.service                        # 文件同步
│
└─ 启动完成

```

- **`jupyter.service`** →  Jupyter Notebook / Lab，用于远程 Python 开发或数据可视化。
- **`mihomo.service`** → 一个网络代理/转发相关的服务（Clash/Mihomo 代理内核）。
- **`wm8960-soundcard.service`** → 对应 WM8960 声卡模块，表示你的树莓派装了这个声卡驱动。

------

### **网络/远程访问类**

- **`ssh.service`** → SSH 远程登录
- **`vncserver-x11-serviced.service`** → VNC 远程桌面服务
- **`wpa_supplicant.service`** → Wi-Fi 无线连接
- **`dhcpcd.service`** → DHCP 客户端，负责获取 IP

------

### **树莓派硬件相关**

- **`hciuart.service`** → 蓝牙串口（UART）
- **`rpi-display-backlight.service`** → 树莓派显示屏背光控制
- **`rpi-eeprom-update.service`** → EEPROM 固件更新

------

### **打印和扫描**

- **`cups.service` / `cups-browsed.service` / `cups.socket`** → 打印机相关
- **`avahi-daemon.service`** → mDNS / Bonjour 服务，用于局域网设备发现（打印机、网络共享等）

------

### **通用系统服务**

- **`cron.service`** → 定时任务
- **`rsyslog.service`** → 系统日志
- **`rsync.service`** → 文件同步服务
- **`lightdm.service`** → 图形界面登录管理器
- **`networking.service`** → 有线/无线网络初始化