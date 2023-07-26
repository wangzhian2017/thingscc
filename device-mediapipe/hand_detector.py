# -*- coding:utf-8 -*-
import cv2
import mediapipe as mp
import math


class handdetector:
    def __init__(self, mode=False, max_hands=1, detectionCon=1, minTrackCon=0.5):
        """
        初始化参数
        :param mode: 是否输入静态图像
        :param maxhands: 检测到手的最大数量
        :param detectionCon: 检测手的置信度
        :param trackCon: 追踪手的置信度
        :param modelcomplex为模型的复杂度
        :param detectioncon和trackcon为置信度阈值，越大越准确
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detectionCon = detectionCon
        self.min_trackCon = minTrackCon
        #self.modelComplex=modelComplexity
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands,
                                        self.detectionCon, self.min_trackCon)
        self.mp_draw = mp.solutions.drawing_utils
        
        
        self.tipIds = [4, 8, 12, 16, 20]#对应手指的指尖
        self.attach_img=[]
        self.key_points = []
        self.direction=[] #5个手指是否伸直, 1:伸直 0:弯曲

    def attach(self, img,handNo=0, draw=True):
        """
        关联手掌
        :param img:要识别的一帧图像
        :param draw:是否对手的标志点进行绘图
        """
        self.attach_img=img
        self.key_points = []
        self.direction=[] 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换颜色空间
        results = self.hands.process(imgRGB)  # 手势识别
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                px, py,pz = int(lm.x * w), int(lm.y * h),lm.z
                self.key_points.append([px, py,pz])

            if draw:
                for handLms in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)  # 用于指定地标如何在图中连接。
      
        return (len(self.key_points)>0)

    def hand_size(self, draw=False):
        xList = []
        yList = []
        for x,y,z in self.key_points:
            xList.append(x)
            yList.append(y)
            if draw:
                cv2.circle(self.attach_img, (x, y), 5, (255, 0, 255), cv2.FILLED)  # 画出关键点

        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        if draw:
            margin=0
            cv2.rectangle(self.attach_img, 
                            (xmin - margin, ymin - margin),
                            (xmax + margin,  ymax + margin),
                            (0, 255, 0), 2)
        return xmin, ymin,xmax,ymax,xmax-xmin,ymax-ymin
    

    def dinstance(self,p1,p2):
        return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
    
    #判断5个手指是否伸直, 1:伸直 0:弯曲
    def analy_direction(self):
        if len(self.direction)<=0:
            if len(self.key_points)>0:
                # 通过判断手指尖与手指根部(0点)到位置点的距离判断手指是否伸开(拇指检测到17点的距离)
                d1=self.dinstance(self.key_points[self.tipIds[0]],self.key_points[17])
                d2=self.dinstance(self.key_points[self.tipIds[0]-1],self.key_points[17])
                if(d1<d2):
                    self.direction.append(0)
                else:
                    d1=self.dinstance(self.key_points[self.tipIds[0]],self.key_points[5])
                    d2=self.dinstance(self.key_points[self.tipIds[0]-1],self.key_points[5])
                    if(d1<d2):
                        self.direction.append(0)
                    else:
                        self.direction.append(1)
                # 4 Fingers
                for i in range(1, 5):
                    d1=self.dinstance(self.key_points[self.tipIds[i]],self.key_points[0])
                    d2=self.dinstance(self.key_points[self.tipIds[i]-1],self.key_points[0])
                    if(d1>d2):
                        self.direction.append(1)
                    else:
                        self.direction.append(0)
        return self.direction
    
    #是否OK手势
    def is_ok(self):
        direction=self.analy_direction()
        if(direction==[0, 0, 1, 1, 1]):
            return True
        else:
            return False
        
    # 判别左右手，需要做一个OK手势进行判断  
    def is_right_or_left(self):
        if not self.is_ok():
            return "none" #未知
        
        if len(self.key_points)>0:
            if self.key_points[17][0] > self.key_points[5][0]:
                return "right" #右手
            else:
                return "left" #左手
            
    #判断手掌朝前还是手背朝前     
    def is_front_or_back(self,is_right):
        if is_right:
            if self.key_points[5][0] <= self.key_points[17][0]:
                return "front" #手掌朝前
            else:
                return "back" #手背朝前
        else:
            if self.key_points[5][0] >= self.key_points[17][0]:
                return "front" #手掌朝前
            else:
                return "back" #手背朝前
    
    def distance(self,index1,index2):
        d=self.dinstance(self.key_points[index1],self.key_points[index2])
        d=math.sqrt(d)
        return d
    
    def point(self,index):
        return (self.key_points[index][0],self.key_points[index][1])
