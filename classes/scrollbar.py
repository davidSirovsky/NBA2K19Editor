import pygame
from constants import COLOR_GRAY, SCROLLBAR_BORDER_SIZE, SCROLLBAR_DECOR_OFFSET, SCROLLBAR_CIRCLE_DIAMETER, SCROLLBAR_MIN_LENGTH
from classes.base_element import BaseElement

class Scrollbar(BaseElement):
    """Полоса прокрутки"""
    
    def __init__(self, x, y, length, orientation='vertical', total_items=50):
        if orientation == 'vertical':
            width = SCROLLBAR_MIN_LENGTH
            height = length
        else:
            width = length
            height = SCROLLBAR_MIN_LENGTH
        
        super().__init__(x, y, width, height)
        
        self.orientation = orientation
        self.total_items = total_items
        self.visible_items = self.calculate_visible_items()
        self.scroll_position = 0
        self.is_dragging = False
        
        # Рассчитываем размер runner
        self.calculate_runner_size()
        
    def calculate_visible_items(self):
        """Рассчитывает количество видимых элементов"""
        if self.orientation == 'vertical':
            return self.height // 20  # Примерно 20 пикселей на строку
        else:
            return self.width // 50  # Примерно 50 пикселей на кнопку
        return 10
    
    def calculate_runner_size(self):
        """Рассчитывает размер и позицию runner"""
        if self.total_items <= self.visible_items:
            self.runner_length = 0
            return
        
        if self.orientation == 'vertical':
            available_length = self.height - SCROLLBAR_BORDER_SIZE * 2 - SCROLLBAR_DECOR_OFFSET * 2
            self.runner_length = max(SCROLLBAR_CIRCLE_DIAMETER, 
                                    available_length * self.visible_items / self.total_items)
        else:
            available_length = self.width - SCROLLBAR_BORDER_SIZE * 2 - SCROLLBAR_DECOR_OFFSET * 2
            self.runner_length = max(SCROLLBAR_CIRCLE_DIAMETER,
                                    available_length * self.visible_items / self.total_items)
    
    def get_runner_rect(self):
        """Возвращает прямоугольник runner"""
        if self.runner_length == 0:
            return pygame.Rect(0, 0, 0, 0)
        
        if self.orientation == 'vertical':
            available_length = self.height - SCROLLBAR_BORDER_SIZE * 2 - SCROLLBAR_DECOR_OFFSET * 2
            max_scroll = available_length - self.runner_length
            runner_y = self.y + SCROLLBAR_BORDER_SIZE + SCROLLBAR_DECOR_OFFSET + (self.scroll_position / max(1, self.total_items - self.visible_items)) * max_scroll
            return pygame.Rect(self.x + 5, runner_y, SCROLLBAR_CIRCLE_DIAMETER, self.runner_length)
        else:
            available_length = self.width - SCROLLBAR_BORDER_SIZE * 2 - SCROLLBAR_DECOR_OFFSET * 2
            max_scroll = available_length - self.runner_length
            runner_x = self.x + SCROLLBAR_BORDER_SIZE + SCROLLBAR_DECOR_OFFSET + (self.scroll_position / max(1, self.total_items - self.visible_items)) * max_scroll
            return pygame.Rect(runner_x, self.y + 5, self.runner_length, SCROLLBAR_CIRCLE_DIAMETER)
    
    def update(self, events, mouse_pos):
        """Обновляет состояние полосы прокрутки"""
        if not self.enabled or not self.visible:
            return
        
        runner_rect = self.get_runner_rect()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if runner_rect.collidepoint(mouse_pos):
                    self.is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_dragging = False
        
        if self.is_dragging and pygame.mouse.get_pressed()[0]:
            if self.orientation == 'vertical':
                delta_y = mouse_pos[1] - runner_rect.centery
                self.scroll_position = max(0, min(self.total_items - self.visible_items,
                                                  self.scroll_position + delta_y / 5))
            else:
                delta_x = mouse_pos[0] - runner_rect.centerx
                self.scroll_position = max(0, min(self.total_items - self.visible_items,
                                                  self.scroll_position + delta_x / 5))
    
    def draw(self, screen):
        """Отрисовывает полосу прокрутки"""
        if not self.visible:
            return
        
        # Ограничители (border)
        if self.orientation == 'vertical':
            # border_0
            border0_points = [
                (self.x + 12, self.y),
                (self.x + 23, self.y + 20),
                (self.x, self.y + 20)
            ]
            pygame.draw.polygon(screen, COLOR_GRAY, border0_points)
            
            # border_1
            border1_points = [
                (self.x + 12, self.y + 20),
                (self.x, self.y),
                (self.x + 23, self.y)
            ]
            pygame.draw.polygon(screen, COLOR_GRAY, border1_points)
            
            # Runner
            if self.runner_length > 0:
                runner_rect = self.get_runner_rect()
                pygame.draw.rect(screen, COLOR_GRAY, runner_rect)
                pygame.draw.circle(screen, COLOR_GRAY, 
                                 (int(runner_rect.centerx), int(runner_rect.top)), 
                                 SCROLLBAR_CIRCLE_DIAMETER // 2)
                pygame.draw.circle(screen, COLOR_GRAY,
                                 (int(runner_rect.centerx), int(runner_rect.bottom)),
                                 SCROLLBAR_CIRCLE_DIAMETER // 2)
        else:
            # border_0
            border0_points = [
                (self.x, self.y + 12),
                (self.x + 20, self.y),
                (self.x + 20, self.y + 23)
            ]
            pygame.draw.polygon(screen, COLOR_GRAY, border0_points)
            
            # border_1
            border1_points = [
                (self.x + 20, self.y + 12),
                (self.x, self.y + 23),
                (self.x, self.y)
            ]
            pygame.draw.polygon(screen, COLOR_GRAY, border1_points)
            
            # Runner
            if self.runner_length > 0:
                runner_rect = self.get_runner_rect()
                pygame.draw.rect(screen, COLOR_GRAY, runner_rect)
                pygame.draw.circle(screen, COLOR_GRAY,
                                 (int(runner_rect.left), int(runner_rect.centery)),
                                 SCROLLBAR_CIRCLE_DIAMETER // 2)
                pygame.draw.circle(screen, COLOR_GRAY,
                                 (int(runner_rect.right), int(runner_rect.centery)),
                                 SCROLLBAR_CIRCLE_DIAMETER // 2)
    
    def get_scroll_offset(self):
        """Возвращает смещение прокрутки"""
        return self.scroll_position