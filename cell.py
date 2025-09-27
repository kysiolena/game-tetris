import pygame
from pygame import Surface

from colors import Colors
from position import Position


class Cell:
    size = 30
    colors = Colors.get_colors()

    @classmethod
    def draw(cls, position: Position, color_index: int, surface: Surface):
        # Cell Color
        cell_color = cls.colors[color_index]

        # Cell Rect
        cell_rect = pygame.Rect(
            # Left position
            position.col * cls.size + 1,
            # Top position
            position.row * cls.size + 1,
            # Width cell
            cls.size - 1,
            # Height cell
            cls.size - 1,
        )

        # Draw Cell Rect
        pygame.draw.rect(surface, cell_color, cell_rect)
