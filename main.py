"""
Главный файл игры "Catch the Ball"
Улучшенная версия с модульной архитектурой
"""
import Kivy
import sys
import config
from database import Database
from game_state import GameState
from ui import UI
from sound_manager import SoundManager


class Game:
    """Главный класс игры"""
    
    def __init__(self):
        pygame.init()
        
        # Создание окна
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Catch the Ball - Олег «СТК»")
        
        # Инициализация компонентов
        self.database = Database()
        self.game_state = GameState()
        self.ui = UI(self.screen, self.database)
        self.sound_manager = SoundManager()
        
        # Подключаем sound_manager к game_state
        self.game_state.sound_manager = self.sound_manager
        
        # Игровой цикл
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.show_exit_confirmation = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._handle_mouse_click(mouse_pos)
            
            # Движение корзины
            if (not self.game_state.show_exit_confirmation and
                not self.game_state.show_difficulty_screen and
                self.game_state.game_started and
                not self.game_state.game_over and
                not self.game_state.paused and
                self.game_state.basket is not None):
                
                if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                    touch_x = event.x * config.WIDTH
                    self.game_state.basket.move(touch_x)
                elif event.type == pygame.MOUSEMOTION:
                    self.game_state.basket.move(event.pos[0])
    
    def _handle_mouse_click(self, mouse_pos):
        """Обработка кликов мыши"""
        # Диалог подтверждения выхода
        if self.game_state.show_exit_confirmation:
            yes_rect, no_rect = self.ui.draw_exit_confirmation()
            if yes_rect.collidepoint(mouse_pos):
                self._confirm_exit()
            elif no_rect.collidepoint(mouse_pos):
                self.game_state.show_exit_confirmation = False
            return
        
        # Кнопка выхода
        if self.ui.exit_rect.collidepoint(mouse_pos):
            self.game_state.show_exit_confirmation = True
            return
        
        # Экран выбора сложности
        if self.game_state.show_difficulty_screen:
            if self.ui.easy_button_rect.collidepoint(mouse_pos):
                self.game_state.set_difficulty(1)
                self.game_state.show_difficulty_screen = False
                self.game_state.restart_game()
            elif self.ui.medium_button_rect.collidepoint(mouse_pos):
                self.game_state.set_difficulty(2)
                self.game_state.show_difficulty_screen = False
                self.game_state.restart_game()
            elif self.ui.hard_button_rect.collidepoint(mouse_pos):
                self.game_state.set_difficulty(3)
                self.game_state.show_difficulty_screen = False
                self.game_state.restart_game()
            return
        
        # Игровой процесс
        if self.game_state.game_started and not self.game_state.game_over:
            # Кнопка паузы
            if self.ui.pause_button_rect.collidepoint(mouse_pos):
                self.game_state.paused = not self.game_state.paused
                return
            
            # Продолжить игру (на экране паузы)
            if self.game_state.paused:
                continue_rect = self.ui.draw_pause_screen()
                if continue_rect.collidepoint(mouse_pos):
                    self.game_state.paused = False
                return
        
        # Экран окончания игры
        if self.game_state.game_over:
            # Сохраняем результат при первом показе экрана окончания
            if not hasattr(self.game_state, '_score_saved'):
                self.database.save_score(
                    self.game_state.player_name,
                    self.game_state.score,
                    self.game_state.current_difficulty
                )
                self.game_state._score_saved = True
            
            restart_rect = self.ui.draw_game_over_screen(self.game_state)
            if restart_rect.collidepoint(mouse_pos):
                self.game_state.show_difficulty_screen = True
                self.game_state.game_over = False
                if hasattr(self.game_state, '_score_saved'):
                    delattr(self.game_state, '_score_saved')
    
    def _confirm_exit(self):
        """Подтверждение выхода и сохранение результата"""
        if self.game_state.game_started:
            self.database.save_score(
                self.game_state.player_name,
                self.game_state.score,
                self.game_state.current_difficulty
            )
        self.running = False
    
    def update(self):
        """Обновление состояния игры"""
        if (self.game_state.game_started and
            not self.game_state.game_over and
            not self.game_state.paused):
            self.game_state.update()
    
    def draw(self):
        """Отрисовка игры"""
        # Фон
        self.ui.draw_background()
        
        # Основной игровой процесс
        if not self.game_state.show_exit_confirmation:
            if self.game_state.show_difficulty_screen:
                self.ui.draw_difficulty_screen()
            
            elif self.game_state.game_started and not self.game_state.game_over:
                # Рисуем игровые объекты
                for shelf in self.game_state.shelves:
                    shelf.draw(self.screen)
                
                for ball in self.game_state.balls:
                    ball.draw(self.screen)
                
                if self.game_state.basket is not None:
                    self.game_state.basket.draw(self.screen)
                
                # Частицы
                self.game_state.particle_system.draw(self.screen)
                
                # UI
                self.ui.draw_game_ui(self.game_state)
            
            # Экран паузы
            if (self.game_state.paused and
                not self.game_state.show_difficulty_screen and
                self.game_state.game_started and
                not self.game_state.game_over):
                self.ui.draw_pause_screen()
            
            # Экран окончания игры
            elif (self.game_state.game_over and
                  not self.game_state.show_difficulty_screen):
                self.ui.draw_game_over_screen(self.game_state)
        
        # Кнопка выхода и заголовок (всегда)
        self.ui.draw_exit_button()
        self.ui.draw_title()
        
        # Диалог подтверждения выхода (поверх всего)
        if self.game_state.show_exit_confirmation:
            self.ui.draw_exit_confirmation()
        
        pygame.display.flip()
    
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        # Сохранение при выходе
        if self.game_state.game_started:
            self.database.save_score(
                self.game_state.player_name,
                self.game_state.score,
                self.game_state.current_difficulty
            )
        
        pygame.quit()
        sys.exit()


def main():
    """Точка входа"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


