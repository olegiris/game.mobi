"""
Модуль для класса Ball (шар)
"""
import pygame
import random
import math
import config


class Ball:
    """Класс шара, падающего в игре"""
    
    def __init__(self, speed: float = None):
        self.size = config.BALL_SIZE
        self.x = random.randint(self.size, config.WIDTH - self.size)
        self.y = -self.size
        self.color = config.WHITE
        self.speed_y = speed if speed is not None else config.BALL_SPEED
        self.speed_x = random.uniform(-self.speed_y / 2, self.speed_y / 2)
        self.rect = pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
        self.active = True
        self.prev_x = self.x
        self.prev_y = self.y
        
        # Загрузка изображения
        self.image = None
        if config.USE_IMAGES:
            self._load_image()
    
    def _load_image(self):
        """Загрузка изображения шара"""
        try:
            original_image = pygame.image.load(config.BALL_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(
                original_image,
                (self.size, self.size)
            )
        except pygame.error as e:
            print(f"Ошибка загрузки изображения шара '{config.BALL_IMAGE_PATH}': {e}")
            self.image = None
    
    def fall(self):
        """Обновление позиции шара"""
        if not self.active:
            return
        
        # Сохраняем предыдущую позицию
        self.prev_x = self.x
        self.prev_y = self.y
        
        # Обновляем позицию
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Отскок от боковых стен
        if self.x - self.size // 2 < 0:
            self.x = self.size // 2
            self.speed_x *= -1
        elif self.x + self.size // 2 > config.WIDTH:
            self.x = config.WIDTH - self.size // 2
            self.speed_x *= -1
        
        # Отскок от верхней части экрана
        if self.y - self.size // 2 < 0:
            self.y = self.size // 2
            self.speed_y *= -1
        
        self.rect.x = int(self.x - self.size // 2)
        self.rect.y = int(self.y - self.size // 2)
        
        # Деактивация, если шар упал слишком низко
        if self.y - self.size // 2 > config.HEIGHT + 100:
            self.active = False
    
    def draw(self, screen: pygame.Surface):
        """Отрисовка шара"""
        if not self.active:
            return
        
        if config.USE_IMAGES and self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                self.size // 2
            )
    
    def check_collision_with_basket(self, basket) -> bool:
        """Проверка столкновения с корзиной"""
        for rect in basket.get_collision_rects():
            if self.rect.colliderect(rect):
                return True
        return False
    
    def handle_collisions_with_shelves(self, shelves, shelves_to_remove_list):
        """Обработка столкновений с полочками"""
        for shelf in shelves[:]:
            if self.rect.colliderect(shelf.rect):
                # Столкновение сверху (шар падает на полочку)
                if self.prev_y + self.size // 2 <= shelf.rect.top:
                    self.y = shelf.rect.top - self.size // 2
                    self.speed_y = -abs(self.speed_y) * config.BOUNCE_COEFF
                    self.speed_x *= config.FRICTION_COEFF
                    self.rect.y = int(self.y - self.size // 2)
                # Столкновение снизу
                elif self.prev_y - self.size // 2 >= shelf.rect.bottom:
                    self.y = shelf.rect.bottom + self.size // 2
                    self.speed_y = abs(self.speed_y) * config.BOUNCE_COEFF
                    self.rect.y = int(self.y - self.size // 2)
                # Столкновение сбоку
                else:
                    if self.prev_x + self.size // 2 <= shelf.rect.left:
                        self.x = shelf.rect.left - self.size // 2
                        self.speed_x = -abs(self.speed_x) * config.BOUNCE_COEFF
                    elif self.prev_x - self.size // 2 >= shelf.rect.right:
                        self.x = shelf.rect.right + self.size // 2
                        self.speed_x = abs(self.speed_x) * config.BOUNCE_COEFF
                    self.rect.x = int(self.x - self.size // 2)
                
                # Добавляем полочку в список для удаления
                if shelf not in shelves_to_remove_list:
                    shelves_to_remove_list.append(shelf)
                break
    
    def update_speed(self, speed: float):
        """Обновление скорости шара"""
        self.speed_y = speed

