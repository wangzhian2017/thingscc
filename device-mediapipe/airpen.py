# -*- coding:utf-8 -*-

import cv2
from hand_detector import handdetector
import numpy
import time

def drawLine(canvas,start,end):
    if (start != ""):
        cv2.line(canvas,start,end,(0,255,0),3)

def main():
    canvas_size=(640,480)
    canvas = numpy.zeros((canvas_size[1],canvas_size[0],3),numpy.uint8)
    ready=False
    hand_width=0 #手掌四指宽度
    pen_postion = "" 
    point8=""
    point8_style={"color":(0, 0, 255),"radius":1}
    hd = handdetector()
    
    cv2.namedWindow("Air Pen",cv2.WINDOW_NORMAL)
    #手势识别：打开摄像头并读取视频帧，将每一帧传递给hands.process()方法进行手势识别。
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while cap.isOpened():
        ret, img = cap.read()  # 读取视频帧
        if not ret:
            break
        img = cv2.flip(img, flipCode=1) 
        attach_result=hd.attach(img,draw=False)
        if attach_result:
            point8 = hd.point(8) #食指顶点
            
            direction=hd.analy_direction()
            print(direction)
            if not ready:
                point8_style={"color":(0, 0, 255),"radius":1}
                if direction==[0, 1, 0, 0, 0] or direction==[1, 1, 0, 0, 0] :
                    hand_width=hd.distance(5,17)
                    ready=True
            if ready:
                if hd.is_ok(): # 清除画布，重新开始
                    canvas = numpy.zeros((canvas_size[1],canvas_size[0],3),numpy.uint8)
                    pen_postion = ""
                    ready=False

                    point8_style={"color":(0, 0, 255),"radius":1}
                else:
                    h_w=hd.distance(5,17)
                    # print(h_w,hand_width)
                    if h_w > 1.2*hand_width: #手指靠近，开始画
                        drawLine(canvas,pen_postion,point8)
                        pen_postion = point8

                        point8_style={"color":(0,255,0),"radius":3}
                    elif h_w >= hand_width and (direction==[0, 1, 0, 0, 0] or direction==[1, 1, 0, 0, 0]):
                        drawLine(canvas,pen_postion,point8)
                        pen_postion = point8
                        point8_style={"color":(0,255,0),"radius":1}
                    else: #手指远离，停止画
                        pen_postion = ""
                        point8_style={"color":(0, 0, 255),"radius":1}


        #合并绘画
        h, w, c = img.shape
        canvas = cv2.resize(canvas, (w, h))
        img_gray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY) 
        _,img_inv = cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR) # 处理后重新转换会彩色图片
        img = cv2.bitwise_and(img,img_inv)
        img = cv2.bitwise_or(img,canvas)
        if(point8!=""):
            cv2.circle(img, point8, point8_style["radius"], point8_style["color"], cv2.FILLED)
        
        cv2.imshow("Air Pen", img)       #CV2窗体
        if cv2.waitKey(1)>0 :  #关闭窗体
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()