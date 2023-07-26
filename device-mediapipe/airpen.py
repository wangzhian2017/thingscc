# -*- coding:utf-8 -*-

import cv2
from hand_detector import handdetector
import numpy
import time



def main():
    canvas_size=(640,480)
    canvas = numpy.zeros((canvas_size[1],canvas_size[0],3),numpy.uint8)
    pen_postion = (0,0)
    pre_time = 0
    cur_time = 0
    hd = handdetector()
    
    cv2.namedWindow("Air Pen",cv2.WINDOW_NORMAL)
    #手势识别：打开摄像头并读取视频帧，将每一帧传递给hands.process()方法进行手势识别。
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while cap.isOpened():
        cur_time = time.time()
        ret, img = cap.read()  # 读取视频帧
        if not ret:
            break
        img = cv2.flip(img, flipCode=1) 
        attach_result=hd.attach(img,draw=False)
        if attach_result:
            direction=hd.analy_direction()
            print(direction)
            point = hd.point(8) #食指顶点
            cv2.circle(img, point, 5, (255, 0, 255), cv2.FILLED)
            if direction==[0, 1, 0, 0, 0] :
                if (pen_postion == (0,0)):
                    pen_postion = point
                cv2.line(canvas,pen_postion,point,(0,255,0),5)
                pen_postion = point
                pre_time = cur_time
            elif hd.is_ok():
                canvas = numpy.zeros((canvas_size[1],canvas_size[0],3),numpy.uint8)
                pen_postion = (0,0)
            elif (cur_time - pre_time)>1:
                pen_postion = (0,0)


        #合并绘画
        h, w, c = img.shape
        canvas = cv2.resize(canvas, (w, h))
        img_gray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY) 
        _,img_inv = cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR) # 处理后重新转换会彩色图片
        img = cv2.bitwise_and(img,img_inv)
        img = cv2.bitwise_or(img,canvas)
        
        cv2.imshow("Air Pen", img)       #CV2窗体
        if cv2.waitKey(1)>0 :  #关闭窗体
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()