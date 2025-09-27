import pygame


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
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]

        # Colors
        self.colors = self.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()

    def get_cell_colors(self):
        dark_grey = (26, 31, 40)
        green = (47, 230, 23)
        red = (232, 18, 18)
        orange = (226, 116, 17)
        yellow = (237, 234, 4)
        purple = (166, 0, 247)
        cyan = (21, 204, 209)
        blue = (13, 64, 216)

        return [dark_grey, green, red, orange, yellow, purple, cyan, blue]

    def draw(self, surface):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                # Cell Value
                cell_value = self.grid[row][col]
                # Cell Color
                cell_color = self.colors[cell_value]

                # Cell Rect
                cell_rect = pygame.Rect(
                    # Left position
                    col * self.cell_size + 1,
                    # Top position
                    row * self.cell_size + 1,
                    # Width cell
                    self.cell_size - 1,
                    # Height cell
                    self.cell_size - 1,
                )

                # Draw Cell Rect
                pygame.draw.rect(surface, cell_color, cell_rect)
