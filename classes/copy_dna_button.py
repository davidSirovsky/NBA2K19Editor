import pygame
from constants import COLOR_BLACK, COLOR_GRAY, COPY_DNA_BUTTON_WIDTH, COPY_DNA_BUTTON_HEIGHT, COPY_DNA_LINE_THICKNESS, COPY_DNA_LINE_SPACING
from classes.base_element import BaseElement

class CopyDNAButton(BaseElement):
    """Кнопка Copy DNA"""
    
    def __init__(self, x, y, copy_function=None):
        super().__init__(x, y, COPY_DNA_BUTTON_WIDTH, COPY_DNA_BUTTON_HEIGHT)
        self.copy_function = copy_function
        self.is_hovered = False
        
    def update(self, events, mouse_pos):
        """Обновляет состояние кнопки"""
        if not self.enabled or not self.visible:
            return
        
        self.is_hovered = self.is_point_inside(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    if self.copy_function:
                        self.copy_function()
    
    def draw(self, screen):
        """Отрисовывает кнопку Copy DNA"""
        if not self.visible:
            return
        
        # Цвет линий
        line_color = COLOR_GRAY if self.is_hovered else COLOR_BLACK
        
        # Три линии одна под другой
        for i in range(3):
            y_pos = self.y + i * (COPY_DNA_LINE_THICKNESS + COPY_DNA_LINE_SPACING)
            pygame.draw.line(screen, line_color, 
                           (self.x, y_pos), 
                           (self.x + COPY_DNA_BUTTON_WIDTH, y_pos), 
                           COPY_DNA_LINE_THICKNESS)