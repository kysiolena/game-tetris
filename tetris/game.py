import datetime
import json
import os
import random
import sys
import time

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
    start_time: float = 0.0
    last_five_statistic_items = []

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

        self.font = os.path.join("tetris", "fonts", "Montserrat-Regular.ttf")

        # Title Font
        self.title_font = pygame.font.Font(self.font, 35)

        # Button Font
        self.button_font = pygame.font.Font(self.font, 25)

        # Text Font
        self.text_font = pygame.font.Font(self.font, 15)

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
        self.grid = Grid(20, 10)

        # Sidebar Rect
        self.sidebar_rect = pygame.Rect(
            self.grid.get_rect().right + OFFSET_X,
            self.grid.get_rect().top,
            SCREEN_WIDTH - self.grid.get_rect().width - 3 * OFFSET_X,
            self.grid.get_rect().height,
        )

        # Statistic
        self.game_statistic = GameStatistic()

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
            1: (270, 250),
            2: (270, 250),
            3: (255, 270),
            4: (255, 250),
            5: (270, 250),
            6: (270, 250),
            7: (270, 250),
            8: (270, 250),
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
        score_rect = pygame.Rect(
            self.sidebar_rect.left,
            self.sidebar_rect.top + 50,
            self.sidebar_rect.width,
            60,
        )

        # Score draw
        self.screen.blit(
            score_surface,
            score_surface.get_rect(
                centerx=score_rect.centerx,
                centery=score_rect.top - 25,
            ),
        )
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
        next_rect = pygame.Rect(
            self.sidebar_rect.left,
            self.sidebar_rect.top + 180,
            self.sidebar_rect.width,
            180,
        )

        # Next block draw
        self.screen.blit(
            next_surface,
            next_surface.get_rect(
                centerx=next_rect.centerx,
                centery=next_rect.top - 25,
            ),
        )
        pygame.draw.rect(self.screen, Colors.LIGHT_BLUE, next_rect, 0, 10)

    def draw_game_over(self) -> None:
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
        self.screen.blit(transparent_surface, (0, 0))

        # Rect
        game_over_rect = pygame.Rect(
            10, SCREEN_HEIGHT // 4, SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2
        )
        pygame.draw.rect(self.screen, Colors.DARK_BLUE, game_over_rect, 0, 10)

        # Title
        title_surface = self.title_font.render("GAME OVER", True, Colors.WHITE)
        self.screen.blit(
            title_surface,
            title_surface.get_rect(
                centerx=game_over_rect.centerx,
                centery=(game_over_rect.top + 40),
            ),
        )

        # Repeat button
        if not self.buttons.get("repeat"):
            self.buttons["repeat"] = Button(
                self.button_font,
                "START NEW GAME",
                ButtonBGColor(Colors.GREEN, Colors.DARK_GREEN),
                ButtonTextColor(Colors.WHITE, Colors.WHITE),
                game_over_rect.centerx - 150,
                game_over_rect.bottom - 100,
                300,
                50,
            )

        self.buttons["repeat"].draw(self.screen)

        # Repeat Game text
        repeat_text_surface = self.text_font.render(
            "Or press Space button on the keyboard", True, Colors.WHITE
        )
        self.screen.blit(
            repeat_text_surface,
            repeat_text_surface.get_rect(
                centerx=game_over_rect.centerx,
                centery=game_over_rect.bottom - 30,
            ),
        )

        # Statistic
        for index, item in enumerate(self.last_five_statistic_items):
            game_score = item["score"]
            game_time = int(item["time"])
            game_date = datetime.datetime.strptime(
                item["date"], "%Y-%m-%d %H:%M:%S"
            ).strftime("%b %d, %Y at %I:%M %p")
            text = (
                f"{index + 1}. Score: {game_score} Time: {game_time}s Date: {game_date}"
            )
            item_surface = self.text_font.render(
                text,
                True,
                Colors.WHITE if index else Colors.DARK_GREEN,
            )
            self.screen.blit(
                item_surface,
                item_surface.get_rect(
                    centerx=self.buttons["repeat"].rect.centerx,
                    centery=(game_over_rect.top + 60 + (index + 1) * 20),
                ),
            )

        # Sound
        self.SOUNDS["process"].stop()

    def draw_control_buttons(self) -> None:

        # Rotate Button
        if not self.buttons.get("rotate"):
            self.buttons["rotate"] = Button(
                self.button_font,
                "ArrUP",
                ButtonBGColor(Colors.WHITE, Colors.LIGHT_GREY),
                ButtonTextColor(Colors.DARK_GREY, Colors.DARK_GREY),
                self.sidebar_rect.centerx - 45,
                self.sidebar_rect.bottom - 210,
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
                self.sidebar_rect.left,
                self.sidebar_rect.bottom - 160,
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
                self.sidebar_rect.right - 80,
                self.sidebar_rect.bottom - 160,
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
                self.sidebar_rect.centerx - 45,
                self.sidebar_rect.bottom - 110,
                90,
                45,
            )

        self.buttons["to_down"].draw(self.screen)

        # Control text
        control_text_1_surface = self.text_font.render(
            "Or use arrow buttons", True, Colors.WHITE
        )
        control_text_2_surface = self.text_font.render(
            "on the keyboard", True, Colors.WHITE
        )

        self.screen.blit(
            control_text_1_surface,
            control_text_1_surface.get_rect(
                centerx=self.sidebar_rect.centerx,
                centery=self.sidebar_rect.bottom - 40,
            ),
        )
        self.screen.blit(
            control_text_2_surface,
            control_text_2_surface.get_rect(
                centerx=self.sidebar_rect.centerx,
                centery=self.sidebar_rect.bottom - 20,
            ),
        )

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
            # End Game
            self.game_over = True

            # Update Statistic
            self.game_statistic.update(
                self.score, time.time() - self.start_time, datetime.datetime.today()
            )

            # Statistic items for display
            self.last_five_statistic_items = self.game_statistic.get_list()[-5:]

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

        # Start Time
        self.start_time = time.time()

        # Statistic items for display
        self.last_five_statistic_items = []

        # Sound
        self.SOUNDS["process"].play(-1)

    def reset(self) -> None:
        self.grid.reset()
        self.init()


class GameStatistic:
    file_path: str = os.path.join("tetris", "statistic", "history.json")

    def update(self, score: int, game_time: float, game_date: datetime.datetime):
        # New items
        new_item = {
            "score": score,
            "time": game_time,
            "date": datetime.datetime.strftime(game_date, "%Y-%m-%d %H:%M:%S"),
        }

        # Old items
        data = self.get_list()

        # Add new items
        data.append(new_item)

        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def get_list(self) -> list:
        try:
            with open(self.file_path, "r") as f:
                data: list = json.load(f)

            return data
        except FileNotFoundError:
            # print("Error: The specified file was not found. Please check the file name and path.")

            return []
