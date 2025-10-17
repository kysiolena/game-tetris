import pygame
from pygame import Surface

from .colors import Colors
from .position import Position
from .settings import CELL_SIZE, OFFSET_X, OFFSET_Y


class Cell:
    COLORS = Colors.get_colors()

    @classmethod
    def draw(
        cls,
        position: Position,
        color_index: int,
        surface: Surface,
        offset_x: int = OFFSET_X,
        offset_y: int = OFFSET_Y,
        size: int = CELL_SIZE,
    ):
        # Cell Color
        cell_color = cls.COLORS[color_index]

        # Cell Rect
        cell_rect = pygame.Rect(
            # Left position
            position.col * size + offset_x,
            # Top position
            position.row * size + offset_y,
            # Width cell
            size - 1,
            # Height cell
            size - 1,
        )

        # Draw Cell Rect
        pygame.draw.rect(surface, cell_color, cell_rect)
