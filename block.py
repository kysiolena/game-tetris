from pygame import Surface

from cell import Cell
from colors import Colors


class Block:
    def __init__(self, id):
        # Type Block
        self.id = id
        # Rotate Cells variants
        self.cells = {}
        # Rotate state current (0 - 3)
        self.rotation_state = 0
        # Colors
        self.colors = Colors.get_colors()

    def draw(self, surface: Surface):
        positions = self.cells[self.rotation_state]

        for position in positions:
            # Draw Cell
            Cell.draw(position, self.id, surface)
