import pygame
from constants import COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, FONT_STANDARD, FONT_SIZE_BIG, BUTTON_MARGIN_DEFAULT
from base_element import BaseElement

class TextButton(BaseElement):
    """Кнопка с текстом"""
    
    def __init__(self, x, y, text, font_size=FONT_SIZE_BIG, margin=BUTTON_MARGIN_DEFAULT,
                 inactive_rect_color=COLOR_WHITE, active_rect_color=COLOR_BLACK,
                 hover_rect_color=COLOR_GRAY, inactive_text_color=COLOR_BLACK,
                 active_text_color=COLOR_WHITE, hover_text_color=COLOR_BLACK,
                 click_function=None):
        
        # Создаём шрифт и рассчитываем размер текста
        font = pygame.font.SysFont(FONT_STANDARD, font_size)
        text_surface = font.render(text, True, inactive_text_color)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        
        # Рассчитываем размер кнопки с учётом margin
        width = text_width + margin[0] + margin[1]
        height = text_height + margin[2] + margin[3]
        
        super().__init__(x, y, width, height)
        
        self.text = text
        self.font_size = font_size
        self.margin = margin
        self.inactive_rect_color = inactive_rect_color
        self.active_rect_color = active_rect_color
        self.hover_rect_color = hover_rect_color
        self.inactive_text_color = inactive_text_color
        self.active_text_color = active_text_color
        self.hover_text_color = hover_text_color
        self.click_function = click_function
        
        self.is_active = False
        self.is_hovered = False
        self.font = font
        
    def get_rect_color(self):
        """Возвращает цвет прямоугольника в зависимости от состояния"""
        if self.is_active:
            return self.active_rect_color
        elif self.is_hovered:
            return self.hover_rect_color
        return self.inactive_rect_color
    
    def get_text_color(self):
        """Возвращает цвет текста в зависимости от состояния"""
        if self.is_active:
            return self.active_text_color
        elif self.is_hovered:
            return self.hover_text_color
        return self.inactive_text_color
    
    def update(self, events, mouse_pos):
        """Обновляет состояние кнопки"""
        if not self.enabled or not self.visible:
            return
        
        # Проверка наведения
        self.is_hovered = self.is_point_inside(mouse_pos)
        
        # Обработка кликов
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    self.is_active = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_hovered and self.is_active:
                    if self.click_function:
                        self.click_function()
                self.is_active = False
    
    def draw(self, screen):
        """Отрисовывает кнопку"""
        if not self.visible:
            return
        
        # Рисуем прямоугольник
        rect_color = self.get_rect_color()
        pygame.draw.rect(screen, rect_color, self.get_rect())
        
        # Рисуем текст
        text_color = self.get_text_color()
        text_surface = self.font.render(self.text, True, text_color)
        text_x = self.x + self.margin[1]
        text_y = self.y + self.margin[2]
        screen.blit(text_surface, (text_x, text_y))
    
    def set_active(self, active):
        """Устанавливает активное состояние кнопки"""
        self.is_active = active