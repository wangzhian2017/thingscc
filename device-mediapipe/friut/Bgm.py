import pygame

class Bgm(object):
    """ 游戏音乐类 """

    def __init__(self):
        pygame.mixer.init()

    def play_menu(self):
        pygame.mixer.music.load("./sound/menu.ogg")
        pygame.mixer.music.play(-1, 0)

    def play_classic(self):
        pygame.mixer.music.load("./sound/start.mp3")
        pygame.mixer.music.play(1, 0)

    def play_throw(self):
        pygame.mixer.music.load("./sound/throw.mp3")
        pygame.mixer.music.play(1, 0)

    def play_splatter(self):
        pygame.mixer.music.load("./sound/splatter.mp3")
        pygame.mixer.music.play(1, 0)

    def play_over(self):
        pygame.mixer.music.load("./sound/over.mp3")
        pygame.mixer.music.play(1, 0)
