import pygame

from .settings import Color


class ButtonColor:
    def __init__(self, base: Color, hover: Color):
        self.base = base
        self.hover = hover


class Button:
    def __init__(
        self,
        font: pygame.font.Font,
        text: str,
        color_bg: ButtonColor,
        color_text: ButtonColor,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self._font = font
        self._text = text

        # Colors
        self._color_bg = color_bg
        self._color_text = color_text

        # Current colors
        self._current_color_bg: Color = color_bg.base
        self._current_color_text: Color = color_text.base

        # Rect
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.Surface) -> None:
        # Text Surface
        text_surface = self._font.render(self._text, True, self._current_color_text)

        # Draw Rect
        pygame.draw.rect(
            screen,
            self._current_color_bg,
            self._rect,
            0,
            10,
        )

        # Draw Text
        screen.blit(
            text_surface,
            text_surface.get_rect(
                centerx=self._rect.centerx,
                centery=self._rect.centery,
            ),
        )

    def mouse_in(self) -> None:
        self._current_color_bg = self._color_bg.hover
        self._current_color_text = self._color_text.hover

    def mouse_out(self) -> None:
        self._current_color_bg = self._color_bg.base
        self._current_color_text = self._color_text.base

    def mouse_move(self, mouse_pos: tuple[int, int]) -> None:
        if self.is_collide(mouse_pos):
            self.mouse_in()
        else:
            self.mouse_out()

    def is_collide(self, mouse_pos: tuple[int, int]) -> bool:
        return self._rect.collidepoint(mouse_pos)

    @property
    def rect(self):
        return self._rect
