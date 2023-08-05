import cv2

import time
import random
import pygame
from pygame.constants import *
from friut.game import game
from friut.bgm import bgm
from friut.pose_detector import posedetector
from friut.background import background
from friut.knife import knife






def main():
    fps = 60
    g=game()
    g.bgm_.play_menu()
    
    pd=posedetector()
    start_pos=""
    end_pos=""
    pTime = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("摄像头读取出错.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        g.clock.tick(fps)
        g.background_list.update()
        g.knife_.update()
        g.throw_fruit_list.update()

        # cTime = time.time()
        # if (cTime-pTime) > 0.5:
        #     pTime=cTime
        #     image = cv2.flip(image, flipCode=1) 
        #     attach_result=pd.attach(image)
        #     if attach_result:
        #         if start_pos=="":
        #             start_pos=pd.point(19)
        #         else:
        #             pos=pd.point(19)
        #             if pos[1]<start_pos[1]: #为了游戏便于游玩，规定只能从上往下切
        #                 start_pos=pos
        #             else:
        #                 g.undercut(start_pos,pos)
        #                 start_pos=""
        image = cv2.flip(image, flipCode=1) 
        attach_result=pd.attach(image)
        if attach_result:
            pos=pd.point(19,(g.width,g.height))
            if start_pos=="":
                start_pos=pos
                end_pos=""
            elif pos[1]>start_pos[1]:
                end_pos=pos
            elif start_pos!="" and end_pos!="":
                g.undercut(start_pos,end_pos)
                start_pos=""
                end_pos=""
            else:
                start_pos=""
                end_pos=""
                    
           
            
        
        g.check_key()
        pygame.display.update()

    cap.release()

if __name__ == '__main__':
    main()

