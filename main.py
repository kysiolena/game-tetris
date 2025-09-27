import sys

import pygame

from grid import Grid

# Screen size
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

# FPS
FPS = 60

# Colors
DARK_BLUE = (44, 44, 127)

if __name__ == "__main__":
    # Init Pygame
    pygame.init()

    # Set game screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set caption game
    pygame.display.set_caption("Tetris")

    # How fast game should be run
    clock = pygame.time.Clock()

    # Game Loop
    # 1. Event Handling
    # 2. Updating Positions
    # 3. Drawing Objects

    # Init Grid
    game_grid = Grid()

    game_grid.grid[0][0] = 1
    game_grid.grid[3][5] = 4
    game_grid.grid[17][8] = 7

    game_grid.print_grid()

    # Init infinity loop
    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Drawing
        screen.fill(DARK_BLUE)

        game_grid.draw(screen)

        # Update screen
        pygame.display.update()

        # Set how fast game should be run
        clock.tick(FPS)
