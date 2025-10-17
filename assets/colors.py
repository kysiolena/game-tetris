from .settings import Color


class Colors:
    DARK_GREY: Color = (26, 31, 40)
    LIGHT_GREY: Color = (235, 232, 232)
    GREEN: Color = (47, 230, 23)
    DARK_GREEN: Color = (35, 191, 17)
    RED: Color = (232, 18, 18)
    ORANGE: Color = (226, 116, 17)
    YELLOW: Color = (237, 234, 4)
    PURPLE: Color = (166, 0, 247)
    CYAN: Color = (21, 204, 209)
    BLUE: Color = (13, 64, 216)
    PINK: Color = (245, 39, 238)
    DARK_BLUE: Color = (44, 44, 127)
    WHITE: Color = (255, 255, 255)
    LIGHT_BLUE: Color = (59, 85, 162)

    @classmethod
    def get_colors(cls) -> list[Color]:
        """
        Get list of Colors
        :return: list[Color]
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
            cls.PINK,
            cls.DARK_BLUE,
            cls.WHITE,
            cls.LIGHT_BLUE,
            cls.DARK_GREEN,
            cls.LIGHT_GREY,
        ]
