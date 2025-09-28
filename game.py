import random
import sys

import pygame
from pygame import Surface

from block import Block
from blocks import LBlock, JBlock, TBlock, IBlock, OBlock, SBlock, ZBlock
from colors import Colors
from grid import Grid


class Game:
    # Screen size
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 600

    # FPS
    FPS = 60

    # All blocks
    BLOCKS: tuple[Block] = (
        LBlock(),
        JBlock(),
        TBlock(),
        IBlock(),
        OBlock(),
        SBlock(),
        ZBlock(),
    )

    def __init__(self):
        # Init Pygame
        pygame.init()

        # Set game screen size
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Set caption game
        pygame.display.set_caption("Tetris")

        # How fast game should be run
        self.clock = pygame.time.Clock()

        # Custom event
        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, 200)

        # Init Grid
        self.grid = Grid()

        # Visible Blocks
        self.visible_blocks: list[Block] = list(self.BLOCKS)

        # Current block
        self.current_block: Block = self.get_random_block()

        # Next block
        self.next_block: Block = self.get_random_block()

    def get_random_block(self) -> Block:
        # Refill list of visible blocks
        if len(self.visible_blocks) == 0:
            self.visible_blocks = list(self.BLOCKS)

        # Get random block
        block = random.choice(self.visible_blocks)

        # Delete block from visible blocks
        self.visible_blocks.remove(block)

        return block

    def draw(self, surface: Surface) -> None:
        self.grid.draw(surface)
        self.current_block.draw(surface)

    def move_left(self) -> None:
        self.current_block.move(0, -1)

        if not self.is_block_inside():
            self.current_block.move(0, 1)

    def move_right(self) -> None:
        self.current_block.move(0, 1)

        if not self.is_block_inside():
            self.current_block.move(0, -1)

    def move_down(self) -> None:
        self.current_block.move(1, 0)

        if not self.is_block_inside():
            self.current_block.move(-1, 0)

    def rotate(self) -> None:
        self.current_block.rotate()

        if not self.is_block_inside():
            self.current_block.undo_rotation()

    def is_block_inside(self) -> bool:
        positions = self.current_block.get_cell_positions()

        for position in positions:
            if not self.grid.is_inside(position):
                return False

        return True

    def event_handler(self) -> None:
        for event in pygame.event.get():
            # __QUIT GAME__
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # __UPDATING POSITIONS__
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_right()
                elif event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_UP:
                    self.rotate()

            # Trigger move block down automatically with one per 200 ms
            if event.type == self.GAME_UPDATE:
                self.move_down()

    def start(self) -> None:
        while True:
            # __EVENT HANDLING__
            self.event_handler()

            # __DRAWING OBJECTS__
            self.screen.fill(Colors.get_colors()[8])

            # Draw Game
            self.draw(self.screen)

            # Update screen
            pygame.display.update()

            # Set how fast Game should be run
            self.clock.tick(self.FPS)
