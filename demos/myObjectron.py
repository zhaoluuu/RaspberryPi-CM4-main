#!/usr/bin/env python3
# encoding: utf-8
import mediapipe as mp
import cv2 as cv
import time

import xgoscreen.LCD_2inch as LCD_2inch
from PIL import Image
from xgolib import XGO
from key import Button

car = XGO(port="/dev/ttyAMA0", version="xgolite")

display = LCD_2inch.LCD_2inch()
display.clear()
splash = Image.new("RGB", (display.height, display.width), "black")
display.ShowImage(splash)
button = Button()


class Objectron:
    def __init__(self, staticMode=False, maxObjects=5, minDetectionCon=0.5, minTrackingCon=0.99):
        self.staticMode=staticMode
        self.maxObjects=maxObjects
        self.minDetectionCon=minDetectionCon
        self.minTrackingCon=minTrackingCon
        self.index=0
        self.modelNames = ['Shoe', 'Chair', 'Cup', 'Camera']
        self.mpObjectron = mp.solutions.objectron
        self.mpDraw = mp.solutions.drawing_utils
        self.mpobjectron = self.mpObjectron.Objectron(
            self.staticMode, self.maxObjects, self.minDetectionCon, self.minTrackingCon, self.modelNames[self.index])

    def findObjectron(self, frame):
        cv.putText(frame, self.modelNames[self.index], (int(frame.shape[1] / 2) + 30, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
        img_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.mpobjectron.process(img_RGB)
        if results.detected_objects:
            for id, detection in enumerate(results.detected_objects):
                self.mpDraw.draw_landmarks(frame, detection.landmarks_2d, self.mpObjectron.BOX_CONNECTIONS)
                self.mpDraw.draw_axis(frame, detection.rotation, detection.translation)
        return frame

    def configUP(self):
        self.index += 1
        if self.index>=4:self.index=0
        self.mpobjectron = self.mpObjectron.Objectron(
            self.staticMode, self.maxObjects, self.minDetectionCon, self.minTrackingCon, self.modelNames[self.index])

if __name__ == '__main__':
    capture = cv.VideoCapture(0)
    capture.set(6, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
    print("capture get FPS : ", capture.get(cv.CAP_PROP_FPS))
    pTime = cTime = 0
    objectron = Objectron()
    while capture.isOpened():
        ret, frame = capture.read()
        # frame = cv.flip(frame, 1)
        action = cv.waitKey(1) & 0xFF
        if action == ord('q'): break
        if action == ord('f') or action == ord('F') : objectron.configUP()
        
        # 按屏幕的按键进行切换 Press the buttons on the screen to switch
        if button.press_d():
            objectron.configUP()

        frame = objectron.findObjectron(frame)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        text = "FPS : " + str(int(fps))
        cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        #cv.imshow('frame', frame)

        
        b, g, r = cv.split(frame)
        image = cv.merge((r, g, b))
        imgok = Image.fromarray(image)
        display.ShowImage(imgok)
        if button.press_b():
            break


    capture.release()
    cv.destroyAllWindows()
