import os,socket,sys,time
import spidev as SPI
import xgoscreen.LCD_2inch as LCD_2inch
from PIL import Image,ImageDraw,ImageFont
from key import Button
from subprocess import check_output
import uiutils

la=uiutils.load_language()

path=os.getcwd()

#define colors
splash_theme_color = (15,21,46)
btn_selected = (24,47,223)
btn_unselected = (20,30,53)
txt_selected = (255,255,255)
txt_unselected = (76,86,127)
splashb_theme_color = (8,10,26)
color_black=(0,0,0)
color_white=(255,255,255)
color_red=(238,55,59)
#display init
display = LCD_2inch.LCD_2inch()
display.Init()
display.clear()
#button
button=Button()
#const
firmware_info='v1.0'
#font
font1 = ImageFont.truetype("/home/pi/model/msyh.ttc",15)
font2 = ImageFont.truetype("/home/pi/model/msyh.ttc",22)
font3 = ImageFont.truetype("/home/pi/model/msyh.ttc",30)
#init splash
splash = Image.new("RGB", (display.height, display.width ),splash_theme_color)
draw = ImageDraw.Draw(splash)

def get_ssid():
    try:
        scanoutput = check_output(["sudo", "iwconfig", "wlan0"])
        for line in scanoutput.split():
            if line.startswith(b"ESSID"):
                ssid = line.split(b'"')[1]
        return ssid
    except:
        return None

def get_ip(ifname):
    import socket,struct,fcntl
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

def ip():
    try:
        ipchr=get_ip('wlan0')
    except:
        ipchr='0.0.0.0'
    return ipchr

def lcd_draw_string(splash,x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True, background_color=(0,0,0)):
    splash.text((x,y),text,fill =color,font = scale) 

def lcd_rect(x,y,w,h,color,thickness):
    draw.rectangle([(x,y),(w,h)],fill=color,width=thickness)

#-------------------------init UI---------------------------------
wifiy = Image.open("./pics/wifi@2x.jpg")
wifin = Image.open("./pics/wifi-un@2x.jpg")
cn = Image.open("./pics/edu.png")
uncn = Image.open("./pics/unedu.png")
lcd_rect(0,195,320,240,(48,50,73),thickness=-1)


#--------------------------get IP&SSID--------------------------
ipadd=ip()
ssid=get_ssid()
print(ipadd)

if ipadd=='0.0.0.0':
    print('wlan disconnected')
    splash.paste(wifin,(65,200))
    lcd_draw_string(draw,100, 200, la['EDUBLOCK']['NONET'], color=color_white, scale=font2)
else:
    print('wlan connected')
    splash.paste(wifiy,(65,200))
    lcd_draw_string(draw,100, 200, ipadd, color=color_white, scale=font2)


display.ShowImage(splash)

import subprocess
import threading

status=0
cmd=b''
order='node /home/pi/Edublocks/server/build/index.js'
pi= subprocess.Popen(order,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
mark=True
running=True
status=0
exitcode=False

status=0

def checks():
    global cmd
    for i in iter(pi.stdout.readline,'b'):
        cmd=i
        if cmd!=b'':
            print(cmd)
        if exitcode:
            break
            

t = threading.Thread(target=checks)
t.start()

def display_status():
    global status,exitcode
    nowstatus=0
    while 1:
        if exitcode:
            break
        if status==nowstatus:
            pass
        else:
            nowstatus=status
            if nowstatus==1:
                splash.paste(uncn,(0,0))
                display.ShowImage(splash)
            elif nowstatus==2:
                splash.paste(uncn,(0,0))
                display.ShowImage(splash)
            elif nowstatus==3:
                splash.paste(cn,(0,0))
                display.ShowImage(splash)


t = threading.Thread(target=display_status)
t.start()

print('---------------')
launch=0
linked=0

while 1:
    if button.press_b():
        exitcode=True
        break
    if cmd[0:6]==b'Launch':
        if launch==0:
            print('server success')
            status=1
        launch=1
        linked=0
    elif cmd[0:6]==b'Device':
        status=2
        print('disconnect')
        launch=1
        linked=0
    elif cmd[0:12]==b'Successfully':
        if linked==0:
            status=3
            print('linked!')
        linked=1
        launch=1

print('aiblocks over')
os.system('sudo fuser -k -n tcp 8081')
print('8081 killed!')
sys.exit()

