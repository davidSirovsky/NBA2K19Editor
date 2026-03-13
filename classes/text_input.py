import pygame
from constants import COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, FONT_STANDARD, FONT_SIZE_MIDDLE, TEXT_INPUT_HEIGHT
from base_element import BaseElement

class TextInput(BaseElement):
    """Поле ввода текста"""
    
    def __init__(self, x, y, length, font=FONT_STANDARD, font_size=FONT_SIZE_MIDDLE, text_color=COLOR_BLACK):
        super().__init__(x, y, length, TEXT_INPUT_HEIGHT)
        
        self.font = pygame.font.SysFont(font, font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.text = ""
        self.cursor_position = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # мс
        
        self.selected_start = -1
        self.selected_end = -1
        self.is_focused = False
        
        self.context_menu = None
        self.clipboard = ""
        
    def get_selected_text(self):
        """Возвращает выделенный текст"""
        if self.selected_start >= 0 and self.selected_end >= 0:
            start = min(self.selected_start, self.selected_end)
            end = max(self.selected_start, self.selected_end)
            return self.text[start:end]
        return ""
    
    def has_selection(self):
        """Проверяет есть ли выделение"""
        return self.selected_start >= 0 and self.selected_end >= 0 and self.selected_start != self.selected_end
    
    def update(self, events, mouse_pos):
        """Обновляет состояние поля ввода"""
        if not self.enabled or not self.visible:
            return
        
        # Обновляем контекстное меню если активно
        if self.context_menu and self.context_menu.visible:
            self.context_menu.update(events, mouse_pos)
            if not self.context_menu.visible:
                self.context_menu = None
            return
        
        # Проверка клика для фокуса
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.is_point_inside(mouse_pos):
                        self.is_focused = True
                        self.cursor_position = self.get_cursor_position_from_mouse(mouse_pos)
                        self.selected_start = -1
                        self.selected_end = -1
                        self.cursor_visible = True
                    else:
                        self.is_focused = False
                        self.context_menu = None
                elif event.button == 3:  # ПКМ
                    if self.is_point_inside(mouse_pos):
                        self.show_context_menu(mouse_pos)
        
        # Обработка клавиатуры
        if self.is_focused:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    if self.is_point_inside(mouse_pos):
                        self.selected_end = self.get_cursor_position_from_mouse(mouse_pos)
        
        # Мигание курсора
        if self.is_focused:
            self.cursor_timer += 16
            if self.cursor_timer >= self.cursor_interval:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible
    
    def get_cursor_position_from_mouse(self, mouse_pos):
        """Определяет позицию курсора по координатам мыши"""
        x = mouse_pos[0] - self.x - 5
        char_width = self.font.size("M")[0]
        position = max(0, min(len(self.text), x // max(1, char_width)))
        return position
    
    def handle_keydown(self, event):
        """Обрабатывает нажатия клавиш"""
        if event.key == pygame.K_BACKSPACE:
            if self.has_selection():
                self.delete_selection()
            elif self.cursor_position > 0:
                self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                self.cursor_position -= 1
        elif event.key == pygame.K_DELETE:
            if self.has_selection():
                self.delete_selection()
            elif self.cursor_position < len(self.text):
                self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
        elif event.key == pygame.K_LEFT:
            if event.mod & pygame.KMOD_SHIFT:
                if self.selected_start < 0:
                    self.selected_start = self.cursor_position
                self.cursor_position = max(0, self.cursor_position - 1)
                self.selected_end = self.cursor_position
            else:
                self.cursor_position = max(0, self.cursor_position - 1)
                self.selected_start = -1
                self.selected_end = -1
        elif event.key == pygame.K_RIGHT:
            if event.mod & pygame.KMOD_SHIFT:
                if self.selected_start < 0:
                    self.selected_start = self.cursor_position
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
                self.selected_end = self.cursor_position
            else:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
                self.selected_start = -1
                self.selected_end = -1
        elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
            self.paste_from_clipboard()
        elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL:
            self.copy_to_clipboard()
        elif event.key == pygame.K_x and event.mod & pygame.KMOD_CTRL:
            self.cut_to_clipboard()
        else:
            # Ввод символов
            if event.unicode and len(event.unicode) == 1:
                if self.has_selection():
                    self.delete_selection()
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += 1
    
    def delete_selection(self):
        """Удаляет выделенный текст"""
        if self.has_selection():
            start = min(self.selected_start, self.selected_end)
            end = max(self.selected_start, self.selected_end)
            self.text = self.text[:start] + self.text[end:]
            self.cursor_position = start
            self.selected_start = -1
            self.selected_end = -1
    
    def copy_to_clipboard(self):
        """Копирует выделенный текст в буфер"""
        if self.has_selection():
            self.clipboard = self.get_selected_text()
    
    def paste_from_clipboard(self):
        """Вставляет текст из буфера"""
        if self.clipboard:
            if self.has_selection():
                self.delete_selection()
            self.text = self.text[:self.cursor_position] + self.clipboard + self.text[self.cursor_position:]
            self.cursor_position += len(self.clipboard)
    
    def cut_to_clipboard(self):
        """Вырезает выделенный текст в буфер"""
        if self.has_selection():
            self.copy_to_clipboard()
            self.delete_selection()
            self.cursor_visible = False
    
    def show_context_menu(self, mouse_pos):
        """Показывает контекстное меню"""
        from context_menu import ContextMenu
        self.context_menu = ContextMenu(mouse_pos[0], mouse_pos[1], self)
        self.context_menu.set_enabled(True)
        self.context_menu.set_visible(True)
    
    def draw(self, screen):
        """Отрисовывает поле ввода"""
        if not self.visible:
            return
        
        # Фон и обводка
        pygame.draw.rect(screen, COLOR_WHITE, self.get_rect())
        pygame.draw.rect(screen, COLOR_BLACK, self.get_rect(), 1)
        
        # Текст
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + 5, self.y + 5))
        
        # Выделение
        if self.has_selection():
            start = min(self.selected_start, self.selected_end)
            end = max(self.selected_start, self.selected_end)
            char_width = self.font.size("M")[0]
            select_x = self.x + 5 + start * char_width
            select_width = (end - start) * char_width
            pygame.draw.rect(screen, COLOR_GRAY, (select_x, self.y + 5, select_width, self.font_size))
        
        # Курсор
        if self.is_focused and self.cursor_visible:
            char_width = self.font.size("M")[0]
            cursor_x = self.x + 5 + self.cursor_position * char_width
            pygame.draw.line(screen, COLOR_BLACK, 
                           (cursor_x, self.y + 5), 
                           (cursor_x, self.y + 5 + self.font_size), 1)
        
        # Контекстное меню
        if self.context_menu and self.context_menu.visible:
            self.context_menu.draw(screen)