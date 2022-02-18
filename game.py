import pygame
from pygame.locals import *

pygame.init()

screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BREAKOUT GAME')

background_color = (0, 0, 0)
paddle_color = (0, 197, 205)
RED = (205, 51, 51)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
ORANGE = (238, 118, 0)


cols = 14
rows = 8


class create_wall():
    def __init__(self):
        self.width = screen_width / cols
        self.height = 10
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - 100
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def create_wall(self):
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = 100 + row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                color = 0
                if row < 2:
                    color = 4
                elif row < 4:
                    color = 3
                elif row < 6:
                    color = 2
                elif row < 8:
                    color = 1
                block_individual = [rect, color]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                block_col = 0
                if block[1] == 4:
                    block_col = RED
                elif block[1] == 3:
                    block_col = ORANGE
                elif block[1] == 2:
                    block_col = GREEN
                elif block[1] == 1:
                    block_col = YELLOW
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, background_color, (block[0]), 1)

class create_paddle():

    def __init__(self):
        self.height = 10
        self.width = int(screen_width / cols)
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - 100
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.speed = 5

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)

class create_ball():

    def __init__(self):
        self.right = -1
        self.down = 1
        self.height = 5
        self.width = 5
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = (screen_width // 2) - (self.width // 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.speed = 2

    def move(self):
        self.rect.x += self.speed * self.right
        self.rect.y += self.speed * self.down
        if self.rect.x >= screen_width:
            self.right = -1
        elif self.rect.x <= 0:
            self.right = 1
        if self.rect.y <= 0:
            self.down = 1
        elif self.rect.y >= screen_height:
            self.down = -1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)

score1_value = 0
score2_value = 0
font = pygame.font.Font('font.ttf', 40)
score1_x = 20
score1_y = 20
score2_x = 300
score2_y = 20


def show_score_1(x, y):
    score1 = font.render(""+str(score1_value), True, (255, 255, 255))
    screen.blit(score1, (x, y))


def show_score_2(x, y):
    score2 = font.render(""+str(score2_value), True, (255, 255, 255))
    screen.blit(score2, (x, y))


wall = create_wall()
wall.create_wall()
paddle = create_paddle()
ball = create_ball()
show_score_1(score1_x, score1_y)
show_score_2(score2_x, score2_y)

run = True
while run:
    pygame.time.Clock().tick(60)
    screen.fill(color="black")
    wall.draw_wall()
    paddle.draw()
    ball.draw()
    ball.move()
    paddle.move()

    # bola verifica a colisão com paddle e se for
    # verdadeira, a boa volta
    if paddle.rect.x - 20 < ball.rect.x < paddle.rect.x + 20 and paddle.rect.y - 8 < ball.rect.y < paddle.rect.y + 8:
        ball.down = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
