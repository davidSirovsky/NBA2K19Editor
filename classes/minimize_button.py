import pygame
from constants import COLOR_BLACK, COLOR_GRAY, BUTTON_MINIMIZE_SIZE
from base_element import BaseElement

class MinimizeButton(BaseElement):
    """Кнопка сворачивания окна"""
    
    def __init__(self, x, y, minimize_function=None):
        super().__init__(x, y, BUTTON_MINIMIZE_SIZE, BUTTON_MINIMIZE_SIZE)
        self.minimize_function = minimize_function
        self.is_hovered = False
        
    def update(self, events, mouse_pos):
        """Обновляет состояние кнопки"""
        if not self.enabled or not self.visible:
            return
        
        self.is_hovered = self.is_point_inside(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    if self.minimize_function:
                        self.minimize_function()
    
    def draw(self, screen):
        """Отрисовывает кнопку Minimize"""
        if not self.visible:
            return
        
        # Цвет линии
        line_color = COLOR_GRAY if self.is_hovered else COLOR_BLACK
        
        # Линия (0,24) -> (24,24)
        start = (self.x, self.y + BUTTON_MINIMIZE_SIZE)
        end = (self.x + BUTTON_MINIMIZE_SIZE, self.y + BUTTON_MINIMIZE_SIZE)
        pygame.draw.line(screen, line_color, start, end, 2)