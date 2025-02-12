from pygame import *
import json
win_width = 1200
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Level1")
# display.set_icon(image.load('shot.jpeg'))
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
score = 0
font.init()
font2 = font.SysFont("Century Gothic", 40)
text = font2.render("Score: " + str(score), True, (0, 0, 0))
window.blit(text, (835, 25))
class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Auto(GameSprite):
    def update(self):
        self.rect.x += self.speed
        self.y = 300
        if self.rect.x >= win_height:
            self.kill
