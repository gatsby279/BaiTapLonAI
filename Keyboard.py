import numpy as np
import cvzone
import cv2
from pynput.keyboard import Controller


class Button:
    # khởi tạo
    def __init__(self, pos, text, size=[40, 40]):
        self.pos = pos  # vị trí của các nút
        self.text = text  # tên nút
        self.size = size  # kích thước


class Keyboard_Control:
    def __init__(self):
        # tạo danh sách các nút mong muốn
        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                     ["A", "S", "D", "F", "G", "H", "J", "K", "L", "dl"],
                     ["Z", "X", "C", "V", "B", "N", "M", ",", ".", " "]]
        # tạo nút
        self.buttonList = []
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                self.buttonList.append(Button([50 * j + 20, 50 * i + 50], key))
        # tạo đối tượng can thiệp vào phím
        self.keys_control = Controller()

    def draw_keyboard(self, img):
        imgNew = np.zeros_like(img, np.uint8)
        for button in self.buttonList:
            x, y = button.pos
            cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                              10, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                          (255, 0, 255), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 9, y + 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        out = img.copy()
        alpha = 0.1
        mask = imgNew.astype(bool)
        #print(mask.shape)
        out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
        return out

    def select_button(self, img, pos):
        for button in self.buttonList:
            x, y = button.pos
            w, h = button.size
            if x < pos[0] < x + w and y < pos[1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 9, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
                return img, button.pos, button.size, button.text
        return img

    def click_button(self, img, pos, size, text):
        x, y = pos
        w, h = size
        self.keys_control.press(text)
        cv2.rectangle(img, pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, text, (x + 9, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
        return img