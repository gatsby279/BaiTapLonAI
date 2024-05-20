import cv2 as cv
import HandTrackingModule as htm
from Mouse import  Mouse_Control
from Keyboard import Keyboard_Control
from time import sleep

# khởi động cam và cài đặt kích thước khung hình
cap = cv.VideoCapture(0)
success, _ = cap.read()
if success is False:
    cap = cv.VideoCapture(0)
    success, _ = cap.read()
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# giá trị click
right = 30
left = 80

# Khởi tạo bộ phát hiện tay
detector = htm.handDetector()

# khởi tạo bộ bàn phím
keyboard = Keyboard_Control()

# khởi tạo bộ điều khiển chuột
mouse = Mouse_Control(wCam, hCam)

while True:
    # Chụp khung hình từ camera
    success, img = cap.read()
    img = cv.flip(img, 1)  # lật khung hình

    # Phát hiện tay
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if lmList:
        # Lấy trạng thái của các ngón tay
        fingers = detector.fingersUp()
        # Lấy tọa độ của ngón trỏ và ngón giữa
        x1, y1 = lmList[8][1:]  # ngón trỏ
        x2, y2 = lmList[12][1:]  # ngón giữa
        x3, y3 = lmList[4][1:]  # ngón cái
        # Tìm khoảng cách giữa ngón trỏ - ngón giữa và ngón trỏ - ngón cái
        distance_click, img, infoLine_click = detector.findDistance((x1, y1), (x2, y2), img, fingers[2] == 1)
        distance_scroll, img, infoLine_scroll = detector.findDistance((x1, y1), (x3, y3), img, fingers[0] == 1)

        # BÀN PHÍM: NGÓN ÚT DUỖI
        if fingers[4] == 1:
            # vẽ bàn phím ảo
            img = keyboard.draw_keyboard(img)
            # lựa chọn nút
            try:
                img, pos, size, text = keyboard.select_button(img, (x1, y1))
                # click nút
                if distance_click < right:
                    img = keyboard.click_button(img, pos, size, text)
                    sleep(0.1)
            except:
                img = keyboard.select_button(img, (x1, y1))

        # SCROLL CHUỘT: NGÓN TRỎ VÀ NGÓN CÁI ĐỀU DUỖI
        elif fingers[0] == 1 and fingers[1] == 1:
            # scroll chuột
            if distance_scroll < right or distance_scroll > left:
                # thiết lập cờ xác định scroll lên - xuống
                if distance_scroll < right: flag_scroll = True  # lên
                elif distance_scroll > left: flag_scroll = False    # xuống
                img = mouse.scroll_mouse(img, (infoLine_scroll[4], infoLine_scroll[5]), flag_scroll)

        # DI CHUYỂN CHUỘT: NGÓN TRỎ DUỖI, NGÓN GIỮA NẮM
        elif fingers[1] == 1 and fingers[2] == 0:
            img = mouse.moving_mouse(img, (x1, y1))

        # CLICK CHUỘT: CẢ NGÓN TRỎ VÀ NGÓN GIỮA ĐỀU DUỖI
        elif fingers[1] == 1 and fingers[2] == 1:
            # click chuột
            if distance_click < right or distance_click > left:
                # thiết lập cờ xác định click trái - phải
                if distance_click < right: flag_click = True  # trái
                elif distance_click > left: flag_click = False  # phải
                img = mouse.click_mouse(img, (infoLine_click[4],infoLine_click[5]), flag_click)
                sleep(0.1)


    # hiển thị
    if img is not None and img.size > 0:
        cv.imshow("Hand Tracking Mouse Control", img)
    cv.waitKey(1)