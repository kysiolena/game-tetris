import sys

import pygame

import blocks
from colors import Colors
from grid import Grid

# Screen size
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

# FPS
FPS = 60

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

    block_l = blocks.LBlock()
    block_j = blocks.JBlock()
    block_o = blocks.OBlock()
    block_t = blocks.TBlock()
    block_s = blocks.SBlock()
    block_z = blocks.ZBlock()
    block_i = blocks.IBlock()

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
        screen.fill(Colors.get_colors()[8])

        game_grid.draw(screen)

        # block_l.draw(screen)
        # block_j.draw(screen)
        # block_o.draw(screen)
        block_t.draw(screen)
        # block_s.draw(screen)
        # block_z.draw(screen)
        # block_i.draw(screen)

        # Update screen
        pygame.display.update()

        # Set how fast game should be run
        clock.tick(FPS)
