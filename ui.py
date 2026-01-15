"""
Модуль для пользовательского интерфейса
"""
import pygame
import math
import random
import config
from database import Database


class UI:
    """Класс для управления пользовательским интерфейсом"""
    
    def __init__(self, screen: pygame.Surface, database: Database):
        self.screen = screen
        self.database = database
        self.font = pygame.font.Font(None, config.FONT_SIZE)
        self.small_font = pygame.font.Font(None, config.FONT_SIZE // 2)
        
        # Фоновые элементы
        self.background_squares = self._create_background_squares()
        
        # Текстовые элементы
        self.title_text = self.font.render("Олег «СТК»", True, config.GRAY)
        self.title_rect = self.title_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 15))
        
        # Кнопки
        self.exit_rect = pygame.Rect(
            config.EXIT_BUTTON_X,
            config.EXIT_BUTTON_Y,
            config.EXIT_BUTTON_WIDTH,
            config.EXIT_BUTTON_HEIGHT
        )
        self.exit_text = self.font.render("Выйти", True, config.BLACK)
        
        self.pause_button_rect = pygame.Rect(
            config.PAUSE_BUTTON_X,
            config.PAUSE_BUTTON_Y,
            config.PAUSE_BUTTON_SIZE,
            config.PAUSE_BUTTON_SIZE
        )
        pause_font = pygame.font.Font(None, config.PAUSE_BUTTON_SIZE)
        self.pause_text = pause_font.render("⏸️", True, config.BLACK)
        self.pause_text_rect = self.pause_text.get_rect(center=self.pause_button_rect.center)
        
        # Кнопки сложности
        self.easy_button_rect = pygame.Rect(
            config.WIDTH // 2 - config.DIFFICULTY_BUTTON_WIDTH // 2,
            config.HEIGHT // 2 - config.DIFFICULTY_BUTTON_HEIGHT * 1.5 - config.BUTTON_SPACING,
            config.DIFFICULTY_BUTTON_WIDTH,
            config.DIFFICULTY_BUTTON_HEIGHT
        )
        self.medium_button_rect = pygame.Rect(
            config.WIDTH // 2 - config.DIFFICULTY_BUTTON_WIDTH // 2,
            config.HEIGHT // 2 - config.DIFFICULTY_BUTTON_HEIGHT // 2,
            config.DIFFICULTY_BUTTON_WIDTH,
            config.DIFFICULTY_BUTTON_HEIGHT
        )
        self.hard_button_rect = pygame.Rect(
            config.WIDTH // 2 - config.DIFFICULTY_BUTTON_WIDTH // 2,
            config.HEIGHT // 2 + config.DIFFICULTY_BUTTON_HEIGHT // 2 + config.BUTTON_SPACING,
            config.DIFFICULTY_BUTTON_WIDTH,
            config.DIFFICULTY_BUTTON_HEIGHT
        )
    
    def _create_background_squares(self):
        """Создание фоновых квадратиков"""
        squares = []
        for _ in range(config.NUM_BACKGROUND_SQUARES):
            size = random.randint(config.SQUARE_MIN_SIZE, config.SQUARE_MAX_SIZE)
            x = random.randint(0, config.WIDTH - size)
            y = random.randint(0, config.HEIGHT - size)
            angle = random.uniform(0, 2 * math.pi)
            color = (random.randint(80, 130), 0, 0, config.SQUARE_ALPHA)
            squares.append((pygame.Rect(x, y, size, size), angle, color))
        return squares
    
    def draw_background(self):
        """Отрисовка фона"""
        self.screen.fill(config.MAROON)
        
        # Рисуем квадратики
        for rect, angle, color in self.background_squares:
            surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surf.fill(color)
            rotated_surf = pygame.transform.rotate(surf, math.degrees(angle))
            rotated_rect = rotated_surf.get_rect(center=rect.center)
            self.screen.blit(rotated_surf, rotated_rect.topleft)
    
    def draw_difficulty_screen(self):
        """Отрисовка экрана выбора сложности"""
        difficulty_title = self.font.render("Выберите сложность", True, config.WHITE)
        difficulty_title_rect = difficulty_title.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 4))
        self.screen.blit(difficulty_title, difficulty_title_rect)
        
        # Кнопка "Легкий"
        mouse_pos = pygame.mouse.get_pos()
        color = config.LIGHT_GRAY
        if self.easy_button_rect.collidepoint(mouse_pos):
            color = config.GRAY
        pygame.draw.rect(self.screen, color, self.easy_button_rect, border_radius=5)
        easy_text = self.font.render("Легкий", True, config.BLACK)
        self.screen.blit(easy_text, easy_text.get_rect(center=self.easy_button_rect.center))
        
        # Кнопка "Средний"
        color = config.LIGHT_GRAY
        if self.medium_button_rect.collidepoint(mouse_pos):
            color = config.GRAY
        pygame.draw.rect(self.screen, color, self.medium_button_rect, border_radius=5)
        medium_text = self.font.render("Средний", True, config.BLACK)
        self.screen.blit(medium_text, medium_text.get_rect(center=self.medium_button_rect.center))
        
        # Кнопка "Сложный"
        color = config.LIGHT_GRAY
        if self.hard_button_rect.collidepoint(mouse_pos):
            color = config.GRAY
        pygame.draw.rect(self.screen, color, self.hard_button_rect, border_radius=5)
        hard_text = self.font.render("Сложный", True, config.BLACK)
        self.screen.blit(hard_text, hard_text.get_rect(center=self.hard_button_rect.center))
    
    def draw_game_ui(self, game_state):
        """Отрисовка игрового интерфейса"""
        # Счет и жизни
        score_text = self.font.render(f"Результат: {game_state.score}", True, config.WHITE)
        lives_text = self.font.render(f"Жизней: {game_state.lives}", True, config.YELLOW)
        
        # Лучший результат
        best_record = self.database.get_best_score()
        best_score = best_record[1] if best_record else 0
        best_score_text = self.font.render(
            f"Лучший результат: {best_score}",
            True,
            config.WHITE
        )
        
        # Счет и жизни - сдвинуты вниз, чтобы не накладывались на кнопку выхода
        self.screen.blit(score_text, (20, config.EXIT_BUTTON_Y + config.EXIT_BUTTON_HEIGHT + 10))
        self.screen.blit(lives_text, (config.WIDTH - lives_text.get_width() - 20, config.EXIT_BUTTON_Y + config.EXIT_BUTTON_HEIGHT + 10))
        self.screen.blit(
            best_score_text,
            ((config.WIDTH - best_score_text.get_width()) // 2, config.EXIT_BUTTON_Y + config.EXIT_BUTTON_HEIGHT + 10)
        )
        
        # Индикатор прогрессии сложности (НОВОЕ!) - сдвинут вниз
        speed_multiplier = game_state.difficulty_multiplier
        if speed_multiplier > 1.0:
            speed_text = self.small_font.render(
                f"⚡ Сложность: x{speed_multiplier:.1f}",
                True,
                config.ORANGE
            )
            self.screen.blit(speed_text, (20, config.EXIT_BUTTON_Y + config.EXIT_BUTTON_HEIGHT + 50))
        
        # Уведомление о повышении сложности (НОВОЕ!)
        if game_state.difficulty_level_up_timer > 0:
            # Пульсирующий эффект
            alpha = int(255 * (game_state.difficulty_level_up_timer / 120))
            overlay = pygame.Surface((config.WIDTH, 100), pygame.SRCALPHA)
            overlay.fill((255, 165, 0, min(alpha, 100)))  # Оранжевый с прозрачностью
            self.screen.blit(overlay, (0, config.HEIGHT // 2 - 50))
            
            level_text = self.font.render(
                f"⚡ СЛОЖНОСТЬ УВЕЛИЧЕНА! x{speed_multiplier:.1f} ⚡",
                True,
                config.WHITE
            )
            level_rect = level_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
            self.screen.blit(level_text, level_rect)
        
        # Прогресс до следующего уровня сложности - сдвинут вниз
        next_level_score = ((game_state.score // config.DIFFICULTY_INCREASE_SCORE) + 1) * config.DIFFICULTY_INCREASE_SCORE
        progress = (game_state.score % config.DIFFICULTY_INCREASE_SCORE) / config.DIFFICULTY_INCREASE_SCORE
        if progress > 0:
            bar_width = 200
            bar_height = 8
            bar_x = 20
            bar_y = config.EXIT_BUTTON_Y + config.EXIT_BUTTON_HEIGHT + 75
            # Фон прогресс-бара
            pygame.draw.rect(
                self.screen,
                config.GRAY,
                (bar_x, bar_y, bar_width, bar_height),
                border_radius=4
            )
            # Заполненная часть
            filled_width = int(bar_width * progress)
            if filled_width > 0:
                pygame.draw.rect(
                    self.screen,
                    config.ORANGE,
                    (bar_x, bar_y, filled_width, bar_height),
                    border_radius=4
                )
            # Текст прогресса
            progress_text = self.small_font.render(
                f"До следующего уровня: {next_level_score - game_state.score}",
                True,
                config.WHITE
            )
            self.screen.blit(progress_text, (bar_x, bar_y + bar_height + 5))
        
        # Кнопка паузы
        pygame.draw.rect(
            self.screen,
            config.LIGHT_GRAY,
            self.pause_button_rect,
            border_radius=5
        )
        self.screen.blit(self.pause_text, self.pause_text_rect)
    
    def draw_pause_screen(self):
        """Отрисовка экрана паузы"""
        pause_overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 150))
        self.screen.blit(pause_overlay, (0, 0))
        
        pause_msg = self.font.render("Пауза", True, config.WHITE)
        pause_msg_rect = pause_msg.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 - config.FONT_SIZE))
        self.screen.blit(pause_msg, pause_msg_rect)
        
        # Кнопка "Продолжить игру"
        continue_text = self.font.render("Продолжить игру", True, config.WHITE)
        continue_rect = continue_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + config.FONT_SIZE * 2))
        
        mouse_pos = pygame.mouse.get_pos()
        if continue_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, config.GRAY, continue_rect.inflate(20, 10), border_radius=5)
        else:
            pygame.draw.rect(self.screen, config.LIGHT_GRAY, continue_rect.inflate(20, 10), border_radius=5)
        
        self.screen.blit(continue_text, continue_rect)
        return continue_rect
    
    def draw_game_over_screen(self, game_state):
        """Отрисовка экрана окончания игры"""
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Проверяем, новый ли это рекорд
        best_record = self.database.get_best_score()
        is_new_record = best_record is None or game_state.score > best_record[1]
        
        if is_new_record:
            end_text = self.font.render(
                f"Новый рекорд! Ваш результат: {game_state.score}",
                True,
                config.GREEN
            )
        else:
            end_text = self.font.render(
                f"Игра окончена :( Ваш результат: {game_state.score}",
                True,
                config.WHITE
            )
        
        text_rect = end_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 - config.FONT_SIZE))
        self.screen.blit(end_text, text_rect)
        
        # Кнопка рестарта
        restart_text = self.font.render("Играть ещё раз", True, config.WHITE)
        restart_rect = restart_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + config.FONT_SIZE))
        
        mouse_pos = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, config.LIGHT_GRAY, restart_rect.inflate(20, 10), border_radius=5)
        
        self.screen.blit(restart_text, restart_rect)
        return restart_rect
    
    def draw_exit_confirmation(self):
        """Отрисовка диалога подтверждения выхода"""
        confirmation_overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        confirmation_overlay.fill((0, 0, 0, 180))
        self.screen.blit(confirmation_overlay, (0, 0))
        
        confirm_text = self.font.render("Вы уверены, что хотите выйти?", True, config.WHITE)
        confirm_text_rect = confirm_text.get_rect(
            center=(config.WIDTH // 2, config.HEIGHT // 2 - config.FONT_SIZE * 2)
        )
        self.screen.blit(confirm_text, confirm_text_rect)
        
        # Кнопка "Да"
        yes_button_rect = pygame.Rect(
            config.WIDTH // 2 - config.CONFIRM_BUTTON_WIDTH - config.CONFIRM_BUTTON_SPACING // 2,
            config.HEIGHT // 2 + config.FONT_SIZE,
            config.CONFIRM_BUTTON_WIDTH,
            config.CONFIRM_BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, config.GREEN, yes_button_rect, border_radius=5)
        yes_text = self.font.render("Да", True, config.BLACK)
        self.screen.blit(yes_text, yes_text.get_rect(center=yes_button_rect.center))
        
        # Кнопка "Нет"
        no_button_rect = pygame.Rect(
            config.WIDTH // 2 + config.CONFIRM_BUTTON_SPACING // 2,
            config.HEIGHT // 2 + config.FONT_SIZE,
            config.CONFIRM_BUTTON_WIDTH,
            config.CONFIRM_BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, config.RED, no_button_rect, border_radius=5)
        no_text = self.font.render("Нет", True, config.BLACK)
        self.screen.blit(no_text, no_text.get_rect(center=no_button_rect.center))
        
        return yes_button_rect, no_button_rect
    
    def draw_exit_button(self):
        """Отрисовка кнопки выхода"""
        pygame.draw.rect(
            self.screen,
            config.EXIT_BUTTON_COLOR,
            self.exit_rect,
            border_radius=5
        )
        self.screen.blit(
            self.exit_text,
            (
                config.EXIT_BUTTON_X + (config.EXIT_BUTTON_WIDTH - self.exit_text.get_width()) // 2,
                config.EXIT_BUTTON_Y + (config.EXIT_BUTTON_HEIGHT - self.exit_text.get_height()) // 2
            )
        )
    
    def draw_title(self):
        """Отрисовка заголовка"""
        self.screen.blit(self.title_text, self.title_rect)

