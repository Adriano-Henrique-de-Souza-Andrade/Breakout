import pygame
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


class wall():
    def __init__(self):
        self.width = screen_width / cols
        self.height = 10

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
wall = wall()
wall.create_wall()
run = True
while run:
    wall.draw_wall()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
