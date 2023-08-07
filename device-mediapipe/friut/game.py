import random
import math
import pygame
from pygame.constants import *
from friut.bgm import bgm
from friut.background import background
from friut.knife import knife
from friut.option import option
from friut.throw import throw
from friut.half import half
from friut.bomb import bomb
from friut.catalog import catalog


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
        # 开始菜单
        self.option_list = pygame.sprite.Group()
        # 完整水果
        self.throw_fruit_list = pygame.sprite.Group()
        # 切开的水果
        self.half_fruit_list = pygame.sprite.Group()

        self.started=False
        self.create_option()

    def update(self):
        self.background_list.update()
        self.knife_.update()
        if self.started:
            self.throw_fruit_list.update()
        else:
            self.option_list.update()
        self.half_fruit_list.update()

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
                if self.started:
                    self.create_fruit()

    def create_option(self):
        option1_circle = option(self.screen, self.width - 405, self.height - 250, "./friut/images/new-game.png", 3,None)
        self.option_list.add(option1_circle)
        option1_fruit = option(self.screen, 
                                    self.width - 405 + option1_circle.rect.width / 2 - 49,
                                    self.height - 250 + option1_circle.rect.height / 2 - 85 / 2,
                                    catalog.image_path[catalog.sandia], -3, catalog.sandia)
        self.option_list.add(option1_fruit)

    def create_fruit(self):
        fruit_image_path = catalog.image_path
        fruit_number = random.randint(1, 3)
        for n in range(fruit_number):
            rand_fruit_index = random.randint(0, len(fruit_image_path) - 1)
            self.bgm_.play_throw()
            v0=random.randint(4, 8)
            fruit = throw(self, fruit_image_path[rand_fruit_index], v0, 5, rand_fruit_index)
            self.throw_fruit_list.add(fruit)

    def create_fruit_half(self, fruit):
        fruit_x=fruit.rect.x
        fruit_y=fruit.rect.y
        angel_velocity=fruit.angel_velocity
        v_angel=fruit.cur_angel
        if fruit.flag == catalog.sandia:
            """ 西瓜被切开 """
            fruit_left = half(self, "./friut/images/sandia-1.png", fruit_x - 50, fruit_y, angel_velocity, v_angel, -5)
            fruit_right = half(self, "./friut/images/sandia-2.png", fruit_x + 50, fruit_y, -angel_velocity, v_angel,5)
            self.half_fruit_list.add(fruit_left)
            self.half_fruit_list.add(fruit_right)
        if fruit.flag == catalog.peach:
            """ 梨被切开 """
            fruit_left = half(self, "./friut/images/peach-1.png", fruit_x - 50, fruit_y, angel_velocity, v_angel, -5)
            fruit_right = half(self, "./friut/images/peach-2.png", fruit_x + 50, fruit_y, -angel_velocity, v_angel,5)
            self.half_fruit_list.add(fruit_left)
            self.half_fruit_list.add(fruit_right)
        if fruit.flag == catalog.banana:
            """ 香蕉被切开 """
            fruit_left = half(self, "./friut/images/banana-1.png", fruit_x - 50, fruit_y, angel_velocity, v_angel, -5)
            fruit_right = half(self, "./friut/images/banana-2.png", fruit_x + 50, fruit_y, -angel_velocity, v_angel,5)
            self.half_fruit_list.add(fruit_left)
            self.half_fruit_list.add(fruit_right)
        if fruit.flag == catalog.apple:
            """ 苹果被切开 """
            fruit_left = half(self, "./friut/images/apple-1.png", fruit_x - 50, fruit_y, angel_velocity, v_angel, -5)
            fruit_right = half(self, "./friut/images/apple-2.png", fruit_x + 50, fruit_y, -angel_velocity, v_angel,5)
            self.half_fruit_list.add(fruit_left)
            self.half_fruit_list.add(fruit_right)
        if fruit.flag == catalog.basaha:
            """ 草莓被切开 """
            fruit_left = half(self, "./friut/images/basaha-1.png", fruit_x - 50, fruit_y, angel_velocity, v_angel, -5)
            fruit_right = half(self, "./friut/images/basaha-2.png", fruit_x + 50, fruit_y, -angel_velocity, v_angel,5)
            self.half_fruit_list.add(fruit_left)
            self.half_fruit_list.add(fruit_right)
        if fruit.flag==catalog.boom:
            """ 炸弹被切开 """
            bomb_=bomb(self,fruit_x,fruit_y,v_angel)
            self.half_fruit_list.add(bomb_)
            pass

    def undercut(self,start_pos,end_pos):
        dy=end_pos[1]-start_pos[1]
        dx=end_pos[0]-start_pos[0]
        distance=(dx**2+dy**2)**0.5
        if(distance<200):
            return
        
        print("undercut")
        x=(end_pos[0]+start_pos[0])/2
        y=(end_pos[1]+start_pos[1])/2
        angle=math.atan2(dy,dx)
        angle=int(angle*180/math.pi)
        self.knife_.show_flash(x,y,angle)
        # pygame.draw.line(self.screen, (0, 255, 0), start_pos, end_pos,3)
        # pygame.draw.circle(self.screen, (255, 0, 0), (x,y),5)
        if pygame.sprite.spritecollideany(self.knife_,self.option_list,pygame.sprite.collide_mask):
            self.bgm_.play_splatter()
            collide_list=pygame.sprite.spritecollide(self.knife_,self.option_list,False,pygame.sprite.collide_mask)
            for item in collide_list:
                self.create_fruit_half(item)
                self.option_list.remove_internal(item)
                self.started=True
            self.bgm_.play_classic()


        if pygame.sprite.spritecollideany(self.knife_,self.throw_fruit_list,pygame.sprite.collide_mask):
            self.bgm_.play_splatter()
            collide_list=pygame.sprite.spritecollide(self.knife_,self.throw_fruit_list,False,pygame.sprite.collide_mask)
            for item in collide_list:
                self.create_fruit_half(item)
                self.throw_fruit_list.remove_internal(item)
                if item.flag==catalog.boom: # 切到炸弹
                    self.bgm_.play_boom()
                    self.started=False
                

            
