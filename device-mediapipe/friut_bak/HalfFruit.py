import pygame

class HalfFruit(pygame.sprite.Sprite):
    """ 水果切片类 """

    def __init__(self, manager,window, image_path, x, y, turn_angel, v_angel, v0):
        pygame.sprite.Sprite.__init__(self)
        self.manager=manager

        # 游戏窗口
        self.window = window

        # 导入水果图像并获取其矩形区域
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # 水果被切开后的
        self.rect.x = x

        # 水果初始y坐标
        self.rect.y = y

        # 旋转速度
        self.turn_angel = turn_angel

        # 水果被切开时开始计时
        self.fruit_t = 0

        # 旋转的总角度
        self.v_angel = v_angel

        # 水果抛出时的水平初速度
        self.v0 = v0

    def update(self):
        """ 水果运动状态更新 """

        # 如果水果的初始X坐标位于窗口左边区域, 取抛出时弧度在1.4  ~ 1.57 之间(70度至90度之间)
        # if self.rect.x <= v1版本.Manager.WIDTH / 2 - self.rect.width:
        #     self.throw_angel = random.randint(140, 157)
        #
        # 如果水果的初始X坐标位于窗口右侧区域, 取抛出时弧度在1.57 * 100 ~ 1.75 * 100之间(90度至110度之间)
        # elif self.rect.x >= v1版本.Manager.WIDTH / 2 + self.rect.width:
        #     self.throw_angel = random.randint(157, 175)

        # 水果旋转后的新图像
        new_fruit = pygame.transform.rotate(self.image, self.v_angel)

        # 将旋转后的新图像贴入游戏窗口, 注意, 旋转后的图像尺寸以及像素都不一样了(尺寸变大了), 所以坐标需要进行适当处理
        self.window.blit(new_fruit, (self.rect.x + self.rect.width / 2 - new_fruit.get_width() / 2,
                                    self.rect.y + self.rect.height / 2 - new_fruit.get_height() / 2))

        # 水果被切开之后的切片做的是平抛运动
        # 可以利用重力加速度来求出每隔一段时间水果运动后的y坐标
        # 公式: h += v0 * t * sin(α) - g * t^2 / 2
        if self.rect.y >= self.manager.HEIGHT:
            self.kill()
        self.rect.y += self.manager.G * self.fruit_t ** 2 / 2

        # 计算水果在水平方向的位移之后的X坐标, 匀速运动，没啥好说的
        # 公式: v0 * t * cos(α)
        self.rect.x += self.v0 * self.fruit_t

        # 累加经过的时间
        self.fruit_t += 0.01

        # 累加旋转总角度
        self.v_angel += self.turn_angel
