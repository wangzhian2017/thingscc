# -*- coding:utf-8 -*-
import cv2
import numpy as np
from queue import Queue
import threading
from arm.hand_detector import handdetector
import time
from arm.mechanical_arm import mechanical_arm

# base_url="http://localhost:8080/device/onnet"
base_url="https://ncoa-dev.cmhktry.com/gateway/smallfeat/OneNet"
product_id="iqDUVzCjyD"
device_name="esp32c3"
arm=mechanical_arm(base_url,product_id,device_name)

grab_queue = Queue(3)
position_move_queue = Queue(3)

def call_service_task():
    while True:
        if not position_move_queue.empty() :
            obj = position_move_queue.get()
            arm.position_move(obj["param"]["angle1"],obj["param"]["angle2"],obj["param"]["angle3"])
            position_move_queue.task_done()
        if not grab_queue.empty() :
            obj = grab_queue.get()
            arm.grab(obj["param"]["angle"])
            grab_queue.task_done()
        
      

def grab(angle):
    param={'angle':angle}
    #return call_service('grab',param)
    if grab_queue.full()==False:
        grab_queue.put({"identifier":"grab","param":param})

def position_move(angle1,angle2,angle3):
    param={'angle1':angle1,'angle2':angle2,'angle3':angle3}
    #return call_service('position_move',param)
    if position_move_queue.full()==False:
        position_move_queue.put({"identifier":"position_move","param":param})



pre_time = 0
cur_time = 0
last_grab_angle=0
last_position_angle1=0
last_position_angle2=0
last_position_angle3=0
def process(hd,frame_shape,center,width,min_pinch): 
    global pre_time,cur_time,last_grab_angle,last_position_angle1,last_position_angle2,last_position_angle3
    cur_time=time.time()
    if  (cur_time - pre_time)>1:
        h, w, c =frame_shape #画板大小
        center_x,center_y =center
        min_x,min_y=0,0
        max_x,max_y=w,h
        if center_x>w/2:
            min_x=center_x-w
        else:
            max_x=center_x+w
        if center_y>h/2:
            min_y=center_y-h/8
        else:
            max_y=center_y+7*h/8
        x,y=hd.point(5) #掌心位置
        angle1=np.interp(x,[min_x,max_x],[180,0])
        angle3=np.interp(y,[min_y,max_y],[95,10])

        #手掌宽度
        min_palm_width=3*width/4
        max_palm_width=7*width/4
        palm_width=hd.distance(5,17)#手掌四指宽度
        angle2=np.interp(palm_width,[min_palm_width,max_palm_width],[75,140])
        if abs(last_position_angle1-angle1)>5 or abs(last_position_angle2-angle2)>5 or abs(last_position_angle3-angle3)>5 :
            position_move(angle1,angle2,angle3)
            last_position_angle1,last_position_angle2,last_position_angle3=angle1,angle2,angle3


        #食指与拇指 捏在一起的程度
        pinch=hd.distance(8,4)
        if hd.is_fist():
            pinch=min_pinch
        max_pinch=2*hd.distance(17,0)
        angle=np.interp(pinch,[min_pinch,max_pinch],[122,70])
        if abs(last_grab_angle-angle)>5 :
            grab(angle)
            last_grab_angle=angle
        
        

        pre_time=cur_time

    
def main():
    t = threading.Thread(target=call_service_task)
    t.setDaemon(True)
    t.start()

    ready=False
    hand_center=(0,0) 
    hand_width=0
    pinch=0
    hd = handdetector()

    cv2.namedWindow("sensor",cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while cap.isOpened():
        ret, frame = cap.read()  # 读取视频帧
        if not ret:
            break
        frame = cv2.flip(frame, flipCode=1) 
        attach_result=hd.attach(frame,draw=False)
        if attach_result:
            point = hd.point(5) 
            cv2.circle(frame, point, 3, (0, 255, 0), cv2.FILLED)
            point = hd.point(4) 
            cv2.circle(frame, point, 2, (0, 0, 255), cv2.FILLED)
            point = hd.point(8) 
            cv2.circle(frame, point, 2, (0, 0, 255), cv2.FILLED)

            if not ready and hd.is_ok():
                hand_center=hd.point(0) #掌心位置
                hand_width=hd.distance(5,17) #手掌四指宽度
                pinch=hd.distance(8,4) #食指与拇指 捏在一起的最小距离
                ready=True
                print("Ready GO!")

            if ready:
                process(hd,frame.shape,hand_center,hand_width,pinch)
        else:
            ready=False
        
        h, w, c =frame.shape
        cv2.line(frame,(0,int(h/2)),(w,int(h/2)),(200,200,200),1)
        cv2.line(frame,(int(w/2),0),(int(w/2),h),(200,200,200),1)
        
        
        cv2.imshow("sensor", frame)       #CV2窗体
        if cv2.waitKey(1)>0 :  #关闭窗体
            break
    cap.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()