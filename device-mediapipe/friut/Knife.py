import pygame

class Knife(object):
    def __init__(self, window):
        self.window = window
        self.apple_flash = pygame.image.load("./images/apple_flash.png")
        self.banana_flash = pygame.image.load("./images/banana_flash.png")
        self.peach_flash = pygame.image.load("./images/peach_flash.png")
        self.sandia_flash = pygame.image.load("./images/sandia_flash.png")

    def show_apple_flash(self, x, y):
        self.window.blit(self.apple_flash, (x, y))

    def show_banana_flash(self, x, y):
        self.window.blit(self.banana_flash, (x, y))

    def show_peach_flash(self, x, y):
        self.window.blit(self.peach_flash, (x, y))

    def show_sandia_flash(self, x, y):
        self.window.blit(self.sandia_flash, (x, y))
