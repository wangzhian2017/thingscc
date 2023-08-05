import pygame
import random
import math

class throw(pygame.sprite.Sprite):
    """ 被抛出的水果类 """

    def __init__(self, game, image_path, speed, turn_angel, flag):
        pygame.sprite.Sprite.__init__(self)

        self.G=game.G
        self.width=game.width
        self.height=game.height
        # 游戏窗口
        self.window = game.screen

        # 导入水果图像并获取其矩形区域
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # 水果抛出时x坐标取随机数
        self.rect.x = random.randint(0, self.width)

        # 水果初始y坐标
        self.rect.y = self.height

        # 旋转速度
        self.turn_angel = turn_angel

        # 水果抛出时与窗口下水平线的夹角弧度，因为要用到随机函数, 所以取整数， 使用时除以100
        self.throw_angel = 157

        # 水果抛出后所经历的时间, 初始化为0
        self.fruit_t = 0

        # 旋转的总角度
        self.v_angel = 0

        # 水果抛出时的初速度
        self.v0 = speed

        # 水果标记
        self.flag = flag

    def update(self):
        """ 水果运动状态更新 """

        # 如果水果的初始X坐标位于窗口左边区域, 取抛出时弧度在1.4  ~ 1.57 之间(70度至90度之间)
        if self.rect.x <= self.width / 2:
            self.throw_angel = random.randint(140, 157)

        # 如果水果的初始X坐标位于窗口右侧区域, 取抛出时弧度在1.57 * 100 ~ 1.75 * 100之间(90度至110度之间)
        elif self.rect.x >= self.height / 2:
            self.throw_angel = random.randint(157, 175)

        # 水果旋转后的新图像
        new_fruit = pygame.transform.rotate(self.image, self.v_angel)

        # 将旋转后的新图像贴入游戏窗口, 注意, 旋转后的图像尺寸以及像素都不一样了(尺寸变大了), 所以坐标需要进行适当处理
        self.window.blit(new_fruit, (self.rect.x + self.rect.width / 2 - new_fruit.get_width() / 2,
                                    self.rect.y + self.rect.height / 2 - new_fruit.get_height() / 2))

        # 水果抛出后的运动时水平匀速运动以及竖直向上的变速运动到达最高点时下落, 所以可以判断水果做的是斜上抛运动
        # 可以利用重力加速度来求出每隔一段时间水果运动后的y坐标
        # 公式: v0 * t * sin(α) - g * t^2 / 2
        if self.rect.y >= self.height + self.rect.height:
            self.kill()
        self.rect.y -= self.v0 * self.fruit_t * math.sin(self.throw_angel / 100) - (self.G *
                                                                                    self.fruit_t ** 2 / 10) / 2

        # 计算水果在水平方向的位移之后的X坐标, 匀速运动，没啥好说的
        # 公式: v0 * t * cos(α)
        self.rect.x += self.v0 * self.fruit_t * math.cos(self.throw_angel / 100)

        # 累加经过的时间
        self.fruit_t += 0.1

        # 累加旋转总角度
        self.v_angel += self.turn_angel
