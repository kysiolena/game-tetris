import pygame

from .settings import Color


class ButtonColor:
    def __init__(self, base: Color, hover: Color):
        self.base = base
        self.hover = hover


class Button:

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font | None = None,
        text: str | None = None,
        color_bg: ButtonColor | None = None,
        color_text: ButtonColor | None = None,
        image_path: str | None = None,
    ):
        self._font = font
        self._text = text

        # Colors
        self._color_bg = color_bg
        self._color_text = color_text

        # Current colors
        self._current_color_bg: Color | None = color_bg.base if color_bg else None
        self._current_color_text: Color | None = color_text.base if color_text else None

        # Image Surface
        self._image: pygame.Surface | None = (
            pygame.image.load(image_path).convert_alpha() if image_path else None
        )

        # Rect
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.Surface) -> None:
        if self._image:
            screen.blit(
                self._image,
                self._image.get_rect(topleft=self._rect.topleft),
            )
        else:
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
        if self._image:
            pass
        else:
            self._current_color_bg = self._color_bg.hover
            self._current_color_text = self._color_text.hover

    def mouse_out(self) -> None:
        if self._image:
            pass
        else:
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
