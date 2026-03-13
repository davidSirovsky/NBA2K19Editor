import pygame
from constants import COLOR_BLACK, COLOR_WHITE, FONT_STANDARD, FONT_SIZE_MIDDLE
from classes.frame import Frame


class TextField(Frame):
    """Текстовое поле для отображения результатов поиска"""

    def __init__(self, x, y, width, height, font=FONT_STANDARD, font_size=FONT_SIZE_MIDDLE, text_color=COLOR_BLACK):
        super().__init__(x, y, width, height)

        self.font = pygame.font.SysFont(font, font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.lines = []
        self.line_height = font_size + 4
        self.max_visible_lines = height // self.line_height
        self.scroll_offset = 0

    def set_lines(self, lines):
        """Устанавливает строки для отображения"""
        self.lines = lines

    def add_line(self, line):
        """Добавляет строку"""
        self.lines.append(line)

    def clear_lines(self):
        """Очищает все строки"""
        self.lines = []

    def draw(self, screen):
        """Отрисовывает текстовое поле"""
        if not self.visible:
            return

        # Фон
        pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())

        # Отрисовка строк с учётом прокрутки
        for i, line in enumerate(self.lines):
            y_pos = self.y + i * self.line_height - self.scroll_offset
            if y_pos >= self.y and y_pos < self.y + self.height:
                text_surface = self.font.render(line, True, self.text_color)
                screen.blit(text_surface, (self.x + 5, y_pos))