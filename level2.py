from pygame import *
import math
font.init()
win_width, win_height = 1200, 700
font = font.SysFont('Century Gothic', 24)
'''font2 = font.SysFont("Century Gothic", 40)'''
window = display.set_mode((win_width, win_height))
display.set_caption("Slingshot with Custom Images")
background = transform.scale(image.load("angrybackground.png"), (win_width, win_height))  # Load the background image
score = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
lost = 0
score = 0
# Load images for ball, slingshot, and blocks
ball_image = transform.scale(image.load("ball.png"), (30, 30))  # Adjust size as necessary
slingshot_image = transform.scale(image.load("slingshot.png"), (50, 150))  # Replace with slingshot image
block_image = transform.scale(image.load("block.png"), (50, 50))  # Block images
win_secretfinal = transform.scale(image.load("win_secretfinal.jpg"), (win_width, win_height))
win_lose = transform.scale(image.load("win_lose.jpg"), (win_width, win_height))
mixer.init()
mainmenu = mixer.Sound("mainmenu.mp3")
secret1sound = mixer.Sound("sound1.mp3")
losesound = mixer.Sound('losesound.mp3')
lv2sound = mixer.Sound('lv2sound.mp3')
scoresound = mixer.Sound('scoresound.mp3')
win_secretsound = mixer.Sound('secretsound.mp3')
# Ball class with an image
class Ball:
    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.in_air = False
        self.stuck = False  # New variable to track if the ball is stuck

    def draw(self):
        window.blit(ball_image, (int(self.x) - 15, int(self.y) - 15))  # Centering image

    def launch(self, angle, power):
        if not self.stuck:  # Don't allow the ball to launch if it's stuck
            self.vx = power * math.cos(math.radians(angle))
            self.vy = -power * math.sin(math.radians(angle))
            self.in_air = True

    def update(self):
        if self.in_air and not self.stuck:  # Only update if the ball is in the air and not stuck
            self.vy += 0.5  # Gravity
            self.x += self.vx
            self.y += self.vy

            # Ball hits the ground
            if self.y > win_height - 30:
                self.y = win_height - 30
                self.vy = 0
                self.in_air = False

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.vx = 0
        self.vy = 0
        self.in_air = False
        self.stuck = False  # Reset stuck state when ball is reset

# Target class with blocks
class Target:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def draw(self):
        for i in range(0, self.rect.height, 50):
            window.blit(block_image, (self.rect.x, self.rect.y + i))  # Stacking blocks vertically

    def check_collision(self, ball):
        # Check for collision and "stick" the ball if it collides
        if self.rect.colliderect(Rect(ball.x - 15, ball.y - 15, 30, 30)):
            ball.stuck = True  # Ball is stuck in the blocks
            ball.in_air = False  # Stop ball's movement
            return True
        return False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# Create ball and target
ball = Ball(200, win_height - 300)
target = Target(win_width - 300, win_height - 300, 50, 150)  # Stacked blocks

# Main game loop variables
angle = 45
power = 30
can_shoot = True
needs_reload = False
show_trajectory = True

# Function to draw trajectory
def draw_trajectory():
    if not ball.in_air and show_trajectory and not ball.stuck:
        length = 100
        end_x = ball.x + length * math.cos(math.radians(angle))
        end_y = ball.y - length * math.sin(math.radians(angle))
        draw.line(window, BLACK, (ball.x, ball.y), (end_x, end_y), 3)

run = True
clock = time.Clock()
while run:
    finish = False
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE and can_shoot and not needs_reload:
                ball.launch(angle, power)
                needs_reload = True
                can_shoot = False

            if e.key == K_r and needs_reload:
                ball.reset()
                can_shoot = True
                needs_reload = False

            if e.key == K_t:
                show_trajectory = not show_trajectory

    keys_pressed = key.get_pressed()
    if keys_pressed[K_UP] and angle < 90 and can_shoot:
        angle += 1
    if keys_pressed[K_DOWN] and angle > 0 and can_shoot:
        angle -= 1
    if keys_pressed[K_RIGHT] and can_shoot:
        power += 1
    if keys_pressed[K_LEFT] and power > 10 and can_shoot:
        power -= 1

    window.blit(background, (0, 0))  # Draw background

    # Always draw the slingshot, even if the ball is launched
    window.blit(slingshot_image, (180, win_height - 300))  # Draw slingshot image
    ball.draw()
    draw_trajectory()
    target.draw()
    if target.check_collision(ball):
        print("Hit!")
        score += 1
        needs_reload = True


    text = font.render(f"Angle: {angle}°  Power: {power}   Reload: {'R' if needs_reload else 'Ready to shoot'}   Trajectory: {'On' if show_trajectory else 'Off'}", True, BLACK)
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(text, (25, 25))
    window.blit(score_text, (50, 45))
    if not finish:
        if score == 20:
            mainmenu.stop()
            window.blit(win_secretfinal, (0, 0))
            draw_text('You had opened secret final! Bravo!', font, (255, 255, 255), window, 280, 175)
            win_secretsound.play()
            secret1sound.play()
            secret1sound.set_volume(0.1)
            finish = True
            #break
        ball.update()
    display.update()
    clock.tick(60)
