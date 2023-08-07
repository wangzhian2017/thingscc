import pygame

class option(pygame.sprite.Sprite):
    """ 开始菜单选项类 """

    def __init__(self, window, x, y, image_path, angel_velocity, flag):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angel_velocity = angel_velocity
        self.cur_angel = 0
        self.flag = flag

    def update(self):
        new_image = pygame.transform.rotate(self.image, -self.cur_angel)
        self.window.blit(new_image, (self.rect.x + self.rect.width / 2 - new_image.get_width() / 2,
                                    self.rect.y + self.rect.height / 2 - new_image.get_height() / 2))
        self.cur_angel += self.angel_velocity
