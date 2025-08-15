from demos.uiutils import la,Button,lal,color_bg,color_unselect,color_select,display_cjk_string,draw,display,splash,font2,color_white,font1
import os,time
from PIL import Image
# Init Key
button = Button()

path = os.getcwd()


# const
firmware_info = "v1.0"



def lcd_rect(x, y, w, h, color, thickness):
    if thickness:
        draw.rectangle([(x, y), (w, h)], color, width=thickness)
    else:
        draw.rectangle([(x, y), (w, h)], fill=None, outline=color_bg, width=2)


lcd_rect(0, 0, 320, 240, color=color_bg, thickness=-1)
display.ShowImage(splash)

MENU_ITEM_PARENT_PATH = "./pics/"
MENU_ITEMS = [
        # pic kinds program show
        ("dog_show", "1movement", "dog_show", lal["DEMOEN"]["SHOW"]),
        ("network", "2vision", "network", lal["DEMOEN"]["NETWORK"]),
        ("mobile", "17vision", "MobileAPP", lal["DEMOEN"]["Mobile"]), #yahboom app control 
        ("xiaozhi", "3voice", "xiaozhi", lal["DEMOEN"]["XIAOZHI"]), 

        # 需要网络 Need network
        ("chatgpt2", "13vision", "chatgpt", lal["DEMOEN"]["CHATGPT"]),#chatgpt
        ("gpt_draw", "14vision", "gpt_draw", lal["DEMOEN"]["GPTDRAW"]),#文生图
        ("gpt_rec", "15vision", "gpt_rec", lal["DEMOEN"]["GPTREC"]),#图生文
        ("gpt_cmd", "18vision", "gpt_cmd", lal["DEMOEN"]["GPTCMD"]), #智能体
        ("draw_dog", "18vision", "anget_dog", lal["DEMOEN"]["ANGETDOG"]), #智能狗,结合摄像头的
        ("speech", "4voice", "speech", lal["DEMOEN"]["SPEECH"]),#语音控制
        ("speechAI", "16vision", "speechAI", lal["DEMOEN"]["SPEECHAI"]),#语音智能视觉
        ("ailine", "19vision", "speech_ai_line", lal["DEMOEN"]["AILINE"]),#巡线清障
        ("aicaw", "11vision", "speech_aicaw", lal["DEMOEN"]["AICAW"]),#抓取
        ("speech_football", "12vision", "speech_football", lal["DEMOEN"]["SFootBall"]),#踢球
        ("sp_track", "17vision", "speech_ai_track_food", lal["DEMOEN"]["AITRACK"]), #物体追踪
        
        

        # 离线AI Offline AI
        ("liPlate", "14vision","mycamera_license",lal['DEMOEN']['PLATE']),
        ("color", "10vision", "color", lal["DEMOEN"]["COLOR"]),
        ("ColorLine", "14vision","myfollow_line",lal['DEMOEN']['CLINE']),
        ("LineCaw", "14vision","mycolor_line_caw",lal['DEMOEN']['LINE_CAW']),
        ("pickup", "14vision","mypick_it_up",lal['DEMOEN']['CAWSPORT']),
        ("Football", "14vision","myplay_football",lal['DEMOEN']['FOOTBALLS']),
        ("BallF", "14vision","myBall_Follow",lal['DEMOEN']['BALLFORLLOW']),
        ("BallTR", "14vision","myBall_Tracking",lal['DEMOEN']['BALLTR']),
        
        
        ("yolo", "14vision","yolofast",lal['DEMOEN']['YOLO']), #yolo
        ("myobject", "14vision","myobject_recognition",lal['DEMOEN']['OBJECT']),
        ("3D", "14vision","myObjectron",lal['DEMOEN']['3DOBJECT']),
        
        ("qrcode", "11vision", "qrcode", lal["DEMOEN"]["QRCODE"]),
        ("QRSPORT", "14vision","myqr_sport",lal['DEMOEN']['QRSPORT']),
       
            
        ("sex", "14vision","mySexandAge",lal['DEMOEN']['AGE_SEX']),
        ("myFace01", "14vision","myFaceDetection",lal['DEMOEN']['FACEONE']),
        ("myFace02", "14vision","myFaceLandmarks",lal['DEMOEN']['FACETWO']),
        ("face_mask", "5vision", "face_mask", lal["DEMOEN"]["MASK"]),
        ("face_decetion", "6vision", "face_decetion", lal["DEMOEN"]["FACETRACK"]),

        ("FingerCtrl", "14vision","myFingerCtrl",lal['DEMOEN']['Finger']),
        ("GFollow", "14vision","myGesture_follows",lal['DEMOEN']['HANDSF']),
        ("hands", "7vision", "hands", lal["DEMOEN"]["HANDS"]),
        ("height", "8vision", "handh", lal["DEMOEN"]["HEIGHT"]),
        ("pose", "9vision", "pose_dog", lal["DEMOEN"]["POSE"]),
        ("segmentation", "6vision","segmentation",lal['DEMOEN']['SEGMENT']),
        ("vision", "2vision","teach_by_demon",lal['DEMOEN']['TEACH']),
        
        ("group", "17vision", "group", lal["DEMOEN"]["GROUP"]), #群组表演

        ("burn", "17vision","burn",lal['DEMOEN']['BURN']),
        ("wifi_set", "12vision", "wifi_set", lal["DEMOEN"]["WIFISET"]),
        ("language", "13vision", "language", lal["DEMOEN"]["LANGUAGE"]),
        ("volume", "14vision", "volume", lal["DEMOEN"]["VOLUME"]),
        ("device", "15vision", "device", lal["DEMOEN"]["DEVICE"]),
        ("imgmess", "14vision","system_img",lal['DEMOEN']['SYSTEMIMG']),
    ]

SELECT_BOX = [80, 68]
BASE_X = [0, 80, 160, 240]
BASE_Y = [36, 104, 172]

# Generate coordinates
MENU_ITEM_COORD = [[x, y, SELECT_BOX[0], SELECT_BOX[1]] for y in BASE_Y for x in BASE_X]
MENU_TEXT_COORD = [[x, y + 48] for y in BASE_Y for x in BASE_X]  
MENU_PIC_COORD = [[x + 26, y + 11] for y in BASE_Y for x in BASE_X] 

MENU_TOTAL_ITEMS = len(MENU_ITEMS) - 1
MENU_TOTAL_PAGES = MENU_TOTAL_ITEMS // 12
MENU_CURRENT_SELECT = 0
MENU_PAGE_SWAP_COUNT = 0

#print("CALC MENUS")
#print(MENU_TOTAL_ITEMS, MENU_TOTAL_PAGES)


def draw_item(row, type, realindex):
    item_coord = MENU_ITEM_COORD[row]
    pic_coord = MENU_PIC_COORD[row]
    text_coord = MENU_TEXT_COORD[row]
    item_text = MENU_ITEMS[realindex][3]
    text_len = len(item_text)
    text_offset = (10 - text_len) * 2 - 2
    
    # Adjust row for clearup/cleardown
    if type == "clearup":
        row -= 1
    elif type == "cleardown":
        row += 1
        if realindex == 28:
            realindex = 0
    
    # Get coordinates again if row changed
    if type in ("clearup", "cleardown"):
        item_coord = MENU_ITEM_COORD[row]
        pic_coord = MENU_PIC_COORD[row]
        text_coord = MENU_TEXT_COORD[row]
    
    if type == "selected":
        rect_color = color_select
        text_color = color_white
        bg_color = color_select
        thickness = 1
    else:  # unselected, clearup, cleardown
        rect_color = color_bg
        text_color = color_unselect
        bg_color = color_bg
        thickness = -1
    

    lcd_rect(
        item_coord[0],
        item_coord[1],
        item_coord[2] + item_coord[0],
        item_coord[3] + item_coord[1],
        color=rect_color,
        thickness=thickness
    )
    

    picpath = f"./pics/{MENU_ITEMS[realindex][0]}.png"
    nav_up = Image.open(picpath)
    draw.bitmap((pic_coord[0], pic_coord[1]), nav_up)
    
    display_cjk_string(
        draw,
        text_coord[0] + text_offset,
        text_coord[1],
        item_text,
        font_size=font1,
        color=text_color,
        background_color=bg_color
    )

def clear_page():
    print("clear page")
    lcd_rect(0, 36, 320, 240, color=color_bg, thickness=-1)


def draw_title_bar(index):
    lcd_rect(0, 0, 320, 35, color=color_bg, thickness=-1)
    draw.line((0, 35, 320, 35), color_unselect)
    display_cjk_string(
        draw,
        77,
        7,
        lal["DEMOEN"]["EXAMPLES"],
        font_size=font2,
        color=color_white,
        background_color=color_bg,
    )
    display_cjk_string(
        draw,
        203,
        7,
        str(index + 1) + "/" + str(MENU_TOTAL_ITEMS + 1),
        font_size=font2,
        color=color_white,
        background_color=color_bg,
    )


def draw_title_open():
    lcd_rect(0, 0, 320, 35, color=color_bg, thickness=-1)
    draw.line((0, 35, 320, 35), color_unselect)
    display_cjk_string(
        draw,
        85,
        7,
        lal["DEMOEN"]["OPENING"],
        font_size=font2,
        color=color_white,
        background_color=color_bg,
    )


def draw_title_error():
    lcd_rect(0, 0, 320, 35, color=color_bg, thickness=-1)
    draw.line((0, 35, 320, 35), color_unselect)
    display_cjk_string(
        draw,
        85,
        7,
        lal["DEMOEN"]["FAIL"],
        font_size=font2,
        color=color_white,
        background_color=color_bg,
    )


draw_title_bar(0)

for i in range(0, 12):
    draw_item(i, "unselected", i)
display.ShowImage(splash)
draw_item(0, "selected", 0)

display.ShowImage(splash)

inputkey = ""
while True:

    key_state_left = 0
    key_state_down = 0
    key_state_right = 0

    if button.press_a():
        key_state_down = 1
    elif button.press_c():
        key_state_left = 1
    elif button.press_d():
        key_state_right = 1
    elif button.press_b():
        os.system("pkill mplayer")
        break

    if key_state_left == 1:
        clear_page()
        if MENU_CURRENT_SELECT % 12 == 0:
            if MENU_PAGE_SWAP_COUNT == 0:
                MENU_PAGE_SWAP_COUNT = MENU_TOTAL_PAGES
                MENU_CURRENT_SELECT = MENU_TOTAL_ITEMS
            else:
                MENU_PAGE_SWAP_COUNT -= 1
                MENU_CURRENT_SELECT -= 1
        else:
            MENU_CURRENT_SELECT -= 1

        print(
            str(MENU_CURRENT_SELECT)
            + ", \t"
            + str(MENU_CURRENT_SELECT % 12)
            + ", "
            + str(MENU_PAGE_SWAP_COUNT)
        )

        draw_title_bar(MENU_CURRENT_SELECT)

        if MENU_PAGE_SWAP_COUNT == MENU_TOTAL_PAGES:
            for i in range(MENU_TOTAL_PAGES * 12, MENU_TOTAL_ITEMS + 1, 1):
                print(i)
                draw_item(i % 12, "unselected", i)
        else:
            for i in range(
                MENU_PAGE_SWAP_COUNT * 12, MENU_PAGE_SWAP_COUNT * 12 + 12, 1
            ):
                print(i)
                draw_item(i % 12, "unselected", i)

        draw_item(MENU_CURRENT_SELECT % 12, "selected", MENU_CURRENT_SELECT)

    if key_state_right == 1:
        clear_page()
        if MENU_CURRENT_SELECT == MENU_TOTAL_ITEMS:
            MENU_PAGE_SWAP_COUNT = 0
            MENU_CURRENT_SELECT = 0
        elif MENU_CURRENT_SELECT % 12 == 11:
            MENU_PAGE_SWAP_COUNT += 1
            MENU_CURRENT_SELECT += 1
        else:
            MENU_CURRENT_SELECT += 1

        print(
            str(MENU_CURRENT_SELECT)
            + ", \t"
            + str(MENU_CURRENT_SELECT % 12)
            + ", "
            + str(MENU_PAGE_SWAP_COUNT)
        )

        draw_title_bar(MENU_CURRENT_SELECT)

        if MENU_PAGE_SWAP_COUNT == MENU_TOTAL_PAGES:
            for i in range(MENU_TOTAL_PAGES * 12, MENU_TOTAL_ITEMS + 1, 1):
                print(i)
                draw_item(i % 12, "unselected", i)
        else:
            for i in range(
                MENU_PAGE_SWAP_COUNT * 12, MENU_PAGE_SWAP_COUNT * 12 + 12, 1
            ):
                print(i)
                draw_item(i % 12, "unselected", i)

        draw_item(MENU_CURRENT_SELECT % 12, "selected", MENU_CURRENT_SELECT)

    if key_state_down == 1:
        try:
            display.ShowImage(splash)
            print("Running: " + MENU_ITEMS[MENU_CURRENT_SELECT][2])
            draw_title_open()
            if MENU_ITEMS[MENU_CURRENT_SELECT][2] == "dog_show":
                import demos.dog_show
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="burn":
                os.system('python3 ./demos/ota.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="MobileAPP":
                os.system('python3 ./app/app_dogzilla.py')
            
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "face_mask":
                os.system("python3 ./demos/face_mask.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "hands":
                os.system(" python3 ./demos/hands.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "face_decetion":
                os.system("python3 ./demos/face_decetion.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "qrcode":
                os.system("python3 ./demos/qrcode.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "speech":
                os.system("python3 ./demos/speech/speech.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "handh":
                os.system("python3 ./demos/hp.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "color":
                os.system("python3 ./demos/color.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "wifi_set":
                os.system("python3 ./demos/wifi_set.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "device":
                os.system("python3 ./demos/device.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "network":
                os.system("python3 ./demos/network.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "language":
                os.system("python3 ./demos/language.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "volume":
                os.system("python3 ./demos/volume.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "xiaozhi":
                os.system("python3 ./demos/xiaozhi_test/main.py")
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] == "pose_dog":
                os.system("python3 ./demos/pose_dog.py")

            ####YAHBOOM####
            ##大模型!!
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="yolofast":
                os.system('python3 ./demos/myyolo.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="teach_by_demon":
                os.system('python3 ./demos/myteach_by_demon.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="segmentation":
                os.system('python3 ./demos/mysegmentation.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="mycamera_license":
                os.system('python3 ./demos/mycamera_license.py')            
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myFaceDetection":
                os.system('python3 ./demos/myFaceDetection.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myFaceLandmarks":
                os.system('python3 ./demos/myFaceLandmarks.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myFingerCtrl":
                os.system('python3 ./demos/myFingerCtrl.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myobject_recognition":
                os.system('python3 ./demos/myobject_recognition.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myObjectron":
                os.system('python3 ./demos/myObjectron.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="mySexandAge":
                os.system('python3 ./demos/mySexandAge.py')                    
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myBall_Follow":
                os.system('python3 ./demos/myBall_Follow.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myBall_Tracking":
                os.system('python3 ./demos/myBall_Tracking.py') 
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="mycolor_line_caw":
                os.system('python3 ./demos/mycolor_line_caw.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myfollow_line":
                os.system('python3 ./demos/myfollow_line.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myGesture_follows":
                os.system('python3 ./demos/myGesture_follows.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="mypick_it_up":
                os.system('python3 ./demos/mypick_it_up.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myplay_football":
                os.system('python3 ./demos/myplay_football.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="myqr_sport":
                os.system('python3 ./demos/myqr_sport.py')


            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="chatgpt":
                os.system('python3 ./demos/Free_QA/chatgpt_main.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="gpt_draw":
                os.system('python3 ./demos/Image_create/Image_main.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="gpt_rec":
                os.system('python3 ./demos/pic_comprehension/sp_AI_Image.py')
                
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="gpt_cmd":  
                if la == 'cn':
                    os.system('python3 ./demos/dog_agent/AIagent_go.py')
                else:
                    os.system('python3 ./demos/dog_agent/AIMain_en.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2] =="anget_dog":
                if la == 'cn':
                    os.system('python3 ./demos/dog_agent/AIagent_go_image.py')
                else:
                    os.system('python3 ./demos/dog_agent/AIMImage_en.py')

            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="speechAI":
                os.system('python3 ./demos/speechAI/speechAI.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="speech_ai_line":
                os.system('python3 ./demos/speech_AI_line/speech_AI_line.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="speech_aicaw":
                os.system('python3 ./demos/speech_AI_caw/speech_AI_caw.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="speech_football":
                os.system('python3 ./demos/speech_AI_football/speech_AI_football.py')
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="speech_ai_track_food":
                os.system('python3 ./demos/speech_AI_food/speech_AI_food.py')

            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="group":
                os.system('python3 ./demos/group.py')
                
            elif MENU_ITEMS[MENU_CURRENT_SELECT][2]=="system_img":
                os.system('python3 ./demos/system_img.py')
            

            print("program done")
            draw_title_bar(MENU_CURRENT_SELECT)
        except BaseException as e:
            print(str(e))
            draw_title_bar(MENU_CURRENT_SELECT)
        print("Key C Pressed.")
        time.sleep(0.5)
        draw_title_bar(MENU_CURRENT_SELECT)

    display.ShowImage(splash)

print("quit")
