"""
Модуль для управления состоянием игры
"""
import random
import math
import config
from ball import Ball
from basket import StickBasket
from shelf import Shelf
from particles import ParticleSystem


class GameState:
    """Класс для управления состоянием игры"""
    
    def __init__(self):
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.game_started = False
        self.game_over = False
        self.paused = False
        self.show_difficulty_screen = True
        self.show_exit_confirmation = False
        self.current_difficulty = 2
        self.player_name = "Проектная Работа"
        
        # Игровые объекты
        self.basket = None
        self.balls = []
        self.shelves = []
        self.particle_system = ParticleSystem()
        self.sound_manager = None  # Будет установлен извне
        
        # Таймеры
        self.ball_creation_timer = 0
        
        # Прогрессия сложности
        self.base_ball_speed = config.BALL_SPEED
        self.current_ball_speed = config.BALL_SPEED
        self.difficulty_multiplier = 1.0
        self.difficulty_level_up_timer = 0  # Таймер для показа уведомления
        self.difficulty_level_up_timer = 0  # Таймер для показа уведомления
    
    def set_difficulty(self, level: int):
        """Установка уровня сложности"""
        if level not in config.DIFFICULTY_SETTINGS:
            level = 2
        
        self.current_difficulty = level
        settings = config.DIFFICULTY_SETTINGS[level]
        
        self.base_ball_speed = settings['ball_speed']
        self.current_ball_speed = self.base_ball_speed
        self.difficulty_multiplier = 1.0
        
        # Создаем корзину с новым размером
        if self.basket:
            self.basket.update_size(settings['basket_width'])
        else:
            self.basket = StickBasket(width=settings['basket_width'])
    
    def restart_game(self):
        """Перезапуск игры"""
        settings = config.DIFFICULTY_SETTINGS[self.current_difficulty]
        
        self.basket = StickBasket(width=settings['basket_width'])
        self.balls = [Ball(speed=self.current_ball_speed)]
        self.shelves = []
        self.particle_system.clear()
        
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.game_started = True
        self.game_over = False
        self.ball_creation_timer = 0
        self.paused = False
        self.base_ball_speed = settings['ball_speed']
        self.current_ball_speed = self.base_ball_speed
        self.difficulty_multiplier = 1.0
    
    def update_difficulty_progression(self):
        """Обновление прогрессии сложности на основе счета"""
        new_multiplier = 1.0 + (self.score // config.DIFFICULTY_INCREASE_SCORE) * 0.1
        if new_multiplier != self.difficulty_multiplier:
            old_multiplier = self.difficulty_multiplier
            self.difficulty_multiplier = new_multiplier
            self.current_ball_speed = self.base_ball_speed * self.difficulty_multiplier
            # Обновляем скорость всех существующих шаров
            for ball in self.balls:
                ball.update_speed(self.current_ball_speed)
            # Добавляем эффект частиц при увеличении сложности
            if new_multiplier > old_multiplier:
                # Большой взрыв частиц в центре экрана
                for i in range(8):
                    angle = (i / 8) * 2 * math.pi
                    x = config.WIDTH // 2 + math.cos(angle) * 100
                    y = config.HEIGHT // 2 + math.sin(angle) * 100
                    self.particle_system.add_explosion(
                        x, y,
                        count=15,
                        color=config.ORANGE
                    )
                # Устанавливаем таймер для показа уведомления
                self.difficulty_level_up_timer = 120  # 2 секунды при 60 FPS
                # Звук повышения сложности
                if self.sound_manager:
                    self.sound_manager.play_sound('levelup')
    
    def create_new_ball(self):
        """Создание нового шара"""
        if len(self.balls) < config.MAX_BALLS:
            self.balls.append(Ball(speed=self.current_ball_speed))
            self.ball_creation_timer = config.BALL_CREATION_DELAY
    
    def create_shelf(self):
        """Создание новой полочки"""
        settings = config.DIFFICULTY_SETTINGS[self.current_difficulty]
        spawn_prob = settings['shelf_spawn_prob']
        
        if (random.random() < spawn_prob and 
            len(self.shelves) < config.MAX_SHELVES):
            self.shelves.append(Shelf())
    
    def update_balls(self):
        """Обновление всех шаров"""
        shelves_to_remove = []
        
        for ball in self.balls[:]:
            ball.fall()
            ball.handle_collisions_with_shelves(self.shelves, shelves_to_remove)
            
            # Проверка столкновения с корзиной
            if ball.check_collision_with_basket(self.basket):
                ball.active = False
                self.score += 1
                # Эффект частиц при поимке (увеличено количество)
                self.particle_system.add_explosion(
                    ball.x, ball.y, 
                    count=30, 
                    color=config.GREEN
                )
                # Звук поимки
                if self.sound_manager:
                    self.sound_manager.play_sound('catch')
                self.update_difficulty_progression()
            
            # Удаление неактивных шаров
            if not ball.active:
                if ball in self.balls:
                    self.balls.remove(ball)
                self.ball_creation_timer = config.BALL_CREATION_DELAY
            
            # Проверка потери жизни
            if ball.y - ball.size // 2 > config.HEIGHT:
                self.lives -= 1
                # Эффект частиц при промахе (увеличено количество)
                self.particle_system.add_explosion(
                    ball.x, config.HEIGHT, 
                    count=25, 
                    color=config.RED
                )
                # Звук промаха
                if self.sound_manager:
                    self.sound_manager.play_sound('miss')
                if ball in self.balls:
                    self.balls.remove(ball)
                self.ball_creation_timer = config.BALL_CREATION_DELAY
                
                if self.lives <= 0:
                    self.game_over = True
        
        # Удаление полочек
        for shelf in shelves_to_remove:
            if shelf in self.shelves:
                self.shelves.remove(shelf)
    
    def update_timers(self):
        """Обновление таймеров"""
        if self.ball_creation_timer > 0:
            self.ball_creation_timer -= 1
        else:
            self.create_new_ball()
    
    def update(self):
        """Обновление состояния игры"""
        if not self.game_started or self.game_over or self.paused:
            return
        
        self.create_shelf()
        self.update_balls()
        self.update_timers()
        self.particle_system.update()
        
        # Уменьшаем таймер уведомления о повышении сложности
        if self.difficulty_level_up_timer > 0:
            self.difficulty_level_up_timer -= 1
        
        # Уменьшаем таймер уведомления о повышении сложности
        if self.difficulty_level_up_timer > 0:
            self.difficulty_level_up_timer -= 1

