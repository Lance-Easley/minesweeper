import pygame
from pprint import pprint
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SEA_BLUE = (0, 175, 255)
GREY = (80, 80, 80)
ORANGE = (255,180,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
MARGIN = 3

pygame.init()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 32)

screen_x = 828
screen_y = 828

screen = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption('Minesweeper')

size = 25

play_grid = []
for row in range(size):
    # Add an empty array that will hold each cell
    # in this row
    play_grid.append([])
    for column in range(size):
        rand = random.randint(0, (size//4) - 1)
        if rand == 0 and row != 0 and row != size - 1 and column != 0 and column != size - 1:
            play_grid[row].append(9)  # Append a cell
        else:
            play_grid[row].append(0)
for row in range(size):
    for column in range(size):
        if play_grid[row][column] != 9:
            total = 0
            if row != 0 and play_grid[row - 1][column] == 9:
                total += 1
            if row != 0 and column != 0 and play_grid[row - 1][column - 1] == 9:
                total += 1
            if row != 0 and column != size - 1 and play_grid[row - 1][column + 1] == 9:
                total += 1
            if row != size - 1 and play_grid[row + 1][column] == 9:
                total += 1
            if row != size - 1 and column != 0 and play_grid[row + 1][column - 1] == 9:
                total += 1
            if row != size - 1 and column != size - 1 and play_grid[row + 1][column + 1] == 9:
                total += 1
            if row != 0 and play_grid[row][column - 1] == 9:
                total += 1
            if column != size - 1 and play_grid[row][column + 1] == 9:
                total += 1
            play_grid[row][column] = total
pprint(play_grid)

clock = pygame.time.Clock()

done = False
while not done:
    screen.fill((0,0,0))
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            if pos[0] <= 450 and pos[1] <= 445:
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    print("Grid coordinates: ", column, row)
                    val_text = font.render(f'{play_grid[row][column]}', True, WHITE)
                    val_textRect = val_text.get_rect()
                    val_textRect.center = (578, 90)
                    if play_grid[row][column] == 9:
                        pass


    for row in range(size):
        for column in range(size):
            color = GREY
            if play_grid[row][column] == 9:
                color = RED
            elif play_grid[row][column] != 0 and play_grid[row][column] != 9:
                color = ORANGE
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * column + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
                0,
            )
    
    clock.tick(60)

    pygame.display.flip()