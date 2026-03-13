import pygame
from constants import COLOR_BLACK, COLOR_GRAY, BUTTON_CLOSE_SIZE
from base_element import BaseElement

class CloseButton(BaseElement):
    """Кнопка закрытия окна"""
    
    def __init__(self, x, y, close_function=None):
        super().__init__(x, y, BUTTON_CLOSE_SIZE, BUTTON_CLOSE_SIZE)
        self.close_function = close_function
        self.is_hovered = False
        
    def update(self, events, mouse_pos):
        """Обновляет состояние кнопки"""
        if not self.enabled or not self.visible:
            return
        
        self.is_hovered = self.is_point_inside(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    if self.close_function:
                        self.close_function()
    
    def draw(self, screen):
        """Отрисовывает кнопку Close"""
        if not self.visible:
            return
        
        # Цвет линий
        line_color = COLOR_GRAY if self.is_hovered else COLOR_BLACK
        
        # Первая линия (0,0) -> (24,24)
        start1 = (self.x, self.y)
        end1 = (self.x + BUTTON_CLOSE_SIZE, self.y + BUTTON_CLOSE_SIZE)
        pygame.draw.line(screen, line_color, start1, end1, 2)
        
        # Вторая линия (24,0) -> (0,24)
        start2 = (self.x + BUTTON_CLOSE_SIZE, self.y)
        end2 = (self.x, self.y + BUTTON_CLOSE_SIZE)
        pygame.draw.line(screen, line_color, start2, end2, 2)