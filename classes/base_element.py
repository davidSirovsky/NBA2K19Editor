import pygame
from constants import COLOR_WHITE, COLOR_BLACK

class BaseElement:
    """Суперкласс для всех интерактивных элементов UI"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enabled = True
        self.visible = True
        self.layer = 0
        
    def get_rect(self):
        """Возвращает прямоугольник элемента"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_point_inside(self, pos):
        """Проверяет, находится ли точка внутри элемента"""
        rect = self.get_rect()
        return rect.collidepoint(pos)
    
    def set_enabled(self, enabled):
        """Включает/выключает элемент"""
        self.enabled = enabled
    
    def set_visible(self, visible):
        """Показывает/скрывает элемент"""
        self.visible = visible
    
    def set_layer(self, layer):
        """Устанавливает слой элемента"""
        self.layer = layer
    
    def update(self, events, mouse_pos):
        """Обновляет состояние элемента (переопределяется в подклассах)"""
        if not self.enabled or not self.visible:
            return
        pass
    
    def draw(self, screen):
        """Отрисовывает элемент (переопределяется в подклассах)"""
        if not self.visible:
            return
        pass
    
    def deactivate_all(self):
        """Деактивирует элемент и все вложенные"""
        self.enabled = False