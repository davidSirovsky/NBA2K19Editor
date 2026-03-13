import pygame
from constants import COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, FONT_STANDARD, FONT_SIZE_MIDDLE
from base_element import BaseElement

class ContextMenu(BaseElement):
    """Контекстное меню для поля ввода"""
    
    def __init__(self, x, y, text_input):
        self.text_input = text_input
        self.items = ['Копировать', 'Вставить', 'Вырезать']
        self.item_height = FONT_SIZE_MIDDLE + 4
        self.margin_x = 4
        self.margin_y = 2
        
        # Рассчитываем размеры
        font = pygame.font.SysFont(FONT_STANDARD, FONT_SIZE_MIDDLE)
        max_width = max(font.size(item)[0] for item in self.items)
        width = max_width + self.margin_x * 2
        height = self.item_height * 3 + self.margin_y * 4
        
        super().__init__(x, y, width, height)
        
        self.hovered_item = -1
        self.font = font
        
    def is_item_active(self, index):
        """Проверяет активен ли пункт меню"""
        if index == 0:  # Копировать
            return self.text_input.has_selection()
        elif index == 1:  # Вставить
            return bool(self.text_input.clipboard)
        elif index == 2:  # Вырезать
            return self.text_input.has_selection()
        return False
    
    def update(self, events, mouse_pos):
        """Обновляет состояние меню"""
        if not self.enabled or not self.visible:
            return
        
        # Проверка наведения на пункты
        self.hovered_item = -1
        for i in range(len(self.items)):
            item_y = self.y + self.margin_y + i * (self.item_height + self.margin_y)
            item_rect = pygame.Rect(self.x, item_y, self.width, self.item_height)
            if item_rect.collidepoint(mouse_pos):
                self.hovered_item = i
                break
        
        # Обработка кликов
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered_item >= 0 and self.is_item_active(self.hovered_item):
                    self.execute_item(self.hovered_item)
                    self.set_visible(False)
                elif not self.get_rect().collidepoint(mouse_pos):
                    self.set_visible(False)
    
    def execute_item(self, index):
        """Выполняет действие пункта меню"""
        if index == 0:
            self.text_input.copy_to_clipboard()
        elif index == 1:
            self.text_input.paste_from_clipboard()
        elif index == 2:
            self.text_input.cut_to_clipboard()
    
    def draw(self, screen):
        """Отрисовывает контекстное меню"""
        if not self.visible:
            return
        
        # Фон меню
        pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())
        pygame.draw.rect(screen, COLOR_BLACK, self.get_rect(), 1)
        
        # Пункты меню
        for i, item in enumerate(self.items):
            item_y = self.y + self.margin_y + i * (self.item_height + self.margin_y)
            item_rect = pygame.Rect(self.x, item_y, self.width, self.item_height)
            
            is_active = self.is_item_active(i)
            is_hovered = (i == self.hovered_item)
            
            # Фон пункта
            if is_hovered:
                pygame.draw.rect(screen, COLOR_GRAY, item_rect)
            
            # Текст пункта
            if is_active:
                text_color = COLOR_BLACK
            else:
                text_color = COLOR_GRAY
            
            text_surface = self.font.render(item, True, text_color)
            text_x = self.x + self.margin_x
            screen.blit(text_surface, (text_x, item_y))