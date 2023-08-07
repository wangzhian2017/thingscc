import pygame
import random

class bomb(pygame.sprite.Sprite):
   def __init__(self, game,  x, y, v_angel):
      self.g=game
      self.win_width=game.width
      self.win_height=game.height

      # 游戏窗口
      self.window = game.screen
      
      # 导入水果图像并获取其矩形区域
      self.image = pygame.image.load("./friut/images/boom.png")
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

      # 旋转的总角度
      self.cur_angel = v_angel

      self.times=60

   def update(self):
      pygame.draw.line(self.window, (255, 255, 255), self.rect.center, (0,0),10)
      pygame.draw.line(self.window, (255, 255, 255), self.rect.center, (0,self.win_height),10)
      pygame.draw.line(self.window, (255, 255, 255), self.rect.center, (self.win_width,0),10)
      pygame.draw.line(self.window, (255, 255, 255), self.rect.center, (self.win_width,self.win_height),10)

      x_bias=random.randint(-10, 10)
      y_bias=random.randint(-10, 10)
      new_bomb = pygame.transform.rotate(self.image, self.cur_angel)
      # 将旋转后的新图像贴入游戏窗口, 注意, 旋转后的图像尺寸以及像素都不一样了(尺寸变大了), 所以坐标需要进行适当处理
      self.window.blit(new_bomb, (x_bias+self.rect.x + self.rect.width / 2 - new_bomb.get_width() / 2,
                                    y_bias+self.rect.y + self.rect.height / 2 - new_bomb.get_height() / 2))
      
      self.times-=1
      if(self.times<=0):
         self.kill()
         self.g.bgm_.play_over()
         self.g.create_option()
      
      
