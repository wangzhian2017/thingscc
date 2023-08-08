import cv2
import pygame
from pygame.constants import *
from friut.game import game
from friut.pose_detector import posedetector


# pyinstaller -F friut_cut.py



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
        g.update()

        image = cv2.flip(image, flipCode=1) 
        attach_result=pd.attach(image)
        if attach_result:
            pos=pd.point(19,(g.width,g.height))
            pygame.draw.circle(g.screen, (255, 255, 255), pos,5)
            if start_pos=="" or abs(pos[1]-start_pos[1])<3 or abs(pos[0]-start_pos[0])<3:
                start_pos=pos
                end_pos=""
            elif abs(pos[1]-start_pos[1])>50 or abs(pos[0]-start_pos[0])>50:
                g.undercut(start_pos,pos)
                start_pos=""
                end_pos=""
           
                    
           
            
        
        g.check_key()
        pygame.display.update()

    cap.release()

if __name__ == '__main__':
    main()

