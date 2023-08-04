import pygame

class knife(pygame.sprite.Sprite):
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load("./friut/images/flash.png")
        self.rect  =self.image.get_rect()

    def update(self, center_x, center_y,angel):
        center=(center_x,center_y)
        new_image = pygame.transform.rotate(self.image, -angel)
        self.window.blit(new_image, new_image.get_rect(center=center))
        
