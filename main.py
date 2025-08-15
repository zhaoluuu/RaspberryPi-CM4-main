from demos.uiutils import *
import time
import os
import socket
from PIL import Image

# 导入必要的模块
from demos.uiutils import *  # 导入UI工具函数
import time                  # 时间处理
import os                    # 操作系统接口
import socket                # 网络通信
from PIL import Image        # 图像处理

# 初始化按键对象
button = Button()

# 加载语言包
la = load_language()

# 全局变量定义
current_selection = 1                    # 当前选中的菜单项 (1-3)
last_battery_check_time = time.time()    # 上次检查电池状态的时间
last_network_check_time = time.time()    # 上次检查网络状态的时间
is_online = False                        # 网络连接状态

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    检测网络连接状态
    通过连接Google DNS服务器(8.8.8.8)来测试网络连通性
    
    参数:
        host: 测试连接的主机地址
        port: 测试连接的端口
        timeout: 连接超时时间(秒)
    
    返回:
        bool: True表示网络连接正常，False表示网络断开
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"error connection: {ex}")
        return False

def update_status():
    """
    更新系统状态显示
    定期检查电池状态和网络连接状态，并更新屏幕显示
    """
    global last_battery_check_time, last_network_check_time, is_online
    now = time.time()

    # 每3秒检查一次电池状态
    if now - last_battery_check_time > 3:
        show_battery()
        last_battery_check_time = now

    # 每3秒检查一次网络状态
    if now - last_network_check_time > 3:
        is_online = is_connected()
        last_network_check_time = now

    # 根据网络状态显示WiFi图标
    if is_online:
        draw.bitmap((10, 0), wifiy)  # 显示WiFi连接图标
    else:
        draw.rectangle((10, 0, 50, 40), fill=0)  # 清除WiFi图标区域

def main_program():
    """
    主程序逻辑
    处理按键输入、菜单选择和功能执行
    """
    global key_state_left, key_state_right, key_state_down, current_selection
    
    # 更新系统状态显示
    update_status()
    
    # 初始化按键状态
    key_state_left = 0
    key_state_down = 0
    key_state_right = 0

    # 检测按键输入并设置对应状态
    if button.press_a():
        key_state_down = 1      # A键按下 - 确认选择
        key_state_left = 0
        key_state_right = 0
    elif button.press_c():
        key_state_down = 0
        key_state_left = 1      # C键按下 - 向左选择
        key_state_right = 0
    elif button.press_d():
        key_state_down = 0
        key_state_left = 0
        key_state_right = 1     # D键按下 - 向右选择
    elif button.press_b():
        print("b button,but nothing to quit")  # B键按下 - 暂无功能

    # 处理向左选择逻辑
    if key_state_left == 1:
        show_battery()  # 显示电池状态
        if current_selection == 1:
            current_selection = 3  # 从第1项跳到第3项
        else:
            current_selection -= 1  # 向左移动选择

    # 处理向右选择逻辑
    if key_state_right == 1:
        show_battery()  # 显示电池状态
        if current_selection == 3:
            current_selection = 1  # 从第3项跳到第1项
        else:
            current_selection += 1  # 向右移动选择

    # 根据当前选择绘制菜单界面
    if current_selection == 1:
        # 选中第1项：RC控制
        lcd_rect(0, 188, 320, 240, color=btn_unselected, thickness=-1)      # 背景色
        lcd_rect(0, 188, 110, 240, color=btn_selected, thickness=-1)        # 选中项高亮
        lcd_draw_string(draw, 7, 195, la["MAIN"]["RC"], color=color_white, scale=font2)
        lcd_draw_string(draw, 112, 195, la["MAIN"]["PROGRAM"], color=color_white, scale=font2)
        lcd_draw_string(draw, 215, 195, la["MAIN"]["TRYDEMO"], color=color_white, scale=font2)
        # 绘制分割线
        draw.line((110, 188, 110, 240), fill=txt_unselected, width=1, joint=None)
        draw.line((210, 188, 210, 240), fill=txt_unselected, width=1, joint=None)
        draw.rectangle((0, 188, 320, 240), outline=txt_unselected, width=1)
        
    elif current_selection == 2:
        # 选中第2项：编程模式
        lcd_rect(0, 188, 320, 240, color=btn_unselected, thickness=-1)      # 背景色
        lcd_rect(110, 188, 210, 240, color=btn_selected, thickness=-1)      # 选中项高亮
        lcd_draw_string(draw, 112, 195, la["MAIN"]["PROGRAM"], color=color_white, scale=font2)
        lcd_draw_string(draw, 7, 195, la["MAIN"]["RC"], color=color_white, scale=font2)
        lcd_draw_string(draw, 215, 195, la["MAIN"]["TRYDEMO"], color=color_white, scale=font2)
        # 绘制分割线
        draw.line((110, 188, 110, 240), fill=txt_unselected, width=1, joint=None)
        draw.line((210, 188, 210, 240), fill=txt_unselected, width=1, joint=None)
        draw.rectangle((0, 188, 320, 240), outline=txt_unselected, width=1)
        
    elif current_selection == 3:
        # 选中第3项：演示模式
        lcd_rect(0, 188, 320, 240, color=btn_unselected, thickness=-1)      # 背景色
        lcd_rect(210, 188, 320, 240, color=btn_selected, thickness=-1)      # 选中项高亮
        lcd_draw_string(draw, 7, 195, la["MAIN"]["RC"], color=color_white, scale=font2)
        lcd_draw_string(draw, 112, 195, la["MAIN"]["PROGRAM"], color=color_white, scale=font2)
        lcd_draw_string(draw, 215, 195, la["MAIN"]["TRYDEMO"], color=color_white, scale=font2)
        # 绘制分割线
        draw.line((110, 188, 110, 240), fill=txt_unselected, width=1, joint=None)
        draw.line((210, 188, 210, 240), fill=txt_unselected, width=1, joint=None)
        draw.rectangle((0, 188, 320, 240), outline=txt_unselected, width=1)

    # 处理确认选择逻辑
    if key_state_down == 1:
        show_battery()  # 显示电池状态
        
        if current_selection == 2:
            # 选择编程模式 - 启动热点
            print("hotspot")
            lcd_rect(0, 188, 160, 240, color=btn_selected, thickness=-1)
            lcd_draw_string(draw, 25, 195, la["MAIN"]["OPENING"], color=color_white, scale=font2)
            time.sleep(1)
            os.system("sudo python3 hotspot.py")  # 启动热点程序
            lcd_rect(0, 188, 160, 240, color=btn_selected, thickness=-1)
            lcd_draw_string(draw, 25, 195, la["MAIN"]["PROGRAM"], color=color_white, scale=font2)

        if current_selection == 1:
            # 选择RC控制模式 - 启动Web控制程序
            os.system("sudo python3 flacksocket/app.py")

        if current_selection == 3:
            # 选择演示模式 - 启动演示程序
            lcd_rect(210, 188, 320, 240, color=btn_selected, thickness=-1)
            lcd_draw_string(draw, 215, 195, la["MAIN"]["OPENING"], color=color_white, scale=font2)
            display.ShowImage(splash)
            print("turn demos")
            os.system("python3 demoen.py")  # 启动演示程序

        print(str(current_selection) + " select")
    
    # 更新屏幕显示
    display.ShowImage(splash)

# 加载图像资源
current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录
logo = Image.open(os.path.join(current_dir, "pics", "luwu@3x.png"))      # 加载Logo图像
wifiy = Image.open(os.path.join(current_dir, "pics", "wifi@2x.png"))     # 加载WiFi图标

# 显示产品类型信息
#lcd_draw_string(draw, 210, 133, firmware_info, color=color_white, scale=font1)  # 显示xgolite的版本信息
lcd_draw_string(draw, 140, 133, "DOGZILLA-Lite", color=color_white, scale=font1)  # 显示Yahboom产品名称
lcd_draw_string(draw, 180, 153, "CM4", color=color_white, scale=font1)           # 显示CM4标识

# 显示电池状态
show_battery()
# 显示Logo图像
draw.bitmap((74, 49), logo)

# 主循环 - 持续运行主程序
while True:
    main_program()
