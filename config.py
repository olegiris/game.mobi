"""
Конфигурационный файл игры
Содержит все константы и настройки
"""
import pygame

# Инициализация pygame для получения информации о дисплее
pygame.init()
info = pygame.display.Info()

# Настройки изображений
USE_IMAGES = True
BALL_IMAGE_PATH = 'Яйцо.png'
BASKET_IMAGE_PATH = 'Корзина.png'
BOARD_IMAGE_PATH = 'Доска.png' # Новая переменная для изображения доски

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
MAROON = (128, 0, 0)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Размеры окна (адаптивно к экрану)
WIDTH = info.current_w
HEIGHT = info.current_h

# Настройки корзины
BASKET_WIDTH = WIDTH // 6
BASKET_HEIGHT = HEIGHT // 12
BASKET_Y = HEIGHT - BASKET_HEIGHT - HEIGHT // 15
BASKET_SPEED = WIDTH // 40
STICK_THICKNESS = 8
STICK_COLOR = BLUE
BASKET_MOVE_SMOOTHNESS = 0.3  # Коэффициент плавности движения корзины

# Настройки шара
BALL_SIZE = WIDTH // 30
BALL_SPEED = HEIGHT // 125  # Базовая скорость
BOUNCE_COEFF = 0.7  # Коэффициент упругости при отскоке от полочек
FRICTION_COEFF = 0.98  # Коэффициент трения при отскосе

# Настройки полочек
SHELF_MIN_WIDTH = WIDTH // 8
SHELF_MAX_WIDTH = WIDTH // 4
SHELF_HEIGHT = HEIGHT // 50
SHELF_SPAWN_PROBABILITY = 0.004  # Вероятность появления полочки за кадр
MAX_SHELVES = 10
# Цвет полочек можно изменить или использовать прозрачность, если будет изображение
SHELF_COLOR = MAROON 

# Настройки игры
INITIAL_LIVES = 3
MAX_BALLS = 3
BALL_CREATION_DELAY = 30  # Задержка перед созданием нового шара
FPS = 60

# Настройки сложности
DIFFICULTY_SETTINGS = {
    1: {  # Легкий
        'ball_speed': HEIGHT // 150,
        'basket_width': WIDTH // 4,
        'shelf_spawn_prob': 0.002,
        'name': 'Легкий'
    },
    2: {  # Средний
        'ball_speed': HEIGHT // 125,
        'basket_width': WIDTH // 6,
        'shelf_spawn_prob': 0.004,
        'name': 'Средний'
    },
    3: {  # Сложный
        'ball_speed': HEIGHT // 100,
        'basket_width': WIDTH // 8,
        'shelf_spawn_prob': 0.006,
        'name': 'Сложный'
    }
}

# Прогрессия сложности
DIFFICULTY_INCREASE_SCORE = 10  # Увеличивать сложность каждые N очков
DIFFICULTY_INCREASE_FACTOR = 1.1  # Множитель увеличения скорости

# Настройки UI
FONT_SIZE = WIDTH // 25
EXIT_BUTTON_WIDTH = WIDTH // 10
EXIT_BUTTON_HEIGHT = HEIGHT // 30
EXIT_BUTTON_X = 35
EXIT_BUTTON_Y = 70
EXIT_BUTTON_COLOR = LIGHT_GRAY
EXIT_BUTTON_TEXT_COLOR = BLACK

PAUSE_BUTTON_SIZE = EXIT_BUTTON_HEIGHT
PAUSE_BUTTON_X = WIDTH - PAUSE_BUTTON_SIZE - 30
PAUSE_BUTTON_Y = 70

# Кнопка переключения звука
SOUND_TOGGLE_BUTTON_WIDTH = WIDTH // 10
SOUND_TOGGLE_BUTTON_HEIGHT = PAUSE_BUTTON_SIZE
# Размещаем слева от кнопки паузы с небольшим отступом
SOUND_TOGGLE_BUTTON_X = PAUSE_BUTTON_X - SOUND_TOGGLE_BUTTON_WIDTH - (WIDTH // 60)
SOUND_TOGGLE_BUTTON_Y = PAUSE_BUTTON_Y
SOUND_TOGGLE_BUTTON_COLOR = LIGHT_GRAY
SOUND_TOGGLE_BUTTON_TEXT_COLOR = BLACK
SOUND_TOGGLE_BUTTON_ON_TEXT = "Звук Вкл" # Текст для кнопки, когда звук включен
SOUND_TOGGLE_BUTTON_OFF_TEXT = "Звук Выкл" # Текст для кнопки, когда звук выключен


DIFFICULTY_BUTTON_WIDTH = WIDTH // 4
DIFFICULTY_BUTTON_HEIGHT = HEIGHT // 15
BUTTON_SPACING = HEIGHT // 25

CONFIRM_BUTTON_WIDTH = DIFFICULTY_BUTTON_WIDTH // 2
CONFIRM_BUTTON_HEIGHT = DIFFICULTY_BUTTON_HEIGHT
CONFIRM_BUTTON_SPACING = WIDTH // 20

# Настройки фона
NUM_BACKGROUND_SQUARES = 30
SQUARE_MIN_SIZE = 15
SQUARE_MAX_SIZE = 40
SQUARE_ALPHA = 80

# Угол наклона стенок корзины
BASKET_WALL_ANGLE = 0.5235987755982988  # π/6 (30 градусов)
BASKET_WALL_WIDTH = BALL_SIZE * 1.5

# Настройки звука (пути к файлам, если будут добавлены)
SOUND_ENABLED = True # Это основная переменная состояния звука
SOUND_CATCH = None  # 'sounds/catch.wav'
SOUND_MISS = None  # 'sounds/miss.wav'
SOUND_BOUNCE = None  # 'sounds/bounce.wav'
SOUND_MUSIC = None  # 'sounds/music.mp3'

# Настройки частиц
PARTICLES_ENABLED = True
PARTICLE_COUNT = 25  # Увеличено для более заметного эффекта
PARTICLE_LIFETIME = 40  # Увеличено время жизни
PARTICLE_SIZE_MIN = 3
PARTICLE_SIZE_MAX = 8
