import pygame
import random
from pygame.constants import *
from Background import Background
from OptionMode import OptionMode
from Bgm import Bgm
from Knife import Knife
from ThrowFruit import ThrowFruit
from HalfFruit import HalfFruit

pygame.init()
class Manager(object):
    # 窗口尺寸
    WIDTH = 640
    HEIGHT = 480

    # 游戏中的定时器常量
    THROWFRUITTIME = pygame.USEREVENT
    pygame.time.set_timer(THROWFRUITTIME, 3000)

    # 重力加速度, 取整数，使用时除以10
    G = random.randint(21, 23)

    # 经典模式miss掉的水果数
    classic_miss = 0

    def __init__(self):
        # 生成游戏窗口
        self.window = pygame.display.set_mode((Manager.WIDTH, Manager.HEIGHT))
        self.window_icon = pygame.image.load("./images/score.png")
        pygame.display.set_icon(self.window_icon)
        pygame.display.set_caption("FruitNinja")

        # 游戏分数
        self.classic_score = 0
        self.zen_score = 0

        # 创建游戏中用到的的精灵组
        self.background_list = pygame.sprite.Group()
        self.circle_option = pygame.sprite.Group()
        self.option_fruit_list = pygame.sprite.Group()
        self.fruit_half_list = pygame.sprite.Group()
        self.throw_fruit_list = pygame.sprite.Group()

        # 导入背景图像并添加入背景精灵组
        self.background = Background(self.window, 0, 0, "./images/background.jpg")
        self.home_mask = Background(self.window, 0, 0, "./images/home-mask.png")
        self.logo = Background(self.window, 20, 10, "./images/logo.png")
        self.ninja = Background(self.window, Manager.WIDTH - 320, 45, "./images/ninja.png")
        self.home_desc = Background(self.window, 20, 135, "./images/home-desc.png")

        self.background_list.add(self.background)
        self.background_list.add(self.home_mask)
        self.background_list.add(self.logo)
        self.background_list.add(self.ninja)
        self.background_list.add(self.home_desc)

        # 创建旋转的圈并添加进精灵组
        self.dojo = OptionMode(self.window, Manager.WIDTH - 600, Manager.HEIGHT - 250, "./images/dojo.png", 3, None)
        self.new_game = OptionMode(self.window, Manager.WIDTH - 405, Manager.HEIGHT - 250, "./images/new-game.png", 3,
                                None)
        self.game_quit = OptionMode(self.window, Manager.WIDTH - 160, Manager.HEIGHT - 150, "./images/quit.png", -3,
                                    None)

        self.circle_option.add(self.dojo)
        self.circle_option.add(self.new_game)
        self.circle_option.add(self.game_quit)

        # 创建主菜单界面旋转的水果并添加进精灵组
        self.home_sandia = OptionMode(self.window, Manager.WIDTH - 405 + self.new_game.rect.width / 2 - 49,
                                    Manager.HEIGHT - 250 + self.new_game.rect.height / 2 - 85 / 2,
                                    "./images/sandia.png", -3, "option_sandia")
        self.home_peach = OptionMode(self.window, Manager.WIDTH - 600 + self.dojo.rect.width / 2 - 31,
                                    Manager.HEIGHT - 250 + self.dojo.rect.height / 2 - 59 / 2,
                                    "./images/peach.png", -3, "option_peach")
        self.home_boom = OptionMode(self.window, Manager.WIDTH - 160 + self.game_quit.rect.width / 2 - 66 / 2,
                                    Manager.HEIGHT - 150 + self.game_quit.rect.height / 2 - 68 / 2,
                                    "./images/boom.png", 3, "option_boom")
        self.option_fruit_list.add(self.home_sandia)
        self.option_fruit_list.add(self.home_peach)
        self.option_fruit_list.add(self.home_boom)

        # 设置定时器
        self.clock = pygame.time.Clock()

        # 模式标记
        self.mode_flag = 0

        # 音效
        self.bgm = Bgm()

        # 刀光
        self.knife = Knife(self.window)

    def create_fruit(self):
        """ 创建水果 """
        if self.mode_flag == 1:
            boom_prob = random.randint(0, 10)
            if boom_prob == 8:
                self.bgm.play_throw()
                boom = ThrowFruit(self.self.window, "./images/boom.png", None, 5, 5)
                self.throw_fruit_list.add(boom)

        fruit_image_path = ["./images/sandia.png", "./images/peach.png",
                            "./images/banana.png", "./images/apple.png",
                            "./images/basaha.png"]
        fruit_number = random.randint(1, 4)
        for n in range(fruit_number):
            rand_fruit_index = random.randint(0, len(fruit_image_path) - 1)
            self.bgm.play_throw()
            fruit = ThrowFruit(self,self.window, fruit_image_path[rand_fruit_index], None, 5, rand_fruit_index)
            self.throw_fruit_list.add(fruit)

    def create_fruit_half(self, fruit_flag, fruit_x, fruit_y, turn_angel, v_angel):
        if fruit_flag == "option_sandia":
            """ 经典模式西瓜被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/sandia-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel,
                                -5)
            fruit_right = HalfFruit(self,self.window, "./images/sandia-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)
        if fruit_flag == "option_peach":
            """ 禅宗模式的梨被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/peach-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/peach-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)

        if fruit_flag == 0:
            """ 西瓜被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/sandia-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/sandia-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)
        if fruit_flag == 1:
            """ 梨被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/peach-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/peach-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)
        if fruit_flag == 2:
            """ 香蕉被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/banana-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/banana-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)
        if fruit_flag == 3:
            """ 苹果被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/apple-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/apple-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)
        if fruit_flag == 4:
            """ 草莓被切开 """
            fruit_left = HalfFruit(self,self.window, "./images/basaha-1.png", fruit_x - 50, fruit_y, turn_angel, v_angel, -5)
            fruit_right = HalfFruit(self,self.window, "./images/basaha-2.png", fruit_x + 50, fruit_y, -turn_angel, v_angel,
                                    5)
            self.fruit_half_list.add(fruit_left)
            self.fruit_half_list.add(fruit_right)

    def impact_check(self):
        """ 碰撞检测 """
        for item in self.option_fruit_list:
            """ 主页的模式选择 """
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > item.rect.left and mouse_pos[0] < item.rect.right \
                    and mouse_pos[1] > item.rect.top and mouse_pos[1] < item.rect.bottom:
                self.bgm.play_splatter()
                self.create_fruit_half(item.flag, item.rect.x, item.rect.y, item.turn_angel, item.v_angel)
                self.option_fruit_list.remove_internal(item)
                if item.flag == "option_sandia":
                    self.mode_flag = 1
                    return 1
                elif item.flag == "option_peach":
                    self.mode_flag = 2
                    return 2
                elif item.flag == "option_boom":
                    return 0

        for item in self.throw_fruit_list:
            """ 游戏开始后判断水果是否被切到 """
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > item.rect.left and mouse_pos[0] < item.rect.right \
                    and mouse_pos[1] > item.rect.top and mouse_pos[1] < item.rect.bottom:
                if item.flag == 0:
                    self.knife.show_sandia_flash(item.rect.x, item.rect.y)
                if item.flag == 1:
                    self.knife.show_peach_flash(item.rect.x, item.rect.y)
                if item.flag == 2:
                    self.knife.show_banana_flash(item.rect.x, item.rect.y)
                if item.flag == 3:
                    self.knife.show_apple_flash(item.rect.x, item.rect.y)
                if item.flag == 4:
                    self.knife.show_apple_flash(item.rect.x, item.rect.y)

                if self.mode_flag == 1:
                    self.classic_score += 2
                if self.mode_flag == 2:
                    self.zen_score += 2
                    print(self.zen_score)
                self.bgm.play_splatter()
                self.create_fruit_half(item.flag, item.rect.x, item.rect.y, item.turn_angel, item.v_angel)
                self.throw_fruit_list.remove_internal(item)
                if item.flag == 5:
                    return 3

    def check_key(self):
        """ 监听事件 """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == Manager.THROWFRUITTIME and self.mode_flag == 1:
                self.create_fruit()
            elif event.type == Manager.THROWFRUITTIME and self.mode_flag == 2:
                self.create_fruit()

    def classic_mode(self):
        """ 经典模式 """
        pygame.font.init()
        self.bgm.play_classic()
        score_image = Background(self.window, 10, 5, "./images/score.png")
        text = pygame.font.Font("./images/SimHei.ttf", 20)  # 设置分数显示的字体
        x_times = pygame.sprite.Group()
        miss_times = pygame.sprite.Group()
        xxx = Background(self.window, Manager.WIDTH - 30, 5, "./images/xxx.png")
        xx = Background(self.window, Manager.WIDTH - 60, 5, "./images/xx.png")
        x = Background(self.window, Manager.WIDTH - 90, 5, "./images/x.png")
        x_times.add(xxx)
        x_times.add(xx)
        x_times.add(x)

        while True:
            # 设置游戏帧率
            self.clock.tick(60)
            pygame.display.update()
            self.check_key()
            self.background_list.sprites()[0].update()
            score_image.update()
            text_score = text.render("%d" % self.classic_score, 1, (0, 255, 0))
            self.window.blit(text_score, (50, 10))
            x_times.update()
            miss_times.update()
            temp_flag = self.impact_check()
            if temp_flag == 3:
                return
            self.throw_fruit_list.update()
            self.fruit_half_list.update()
            if Manager.classic_miss == 1:
                xf = Background(self.window, Manager.WIDTH - 90, 5, "./images/xf.png")
                miss_times.add(xf)
            elif Manager.classic_miss == 2:
                xf = Background(self.window, Manager.WIDTH - 90, 5, "./images/xf.png")
                miss_times.add(xf)
                xxf = Background(self.window, Manager.WIDTH - 60, 5, "./images/xxf.png")
                miss_times.add(xxf)
            elif Manager.classic_miss >= 3:
                self.bgm.play_over()
                Manager.classic_miss = 0
                return

    def zen_mode(self):
        """ 禅宗模式 """
        self.bgm.play_classic()

        # 记录分数
        record_time = 0
        while True:
            # 设置游戏帧率
            self.clock.tick(60)
            self.check_key()
            self.background_list.sprites()[0].update()
            self.impact_check()
            self.throw_fruit_list.update()
            self.fruit_half_list.update()
            pygame.display.update()

            if record_time == 3000:
                return
            record_time += 1


def main():
    """ 主页 """
    manager = Manager()
    manager.bgm.play_menu()
    while True:
        # 设置游戏帧率
        manager.clock.tick(60)
        manager.background_list.update()
        manager.circle_option.update()
        manager.option_fruit_list.update()
        manager.fruit_half_list.update()

        temp_flag = manager.impact_check()
        pygame.display.update()
        if temp_flag == 1:
            manager.classic_mode()
            manager.__init__()
            manager.bgm.play_over()
            manager.bgm.play_menu()

        if temp_flag == 2:
            manager.zen_mode()
            manager.__init__()
            manager.bgm.play_over()
            manager.bgm.play_menu()

        elif temp_flag == 0:
            pygame.quit()
            exit()
        elif temp_flag == 3:
            manager.__init__()
            manager.bgm.play_over()
            manager.bgm.play_menu()
        manager.check_key()


if __name__ == '__main__':
    #https://blog.51cto.com/u_16099272/6303062
    
    print("切水果开始")
    main()