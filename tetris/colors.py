class Colors:
    DARK_GREY = (26, 31, 40)
    GREEN = (47, 230, 23)
    DARK_GREEN = (35, 191, 17)
    RED = (232, 18, 18)
    ORANGE = (226, 116, 17)
    YELLOW = (237, 234, 4)
    PURPLE = (166, 0, 247)
    CYAN = (21, 204, 209)
    BLUE = (13, 64, 216)
    DARK_BLUE = (44, 44, 127)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (59, 85, 162)

    @classmethod
    def get_colors(cls) -> list[tuple[int, int, int]]:
        """
        Get list of Colors
        :return: list[tuple[int, int, int]]
        """
        return [
            cls.DARK_GREY,
            cls.GREEN,
            cls.RED,
            cls.ORANGE,
            cls.YELLOW,
            cls.PURPLE,
            cls.CYAN,
            cls.BLUE,
            cls.DARK_BLUE,
            cls.WHITE,
            cls.LIGHT_BLUE,
            cls.DARK_GREEN,
        ]
