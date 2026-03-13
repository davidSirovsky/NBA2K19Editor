import pygame

def create_vertical_line(screen, start, end, color, width=1):
    """Создаёт вертикальную линию"""
    pygame.draw.line(screen, color, start, end, width)

def create_horizontal_line(screen, start, end, color, width=1):
    """Создаёт горизонтальную линию"""
    pygame.draw.line(screen, color, start, end, width)

def create_label(screen, text, pos, font_name, font_size, color):
    """Создаёт надпись"""
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def check_collision(rect1, rect2):
    """Проверяет пересечение двух прямоугольников"""
    return rect1.colliderect(rect2)

def is_point_in_rect(point, rect):
    """Проверяет находится ли точка в прямоугольнике"""
    return rect.collidepoint(point)

def clamp(value, min_value, max_value):
    """Ограничивает значение в диапазоне"""
    return max(min_value, min(value, max_value))

def calculate_button_width(text, font_size, margin):
    """Рассчитывает ширину кнопки по тексту"""
    font = pygame.font.SysFont('Calibri', font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface.get_width() + margin[0] + margin[1]