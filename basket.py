"""
Модуль для класса StickBasket (корзина)
"""
import pygame
import math
import config


class StickBasket:
    """Класс корзины для ловли шаров"""
    
    def __init__(self, width: int = None, height: int = None):
        self.width = width if width is not None else config.BASKET_WIDTH
        self.height = height if height is not None else config.BASKET_HEIGHT
        self.y = config.BASKET_Y
        self.x = config.WIDTH // 2 - self.width // 2
        self.speed = 0
        self.target_x = self.x
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Загрузка изображения
        self.image = None
        if config.USE_IMAGES:
            self._load_image()
        
        # Инициализация палок и полигонов
        if not config.USE_IMAGES or self.image is None:
            self.sticks = []
            self.create_sticks()
        else:
            self.sticks = []
    
    def _load_image(self):
        """Загрузка изображения корзины"""
        try:
            original_image = pygame.image.load(config.BASKET_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(
                original_image,
                (self.width, self.height)
            )
        except pygame.error as e:
            print(f"Ошибка загрузки изображения корзины '{config.BASKET_IMAGE_PATH}': {e}")
            self.image = None
            if not hasattr(self, 'sticks'):
                self.sticks = []
                self.create_sticks()
    
    def create_sticks(self):
        """Создание геометрических элементов корзины"""
        self.sticks = []
        bottom = pygame.Rect(
            self.x,
            self.y + self.height - config.STICK_THICKNESS,
            self.width,
            config.STICK_THICKNESS
        )
        
        left_stick_approx = pygame.Rect(
            self.x,
            self.y,
            config.STICK_THICKNESS,
            self.height
        )
        right_stick_approx = pygame.Rect(
            self.x + self.width - config.STICK_THICKNESS,
            self.y,
            config.STICK_THICKNESS,
            self.height
        )
        self.sticks.extend([bottom, left_stick_approx, right_stick_approx])
        
        # Координаты для отрисовки наклонных стенок
        self.left_wall_points = [
            (self.x, self.y),
            (self.x + config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
             self.y + config.BASKET_WALL_WIDTH * math.sin(config.BASKET_WALL_ANGLE)),
            (self.x + config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
             self.y + self.height - config.STICK_THICKNESS),
            (self.x, self.y + self.height - config.STICK_THICKNESS)
        ]
        self.right_wall_points = [
            (self.x + self.width, self.y),
            (self.x + self.width - config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
             self.y + config.BASKET_WALL_WIDTH * math.sin(config.BASKET_WALL_ANGLE)),
            (self.x + self.width - config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
             self.y + self.height - config.STICK_THICKNESS),
            (self.x + self.width, self.y + self.height - config.STICK_THICKNESS)
        ]
    
    def move(self, target_x: float):
        """Плавное движение корзины к цели"""
        self.target_x = max(0, min(target_x - self.width // 2, config.WIDTH - self.width))
        # Интерполяция для плавности
        self.x += (self.target_x - self.x) * config.BASKET_MOVE_SMOOTHNESS
        self.rect.x = int(self.x)
        
        if not config.USE_IMAGES or self.image is None:
            # Обновляем позиции прямоугольников
            self.sticks[0].x = int(self.x)  # bottom
            self.sticks[1].x = int(self.x)  # left
            self.sticks[2].x = int(self.x + self.width - config.STICK_THICKNESS)  # right
            
            # Обновляем координаты наклонных стенок
            self.left_wall_points = [
                (self.x, self.y),
                (self.x + config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
                 self.y + config.BASKET_WALL_WIDTH * math.sin(config.BASKET_WALL_ANGLE)),
                (self.x + config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
                 self.y + self.height - config.STICK_THICKNESS),
                (self.x, self.y + self.height - config.STICK_THICKNESS)
            ]
            self.right_wall_points = [
                (self.x + self.width, self.y),
                (self.x + self.width - config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
                 self.y + config.BASKET_WALL_WIDTH * math.sin(config.BASKET_WALL_ANGLE)),
                (self.x + self.width - config.BASKET_WALL_WIDTH * math.cos(config.BASKET_WALL_ANGLE),
                 self.y + self.height - config.STICK_THICKNESS),
                (self.x + self.width, self.y + self.height - config.STICK_THICKNESS)
            ]
    
    def draw(self, screen: pygame.Surface):
        """Отрисовка корзины"""
        if config.USE_IMAGES and self.image:
            screen.blit(self.image, self.rect)
        else:
            # Рисуем дно
            pygame.draw.rect(screen, config.STICK_COLOR, self.sticks[0])
            # Рисуем наклонные стенки
            pygame.draw.polygon(screen, config.STICK_COLOR, self.left_wall_points)
            pygame.draw.polygon(screen, config.STICK_COLOR, self.right_wall_points)
    
    def get_collision_rects(self):
        """Получить прямоугольники для проверки столкновений"""
        if config.USE_IMAGES and self.image:
            return [pygame.Rect(self.x, self.y, self.width, self.height)]
        else:
            return self.sticks
    
    def update_size(self, new_width: int):
        """Обновление размера корзины"""
        self.width = new_width
        self.rect.width = new_width
        self.x = config.WIDTH // 2 - self.width // 2
        self.rect.x = int(self.x)
        
        if config.USE_IMAGES and self.image:
            try:
                original_image = pygame.image.load(config.BASKET_IMAGE_PATH).convert_alpha()
                self.image = pygame.transform.scale(
                    original_image,
                    (self.width, self.height)
                )
            except pygame.error:
                pass
        else:
            self.create_sticks()

