import cv2 as cv
import pyautogui
import numpy as np

class Mouse_Control:
    def __init__(self, wCam, hCam):
        self.screenControl = 100  # Khoảng cách điều khiển màn hình
        self.smoothening = 2    # hệ số làm mượt
        self.wCam, self.hCam = wCam, hCam
        self.wScr, self.hScr = pyautogui.size()    # Kích thước màn hình
        self.newLocX, self.newLocY = self.wScr / 2, self.hScr / 2
        self.oldLocX, self.oldLocY = self.wScr / 2, self.hScr / 2

    def moving_mouse(self, img, pos):
        # vẽ khung điều khiển
        cv.rectangle(img, (self.screenControl, self.screenControl - 50), (self.wCam - self.screenControl, self.hCam - self.screenControl - 80),
                     (255, 255, 255), 2)
        # Chuyển đổi tọa độ sang kích thước màn hình
        mouse_x = np.interp(pos[0], (self.screenControl, self.wCam - self.screenControl), (0, self.wScr))
        mouse_y = np.interp(pos[1], (self.screenControl - 50, self.hCam - self.screenControl - 90), (0, self.hScr))
        # Làm mượt chuyển động chuột
        newLocX = self.oldLocX + (mouse_x - self.oldLocX) / self.smoothening
        newLocY = self.oldLocY + (mouse_y - self.oldLocY) / self.smoothening
        # Di chuyển chuột
        pyautogui.moveTo(newLocX, newLocY)
        cv.circle(img, (pos[0], pos[1]), 5, (0, 0, 255), cv.FILLED)
        # Cập nhật vị trí cũ
        self.oldLocX, self.oldLocY = newLocX, newLocY
        return img

    def click_mouse(self, img, pos, flag):
        if flag == True: pyautogui.click()   # click chuột trái
        else: pyautogui.rightClick()    # click chuột trái
        cv.circle(img, pos, 5, (0, 255, 0), cv.FILLED)  # vẽ vòng tròn xanh báo hiệu click
        return img

    def scroll_mouse(self,img, pos, flag):
        if flag == True: pyautogui.scroll(100)
        else: pyautogui.scroll(-100)
        cv.circle(img, pos, 5, (0, 255, 0), cv.FILLED)  # vẽ vòng tròn xanh báo hiệu click
        return img






