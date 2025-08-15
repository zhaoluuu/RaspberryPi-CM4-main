import os,socket,sys,time
import spidev as SPI
import xgoscreen.LCD_2inch as LCD_2inch
from PIL import Image,ImageDraw,ImageFont
from key import Button
import numpy as np

import sys
sys.path.append("..")
import uiutils
la=uiutils.load_language()

display = LCD_2inch.LCD_2inch()
display.clear()
splash = Image.new("RGB", (display.height, display.width ),"black")
display.ShowImage(splash)
button=Button()
zhy = False

import pyzbar.pyzbar as pyzbar
import cv2


def cv2AddChineseText(img, text, position, textColor=(200, 0, 200), textSize=10):
    if (isinstance(img, np.ndarray)):  
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("/home/pi/model/msyh.ttc", textSize, encoding="utf-8")
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
 
def makefile(s,p):
    t1='''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CN

network={
    ssid="'''
    t2='''
    key_mgmt=WPA-PSK
    }
    '''
    t3='''"
    psk="'''
    files=t1+s+t3+p+'"'+t2
    print(files)
    return files

font = cv2.FONT_HERSHEY_SIMPLEX 
cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
if(not cap.isOpened()):
    print("[camera.py:cam]:can't open this camera")

wifi="/etc/wpa_supplicant/wpa_supplicant.conf"

with open(wifi, 'r') as f:
    content=f.read()
    print(content)
    s=content.find('ssid=')
    print(s)
    end=s+6
    while content[end]!='"':
        end+=1
    ssid=content[s+6:end]
    p=content.find('psk=')
    end=p+5
    while content[end]!='"':
        end+=1
    pwd=content[p+5:end]

found = False

while(True):
    ret, img = cap.read() 
    img_ROI_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(img_ROI_gray) 

    if len(barcodes) == 0:
        print('useless data')
        text = "{}".format(la['NETWORK']['NOQR'])
        img=cv2AddChineseText(img,text, (10, 30),(255, 0, 0),50)
        found = False
    else:
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            if len(barcodeData) == 0:
                pass
            elif len(barcodeData) != 0:
                count_space = barcodeData.count(" ")
                print(count_space)
                if count_space != 0:
                    print('space')
                    text = "{}".format(la['NETWORK']['SPACE'])
                    img=cv2AddChineseText(img,text, (10, 30),(0, 0, 255),45)
                    break
                else:
                    a = barcodeData.find("S:")
                    b = barcodeData.find(";T:")
                    SSID = barcodeData[a+2:b]
                    print(SSID)
                    print(SSID.count(" "))
                    c = barcodeData.find("P:")
                    d = len(barcodeData)
                    PWD = barcodeData[c+2:d-9]
                    print(PWD)
                    print(PWD.count(" "))
                    fc=makefile(SSID,PWD)
                    with open(wifi, 'w') as f:
                        f.write(fc)
                    text = "{}".format(la['NETWORK']['SUCCESS'])
                    img=cv2AddChineseText(img,text, (10, 30),(0, 255, 0), 50)
                    #..
                    b,g,r = cv2.split(img)
                    img = cv2.merge((r,g,b))
                    imgok = Image.fromarray(img)
                    display.ShowImage(imgok)
                    time.sleep(0.5)
                    found = True
                    #sys.exit()
                    break
    if found:
        os.system("sudo wpa_cli -i wlan0 reconfigure")
        time.sleep(1)
        break
    else:
        print('None')
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    imgok = Image.fromarray(img)
    display.ShowImage(imgok)
    
    if button.press_c():
        ssid='XGO2'
        pwd='LuwuDynamics'
        fc=makefile(ssid,pwd)
        with open(wifi, 'w') as f:
            f.write(fc)
    if (cv2.waitKey(1)) == ord('q'):
        break
    if button.press_b():
        break
print('network')
cap.release()
cv2.destroyAllWindows() 
