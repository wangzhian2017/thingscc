import pygame

class knife(pygame.sprite.Sprite):
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load("./friut/images/flash.png")
        self.rect  =self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.cur_angle=0
        self.times=0

    def show_flash(self, center_x, center_y,angel):
        self.times=0
        self.cur_angle=angel
        new_image = pygame.transform.rotate(self.image, self.cur_angle)
        center=(center_x,center_y)
        self.rect=new_image.get_rect(center=center)
        self.mask=pygame.mask.from_surface(new_image)
        self.window.blit(new_image, self.rect)

    def update(self):
        self.times+=1
        if self.times<=10:
            new_image = pygame.transform.rotate(self.image, self.cur_angle)
            self.window.blit(new_image, self.rect)
                
        
