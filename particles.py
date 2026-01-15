"""
Модуль для системы частиц (визуальные эффекты)
"""
import pygame
import random
import math
import config


class Particle:
    """Класс одной частицы"""
    
    def __init__(self, x: float, y: float, color: tuple = None):
        self.x = x
        self.y = y
        self.color = color if color else config.YELLOW
        self.velocity_x = random.uniform(-5, 5)  # Увеличена скорость
        self.velocity_y = random.uniform(-8, -2)  # Увеличена скорость
        self.lifetime = config.PARTICLE_LIFETIME
        self.max_lifetime = config.PARTICLE_LIFETIME
        self.size = random.randint(config.PARTICLE_SIZE_MIN, config.PARTICLE_SIZE_MAX)
    
    def update(self):
        """Обновление позиции и времени жизни частицы"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.2  # Гравитация
        self.lifetime -= 1
    
    def draw(self, screen: pygame.Surface):
        """Отрисовка частицы"""
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color_with_alpha = (*self.color[:3], alpha)
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))
    
    def is_alive(self) -> bool:
        """Проверка, жива ли частица"""
        return self.lifetime > 0


class ParticleSystem:
    """Система управления частицами"""
    
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x: float, y: float, count: int = None, color: tuple = None):
        """Добавить взрыв частиц"""
        if not config.PARTICLES_ENABLED:
            return
        
        count = count if count is not None else config.PARTICLE_COUNT
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        """Обновление всех частиц"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Отрисовка всех частиц"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Очистка всех частиц"""
        self.particles.clear()

