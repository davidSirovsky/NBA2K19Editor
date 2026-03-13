import pygame
from constants import COLOR_WHITE, COLOR_BLACK, CHECKBOX_SIZE, CHECKBOX_INNER_SIZE, CHECKBOX_OFFSET
from classes.base_element import BaseElement

class Checkbox(BaseElement):
    """Чекбокс"""
    
    def __init__(self, x, y, initial_state=False):
        super().__init__(x, y, CHECKBOX_SIZE, CHECKBOX_SIZE)
        self.state = initial_state
        self.is_hovered = False
        
    def update(self, events, mouse_pos):
        """Обновляет состояние чекбокса"""
        if not self.enabled or not self.visible:
            return
        
        self.is_hovered = self.is_point_inside(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    self.state = not self.state
    
    def draw(self, screen):
        """Отрисовывает чекбокс"""
        if not self.visible:
            return
        
        # Нижний rectangle (белый с чёрной обводкой)
        pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())
        pygame.draw.rect(screen, COLOR_BLACK, self.get_rect(), 1)
        
        # Верхний rectangle (цвет зависит от состояния)
        inner_color = COLOR_BLACK if self.state else COLOR_WHITE
        inner_rect = pygame.Rect(
            self.x + CHECKBOX_OFFSET,
            self.y + CHECKBOX_OFFSET,
            CHECKBOX_INNER_SIZE,
            CHECKBOX_INNER_SIZE
        )
        pygame.draw.rect(screen, inner_color, inner_rect)
    
    def get_state(self):
        """Возвращает состояние чекбокса"""
        return self.state
    
    def set_state(self, state):
        """Устанавливает состояние чекбокса"""
        self.state = state