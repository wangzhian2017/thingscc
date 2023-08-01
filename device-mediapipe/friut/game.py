import pygame,sys, os
import random


fruits={}

def generate_fruit(fruit):
    path = os.path.join(os.getcwd(),'images', fruit+'.png')
    fruits[fruit] = {
        'img' : pygame.image.load(path),
        'x' : random.randint(100, 500),
        'y' : 800,
        'speed_x' : random.randint(-10, 10),
        'speed_y' : random.randint(-80, -60),
        'throw' : False,
        't' : 0,
        'hit' : False,
    }
    if(random.random() >= 0.75):
        fruits[fruit]['throw'] = True
    else:
        fruits[fruit]['throw'] = False

def main():
    fps = 13
    score = 0
    fruit_labels = ['watermelon', 'orange']
    for lable in fruit_labels:
        generate_fruit(lable)

    pygame.init()
    screen = pygame.display.set_mode((600,400))
    screen.fill((255,255,255))
    pygame.display.set_caption("水果游戏")
    

    clock = pygame.time.Clock()
    game_over = False
    while True : 
        screen.fill((255,255,255))
        for k,v in fruits.items():
            if v['throw']:
                v['x'] = v['x'] + v['speed_x']
                v['y'] = v['y'] + v['speed_y']
                v['speed_y'] += v['t']
                v['t'] += 1
                if v['y'] <= 800:
                    screen.blit(v['img'], (v['x'],v['y']))
                else:
                    generate_fruit(k)
                current_position = pygame.mouse.get_pos()
                if not v['hit'] and current_position[0] > v['x'] and current_position[0] < v['x']+60 and current_position[1] > v['y'] and current_position[1] < v['y']+60:
                    path = os.path.join(os.getcwd(),'images','half_'+k+'.png')
                    v['img'] = pygame.image.load(path)
                    v['speed_x'] += 10
                    score += 1
                    # score_text = font.render(str(score), True, black, white)
                    v['hit'] = True

            else:
                generate_fruit(k)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            

        pygame.display.update()
        clock.tick(fps)



if __name__ == '__main__':
    main()
