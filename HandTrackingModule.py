import cv2
import mediapipe as mp
import math


class handDetector():
    def __init__(self):
        self.hand_module = mp.solutions.hands
        self.hand_object = self.hand_module.Hands()
        self.drawing_util = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.hand_process = self.hand_object.process(imgRGB)
        self.hands = self.hand_process.multi_hand_landmarks

        if self.hands:
            for hand in self.hands:
                self.drawing_util.draw_landmarks(img, hand, self.hand_module.HAND_CONNECTIONS)

        return img

    def findPosition(self, img):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.hands:
            hand = self.hands[0]
            for id, point in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(point.x * w), int(point.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),(0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # ngón cái
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # các ngón còn lại
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, pos1, pos2, img, draw=True,r=5, t=3):
        x1, y1 = pos1
        x2, y2 = pos2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        distance = math.hypot(x2 - x1, y2 - y1)

        return distance, img, (x1, y1, x2, y2, cx, cy)

