import cv2
import math
import time
import pygame
from pygame.constants import *
from friut.bgm import bgm
from friut.pose_detector import posedetector
from friut.background import background
from friut.knife import knife

# 游戏中的定时器常量
THROWFRUITTIME = pygame.USEREVENT+1
def check_key():
    """ 监听事件 """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            print(event)
        elif event.type == THROWFRUITTIME:
            print("create_fruit")
            # create_fruit()

def main():
    # 窗口尺寸
    width = 640
    height = 480
    fps = 20
    pygame.init()
    screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
    icon = pygame.image.load("./friut/images/score.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Fruit")
    pygame.time.set_timer(THROWFRUITTIME, 3000)

    pd=posedetector()
    bgm_ = bgm()
    bgm_.play_menu()
    clock = pygame.time.Clock()

    background_list = pygame.sprite.Group()
    # 导入背景图像并添加入背景精灵组
    background_list.add(background(screen, 0, 0, "./friut/images/background.jpg",True)) 
    background_list.add(background(screen, 0, 0, "./friut/images/home-mask.png"))
    background_list.add(background(screen, 20, 10, "./friut/images/logo.png"))
    background_list.add(background(screen, 20, 135, "./friut/images/home-desc.png"))
    knife_ = knife(screen)

    background_list.update()

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

        clock.tick(fps)
        

        cTime = time.time()
        if (cTime-pTime) > 1:
            pTime=cTime
            image = cv2.flip(image, flipCode=1) 
            attach_result=pd.attach(image)
            if attach_result:
                if start_pos=="":
                    start_pos=pd.point(19)
                elif end_pos=="":
                    pos=pd.point(19)
                    if pos[1]<start_pos[1]: #为了游戏便于游玩，规定只能从上往下切
                        end_pos=""
                        start_pos=pos
                    else:
                        end_pos=pos
                else:
                    x=(end_pos[0]+start_pos[0])/2
                    y=(end_pos[1]+start_pos[1])/2
                    dy=end_pos[1]-start_pos[1]
                    dx=end_pos[0]-start_pos[0]
                    angle=math.atan2(dy,dx)
                    angle=int(angle*180/math.pi)
                    knife_.update(x,y,angle)
                    bgm_.play_splatter()
                    pygame.draw.line(screen, (0, 255, 0), start_pos, end_pos,3)
                    pygame.draw.circle(screen, (255, 0, 0), (x,y),5)
                    start_pos=""
                    end_pos=""
            

        
        
        check_key()
        pygame.display.update()

    cap.release()

if __name__ == '__main__':
    main()

