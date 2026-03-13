import pygame
from constants import COLOR_WHITE, COLOR_BLACK
from classes.base_element import BaseElement

class Frame(BaseElement):
    """Фрейм с обрезкой содержимого по границам"""
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.children = []
        self.clip_content = True
        
    def add_child(self, child):
        """Добавляет дочерний элемент"""
        self.children.append(child)
        child.set_layer(self.layer)
        
    def remove_child(self, child):
        """Удаляет дочерний элемент"""
        if child in self.children:
            self.children.remove(child)
            
    def clear_children(self):
        """Очищает всех дочерних элементов"""
        self.children = []
        
    def set_layer(self, layer):
        """Устанавливает слой для фрейма и всех детей"""
        super().set_layer(layer)
        for child in self.children:
            child.set_layer(layer)
    
    def is_child_visible(self, child):
        """Проверяет, виден ли дочерний элемент внутри фрейма"""
        if not self.clip_content:
            return True
        child_rect = child.get_rect()
        frame_rect = self.get_rect()
        # Элемент виден если хотя бы часть его внутри фрейма
        return frame_rect.colliderect(child_rect)
    
    def update(self, events, mouse_pos):
        """Обновляет состояние фрейма и всех видимых детей"""
        if not self.enabled or not self.visible:
            return
        
        for child in self.children:
            if self.is_child_visible(child):
                child.update(events, mouse_pos)
            else:
                # Деактивируем скрытые элементы но сохраняем состояние
                child.set_enabled(False)
    
    def draw(self, screen):
        """Отрисовывает фрейм и всех видимых детей с обрезкой"""
        if not self.visible:
            return
        
        # Создаём поверхность для обрезки
        if self.clip_content:
            child_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            child_surface.fill(COLOR_WHITE)
            
            for child in self.children:
                if child.visible:
                    # Смещаем координаты детей относительно фрейма
                    original_x = child.x
                    original_y = child.y
                    child.x -= self.x
                    child.y -= self.y
                    child.draw(child_surface)
                    child.x = original_x
                    child.y = original_y
            
            screen.blit(child_surface, (self.x, self.y))
        else:
            # Без обрезки
            pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())
            for child in self.children:
                if child.visible:
                    child.draw(screen)
    
    def deactivate_all(self):
        """Деактивирует фрейм и все дочерние элементы"""
        super().deactivate_all()
        for child in self.children:
            child.deactivate_all()