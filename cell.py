import pygame
from pygame import Surface

from colors import Colors
from position import Position


class Cell:
    SIZE = 30
    OFFSET_TOP = 11
    OFFSET_LEFT = 11
    COLORS = Colors.get_colors()

    @classmethod
    def draw(cls, position: Position, color_index: int, surface: Surface):
        # Cell Color
        cell_color = cls.COLORS[color_index]

        # Cell Rect
        cell_rect = pygame.Rect(
            # Left position
            position.col * cls.SIZE + cls.OFFSET_LEFT,
            # Top position
            position.row * cls.SIZE + cls.OFFSET_TOP,
            # Width cell
            cls.SIZE - 1,
            # Height cell
            cls.SIZE - 1,
        )

        # Draw Cell Rect
        pygame.draw.rect(surface, cell_color, cell_rect)
