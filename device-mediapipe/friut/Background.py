import pygame

class background(pygame.sprite.Sprite):
    """ 背景图片 """

    def __init__(self, window, x, y, image_path,resizeable=False):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.resizeable=resizeable

    def update(self):
        if self.resizeable:
            self.rect.width=self.window.get_width()
            self.rect.height=self.window.get_height()

        self.window.blit(self.image, self.rect)