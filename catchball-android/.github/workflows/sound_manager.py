
"""
Модуль для управления звуками
"""
import pygame
import config
import numpy # Для функций округления, если потребуется, но numpy уже хорошо справляется

# Попытка импорта numpy для генерации звуков
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class SoundManager:
    """Класс для управления звуковыми эффектами"""
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
        if config.SOUND_ENABLED:
            # Увеличим частоту дискретизации для лучшего качества звука,
            # но 22050 тоже нормально. 44100 - стандарт CD качества.
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._create_sounds()
    
    def _generate_sound(self, frequencies, duration: float, volume: float = 0.3, 
                        attack_duration: float = 0.01, release_duration: float = 0.05,
                        waveform: str = 'sine'):
        """
        Генерация звукового эффекта.
        
        :param frequencies: Частота (float), список частот (list[float]) для аккорда,
                            или кортеж (start_freq, end_freq) для частотного свипа.
        :param duration: Длительность звука в секундах.
        :param volume: Общая громкость (от 0 до 1).
        :param attack_duration: Время нарастания громкости в начале звука (секунды).
        :param release_duration: Время затухания громкости в конце звука (секунды).
        :param waveform: Тип волны ('sine', 'square', 'sawtooth'). По умолчанию 'sine'.
        """
        if not HAS_NUMPY:
            return None
        
        try:
            sample_rate = pygame.mixer.get_init()[0] # Получаем текущую частоту дискретизации
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.float32) # Использовать float для точности
            
            # Генерация основной формы волны
            if isinstance(frequencies, (list, tuple)) and len(frequencies) == 2 and isinstance(frequencies[0], (int, float)):
                # Частотный свип (sweep)
                start_freq, end_freq = frequencies
                phase = 0.0
                for i in range(frames):
                    # Линейная интерполяция частоты
                    current_freq = start_freq + (end_freq - start_freq) * (i / frames)
                    phase += 2 * np.pi * current_freq / sample_rate
                    if waveform == 'sine':
                        arr[i] = np.sin(phase)
                    elif waveform == 'square':
                        arr[i] = np.sign(np.sin(phase))
                    elif waveform == 'sawtooth':
                        arr[i] = 2 * (phase / (2 * np.pi) % 1) - 1
            else:
                # Одиночная частота или аккорд
                if not isinstance(frequencies, list):
                    frequencies = [frequencies] # Превращаем одиночную частоту в список
                
                t = np.linspace(0, duration, frames, endpoint=False)
                total_wave = np.zeros(frames)
                for freq in frequencies:
                    if waveform == 'sine':
                        total_wave += np.sin(2 * np.pi * freq * t)
                    elif waveform == 'square':
                        total_wave += np.sign(np.sin(2 * np.pi * freq * t))
                    elif waveform == 'sawtooth':
                        total_wave += 2 * ((2 * np.pi * freq * t / (2 * np.pi)) % 1) - 1
                
                # Нормализация для аккордов, чтобы не превысить 1.0
                if len(frequencies) > 1:
                    total_wave /= len(frequencies) 
                
                arr[:, 0] = arr[:, 1] = total_wave
            
            # Применение огибающей громкости (Attack-Release)
            attack_frames = int(attack_duration * sample_rate)
            release_frames = int(release_duration * sample_rate)
            
            envelope = np.ones(frames, dtype=np.float32)
            if attack_frames > 0:
                envelope[:attack_frames] = np.linspace(0, 1, attack_frames)
            if release_frames > 0:
                # Если релиз перекрывает аттак, это может быть неверно.
                # Убедимся, что релиз начинается после аттака и не раньше конца звука.
                release_start = max(0, frames - release_frames)
                envelope[release_start:] *= np.linspace(1, 0, frames - release_start) # Умножаем, чтобы сохранить форму аттака
            
            arr *= envelope[:, np.newaxis] # Применяем огибающую к обоим каналам
            
            # Масштабирование до 16-битного диапазона и применение общей громкости
            max_sample_value = 2**(16 - 1) - 1
            arr = arr * max_sample_value * volume
            
            # Обрезка значений, чтобы избежать клиппинга
            arr = np.clip(arr, -max_sample_value, max_sample_value)
            
            # Преобразование в 16-битные целые числа
            sound = pygame.sndarray.make_sound(arr.astype(np.int16))
            return sound
        except Exception as e:
            print(f"Ошибка при генерации звука: {e}")
            return None
    
    def _create_sounds(self):
        """Создание звуковых эффектов программно"""
        if not HAS_NUMPY:
            print("Numpy не установлен. Звуки отключены. Установите: pip install numpy")
            return
        
        try:
            # Звук поимки шара - быстрый, восходящий приятный тон/аккорд
            # Используем аккорд для более насыщенного звука и быстрый аттак/релиз
            catch_sound = self._generate_sound(frequencies=[800, 1200], duration=0.1, volume=0.25, 
                                               attack_duration=0.005, release_duration=0.05)
            if catch_sound:
                self.sounds['catch'] = catch_sound
            
            # Звук промаха - низкий, нисходящий, немного грубый тон (square wave)
            miss_sound = self._generate_sound(frequencies=(400, 200), duration=0.4, volume=0.3, 
                                              attack_duration=0.02, release_duration=0.1, waveform='square')
            if miss_sound:
                self.sounds['miss'] = miss_sound
            
            # Звук отскока от полочки - очень короткий, ударный звук с легким свипом
            bounce_sound = self._generate_sound(frequencies=(700, 600), duration=0.08, volume=0.2, 
                                                attack_duration=0.001, release_duration=0.04)
            if bounce_sound:
                self.sounds['bounce'] = bounce_sound
            
            # Звук повышения сложности - более долгий, торжественный восходящий свип
            levelup_sound = self._generate_sound(frequencies=(600, 1200), duration=0.7, volume=0.35, 
                                                 attack_duration=0.05, release_duration=0.2)
            if levelup_sound:
                self.sounds['levelup'] = levelup_sound
            
            # Добавим звук для кнопки или подтверждения (пример)
            confirm_sound = self._generate_sound(frequencies=900, duration=0.07, volume=0.2, 
                                                 attack_duration=0.005, release_duration=0.03)
            if confirm_sound:
                self.sounds['confirm'] = confirm_sound
            
            # Звук для "Game Over" (пример)
            gameover_sound = self._generate_sound(frequencies=(250, 100), duration=1.0, volume=0.4,
                                                  attack_duration=0.1, release_duration=0.5, waveform='sawtooth')
            if gameover_sound:
                self.sounds['gameover'] = gameover_sound

        except Exception as e:
            print(f"Ошибка создания звуков: {e}")
    
    def play_sound(self, sound_name: str):
        """Воспроизведение звука"""
        if config.SOUND_ENABLED and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                # Иногда может быть ошибка, если микшер не готов или звук слишком короткий.
                # Можно записать в лог, но не прерывать игру.
                pass 
            except Exception as e:
                print(f"Неизвестная ошибка при воспроизведении звука '{sound_name}': {e}")
    
    def play_music(self, loop: bool = True):
        """Воспроизведение музыки"""
        # Музыка по-прежнему требует файл, так что оставим заглушку
        # Если нужно генерировать музыку, это значительно сложнее и выходит за рамки
        # простых звуковых эффектов.
        pass
    
    def stop_music(self):
        """Остановка музыки"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

