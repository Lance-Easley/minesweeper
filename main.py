import pygame
from pprint import pprint
import random

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (80, 80, 80)
ORANGE = (255,160,0)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid cell
CELL_WIDTH = 30
CELL_HEIGHT = 30
CELL_MARGIN = 3
GRID_SIZE = 10
BOMB_COUNT = 10

pygame.init()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 26)

screen_x = CELL_WIDTH * GRID_SIZE + CELL_MARGIN * GRID_SIZE + CELL_MARGIN
screen_y = CELL_HEIGHT * GRID_SIZE + CELL_MARGIN * GRID_SIZE + CELL_MARGIN

screen = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption('Minesweeper')

def generate_grids(solved, display):
    # Display: 0 = Undiscovered, 1 = Bomb Near Cell, 2 = No Bomb Near Cell, 9 = Flagged
    # Solved: 9 = Bomba, all other numbers are the surrounding bomba counts
    # Make grids and fill the solved grid with bombs
    for row in range(GRID_SIZE):
        solved.append([])
        display.append([])
        for column in range(GRID_SIZE):
            solved[row].append(0)
            display[row].append(0)

    for row, col in random.sample({(row_i, col_i) for col_i in range(GRID_SIZE) for row_i in range(GRID_SIZE)}, BOMB_COUNT):
        solved[row][col] = 9

    # Comb through the solved grid to count how many bombs are next to each cell
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if solved[row][column] != 9:
                total = 0

                if row != 0 and solved[row - 1][column] == 9:
                    total += 1
                if row != 0 and column != 0 and solved[row - 1][column - 1] == 9:
                    total += 1
                if row != 0 and column != GRID_SIZE - 1 and solved[row - 1][column + 1] == 9:
                    total += 1
                if row != GRID_SIZE - 1 and solved[row + 1][column] == 9:
                    total += 1
                if row != GRID_SIZE - 1 and column != 0 and solved[row + 1][column - 1] == 9:
                    total += 1
                if row != GRID_SIZE - 1 and column != GRID_SIZE - 1 and solved[row + 1][column + 1] == 9:
                    total += 1
                if column != 0 and solved[row][column - 1] == 9:
                    total += 1
                if column != GRID_SIZE - 1 and solved[row][column + 1] == 9:
                    total += 1

                solved[row][column] = total
    return solved, display

def check_adjacents(solved, display, row, col):
    solved[row][col] = 2
    
    if solved[max(0, row - 1)][col] != 2:
        solved[max(0, row - 1)][col] = 1
        if display[max(0, row - 1)][col] == 0:
            check_adjacents(solved, display, max(0, row - 1), col)

    if solved[max(0, row - 1)][max(0, col - 1)] != 2:
        solved[max(0, row - 1)][max(0, col - 1)] = 1
        if display[max(0, row - 1)][max(0, col - 1)] == 0:
            check_adjacents(solved, display, max(0, row - 1), max(0, col - 1))

    if solved[max(0, row - 1)][min(GRID_SIZE - 1, col + 1)] != 2:
        solved[max(0, row - 1)][min(GRID_SIZE - 1, col + 1)] = 1
        if display[max(0, row - 1)][min(GRID_SIZE - 1, col + 1)] == 0:
            check_adjacents(solved, display, max(0, row - 1), min(GRID_SIZE - 1, col + 1))

    if solved[min(GRID_SIZE - 1, row + 1)][col] != 2:
        solved[min(GRID_SIZE - 1, row + 1)][col] = 1
        if display[min(GRID_SIZE - 1, row + 1)][col] == 0:
            check_adjacents(solved, display, min(GRID_SIZE - 1, row + 1), col)

    if solved[min(GRID_SIZE - 1, row + 1)][max(0, col - 1)] != 2:
        solved[min(GRID_SIZE - 1, row + 1)][max(0, col - 1)] = 1
        if display[min(GRID_SIZE - 1, row + 1)][max(0, col - 1)] == 0:
            check_adjacents(solved, display, min(GRID_SIZE - 1, row + 1), max(0, col - 1))

    if solved[min(GRID_SIZE - 1, row + 1)][min(GRID_SIZE - 1, col + 1)] != 2:
        solved[min(GRID_SIZE - 1, row + 1)][min(GRID_SIZE - 1, col + 1)] = 1
        if display[min(GRID_SIZE - 1, row + 1)][min(GRID_SIZE - 1, col + 1)] == 0:
            check_adjacents(solved, display, min(GRID_SIZE - 1, row + 1), min(GRID_SIZE - 1, col + 1))
            
    if solved[row][max(0, col - 1)] != 2:
        solved[row][max(0, col - 1)] = 1
        if display[row][max(0, col - 1)] == 0:
            check_adjacents(solved, display, row, max(0, col - 1))
            
    if solved[row][min(GRID_SIZE - 1, col + 1)] != 2:
        solved[row][min(GRID_SIZE - 1, col + 1)] = 1
        if display[row][min(GRID_SIZE - 1, col + 1)] == 0:
            check_adjacents(solved, display, row, min(GRID_SIZE - 1, col + 1))

def draw_cell(row, column, color):
    pygame.draw.rect(screen, color, ((CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN, (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN, CELL_WIDTH, CELL_HEIGHT), 0, 2)

while True:
    solved_grid = []
    display_grid = []
    generate_grids(solved_grid, display_grid)
    if solved_grid[GRID_SIZE // 2][GRID_SIZE // 2] == 0:
        display_grid[GRID_SIZE // 2][GRID_SIZE // 2] = 1
        check_adjacents(display_grid, solved_grid, GRID_SIZE // 2, GRID_SIZE // 2)
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
            if event.button == 1:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (CELL_WIDTH + CELL_MARGIN)
                row = pos[1] // (CELL_HEIGHT + CELL_MARGIN)
                print("Grid coordinates: ", column, row)
                if solved_grid[row][column] == 9:
                    pass # Game Over
                if display_grid[row][column] == 0:
                    if solved_grid[row][column] == 0:
                        check_adjacents(display_grid, solved_grid, row, column)
                        
                    display_grid[row][column] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (CELL_WIDTH + CELL_MARGIN)
                row = pos[1] // (CELL_HEIGHT + CELL_MARGIN)
                print("Grid coordinates: ", column, row)
                if display_grid[row][column] == 0:
                    display_grid[row][column] = 9
                elif display_grid[row][column] == 9:
                    display_grid[row][column] = 0
            if event.key == pygame.K_s:
                print("Display:")
                pprint(display_grid)
                print("Solved:")
                pprint(solved_grid)


    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if display_grid[row][column] == 1 or display_grid[row][column] == 2: # Numbered Spaces
                if solved_grid[row][column] == 9:
                    draw_cell(row, column, RED)
                elif solved_grid[row][column] != 0 and solved_grid[row][column] != 9:
                    draw_cell(row, column, ORANGE)

                    # Number text
                    num_text = font.render(f"{solved_grid[row][column]}", True, WHITE)
                    num_textRect = num_text.get_rect()
                    num_textRect.center = (
                        ((CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN) + CELL_WIDTH // 2, 
                        ((CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN) + (CELL_HEIGHT + CELL_MARGIN) // 2,
                    )
                    screen.blit(num_text, num_textRect)
                else:
                    draw_cell(row, column, GREY)

            elif display_grid[row][column] == 9: # Flagged
                draw_cell(row, column, YELLOW)

            else: # Undiscovered
                draw_cell(row, column, ORANGE)
    
    clock.tick(60)

    pygame.display.flip()