from pygame import Surface

from cell import Cell
from colors import Colors
from position import Position


class Grid:
    def __init__(self):
        # Rows number
        self.num_rows = 20
        # Columns number
        self.num_cols = 10

        # Cell size
        self.cell_size = 30

        # Grid matrix
        # [
        #   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], x 20
        # ]
        self.grid = [[0 for _j in range(self.num_cols)] for _i in range(self.num_rows)]

        # Colors
        self.colors = Colors.get_colors()

    def print_grid(self) -> None:
        """
        Print the Grid to the console
        :return: None
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()

    def is_inside(self, position: Position) -> bool:
        is_in_rows = 0 <= position.row < self.num_rows
        is_in_cols = 0 <= position.col < self.num_cols

        if is_in_rows and is_in_cols:
            return True

        return False

    def draw(self, surface: Surface) -> None:
        """
        Draw the Grid to the surface
        :return: None
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                # Color Cell
                color_index = self.grid[row][col]
                # Draw Cell
                Cell.draw(Position(row, col), color_index, surface)
