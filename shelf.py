"""
Модуль для класса Shelf (полочка)
"""
import pygame
import random
import config


class Shelf:
    """Класс полочки, от которой отскакивают шары"""
    
    def __init__(self):
        self.width = random.randint(config.SHELF_MIN_WIDTH, config.SHELF_MAX_WIDTH)
        self.height = config.SHELF_HEIGHT
        self.x = random.randint(0, config.WIDTH - self.width)
        self.y = random.randint(config.HEIGHT // 4, config.HEIGHT // 2)
        self.color = config.LIGHT_GRAY
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.angle = 0  # Угол не используется для отрисовки rect
    
    def draw(self, screen: pygame.Surface):
        """Отрисовка полочки"""
        pygame.draw.rect(screen, self.color, self.rect)

