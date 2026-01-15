[app]

# Название приложения
title = Ловец Яиц

# Имя пакета
package.name = com.stk.catchball

# Домен
package.domain = com.stk

# Версия приложения
version = 1.0.0

# Главный файл
source.main = main.py

# Версия Python
python.version = 3.9

# Android настройки
android.api = 31
android.minapi = 21
android.sdk = 26
android.ndk = 25b
android.ndk_api = 21

# Разрешения
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Ориентация
orientation = portrait

# Полноэкранный режим
fullscreen = 1

# Требования
requirements = python3,kivy==2.1.0

# Иконка
icon.filename = assets/icon.png

# Заставка
presplash.filename = assets/presplash.png

# Архитектура
android.arch = armeabi-v7a, arm64-v8a, x86, x86_64

# Логирование
log_level = 2

# Включаемые файлы
source.include_exts = py,png,jpg,json,kv,atlas,ttf

# Исключения
source.exclude_exts = spec

# Подписи (оставьте пустыми для debug)
android.release_artifact = bin/CatchBall-{version}-release-unsigned.apk

# Параметры выпуска
# android.keystore = 
# android.keystore_passwd =
# android.keyalias =
# android.keyalias_passwd =

[buildozer]

# Путь к бинарным файлам
log_level = 2
warn_on_root = 1