"""
Модуль для работы с базой данных рекордов
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional, Tuple, List


class Database:
    """Класс для работы с базой данных рекордов"""
    
    def __init__(self, db_path: str = 'scores.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных и создание таблицы"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Создаем таблицу, если её нет
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS highscores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        difficulty INTEGER DEFAULT 2,
                        date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Проверяем существование колонок и добавляем их, если нужно
                cursor.execute("PRAGMA table_info(highscores)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'difficulty' not in columns:
                    cursor.execute("ALTER TABLE highscores ADD COLUMN difficulty INTEGER DEFAULT 2")
                
                if 'date' not in columns:
                    cursor.execute("ALTER TABLE highscores ADD COLUMN date TEXT DEFAULT CURRENT_TIMESTAMP")
                
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка инициализации базы данных: {e}")
    
    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для работы с подключением к БД"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def get_best_score(self) -> Optional[Tuple[str, int]]:
        """Получить лучший результат"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, score FROM highscores ORDER BY score DESC LIMIT 1"
                )
                record = cursor.fetchone()
                return record if record else None
        except sqlite3.Error as e:
            print(f"Ошибка получения рекорда: {e}")
            return None
    
    def save_score(self, name: str, score: int, difficulty: int = 2) -> bool:
        """Сохранить результат"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Получаем текущий рекорд
                best = self.get_best_score()
                
                if best is None or score > best[1]:
                    # Если это новый рекорд, обновляем существующий или создаем новый
                    if best:
                        cursor.execute(
                            "UPDATE highscores SET name = ?, score = ?, difficulty = ? "
                            "WHERE id = (SELECT id FROM highscores ORDER BY score DESC LIMIT 1)",
                            (name, score, difficulty)
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO highscores (name, score, difficulty) VALUES (?, ?, ?)",
                            (name, score, difficulty)
                        )
                else:
                    # Просто добавляем результат в таблицу
                    cursor.execute(
                        "INSERT INTO highscores (name, score, difficulty) VALUES (?, ?, ?)",
                        (name, score, difficulty)
                    )
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Ошибка сохранения результата: {e}")
            return False
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, int]]:
        """Получить топ результатов"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, score, difficulty FROM highscores "
                    "ORDER BY score DESC LIMIT ?",
                    (limit,)
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения топ результатов: {e}")
            return []

