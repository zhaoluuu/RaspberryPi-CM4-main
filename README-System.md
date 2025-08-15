# 启动流程概述
1. 触发点（开机后）：系统进入 multi-user 运行级别末尾时，/etc/rc.local 由 root 执行。
2. 切换工作目录到项目根：cd /home/pi/RaspberryPi-CM4-main/
3. 实际启动项：注释掉了 main.py，启用了
sudo python3 remix.py
4. 由remix.py代理启动main.py，选择预约cn/en。