from block import Block
from position import Position


class LBlock(Block):
    """
    Matrix 3x3
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(2, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)],
        }


class JBlock(Block):
    """
    Matrix 3x3
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(2, 2), Position(1, 2), Position(1, 1), Position(1, 0)],
            3: [Position(2, 0), Position(2, 1), Position(1, 1), Position(0, 1)],
        }


class IBlock(Block):
    """
    Matrix 4x4
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(2, 3)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)],
        }


class OBlock(Block):
    """
    Matrix 2x2
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            1: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            2: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            3: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
        }


class SBlock(Block):
    """
    Matrix 3x3
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)],
        }


class TBlock(Block):
    """
    Matrix 3x3
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(1, 2), Position(0, 1), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(1, 0), Position(0, 1), Position(1, 1), Position(2, 1)],
        }


class ZBlock(Block):
    """
    Matrix 3x3
    """

    def __init__(self):
        # Set type of Block
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(0, 1), Position(1, 1), Position(2, 0)],
        }
