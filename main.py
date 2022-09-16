import pygame
from pprint import pprint
import random

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (80, 80, 80)
ORANGE = (255,180,0)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid cell
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

def generate_grids(solved, display):
    # Make grids and fill the solved grid with bombs
    for row in range(size):
        solved.append([])
        display.append([])
        for column in range(size):
            rand = random.randint(0, (size//4))
            if rand == 0:
                solved[row].append(9) # Bomba
            else:
                solved[row].append(0)
            display[row].append(0)

    # Comb through the solved grid to count how many bombs are next to each cell
    for row in range(size):
        for column in range(size):
            if solved[row][column] != 9:
                total = 0
                if solved[max(0, row - 1)][column] == 9:
                    total += 1
                if solved[max(0, row - 1)][max(0, column - 1)] == 9:
                    total += 1
                if solved[max(0, row - 1)][min(size - 1, column + 1)] == 9:
                    total += 1
                if solved[min(size - 1, row + 1)][column] == 9:
                    total += 1
                if solved[min(size - 1, row + 1)][max(0, column - 1)] == 9:
                    total += 1
                if solved[min(size - 1, row + 1)][min(size - 1, column + 1)] == 9:
                    total += 1
                if solved[row][max(0, column - 1)] == 9:
                    total += 1
                if solved[row][min(size - 1, column + 1)] == 9:
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

    if solved[max(0, row - 1)][min(size - 1, col + 1)] != 2:
        solved[max(0, row - 1)][min(size - 1, col + 1)] = 1
        if display[max(0, row - 1)][min(size - 1, col + 1)] == 0:
            check_adjacents(solved, display, max(0, row - 1), min(size - 1, col + 1))

    if solved[min(size - 1, row + 1)][col] != 2:
        solved[min(size - 1, row + 1)][col] = 1
        if display[min(size - 1, row + 1)][col] == 0:
            check_adjacents(solved, display, min(size - 1, row + 1), col)

    if solved[min(size - 1, row + 1)][max(0, col - 1)] != 2:
        solved[min(size - 1, row + 1)][max(0, col - 1)] = 1
        if display[min(size - 1, row + 1)][max(0, col - 1)] == 0:
            check_adjacents(solved, display, min(size - 1, row + 1), max(0, col - 1))

    if solved[min(size - 1, row + 1)][min(size - 1, col + 1)] != 2:
        solved[min(size - 1, row + 1)][min(size - 1, col + 1)] = 1
        if display[min(size - 1, row + 1)][min(size - 1, col + 1)] == 0:
            check_adjacents(solved, display, min(size - 1, row + 1), min(size - 1, col + 1))
            
    if solved[row][max(0, col - 1)] != 2:
        solved[row][max(0, col - 1)] = 1
        if display[row][max(0, col - 1)] == 0:
            check_adjacents(solved, display, row, max(0, col - 1))
            
    if solved[row][min(size - 1, col + 1)] != 2:
        solved[row][min(size - 1, col + 1)] = 1
        if display[row][min(size - 1, col + 1)] == 0:
            check_adjacents(solved, display, row, min(size - 1, col + 1))

def draw_cell(row, column, color):
    pygame.draw.rect(screen, color, ((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT), 0)

while True:
    solved_grid = []
    display_grid = []
    generate_grids(solved_grid, display_grid)
    if solved_grid[size // 2][size // 2] == 0:
        display_grid[size // 2][size // 2] = 1
        check_adjacents(display_grid, solved_grid, size // 2, size // 2)
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
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
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
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
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


    for row in range(size):
        for column in range(size):
            if display_grid[row][column] == 1 or display_grid[row][column] == 2: # Numbered Spaces
                if solved_grid[row][column] == 9:
                    draw_cell(row, column, RED)
                elif solved_grid[row][column] != 0 and solved_grid[row][column] != 9:
                    draw_cell(row, column, ORANGE)

                    # Number text
                    num_text = font.render(f"{solved_grid[row][column]}", True, WHITE)
                    num_textRect = num_text.get_rect()
                    num_textRect.center = (
                        ((MARGIN + WIDTH) * column + MARGIN) + WIDTH // 2, 
                        ((MARGIN + HEIGHT) * row + MARGIN) + (HEIGHT + MARGIN) // 2,
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