import pygame

class Background(pygame.sprite.Sprite):
    """ 背景图片 """

    def __init__(self, window, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.window.blit(self.image, self.rect)
