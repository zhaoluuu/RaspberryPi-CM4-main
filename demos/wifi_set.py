import os,socket,sys,time
import spidev as SPI
import xgoscreen.LCD_2inch as LCD_2inch
from PIL import Image,ImageDraw,ImageFont
from key import Button
import numpy as np
from numpy import linalg
from xgolib import XGO

import sys
sys.path.append("..")
import uiutils
la=uiutils.load_language()

button=Button()
#define colors
color_bg=(8,10,26)
color_unselect=(89,99,149)
color_select=(24,47,223)
color_white=(255,255,255)
splash_theme_color = (15,21,46)
#display init
display = LCD_2inch.LCD_2inch()
display.clear()
#splash
splash = Image.new("RGB", (display.height, display.width ),splash_theme_color)
draw = ImageDraw.Draw(splash)

display.ShowImage(splash)
#font
font1 = ImageFont.truetype("/home/pi/model/msyh.ttc",12)
font2 = ImageFont.truetype("/home/pi/model/msyh.ttc",20)

def display_cjk_string(splash,x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True, background_color=(0,0,0)):
    splash.text((x,y),text,fill =color,font = font_size) 
def lcd_rect(x,y,w,h,color,thickness):
    draw.rectangle([(x,y),(w,h)],fill=color,width=thickness)

wifi1="/etc/default/crda"
wifi2="/etc/wpa_supplicant/wpa_supplicant.conf"

with open(wifi1, 'r') as f:
    content=f.read()
    ct=content.find('REGDOMAIN=')
    ct_code=content[ct+10:ct+12]

with open(wifi2, 'r') as f:
    content2=f.read()
    ct2=content2.find('country=')
    ct_code2=content2[ct2+8:ct2+10]

display_cjk_string(draw,15,17, la['WIFISET']['NOW']+ct_code, font_size=font2, color=color_white, background_color=color_bg)
display_cjk_string(draw,15,77, la['WIFISET']['SET'], font_size=font2, color=color_white, background_color=color_bg)
display.ShowImage(splash)
print(ct_code,ct_code2)

country_list=[
    ['United States','US'],
    ['Britain(UK)','GB'],
    ['Japan','JP'],
    ['Koera(South)','KR'],
    ['China','CN'],
    ['Australia','AU'],
    ['Canada','CA'],
    ['France','FR'],
    ['Hong Kong','HK'],
    ['Singapore','SG'],
]
select=0
while 1:
    lcd_rect(0,70,320,120,(255,0,0),-1)
    display_cjk_string(draw,15,77, la['WIFISET']['SET']+country_list[select][0], font_size=font2, color=color_white, background_color=color_bg)
    display.ShowImage(splash)
    if button.press_c():
        if select==0:
            select=len(country_list)-1
        else:
            select-=1
    elif button.press_d():
        if select==len(country_list)-1:
            select=0
        else:
            select+=1
    elif button.press_a():
        break
    elif button.press_b():
        time.sleep(0.5)
        sys.exit()

ct_code=country_list[select][1]
print(ct_code)
ct_list=list(content)
ct_list[ct+10:ct+12]=ct_code
content=''.join(ct_list)

ct_list2=list(content2)
ct_list2[ct2+8:ct2+10]=ct_code
content2=''.join(ct_list2)
print(content,content2)

with open(wifi1, 'w') as f:
    f.write(content)

with open(wifi2, 'w') as f:
    f.write(content2)

display_cjk_string(draw,15,157, la['WIFISET']['SAVED'], font_size=font2, color=color_white, background_color=color_bg)
display.ShowImage(splash)





