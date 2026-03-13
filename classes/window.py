import pygame
from constants import COLOR_WHITE, BUTTON_MARGIN, BUTTON_CLOSE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_MINIMIZE_SIZE
from classes.frame import Frame
from classes.close_button import CloseButton
from classes.minimize_button import MinimizeButton

class Window(Frame):
    """Основное окно приложения"""
    
    def __init__(self, x, y, width, height, show_minimize=True):
        super().__init__(x, y, width, height)
        
        self.show_minimize = show_minimize
        self.layer = 0
        
        # Создаём кнопки управления окном
        close_x = x + width - BUTTON_CLOSE_SIZE - BUTTON_MARGIN
        close_y = y + BUTTON_MARGIN
        self.close_button = CloseButton(close_x, close_y, self.close_window)
        self.add_child(self.close_button)
        
        if show_minimize:
            minimize_x = close_x - BUTTON_MINIMIZE_SIZE - BUTTON_MARGIN
            self.minimize_button = MinimizeButton(minimize_x, close_y, self.minimize_window)
            self.add_child(self.minimize_button)
        
        # Текст слоя
        self.layer_text = f"Слой {self.layer}"
        self.layer_font = pygame.font.SysFont('Calibri', 16)
        
        self.close_function = None
        self.minimize_function = None
    
    def set_close_function(self, function):
        """Устанавливает функцию закрытия"""
        self.close_function = function
    
    def set_minimize_function(self, function):
        """Устанавливает функцию сворачивания"""
        self.minimize_function = function
    
    def close_window(self):
        """Закрывает окно"""
        if self.close_function:
            self.close_function()
    
    def minimize_window(self):
        """Сворачивает окно"""
        if self.minimize_function:
            self.minimize_function()
    
    def set_layer(self, layer):
        """Устанавливает слой окна"""
        super().set_layer(layer)
        self.layer = layer
        self.layer_text = f"Слой {self.layer}"
    
    def draw(self, screen):
        """Отрисовывает окно"""
        if not self.visible:
            return
        
        # Фон окна
        pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())
        
        # Текст слоя
        layer_surface = self.layer_font.render(self.layer_text, True, (0, 0, 0))
        screen.blit(layer_surface, (self.x + 5, self.y + self.height - 20))
        
        # Отрисовка детей
        for child in self.children:
            if child.visible:
                child.draw(screen)