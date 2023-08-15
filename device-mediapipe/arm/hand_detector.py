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

    def attach(self, img,handNo=0, draw=True):
        """
        关联手掌
        :param img:要识别的一帧图像
        :param draw:是否对手的标志点进行绘图
        """
        self.attach_img=img
        self.key_points = []
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
    

    def hamming_distance(self,p1,p2):
        if len(self.key_points)<=0:
            return -1
        d=abs(self.key_points[p1][0]-self.key_points[p2][0])+abs(self.key_points[p1][1]-self.key_points[p2][1])
        return d
    
    #判断5个手指是否伸直, 1:伸直 0:弯曲
    def analy_direction(self):
        direction=[] 
        for i in range(0, 5):
            if self.is_finger_open(i):
                direction.append(1)
            else:
                direction.append(0)
            
        return direction
    
    def is_finger_open(self,index):
        '''
        index: 0拇指 1食指 2中指 3无名指 4小指
        '''
        if len(self.key_points)<=0:
            return False
        
        # 通过判断手指尖与手指根部(0点)到位置点的距离判断手指是否伸开(拇指检测到17点的距离)
        if index==0:
            d1=self.hamming_distance(self.tipIds[0],17)
            d2=self.hamming_distance(self.tipIds[0]-1,17)
            if(d1<d2):
                return False
            else:
                d1=self.hamming_distance(self.tipIds[0],5)
                d2=self.hamming_distance(self.tipIds[0]-1,5)
                if(d1<d2):
                    return False
                else:
                    return True
        elif index==1 or index==2 or index==3 or index==4:
            d1=self.hamming_distance(self.tipIds[index],0)
            d2=self.hamming_distance(self.tipIds[index]-1,0)
            if(d1>d2):
                return True
            else:
                return False
            
        return False

        

    #是否OK手势
    def is_ok(self):
        open2=self.is_finger_open(2)
        open3=self.is_finger_open(3)
        open4=self.is_finger_open(4)
        if open2==1 and open3==1 and open4==1:
            open0=self.is_finger_open(0)
            open1=self.is_finger_open(1)
            if open0==0 and open1==0:
                return True
            elif open1==0:
                d1=self.hamming_distance(6,8)
                d2=self.hamming_distance(4,8)
                if(d1>d2):
                    return True;

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
    
    def distance(self,p1,p2):
        if len(self.key_points)<=0:
            return -1
        d_x=self.key_points[p1][0]-self.key_points[p2][0]
        d_y=self.key_points[p1][0]-self.key_points[p2][0]
        d=math.hypot(d_x,d_y)
        return d
    
    def point(self,index):
        return (self.key_points[index][0],self.key_points[index][1])
