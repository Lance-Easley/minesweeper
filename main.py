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
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
MARGIN = 3

pygame.init()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 26)

screen_x = 828
screen_y = 828

screen = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption('Minesweeper')

size = 25

def generate_grids(grid1, grid2):
    for row in range(size):
        # Add an empty array that will hold each cell
        # in this row
        grid1.append([])
        grid2.append([])
        for column in range(size):
            rand = random.randint(0, (size//4) - 1)
            if rand == 0 and row != 0 and row != size - 1 and column != 0 and column != size - 1:
                grid1[row].append(9)  # Append a cell
            else:
                grid1[row].append(0)
            grid2[row].append(0)

    for row in range(size):
        for column in range(size):
            if grid1[row][column] != 9:
                total = 0
                if row != 0 and grid1[row - 1][column] == 9:
                    total += 1
                if row != 0 and column != 0 and grid1[row - 1][column - 1] == 9:
                    total += 1
                if row != 0 and column != size - 1 and grid1[row - 1][column + 1] == 9:
                    total += 1
                if row != size - 1 and grid1[row + 1][column] == 9:
                    total += 1
                if row != size - 1 and column != 0 and grid1[row + 1][column - 1] == 9:
                    total += 1
                if row != size - 1 and column != size - 1 and grid1[row + 1][column + 1] == 9:
                    total += 1
                if row != 0 and grid1[row][column - 1] == 9:
                    total += 1
                if column != size - 1 and grid1[row][column + 1] == 9:
                    total += 1
                grid1[row][column] = total
    return grid1, grid2

def check_adjacents(grid1, grid2, row, col):
    grid1[row][col] = 2
    if row != 0:
        if grid1[row - 1][col] != 2:
            grid1[row - 1][col] = 1
            if grid2[row - 1][col] == 0:
                check_adjacents(grid1, grid2, row - 1, col)
    if row != 0 and col != 0:
        if grid1[row - 1][col - 1] != 2:
            grid1[row - 1][col - 1] = 1
            if grid2[row - 1][col - 1] == 0:
                check_adjacents(grid1, grid2, row - 1, col - 1)
    if row != 0 and col != size - 1:
        if grid1[row - 1][col + 1] != 2:
            grid1[row - 1][col + 1] = 1
            if grid2[row - 1][col + 1] == 0:
                check_adjacents(grid1, grid2, row - 1, col + 1)
    if row != size - 1:
        if grid1[row + 1][col] != 2:
            grid1[row + 1][col] = 1
            if grid2[row + 1][col] == 0:
                check_adjacents(grid1, grid2, row + 1, col)
    if row != size - 1 and col != 0:
        if grid1[row + 1][col - 1] != 2:
            grid1[row + 1][col - 1] = 1
            if grid2[row + 1][col - 1] == 0:
                check_adjacents(grid1, grid2, row + 1, col - 1)
    if row != size - 1 and col != size - 1:
        if grid1[row + 1][col + 1] != 2:
            grid1[row + 1][col + 1] = 1
            if grid2[row + 1][col + 1] == 0:
                check_adjacents(grid1, grid2, row + 1, col + 1)
    if row != 0 and col != 0:
        if grid1[row][col - 1] != 2:
            grid1[row][col - 1] = 1
            if grid2[row][col - 1] == 0:
                check_adjacents(grid1, grid2, row, col - 1)
    if col != size - 1:
        if grid1[row][col + 1] != 2:
            grid1[row][col + 1] = 1
            if grid2[row][col + 1] == 0:
                check_adjacents(grid1, grid2, row, col + 1)

while True:
    play_grid = []
    game_grid = []
    generate_grids(play_grid, game_grid)
    if play_grid[size // 2][size // 2] == 0:
        game_grid[size // 2][size // 2] = 1
        check_adjacents(game_grid, play_grid, size // 2, size // 2)
        break

clock = pygame.time.Clock()

done = False
while not done:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            print("Grid coordinates: ", column, row)
            if play_grid[row][column] == 9:
                pygame.quit()
                exit()
            if game_grid[row][column] == 0:
                if play_grid[row][column] == 0:
                    check_adjacents(game_grid, play_grid, row, column)
                    
                game_grid[row][column] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                print("Grid coordinates: ", column, row)
                if game_grid[row][column] == 0:
                    game_grid[row][column] = 9
                elif game_grid[row][column] == 9:
                    game_grid[row][column] = 0


    for row in range(size):
        for column in range(size):
            color = GREY
            if game_grid[row][column] == 1 or game_grid[row][column] == 2:
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
                # Player text
                num_text = font.render(f"{play_grid[row][column]}", True, WHITE)
                num_textRect = num_text.get_rect()
                num_textRect.center = (
                    ((MARGIN + WIDTH) * column + MARGIN) + WIDTH // 2, 
                    ((MARGIN + HEIGHT) * row + MARGIN) + (HEIGHT + MARGIN) // 2,
                )
                screen.blit(num_text, num_textRect)
            elif game_grid[row][column] == 9:
                color = YELLOW
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
            else:
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