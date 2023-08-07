import pygame

class bgm(object):
    """ 游戏音乐类 """

    def __init__(self):
        pygame.mixer.init()

    def play_menu(self):
        pygame.mixer.music.load("./friut/sound/menu.ogg")
        pygame.mixer.music.play(-1, 0)

    def play_classic(self):
        pygame.mixer.music.load("./friut/sound/start.mp3")
        pygame.mixer.music.play(1, 0)

    def play_throw(self):
        pygame.mixer.music.load("./friut/sound/throw.mp3")
        pygame.mixer.music.play(1, 0)

    def play_splatter(self):
        pygame.mixer.music.load("./friut/sound/splatter.mp3")
        pygame.mixer.music.play(1, 0)

    def play_over(self):
        pygame.mixer.music.load("./friut/sound/over.mp3")
        pygame.mixer.music.play(1, 0)

    def play_boom(self):
        pygame.mixer.music.load("./friut/sound/boom.mp3")
        pygame.mixer.music.play(1, 0)
