import random
import sys

import pygame
from pygame import Surface

from block import Block
from blocks import LBlock, JBlock, TBlock, IBlock, OBlock, SBlock, ZBlock
from colors import Colors
from grid import Grid


class Game:
    """
    __Scoring System
    100 points for a single line clear
    300 points for a double line clear
    500 points for a triple line clear
    1 point for each move down by the player

    __Move Block
    LEFT - press arrow left
    RIGHT - press arrow right
    DOWN - press arrow down

    __Rotate Block
    ROTATE - press arrow up

    __Restart Game
    RESTART - press space
    """

    # FPS
    FPS: int = 60

    # Speed
    SPEED: int = 1

    # Screen size
    SCREEN_WIDTH: int = 500
    SCREEN_HEIGHT: int = 620

    # Score position
    SCORE_POSITION: tuple[int, int, int, int] = (365, 20, 50, 50)
    # Next block position
    NEXT_BLOCK_POSITION: tuple[int, int, int, int] = (375, 180, 50, 50)
    # Game Over position
    GAME_OVER_POSITION: tuple[int, int, int, int] = (320, 450, 50, 50)

    # Next Block offset x, y
    NEXT_BLOCK_OFFSET: dict[int, tuple[int, int]] = {
        1: (270, 270),
        2: (270, 270),
        3: (255, 290),
        4: (250, 280),
        5: (270, 270),
        6: (270, 270),
        7: (270, 270),
    }

    visible_blocks: list[Block] = []
    current_block: Block | None = None
    next_block: Block | None = None
    game_over: bool = False
    score: int = 0

    def __init__(self):
        # Init Pygame
        pygame.init()

        # Title Font
        self.title_font = pygame.font.Font(None, 40)

        # Score Surface
        self.score_surface = self.title_font.render("Score", True, Colors.WHITE)
        # Next block Surface
        self.next_surface = self.title_font.render("Next", True, Colors.WHITE)
        # Game Over Surface
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.WHITE)

        # Score Rect
        self.score_rect = pygame.Rect(320, 55, 170, 60)
        # Next block Rect
        self.next_rect = pygame.Rect(320, 215, 170, 180)

        # Set game screen size
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Set caption game
        pygame.display.set_caption("Tetris")

        # How fast game should be run
        self.clock = pygame.time.Clock()

        # Custom event
        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, 200 // self.SPEED)

        # Init Grid
        self.grid = Grid()

        # Init game
        self.init()

    @staticmethod
    def get_blocks_list() -> list[Block]:
        return [
            LBlock(),
            JBlock(),
            TBlock(),
            IBlock(),
            OBlock(),
            SBlock(),
            ZBlock(),
        ]

    def get_random_block(self) -> Block:
        # Refill list of visible blocks
        if len(self.visible_blocks) == 0:
            self.visible_blocks = self.get_blocks_list()

        # Get random block
        block = random.choice(self.visible_blocks)

        # Delete block from visible blocks
        self.visible_blocks.remove(block)

        return block

    def draw(self, surface: Surface) -> None:
        self.grid.draw(surface)
        self.current_block.draw(surface)

        offset_x, offset_y = self.NEXT_BLOCK_OFFSET[self.next_block.id]
        self.next_block.draw(surface, offset_x, offset_y)

    def move_left(self) -> None:
        self.current_block.move(0, -1)

        if not self.is_block_inside() or not self.is_block_fits():
            self.current_block.move(0, 1)

    def move_right(self) -> None:
        self.current_block.move(0, 1)

        if not self.is_block_inside() or not self.is_block_fits():
            self.current_block.move(0, -1)

    def move_down(self, by_player: bool = False) -> None:
        self.current_block.move(1, 0)

        if by_player:
            self.update_score(0, 1)

        if not self.is_block_inside() or not self.is_block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def rotate(self) -> None:
        self.current_block.rotate()

        if not self.is_block_inside() or not self.is_block_fits():
            self.current_block.undo_rotation()

    def lock_block(self):

        positions = self.current_block.get_cell_positions()

        for position in positions:
            # 0 - empty Cell
            # Set Cell of the Grid to Current Block ID (1 - 4)
            self.grid.grid[position.row][position.col] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        # Clear full lines
        rows_cleared = self.grid.clear_full_rows()

        # Update Score
        self.update_score(rows_cleared, 0)

        # Game Over
        if not self.is_block_fits():
            self.game_over = True

    def is_block_inside(self) -> bool:
        positions = self.current_block.get_cell_positions()

        for position in positions:
            if not self.grid.is_inside(position):
                return False

        return True

    def is_block_fits(self) -> bool:
        positions = self.current_block.get_cell_positions()

        for position in positions:
            if not self.grid.is_empty(position):
                return False

        return True

    def update_score(self, lines_cleared: int = 0, move_down_points: int = 0) -> None:
        # If it has lines cleared
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500

        # Add move down points
        self.score += move_down_points

    def event_handler(self) -> None:
        for event in pygame.event.get():
            # __QUIT GAME__
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # __UPDATING POSITIONS__
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_down(True)
                    elif event.key == pygame.K_UP:
                        self.rotate()

            # Trigger move block down automatically with one per 200 ms
            if event.type == self.GAME_UPDATE and not self.game_over:
                self.move_down()

    def start(self) -> None:
        while True:
            # __EVENT HANDLING__
            self.event_handler()

            # __DRAWING OBJECTS__
            # Score Value Surface
            score_value_surface = self.title_font.render(
                str(self.score), True, Colors.WHITE
            )

            self.screen.fill(Colors.DARK_BLUE)

            # Score
            self.screen.blit(self.score_surface, self.SCORE_POSITION)
            pygame.draw.rect(self.screen, Colors.LIGHT_BLUE, self.score_rect, 0, 10)
            self.screen.blit(
                score_value_surface,
                score_value_surface.get_rect(
                    centerx=self.score_rect.centerx, centery=self.score_rect.centery
                ),
            )

            # Next block
            self.screen.blit(self.next_surface, self.NEXT_BLOCK_POSITION)
            pygame.draw.rect(self.screen, Colors.LIGHT_BLUE, self.next_rect, 0, 10)

            # Game Over
            if self.game_over:
                self.screen.blit(self.game_over_surface, self.GAME_OVER_POSITION)

            # Draw Game
            self.draw(self.screen)

            # Update screen
            pygame.display.update()

            # Set how fast Game should be run
            self.clock.tick(self.FPS)

    def init(self) -> None:
        # Visible Blocks
        self.visible_blocks = self.get_blocks_list()

        # Current block
        self.current_block = self.get_random_block()

        # Next block
        self.next_block = self.get_random_block()

        # Game Over
        self.game_over = False

        # Score
        self.score = 0

    def reset(self) -> None:
        self.grid.reset()
        self.init()
