# -*- coding:utf-8 -*-
import cv2
import numpy as np
import requests #  import grequests as requests
from queue import Queue
import threading
from hand_detector import handdetector
import time

base_url="http://master.thingscc.com:8080"
product_id="iqDUVzCjyD"
device_name="esp32c3"



grab_queue = Queue(3)
lift_queue = Queue(3)
rotate_queue = Queue(3)
backforward_queue = Queue(3)
def call_service(identifier,json_param):
    try:
        print(identifier,json_param)
        url=base_url+"/device/onnet/service/"+product_id+"/"+device_name+"/"+identifier
        r = requests.post(url,json = json_param, headers= {'Content-Type':'application/json;charset=UTF-8'})
        # print(r.json())
       
        return r.json()
    except:
        print('call_service网络请求异常')

def call_service_task():
    while True:
        if not grab_queue.empty() :
            obj = grab_queue.get()
            call_service(obj["identifier"],obj["param"])
            grab_queue.task_done()
        if not lift_queue.empty() :
            obj = lift_queue.get()
            call_service(obj["identifier"],obj["param"])
            lift_queue.task_done()
        if not rotate_queue.empty() :
            obj = rotate_queue.get()
            call_service(obj["identifier"],obj["param"])
            rotate_queue.task_done()
        if not backforward_queue.empty() :
            obj = backforward_queue.get()
            call_service(obj["identifier"],obj["param"])
            backforward_queue.task_done()

def grab(angle):
    angle=round(angle,2)
    param={'angle':angle}
    #return call_service('grab',param)
    if grab_queue.full()==False:
        grab_queue.put({"identifier":"grab","param":param})

def lift(angle):
    angle=round(angle,2)
    param={'angle':angle}
    #return call_service('lift',param)
    if lift_queue.full()==False:
        lift_queue.put({"identifier":"lift","param":param})


def rotate(angle):
    angle=round(angle,2)
    param={'angle':angle}
    #return call_service('rotate',param)
    if rotate_queue.full()==False:
        rotate_queue.put({"identifier":"rotate","param":param})

def backforward(angle):
    angle=round(angle,2)
    param={'angle':angle}
    #return call_service('backforward',param)
    if backforward_queue.full()==False:
        backforward_queue.put({"identifier":"backforward","param":param})


pre_time = 0
cur_time = 0
def process(hd,frame_shape,center,width,min_pinch): 
    global pre_time,cur_time
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
        angle=np.interp(x,[min_x,max_x],[180,0])
        rotate(angle)
        angle=np.interp(y,[min_y,max_y],[95,10])
        lift(angle)
        #手掌宽度
        min_palm_width=3*width/4
        max_palm_width=7*width/4
        palm_width=hd.distance(5,17)#手掌四指宽度
        angle=np.interp(palm_width,[min_palm_width,max_palm_width],[75,140])
        backforward(angle)
        #食指与拇指 捏在一起的程度
        pinch=hd.distance(8,4)
        max_pinch=2*hd.distance(17,0)
        angle=np.interp(pinch,[min_pinch,max_pinch],[122,0])
        grab(angle)

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
        attach_result=hd.attach(frame)
        if attach_result:
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
        
        cv2.imshow("sensor", frame)       #CV2窗体
        if cv2.waitKey(1)>0 :  #关闭窗体
            break
    cap.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()