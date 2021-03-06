import pygame
from pygame.locals import *

pygame.init()

screen_width = 400
screen_height = 600
count_hit_paddle = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BREAKOUT GAME')

background_color = (0, 0, 0)
paddle_color = (0, 197, 205)
RED = (205, 51, 51)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
ORANGE = (238, 118, 0)
WHITE = (255, 255, 255)

brick_sound = pygame.mixer.Sound('sounds_brick.wav')
paddle_sound = pygame.mixer.Sound('sounds_paddle.wav')
wall_sound = pygame.mixer.Sound('sounds_wall.wav')

cols = 14
rows = 8
score = 0
chances = 0


class Wall:
    def __init__(self):
        self.width = screen_width / cols
        self.height = 10
        self.blocks = []

    def create_wall(self):
        self.blocks = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = 100 + row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                value = 0
                color = 0
                if row < 2:
                    color = 4
                    value = 7
                elif row < 4:
                    color = 3
                    value = 5
                elif row < 6:
                    color = 2
                    value = 3
                elif row < 8:
                    color = 1
                    value = 1
                block_individual = [rect, color, value]
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


class CreatePaddle:
    def __init__(self):
        self.short = False
        self.height = 10
        self.width = int(screen_width / cols)
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - 100
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.speed = 5

    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.x = mouse_x - int(screen_width / cols)/2

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)


class CreateBall:
    def __init__(self):
        self.game_over = 1
        self.score = 0
        self.right = -1
        self.down = 1
        self.height = 5
        self.width = 5
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = (screen_width // 2) - (self.width // 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.speed = 0
        self.level = 0

    def move(self):

        self.rect.x += self.speed * self.right
        self.rect.y += self.speed * self.down
        if self.rect.x >= screen_width and self.right > 0:
            self.right *= -1
            wall_sound.play()
        elif self.rect.x <= 0 and self.right < 0:
            self.right *= -1
            wall_sound.play()
        if self.rect.y <= 0 and self.down < 0:
            self.down *= -1
            wall_sound.play()
        elif self.rect.y >= screen_height and self.down > 0:
            self.down *= -1
            wall_sound.play()

        # speed set
        if count_hit_paddle < 4:
            self.speed = 2.5
        elif count_hit_paddle < 12:
            self.speed = 3
        elif self.rect.y <= 141 and self.level == 0:
            self.level = 1
            self.speed = 3.5

        elif self.rect.y <= 121 and self.level == 1:
            self.speed = 4

        # set to become harder
        collision_thresh = 5
        wall_destroyed = 1
        row_count = 0

        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.down > 0:
                        self.down *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.down < 0:
                        self.down *= -1
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.right > 0:
                        self.right *= -1
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.right < 0:
                        self.right *= -1
                    # reduce the block's strength by doing damage to it
                    wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                    self.score += wall.blocks[row_count][item_count][2]
                    brick_sound.play()

                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0

                # increase item counter
                item_count += 1

            # increase row counter
            row_count += 1

        # after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)


wall = Wall()
wall.create_wall()
paddle = CreatePaddle()
ball = CreateBall()

run = True
while run:
    pygame.time.Clock().tick(60)
    screen.fill(color="black")
    wall.draw_wall()
    paddle.draw()
    ball.draw()
    ball.move()
    paddle.move()

    mx, my = pygame.mouse.get_pos()

    font = pygame.font.Font('font.ttf', 30)
    text = font.render(str(f"{ball.score:03}"), True, WHITE)
    screen.blit(text, (40, 50))
    text = font.render('000', True, WHITE)
    screen.blit(text, (275, 50))
    text = font.render('1', True, WHITE)
    screen.blit(text, (20, 10))
    text = font.render(f"{chances}", True, WHITE)
    screen.blit(text, (250, 10))

    if mx - 20 < ball.rect.x < mx + 20 and paddle.rect.y - 8 < ball.rect.y < paddle.rect.y + 8:
        if ball.down == 1:
            count_hit_paddle += 1
        ball.down = -1
        if mx - 14 < ball.rect.x < mx + 10:
            if ball.rect.x > mx and ball.right < 0:
                ball.right = 1
            elif ball.rect.x < mx and ball.right > 0:
                ball.right = -1
        elif mx - 20 < ball.rect.x < mx + 20:
            if ball.rect.x > mx and ball.right < 0:
                ball.right = 2
            elif ball.rect.x < mx and ball.right > 0:
                ball.right = -2
        paddle_sound.play()

    if ball.rect.y < 100:
        paddle.rect.width = int(screen_width / cols) / 2

    if ball.rect.y > 590:
        chances += 1
        ball.rect.x = (screen_width // 2)
        ball.rect.y = (screen_width // 2)
        if chances == 3:
            font = pygame.font.Font('Upheaval.ttf', 50)
            text = font.render(str("YOU LOSE"), True, RED)
            screen.blit(text, (87, 320))
            font = pygame.font.Font('Upheaval.ttf', 20)
            text = font.render(str(" Wait 5 scs to play again"), True, RED)
            screen.blit(text, (60, 370))
            text = font.render(str("Press Esc to exit the game"), True, RED)
            screen.blit(text, (60, 390))
            pygame.display.flip()

            pygame.time.wait(5000)
            ball.score = 0
            wall.create_wall()
            paddle.rect.width = int(screen_width / cols)
            chances = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
