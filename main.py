import pygame
import sys
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLACK, COLOR_WHITE
from classes.window import Window
from classes.text_input import TextInput
from classes.text_field import TextField
from classes.button_ribbon import ButtonRibbon
from classes.scrollbar import Scrollbar
from classes.copy_dna_button import CopyDNAButton

def main():
    # Инициализация Pygame
    pygame.init()
    pygame.display.set_caption('Application')
    
    # Создание окна без рамок
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    
    # Создаём основное окно приложения
    app_window = Window(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, show_minimize=True)
    app_window.set_close_function(lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
    app_window.set_minimize_function(lambda: pygame.display.iconify())
    
    # Создаём линию 1
    line1_start = (250, 0)
    line1_end = (250, 900)
    
    # Создаём линию 2
    line2_start = (610, 0)
    line2_end = (610, 900)
    
    # Создаём надпись SEARCH
    search_font = pygame.font.SysFont('Calibri', 24)
    search_text = search_font.render('SEARCH', True, COLOR_BLACK)
    search_pos = (275, 15)
    
    # Создаём поле ввода
    search_input = TextInput(275, 47, 300)
    app_window.add_child(search_input)
    
    # Создаём текстовое поле для результатов
    text_field = TextField(275, 100, 300, 770)
    text_field.set_lines([f"Result {i}" for i in range(50)])
    app_window.add_child(text_field)
    
    # Создаём вертикальную полосу прокрутки
    scrollbar_vert = Scrollbar(581, 100, 770, orientation='vertical', total_items=50)
    app_window.add_child(scrollbar_vert)
    text_field.scrollbar = scrollbar_vert
    
    # Создаём ленту кнопок
    button_ribbon = ButtonRibbon(624, 47, 776, 30)
    app_window.add_child(button_ribbon)
    
    # Создаём горизонтальную полосу прокрутки для ленты
    scrollbar_horiz = Scrollbar(624, 77, 776, orientation='horizontal', total_items=10)
    app_window.add_child(scrollbar_horiz)
    
    # Создаём кнопку Copy DNA
    copy_dna_button = CopyDNAButton(1404, 875)
    app_window.add_child(copy_dna_button)
    
    # Основной цикл
    running = True
    while running:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Обновляем все элементы
        app_window.update(events, mouse_pos)
        
        # Синхронизируем прокрутку с текстовым полем
        if scrollbar_vert:
            text_field.scroll_offset = scrollbar_vert.get_scroll_offset()
        
        # Отрисовка
        screen.fill(COLOR_WHITE)
        
        # Рисуем линии
        pygame.draw.line(screen, COLOR_BLACK, line1_start, line1_end, 1)
        pygame.draw.line(screen, COLOR_BLACK, line2_start, line2_end, 1)
        
        # Рисуем надпись SEARCH
        screen.blit(search_text, search_pos)
        
        # Рисуем окно и все элементы
        app_window.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()