import random
import math
import pygame
from pygame.constants import *
from friut.bgm import bgm
from friut.background import background
from friut.knife import knife
from friut.throw import throw


class game:

    THROWFRUITTIME = pygame.USEREVENT+1
    # 重力加速度, 取整数，使用时除以10
    G = random.randint(21, 23)
    
    def __init__(self):
        self.width = 640
        self.height = 480
        pygame.init()
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)
        icon = pygame.image.load("./friut/images/score.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Fruit")
        pygame.time.set_timer(self.THROWFRUITTIME, 5000)
    
        self.clock = pygame.time.Clock()
        self.bgm_ = bgm()
        # 导入背景图像并添加入背景精灵组
        self.background_list = pygame.sprite.Group()
        self.background_list.add(background(self.screen, 0, 0, "./friut/images/background.jpg",True)) 
        self.background_list.add(background(self.screen, 0, 0, "./friut/images/home-mask.png"))
        self.background_list.add(background(self.screen, 20, 10, "./friut/images/logo.png"))
        self.background_list.add(background(self.screen, 20, 135, "./friut/images/home-desc.png"))
        # 刀
        self.knife_ = knife(self.screen)
        # 完整水果
        self.throw_fruit_list = pygame.sprite.Group()

    def check_key(self):
        """ 监听事件 """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h
            elif event.type == self.THROWFRUITTIME:
                self.create_fruit()

    def create_fruit(self):
        fruit_image_path = ["./friut/images/sandia.png", "./friut/images/peach.png",
                            "./friut/images/banana.png", "./friut/images/apple.png",
                            "./friut/images/basaha.png","./friut/images/boom.png"]
        fruit_number = random.randint(1, 3)
        for n in range(fruit_number):
            rand_fruit_index = random.randint(0, len(fruit_image_path) - 1)
            self.bgm_.play_throw()
            v0=random.randint(4, 8)
            fruit = throw(self, fruit_image_path[rand_fruit_index], v0, 5, rand_fruit_index)
            self.throw_fruit_list.add(fruit)

    def undercut(self,start_pos,end_pos):
        x=(end_pos[0]+start_pos[0])/2
        y=(end_pos[1]+start_pos[1])/2
        dy=end_pos[1]-start_pos[1]
        dx=end_pos[0]-start_pos[0]
        angle=math.atan2(dy,dx)
        angle=int(angle*180/math.pi)
        self.knife_.show_flash(x,y,angle)
        if pygame.sprite.spritecollideany(self.knife_,self.throw_fruit_list,pygame.sprite.collide_mask):
            self.bgm_.play_splatter()
            collide_list=pygame.sprite.spritecollide(self.knife_,self.throw_fruit_list,False,pygame.sprite.collide_mask)
            for item in collide_list:
                pass

            # pygame.draw.line(self.screen, (0, 255, 0), start_pos, end_pos,3)
            # pygame.draw.circle(self.screen, (255, 0, 0), (x,y),5)
