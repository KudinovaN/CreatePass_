#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Генератор паролей с графическим интерфейсом.

Этот файл содержит точку входа в приложение для генерации паролей.
При запуске создаётся экземпляр приложения PyQt5 и запускается
главное окно графического интерфейса.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui import PasswordGeneratorUI


def main():
    """
    Основная функция приложения, запускает пользовательский интерфейс.
    
    Returns:
        int: Код завершения приложения.
    """
    # Создаем экземпляр QApplication
    app = QApplication(sys.argv)
    
    # Устанавливаем иконку приложения
    icon_path = "icon.ico"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Создаем и показываем главное окно
    main_window = PasswordGeneratorUI()
    main_window.show()
    
    # Запускаем цикл обработки событий
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main()) 