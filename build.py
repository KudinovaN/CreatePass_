#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для сборки приложения генератора паролей в exe-файл.

Этот скрипт использует PyInstaller для упаковки Python-приложения
в автономный исполняемый файл (.exe), который можно запустить
на любом компьютере с Windows без установки Python.
"""

import os
import sys
import shutil
import subprocess
import platform

def check_pyinstaller():
    """
    Проверяет, установлен ли PyInstaller, и устанавливает его при необходимости.
    """
    try:
        import PyInstaller
        print("PyInstaller уже установлен.")
    except ImportError:
        print("PyInstaller не установлен. Устанавливаем...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller успешно установлен.")

def build_exe():
    """
    Создает exe-файл из приложения с помощью PyInstaller.
    """
    print("Начинаем сборку exe-файла...")
    
    # Проверяем наличие иконки
    icon_path = "icon.ico"
    if not os.path.exists(icon_path):
        print(f"Предупреждение: Файл иконки {icon_path} не найден!")
        icon_option = []
    else:
        icon_option = ["--icon", icon_path]
    
    # Создаем команду для PyInstaller
    command = [
        "pyinstaller",
        "--name=Генератор_паролей",
        "--onefile",  # Создаем один exe-файл
        "--windowed",  # Без консольного окна
        "--clean",  # Очищаем кэш перед сборкой
        "--noconfirm",  # Без подтверждения перезаписи
        *icon_option,  # Опция иконки (если есть)
        "--add-data", f"{icon_path};.",  # Добавляем иконку в exe
        "main.py"  # Основной файл приложения
    ]
    
    # Запускаем команду
    print("Запускаем PyInstaller...")
    print("Команда:", " ".join(command))
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Выводим результат
    if result.returncode == 0:
        print("Сборка успешно завершена!")
        
        # Путь к созданному exe-файлу
        exe_path = os.path.join("dist", "Генератор_паролей.exe")
        
        if os.path.exists(exe_path):
            print(f"Исполняемый файл создан: {os.path.abspath(exe_path)}")
        else:
            print("Ошибка: Исполняемый файл не найден. Проверьте вывод PyInstaller.")
    else:
        print("Произошла ошибка при сборке:")
        print(result.stdout)
        print(result.stderr)

def clean_build_files():
    """
    Очищает временные файлы сборки.
    """
    print("Очищаем временные файлы сборки...")
    
    # Папки для удаления
    dirs_to_remove = ["build", "__pycache__"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Удаляем {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Файлы для удаления
    spec_file = "Генератор_паролей.spec"
    if os.path.exists(spec_file):
        print(f"Удаляем {spec_file}...")
        os.remove(spec_file)
    
    print("Очистка завершена.")

def main():
    """
    Основная функция для запуска процесса сборки.
    """
    print("=== Сборка приложения 'Генератор паролей' ===")
    
    # Проверяем операционную систему
    if platform.system() != "Windows":
        print("Предупреждение: Сборка выполняется не на Windows. Результат может не работать на Windows.")
    
    # Проверяем и устанавливаем PyInstaller
    check_pyinstaller()
    
    # Собираем exe-файл
    build_exe()
    
    # Очищаем временные файлы
    clean_build_files()
    
    print("=== Сборка завершена ===")
    print("Теперь вы можете распространять файл 'dist/Генератор_паролей.exe'.")
    print("Он содержит все необходимые компоненты и работает без установки Python.")

if __name__ == "__main__":
    main() 