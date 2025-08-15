import os, socket, sys, time
import xgoscreen.LCD_2inch as LCD_2inch
from PIL import Image, ImageDraw, ImageFont
from key import Button

import sys

sys.path.append("..")
import uiutils

la = uiutils.load_language()

button = Button()

color_bg = (8, 10, 26)
color_unselect = (89, 99, 149)
color_select = (24, 47, 223)
color_white = (255, 255, 255)
splash_theme_color = (15, 21, 46)
purple = (24, 47, 223)

display = LCD_2inch.LCD_2inch()
display.clear()
splash = Image.new("RGB", (display.height, display.width), splash_theme_color)
draw = ImageDraw.Draw(splash)
display.ShowImage(splash)

# font
font1 = ImageFont.truetype("/home/pi/model/msyh.ttc", 16)
font2 = ImageFont.truetype("/home/pi/model/msyh.ttc", 18)

vol_logo = Image.open("/home/pi/RaspberryPi-CM4-main/pics/s@2x.png")


def display_cjk_string(
    splash,
    x,
    y,
    text,
    color=(255, 255, 255),
    font_size=1,
    scale=1,
    mono_space=False,
    auto_wrap=True,
    background_color=(0, 0, 0),
):
    splash.text((x, y), text, fill=color, font=font_size)


def lcd_rect(x, y, w, h, color, thickness):
    draw.rectangle([(x, y), (w, h)], fill=color, width=thickness)


splash.paste(vol_logo, (133, 25), vol_logo)
text_width = draw.textlength(la["VOLUME"]["VOLUMe"], font=font2)
title_x = (320 - text_width) / 2
display_cjk_string(
    draw,
    title_x,
    90,
    la["VOLUME"]["VOLUMe"],
    font_size=font2,
    color=color_white,
    background_color=color_bg,
)
display.ShowImage(splash)


def volume_level():
    # 返回当前的目录
    current_dir = os.getcwd()
    # test
    print(current_dir)
    # 用于路径拼接文件路径
    volume_ini_path = os.path.join(current_dir, "volume", "volume.ini")
    # test
    print(volume_ini_path)
    with open(volume_ini_path, "r") as f:  # r为标识符，表示只读
        volume = f.read()
        # test
        print(volume)
    return volume

res =volume_level()
volume = int(res)
select = 0

while 1:
    draw.rectangle([(20, 150), (300, 170)], fill=color_unselect)
    vol_width = 20 + int(280 / 100 * volume)
    draw.rectangle([(20, 150), (vol_width, 170)], fill=purple)
    draw.rectangle([(144, 180), (320, 240)], fill=splash_theme_color)
    display_cjk_string(
        draw,
        144,
        180,
        str(volume) + "%",
        font_size=font2,
        color=color_white,
        background_color=color_bg,
    )
    display.ShowImage(splash)
    if button.press_c():
        if volume == 0:
            pass
        else:
            volume -= 5
    elif button.press_d():
        if volume == 100:
            pass
        else:
            volume += 5
    elif button.press_a():
        print('a')
        break
    elif button.press_b():
        print('b')
        os._exit(0)

current_dir = os.getcwd()

volume_ini_path = os.path.join(current_dir, "volume", "volume.ini")

with open(volume_ini_path, "w") as f:
    f.write(str(volume))

oscmd = "sudo -u pi pactl set-sink-volume 1 " + str(volume) + "%"
print(oscmd)
os.system('sudo -u pi pulseaudio --start')
os.system(oscmd)
text_width = draw.textlength(la["VOLUME"]["SAVED"], font=font2)
title_x = (320 - text_width) / 2
display_cjk_string(
    draw,
    title_x,
    210,
    la["VOLUME"]["SAVED"],
    font_size=font2,
    color=color_white,
    background_color=color_bg,
)
display.ShowImage(splash)
