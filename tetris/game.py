import os
import random
import sys

import pygame
from pygame import Surface

from .block import Block
from .blocks import LBlock, JBlock, TBlock, IBlock, OBlock, SBlock, ZBlock, UBlock
from .button import Button, ButtonBGColor, ButtonTextColor
from .colors import Colors
from .grid import Grid
from .settings import *


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

    visible_blocks: list[Block] = []
    current_block: Block | None = None
    next_block: Block | None = None
    game_over: bool = False
    score: int = 0

    # Buttons
    buttons: dict[str, Button] = {}

    def __init__(self):
        # Init Pygame
        pygame.init()

        # Sounds
        self.SOUNDS: dict = {
            "process": pygame.mixer.Sound(
                os.path.join("tetris", "sounds", "music.ogg")
            ),
            "rotate": pygame.mixer.Sound(
                os.path.join("tetris", "sounds", "rotate.ogg")
            ),
            "clear": pygame.mixer.Sound(os.path.join("tetris", "sounds", "clear.ogg")),
        }

        # Title Font
        self.title_font = pygame.font.Font(None, 40)

        # Button Font
        self.button_font = pygame.font.Font(None, 30)

        # Set game screen size
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
            UBlock(),
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

        # Next Block offset x, y
        next_block_offsets: dict[int, tuple[int, int]] = {
            1: (270, 270),
            2: (270, 270),
            3: (255, 290),
            4: (255, 270),
            5: (270, 270),
            6: (270, 270),
            7: (270, 270),
            8: (270, 270),
        }

        offset_x, offset_y = next_block_offsets[self.next_block.id]
        self.next_block.draw(surface, offset_x, offset_y)

    def draw_score(self) -> None:
        # Score Surface
        score_surface = self.title_font.render("Score", True, Colors.WHITE)

        # Score Value Surface
        score_value_surface = self.title_font.render(
            str(self.score), True, Colors.WHITE
        )

        # Score Rect
        score_rect = pygame.Rect(320, 55, 170, 60)

        # Score draw
        self.screen.blit(score_surface, (365, 20, 50, 50))
        pygame.draw.rect(self.screen, Colors.LIGHT_BLUE, score_rect, 0, 10)
        self.screen.blit(
            score_value_surface,
            score_value_surface.get_rect(
                centerx=score_rect.centerx, centery=score_rect.centery
            ),
        )

    def draw_next(self) -> None:
        # Next block Surface
        next_surface = self.title_font.render("Next", True, Colors.WHITE)

        # Next block Rect
        next_rect = pygame.Rect(320, 215, 170, 180)

        # Next block draw
        self.screen.blit(next_surface, (375, 180, 50, 50))
        pygame.draw.rect(self.screen, Colors.LIGHT_BLUE, next_rect, 0, 10)

    def draw_game_over(self) -> None:
        # Game Over Surface
        game_over_surface = self.title_font.render("GAME OVER", True, Colors.WHITE)

        # Game Over Rect
        game_over_rect = pygame.Rect(
            10, SCREEN_HEIGHT // 4, SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2
        )

        # Backdrop
        transparent_surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        game_over_bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(
            transparent_surface,
            Colors.WHITE + (128,),
            game_over_bg_rect,
            0,
        )

        # Game Over draw
        self.screen.blit(transparent_surface, (0, 0))
        pygame.draw.rect(self.screen, Colors.DARK_BLUE, game_over_rect, 0, 10)
        self.screen.blit(
            game_over_surface,
            game_over_surface.get_rect(
                centerx=game_over_rect.centerx,
                centery=(SCREEN_HEIGHT // 4 + 40),
            ),
        )

        self.draw_repeat_button()

        # Sound
        self.SOUNDS["process"].stop()

    def draw_repeat_button(self) -> None:
        # Repeat Button
        if not self.buttons.get("repeat"):
            self.buttons["repeat"] = Button(
                self.button_font,
                "START NEW GAME",
                ButtonBGColor(Colors.GREEN, Colors.DARK_GREEN),
                ButtonTextColor(Colors.WHITE, Colors.WHITE),
                SCREEN_WIDTH // 2 - 150,
                SCREEN_HEIGHT - SCREEN_HEIGHT // 4 - 70,
                300,
                50,
            )

        self.buttons["repeat"].draw(self.screen)

    def draw_control_buttons(self) -> None:

        # Rotate Button
        if not self.buttons.get("rotate"):
            self.buttons["rotate"] = Button(
                self.button_font,
                "ArrUP",
                ButtonBGColor(Colors.WHITE, Colors.LIGHT_GREY),
                ButtonTextColor(Colors.DARK_GREY, Colors.DARK_GREY),
                355,
                420,
                90,
                45,
            )

        self.buttons["rotate"].draw(self.screen)

        # To Left Button
        if not self.buttons.get("to_left"):
            self.buttons["to_left"] = Button(
                self.button_font,
                "ArrL",
                ButtonBGColor(Colors.WHITE, Colors.LIGHT_GREY),
                ButtonTextColor(Colors.DARK_GREY, Colors.DARK_GREY),
                320,
                475,
                80,
                45,
            )

        self.buttons["to_left"].draw(self.screen)

        # To Right Button
        if not self.buttons.get("to_right"):
            self.buttons["to_right"] = Button(
                self.button_font,
                "ArrR",
                ButtonBGColor(Colors.WHITE, Colors.LIGHT_GREY),
                ButtonTextColor(Colors.DARK_GREY, Colors.DARK_GREY),
                # (405, 475, 80, 45)
                405,
                475,
                80,
                45,
            )

        self.buttons["to_right"].draw(self.screen)

        # To Down Button
        if not self.buttons.get("to_down"):
            self.buttons["to_down"] = Button(
                self.button_font,
                "ArrD",
                ButtonBGColor(Colors.WHITE, Colors.LIGHT_GREY),
                ButtonTextColor(Colors.DARK_GREY, Colors.DARK_GREY),
                355,
                530,
                90,
                45,
            )

        self.buttons["to_down"].draw(self.screen)

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
        else:
            # Sound
            self.SOUNDS["rotate"].play()

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

        if rows_cleared > 0:
            # Sound
            self.SOUNDS["clear"].play()

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

            # __MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse current position
                mouse_pos = pygame.mouse.get_pos()

                if self.game_over:
                    # Repeat Button
                    repeat_button = self.buttons.get("repeat")
                    if repeat_button and repeat_button.is_collide(mouse_pos):
                        self.reset()
                else:
                    # Rotate Button
                    rotate_button = self.buttons.get("rotate")
                    if rotate_button and rotate_button.is_collide(mouse_pos):
                        self.rotate()

                    # To Left Button
                    left_button = self.buttons.get("to_left")
                    if left_button and left_button.is_collide(mouse_pos):
                        self.move_left()

                    # To Right Button
                    right_button = self.buttons.get("to_right")
                    if right_button and right_button.is_collide(mouse_pos):
                        self.move_right()

                    # To Down Button
                    down_button = self.buttons.get("to_down")
                    if down_button and down_button.is_collide(mouse_pos):
                        self.move_down(True)

            if event.type == pygame.MOUSEMOTION:
                # Mouse current position
                mouse_pos = pygame.mouse.get_pos()

                if self.game_over:
                    # Repeat Button
                    repeat_button = self.buttons.get("repeat")
                    if repeat_button:
                        repeat_button.mouse_move(mouse_pos)

                else:
                    # Rotate Button
                    rotate_button = self.buttons.get("rotate")
                    if rotate_button:
                        rotate_button.mouse_move(mouse_pos)

                    # To Left Button
                    left_button = self.buttons.get("to_left")
                    if left_button:
                        left_button.mouse_move(mouse_pos)

                    # To Right Button
                    right_button = self.buttons.get("to_right")
                    if right_button:
                        right_button.mouse_move(mouse_pos)

                    # To Down Button
                    down_button = self.buttons.get("to_down")
                    if down_button:
                        down_button.mouse_move(mouse_pos)

            # Trigger move block down automatically with one per 200 ms
            if event.type == self.GAME_UPDATE and not self.game_over:
                self.move_down()

    def start(self) -> None:
        while True:
            # __EVENT HANDLING__
            self.event_handler()

            # __DRAWING OBJECTS__
            self.screen.fill(Colors.DARK_BLUE)

            self.draw_score()
            self.draw_next()
            self.draw_control_buttons()

            # Draw Game
            self.draw(self.screen)

            # Game Over
            if self.game_over:
                self.draw_game_over()

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

        # Sound
        self.SOUNDS["process"].play(-1)

    def reset(self) -> None:
        self.grid.reset()
        self.init()
