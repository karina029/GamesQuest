from pygame import *
import time as timer
from random import *
import sys

win_width = 1200
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Quest")
# display.set_icon(image.load('shot.jpeg'))
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
win_secretfinal = transform.scale(image.load("win_secretfinal.jpg"), (win_width, win_height))
win_lose = transform.scale(image.load("win_lose.jpg"), (win_width, win_height))
lost = 0
# final = transform.scale(image.load("final.jpeg"), (win_width, win_height))

mixer.init()
mainmenu = mixer.Sound("mainmenu.mp3")
mainmenu.play()
mainmenu.set_volume(0.2)
losesound = mixer.Sound('losesound.mp3')
secret1sound = mixer.Sound("sound1.mp3")
lv2sound = mixer.Sound('lv2sound.mp3')
scoresound = mixer.Sound('scoresound.mp3')
win_secretsound = mixer.Sound('secretsound.mp3')


class GameSprite(sprite.Sprite):
    def __init__(self, play_btner_img, play_btner_x, play_btner_y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(play_btner_img), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = play_btner_x
        self.rect.y = play_btner_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class play_btner(GameSprite):
    def __init__(self, play_btner_image, play_btner_x, play_btner_y, size_x, size_y, play_btner_speed):

        super().__init__(play_btner_image, play_btner_x, play_btner_y, size_x, size_y, play_btner_speed)
        self.animation_set = [transform.scale(image.load(f"anim1/{i}.png"), (100, 100)) for i in range(1, 61)]
        self.i = 0
        self.cadr = 0

    def update(self):
        move = False
        keys = key.get_pressed()
        self.cadr += 1
        '''
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
        '''
        if keys[K_f] and self.rect.x > 0:
            move = True
            if self.cadr % 10 == 0:  # ! %10 - затримка кадру. Буде раз 10 кадрів оновлюватись анімація
                self.i += 1
            self.rect.x -= self.speed
            self.image = self.animation_set[self.i % 16 + 4]

        if keys[K_g] and self.rect.x < win_width - self.rect.width:
            move = True
            if self.cadr % 10 == 0:
                self.i += 1
            self.rect.x += self.speed
            self.image = self.animation_set[self.i % 4 + 8]
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

        '''pos = mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width/2
        self.rect.y = pos[1] - self.rect.height/2'''
        self.reset()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height + 50:
            self.rect.y = - 50
            '''if self.rect.y < win_height:
            #self.rect.y -= 50'''
            self.speed = randint(1, 4)
            global lost
            lost += 1
        self.reset()


font.init()
font2 = font.SysFont("Century Gothic", 40)
font3 = font.SysFont("Century Gothic", 30)

score = 0

start_life = 2000
xp = start_life

run = True
clock = time.Clock()
finish = False
play_btner2 = play_btner("rul.png", win_width / 2, win_height - 100, 500, 120, 20)
sonic = play_btner("sonic.png", win_width / 2, win_height - 200, 120, 100, 20)
bike = play_btner("rul.png", win_width / 2, win_height - 200, 400, 120, 20)

level = 2

click = False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Car(GameSprite):
    global lost
    lost = 0

    def __init__(self, img, x, y, width, height, target_x, target_y, speed=5):
        super().__init__(img, x, y, width, height, speed)
        self.original_width = width
        self.original_height = height
        self.target_x = target_x  # Цільова позиція (наприклад, позиція гравця)
        self.target_y = target_y
        self.arrived = False
        self.img_copy = self.image

    def update(self):
        if not self.arrived:
            # Обчислюємо напрямок руху до цілі
            direction_x = self.target_x - self.rect.x
            direction_y = self.target_y - self.rect.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            # Збільшуємо розмір автомобіля при наближенні
            scale_factor = max(1.0, 2.0 - distance / 300)  # Чим ближче, тим більше (макс збільшення в 2 рази)
            self.image = transform.scale(self.img_copy,
                                         (int(self.original_width * scale_factor),
                                          int(self.original_height * scale_factor)))

            # Рухаємо автомобіль у напрямку до цільової точки
            if distance != 0:
                self.rect.x += self.speed * (direction_x / distance)
                self.rect.y += self.speed * (direction_y / distance)

            # Перевіряємо, чи досяг автомобіль цільової точки
            if distance < 50:  # Якщо автомобіль близький до цілі
                self.arrived = True
                self.respawn()  # Відроджуємо автомобіль на новому місці
                global score
                score += 1
        self.reset()

    def respawn(self):
        # Автомобіль з'являється за горизонтом (зверху екрану) з новими координатами
        self.rect.x = (600)
        self.rect.y = randint(250, 300)  # Починає виїжджати зверху за межами екрану
        self.arrived = False  # Скидаємо стан, щоб автомобіль знову почав рух
        self.speed += randint(0, 1)  # Встановлюємо нову швидкість
        self.target_x = randint(0, win_width)
        self.reset()


# Додаємо автомобілі для тестування
cars = sprite.Group()
car = Car("car1.png", randint(0, win_width), randint(250, 300), 75, 50, randint(0, win_width), win_height)
car2 = Car("car2.png", randint(0, win_width), randint(250, 300), 75, 50, randint(0, win_width), win_height)
car3 = Car("car3.png", randint(0, win_width), randint(250, 300), 75, 50, randint(0, win_width), win_height)
car4 = Car("car4.png", randint(0, win_width), randint(250, 300), 75, 100, randint(0, win_width), win_height)
carsl = [car, car2, car3, car4]
for i in carsl:
    cars.add(i)

background1 = transform.scale(image.load("backgroundl1.jpg"), (win_width, win_height))


def levels():  # !!!!!!
    running = True
    global level
    # window = display.set_mode((1000,700))
    backgroundOptions = transform.scale(image.load("background.jpg").convert(), (win_width, win_height))
    lv1 = GameSprite("rul.png", 20, 100, 600, 200, 0)
    lv2 = GameSprite("ball.png", 700, 100, 200, 200, 0)

    click = False
    while running:
        window.blit(backgroundOptions, (0, 0))

        draw_text('GAME SCREEN', font2, (255, 255, 255), window, 20, 20)
        lv1.reset()
        lv2.reset()
        # writing text on top of button
        draw_text('GAME 1', font2, (255, 255, 255), window, 300, 300)
        draw_text('GAME 2', font2, (255, 255, 255), window, 700, 300)

        mx, my = mouse.get_pos()

        # defining functions when a certain button is pressed
        if lv1.rect.collidepoint((mx, my)):
            if click:
                level = 1
                run()
            '''    

            '''

        if lv2.rect.collidepoint((mx, my)):
            if click:
                mainmenu.stop()
                lv2sound.play()
                lv2sound.set_volume(0.2)
                import level2
                # window = display.set_mode((win_width, win_height))

        click = False

        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    click = True

        display.update()
        time.delay(60)


def level1():
    global level
    window.blit(background1, (0, 0))
    # Оновлення та малювання всіх об'єктів
    cars.update()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    collide = sprite.spritecollide(play_btner2, cars, False)
    for c in collide:
        global lost
        lost += 1
        c.respawn()

    text = font3.render("Score: " + str(score), True, (120, 120, 120))
    window.blit(text, (25, 25))
    text = font3.render("Lost: " + str(lost), True, (120, 120, 120))
    window.blit(text, (25, 55))

backgroundl2 = transform.scale(image.load("backgroundl2.jpg"), (win_width, win_height))


def level2():
    global level
    window.blit(backgroundl2, (0, 0))


def run():
    global level
    finish = False
    while run:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    levels()
        if not finish:
            if level == 1:
                level1()
            elif level == 2:
                level2()
                mainmenu.stop()
                lv2sound.play()
                lv2sound.set_volume(0.1)
            if score == 20:
                mainmenu.stop()
                window.blit(win_secretfinal, (0, 0))
                draw_text('You had opened secret final! Bravo!', font2, (255, 255, 255), window, 280, 175)
                win_secretsound.play()
                secret1sound.play()
                secret1sound.set_volume(0.1)
                finish = True
            if lost == 10:
                mainmenu.stop()
                window.blit(win_lose, (0, 0))
                draw_text('You are lose! Sorry to see that', font2, (255, 255, 255), window, 280, 175)
                losesound.play()
                losesound.set_volume(0.1)
                finish = True

            play_btner2.update()
            play_btner2.reset()

        display.update()
        time.delay(50)


from level1 import *
while run:
    if not finish:
        window.blit(background, (0, 0))
        # time = timer()
        if level == 1:
            bike.update()
        else:
            sonic.update()
        draw_text('Main Menu', font2, (255, 255, 255), window, 250, 40)
        # creating buttons
        levels_btn = Rect(250, 180, 200, 50)

        mx, my = mouse.get_pos()
        # defining functions when a certain button is presse

        if levels_btn.collidepoint((mx, my)):
            draw.rect(window, (155, 255, 0), levels_btn)
            if click:
                levels()  # !!!!!!!!!

        else:
            draw.rect(window, (255, 0, 0), levels_btn)

        # writing text on top of button
        draw_text('GAMES', font2, (255, 255, 255), window, 280, 175)

        click = False
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    quit()
                    sys.exit()
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    click = True
    display.update()
    clock.tick(60)

