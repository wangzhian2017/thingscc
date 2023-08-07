import pygame
import time

class knife(pygame.sprite.Sprite):
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load("./friut/images/flash.png")
        self.rect  =self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.last_time=0
        self.cur_angle=0
        self.center=(0,0)

    def show_flash(self, center_x, center_y,angel):
        self.center_x=(center_x,center_y)
        self.cur_angle=angel
        new_image = pygame.transform.rotate(self.image, self.cur_angle)
        center=(center_x,center_y)
        self.rect=new_image.get_rect(center=center)
        self.mask=pygame.mask.from_surface(new_image)
        self.window.blit(new_image, self.rect)
        self.last_time=time.time()

    def update(self):
        if self.last_time>0:
            cTime = time.time()
            if (cTime-self.last_time) <= 1:
                new_image = pygame.transform.rotate(self.image, self.cur_angle)
                self.window.blit(new_image, self.rect)
        
