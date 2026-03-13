import pygame
from constants import BUTTON_RIBBON_NAMES, FONT_SIZE_BIG, BUTTON_MARGIN_DEFAULT
from classes.frame import Frame
from classes.button import TextButton

class ButtonRibbon(Frame):
    """Лента кнопок с горизонтальной прокруткой"""
    
    def __init__(self, x, y, width, height, button_names=BUTTON_RIBBON_NAMES):
        super().__init__(x, y, width, height)
        
        self.buttons = []
        self.active_button_index = -1
        
        # Создаём кнопки
        current_x = x
        for i, name in enumerate(button_names):
            button = TextButton(
                x=current_x,
                y=y,
                text=name,
                font_size=FONT_SIZE_BIG,
                margin=BUTTON_MARGIN_DEFAULT,
                click_function=lambda idx=i: self.on_button_click(idx)
            )
            self.buttons.append(button)
            self.add_child(button)
            current_x += button.width + BUTTON_MARGIN_DEFAULT[0]
        
        # Рассчитываем общую ширину
        self.total_width = current_x - x
    
    def on_button_click(self, index):
        """Обработчик клика на кнопку"""
        self.active_button_index = index
        for i, button in enumerate(self.buttons):
            button.set_active(i == index)
    
    def update(self, events, mouse_pos):
        """Обновляет состояние ленты кнопок"""
        # Проверяем видимость каждой кнопки
        for button in self.buttons:
            button_rect = button.get_rect()
            frame_rect = self.get_rect()
            
            if frame_rect.colliderect(button_rect):
                button.set_enabled(True)
            else:
                button.set_enabled(False)
        
        super().update(events, mouse_pos)
    
    def set_scroll_offset(self, offset):
        """Устанавливает смещение прокрутки"""
        for i, button in enumerate(self.buttons):
            button.x = self.x + i * (button.width + BUTTON_MARGIN_DEFAULT[0]) - offset