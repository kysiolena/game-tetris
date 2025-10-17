import pygame
from pygame import Surface

from .cell import Cell
from .colors import Colors
from .position import Position
from .settings import CELL_SIZE, OFFSET_X, OFFSET_Y


class Grid:
    def __init__(self, num_rows: int = 20, num_cols: int = 10):
        # Rows number
        self.num_rows = num_rows
        # Columns number
        self.num_cols = num_cols

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

    def is_empty(self, position: Position) -> bool:
        if self.grid[position.row][position.col] == 0:
            return True

        return False

    def is_row_full(self, row: int) -> bool:
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False

        return True

    def clear_full_rows(self) -> int:
        completed = 0

        # Check all rows from bottom to top
        for row in range(self.num_rows - 1, 0, -1):
            # Clear the row if it is full
            if self.is_row_full(row):
                self.clear_row(row)

                completed += 1
            # Move down the row if the row beyond it is full
            elif completed > 0:
                self.move_row_down(row, completed)

        return completed

    def clear_row(self, row: int) -> None:
        for col in range(self.num_cols):
            self.clear_col(row, col)

    def clear_col(self, row: int, col: int) -> None:
        # Set value column to 0
        self.grid[row][col] = 0

    def reset(self) -> None:
        for row in range(self.num_rows):
            self.clear_row(row)

    def move_row_down(self, row: int, cleared_num_rows: int) -> None:
        for col in range(self.num_cols):
            # Replace the columns of the cleared row with the columns of the row above
            self.grid[row + cleared_num_rows][col] = self.grid[row][col]
            # Clear column
            self.clear_col(row, col)

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

    def get_rect(self, x: int = OFFSET_X, y: int = OFFSET_Y) -> pygame.Rect:
        return pygame.Rect(x, y, self.num_cols * CELL_SIZE, self.num_rows * CELL_SIZE)
