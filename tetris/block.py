from pygame import Surface

from .cell import Cell
from .colors import Colors
from .position import Position


class Block:
    def __init__(self, id: int):
        # Type Block
        self.id = id
        # Rotate Cells variants
        self.cells: dict[int, list[Position]] = {}
        # Offsets
        self.row_offset = 0
        self.col_offset = 0
        # Rotate state current (0 - 3)
        self.rotation_state = 0
        # Colors
        self.colors = Colors.get_colors()

    def move(self, rows: int, cols: int) -> None:
        self.row_offset += rows
        self.col_offset += cols

    def rotate(self):
        self.rotation_state += 1

        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1

        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1

    def get_cell_positions(self) -> list[Position]:
        positions = self.cells[self.rotation_state]
        moved_positions = []

        for position in positions:
            # Change Position
            position = Position(
                position.row + self.row_offset, position.col + self.col_offset
            )
            moved_positions.append(position)

        return moved_positions

    def draw(self, surface: Surface, offset_x: int = 11, offset_y: int = 11) -> None:
        positions = self.get_cell_positions()

        for position in positions:
            # Draw Cell
            Cell.draw(position, self.id, surface, offset_x, offset_y)
