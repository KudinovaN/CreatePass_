#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль графического интерфейса для генератора паролей.

Этот модуль содержит класс PasswordGeneratorUI, который предоставляет
графический интерфейс для генератора паролей в современном минималистичном стиле.
"""

import os
import pyperclip
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QSlider, QComboBox, QListWidget, QListWidgetItem, QMessageBox, 
                           QGroupBox, QCheckBox, QFrame, QApplication, 
                           QStyledItemDelegate, QStyle)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QColor, QPalette, QCursor, QPixmap

from password_generator import PasswordGenerator


class PasswordGeneratorUI(QMainWindow):
    """
    Графический интерфейс приложения генератора паролей.
    
    Attributes:
        generator (PasswordGenerator): Экземпляр класса генератора паролей.
    """
    
    # Определяем цвета темы - сиреневая гамма
    PURPLE_LIGHT = "#ffc0cb"
    PURPLE_MEDIUM = "#ffb6c1"
    PURPLE_DARK = "#fc6c85"
    PURPLE_VERY_DARK = "#e52b50"
    WHITE = "#FFFFFF"
    GRAY_LIGHT = "#F5F5F5"
    GRAY_MEDIUM = "#E0E0E0"
    GRAY_DARK = "#ffb6c1"
    BLACK = "#303030"
    
    def __init__(self):
        """
        Инициализирует главное окно приложения.
        """
        super().__init__()
        
        # Инициализация генератора паролей
        self.generator = PasswordGenerator()
        
        # Настройка окна
        self.setWindowTitle("Генератор паролей")
        # Устанавливаем фиксированный размер окна (нельзя изменить)
        self.setFixedSize(500, 730)
        
        # Устанавливаем иконку приложения
        self.setup_app_icon()
        
        # Устанавливаем стиль приложения
        self.apply_stylesheet()
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создание главного макета
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)  # Уменьшенные отступы между секциями
        main_layout.setContentsMargins(20, 20, 20, 20)  # Уменьшенные поля
        
        # Заголовок приложения
        title_label = QLabel("ГЕНЕРАТОР ПАРОЛЕЙ")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))  # Немного меньший заголовок
        main_layout.addWidget(title_label)
        
        # Инициализация интерфейса
        self._init_password_section(main_layout)
        self._init_settings_section(main_layout)
        self._init_history_section(main_layout)
        
        # Генерация первого пароля при запуске
        self.generate_password()
    
    def setup_app_icon(self):
        """
        Устанавливает иконку приложения.
        """
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            # Устанавливаем иконку для всего приложения
            QApplication.instance().setWindowIcon(app_icon)
    
    def apply_stylesheet(self):
        """
        Применяет таблицу стилей CSS к приложению.
        """
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {self.WHITE};
                color: {self.BLACK};
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
            
            #titleLabel {{
                color: {self.PURPLE_VERY_DARK};
                margin-bottom: 8px;
            }}
            
            QGroupBox {{
                border: 2px solid {self.PURPLE_MEDIUM};
                border-radius: 8px;
                margin-top: 12px;
                font-weight: bold;
                font-size: 13px;
                padding: 15px;
                background-color: {self.WHITE};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                color: {self.PURPLE_VERY_DARK};
                background-color: {self.WHITE};
            }}
            
            QLabel {{
                font-size: 12px;
                color: {self.BLACK};
            }}
            
            QLineEdit {{
                border: 2px solid {self.PURPLE_MEDIUM};
                border-radius: 5px;
                padding: 6px;
                background-color: {self.WHITE};
                color: {self.BLACK};
                selection-background-color: {self.PURPLE_LIGHT};
            }}
            
            QLineEdit:focus {{
                border-color: {self.PURPLE_DARK};
            }}
            
            #passwordField {{
                font-size: 14px;
                font-family: 'Consolas', 'Courier New', monospace;
                border-width: 2px;
                border-color: {self.PURPLE_DARK};
                padding: 10px;
                margin: 4px 0;
                background-color: {self.GRAY_LIGHT};
                border-radius: 6px;
            }}
            
            QPushButton {{
                background-color: {self.PURPLE_MEDIUM};
                color: {self.BLACK};
                border: none;
                border-radius: 5px;
                padding: 7px 12px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QPushButton:hover {{
                background-color: {self.PURPLE_DARK};
                color: {self.WHITE};
            }}
            
            QPushButton:pressed {{
                background-color: {self.PURPLE_VERY_DARK};
            }}
            
            #generateButton {{
                background-color: {self.PURPLE_DARK};
                color: {self.WHITE};
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 6px;
            }}
            
            #generateButton:hover {{
                background-color: {self.PURPLE_VERY_DARK};
            }}
            
            QComboBox {{
                border: 2px solid {self.PURPLE_MEDIUM};
                border-radius: 5px;
                padding: 6px;
                background-color: {self.WHITE};
                color: {self.BLACK};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: center right;
                padding-right: 5px;
            }}
            
            QComboBox::down-arrow {{
                image: url(none);
                width: 16px;
                height: 16px;
            }}
            
            QComboBox::down-arrow:on {{
                top: 1px;
                left: 1px;
            }}
            
            QComboBox:hover {{
                border-color: {self.PURPLE_DARK};
            }}
            
            QSlider::groove:horizontal {{
                border: 1px solid {self.GRAY_MEDIUM};
                height: 6px;
                background: {self.GRAY_LIGHT};
                margin: 2px 0;
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: {self.PURPLE_DARK};
                border: 1px solid {self.PURPLE_DARK};
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            
            QSlider::handle:horizontal:hover {{
                background: {self.PURPLE_VERY_DARK};
            }}
            
            QListWidget {{
                border: 2px solid {self.PURPLE_MEDIUM};
                border-radius: 5px;
                padding: 4px;
                background-color: {self.WHITE};
                alternate-background-color: {self.GRAY_LIGHT};
                font-size: 12px;
            }}
            
            QListWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {self.GRAY_MEDIUM};
            }}
            
            QListWidget::item:selected {{
                background-color: {self.PURPLE_LIGHT};
                color: {self.BLACK};
            }}
            
            QListWidget::item:hover {{
                background-color: {self.GRAY_LIGHT};
            }}
        """)
    
    def _init_password_section(self, main_layout):
        """
        Инициализирует секцию отображения пароля.
        
        Args:
            main_layout (QVBoxLayout): Главный макет приложения.
        """
        # Секция генерации пароля
        password_group = QGroupBox("Ваш пароль")
        password_group.setAlignment(Qt.AlignHCenter)  # Центрируем заголовок
        password_layout = QVBoxLayout(password_group)
        password_layout.setSpacing(10)  # Уменьшенный отступ
        password_layout.setContentsMargins(10, 10, 10, 10)  # Меньшие отступы
        
        # Поле для отображения пароля
        self.password_field = QLineEdit()
        self.password_field.setObjectName("passwordField")
        self.password_field.setReadOnly(True)
        self.password_field.setAlignment(Qt.AlignCenter)
        self.password_field.setFont(QFont("Consolas", 14))  # Устанавливаем стандартный размер шрифта
        self.password_field.setCursor(QCursor(Qt.IBeamCursor))
        self.password_field.setTextMargins(5, 0, 5, 0)  # Добавляем отступы внутри поля
        
        password_layout.addWidget(self.password_field)
        
        # Кнопка копирования пароля (единственная кнопка в этой секции)
        self.copy_button = QPushButton("Копировать")
        self.copy_button.setToolTip("Скопировать пароль в буфер обмена")
        self.copy_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.copy_button.clicked.connect(self.copy_password)
        
        password_layout.addWidget(self.copy_button)
        
        # Добавление секции генерации в главный макет
        main_layout.addWidget(password_group)
    
    def _init_settings_section(self, main_layout):
        """
        Инициализирует секцию настроек пароля.
        
        Args:
            main_layout (QVBoxLayout): Главный макет приложения.
        """
        # Секция настроек пароля
        settings_group = QGroupBox("Настройки пароля")
        settings_group.setAlignment(Qt.AlignHCenter)  # Центрируем заголовок
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(15)  # Меньший отступ
        settings_layout.setContentsMargins(10, 10, 10, 10)  # Меньшие отступы
        
        # Выбор режима генерации
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Режим:")
        mode_label.setMinimumWidth(60)  # Меньшая ширина метки
        mode_layout.addWidget(mode_label)
        
        # Создаем стилизованный ComboBox с иконкой раскрывающегося списка
        self.mode_combo = QComboBox()
        self.mode_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Добавляем кастомный стиль с иконкой галочки
        self.mode_combo.setStyleSheet(f"""
            QComboBox::down-arrow {{
                image: url('');
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox {{
                padding-right: 20px; /* Место для иконки */
                background-image: url('');
                background-position: center right;
                background-repeat: no-repeat;
                selection-background-color: {self.PURPLE_LIGHT};
            }}
        """)
        
        # Добавляем иконку выпадающего списка (используем нашу иконку, если она есть)
        if os.path.exists("icon.ico"):
            arrow_icon = QIcon("icon.ico")
        else:
            arrow_icon = self.style().standardIcon(QStyle.SP_ArrowDown)
            
        self.mode_combo.view().window().setWindowIcon(arrow_icon)
        
        # Заполнение комбобокса режимами
        for mode in self.generator.get_available_modes():
            description = self.generator.get_mode_description(mode)
            self.mode_combo.addItem(description, mode)
        
        mode_layout.addWidget(self.mode_combo, 1)
        settings_layout.addLayout(mode_layout)
        
        # Настройка длины пароля
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина:")
        length_label.setMinimumWidth(60)  # Меньшая ширина метки
        length_layout.addWidget(length_label)
        
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setMinimum(4)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)
        self.length_slider.setTickPosition(QSlider.TicksBelow)
        self.length_slider.setTickInterval(4)
        self.length_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.length_slider.valueChanged.connect(self.update_length_display)
        length_layout.addWidget(self.length_slider, 1)
        
        self.length_display = QLineEdit()
        self.length_display.setMaximumWidth(40)  # Меньшая ширина поля
        self.length_display.setAlignment(Qt.AlignCenter)
        self.length_display.setText(str(self.length_slider.value()))
        self.length_display.setValidator(QIntValidator(4, 32))
        self.length_display.editingFinished.connect(self.update_length_slider)
        length_layout.addWidget(self.length_display)
        
        settings_layout.addLayout(length_layout)
        
        # Кнопка генерации пароля
        generate_layout = QHBoxLayout()
        generate_button = QPushButton("СГЕНЕРИРОВАТЬ ПАРОЛЬ")
        generate_button.setObjectName("generateButton")
        generate_button.setMinimumHeight(40)  # Уменьшенная высота кнопки
        generate_button.setCursor(QCursor(Qt.PointingHandCursor))
        generate_button.clicked.connect(self.generate_password)
        
        generate_layout.addWidget(generate_button)
        
        settings_layout.addLayout(generate_layout)
        
        # Добавление секции настроек в главный макет
        main_layout.addWidget(settings_group)
    
    def _init_history_section(self, main_layout):
        """
        Инициализирует секцию истории паролей.
        
        Args:
            main_layout (QVBoxLayout): Главный макет приложения.
        """
        # Секция истории паролей
        history_group = QGroupBox("История паролей")
        history_group.setAlignment(Qt.AlignHCenter)  # Центрируем заголовок
        history_layout = QVBoxLayout(history_group)
        history_layout.setSpacing(8)  # Меньший отступ
        history_layout.setContentsMargins(10, 10, 10, 10)  # Меньшие отступы
        
        # Список истории паролей
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        self.history_list.itemDoubleClicked.connect(self.select_password_from_history)
        self.history_list.setCursor(QCursor(Qt.PointingHandCursor))
        self.history_list.setMinimumHeight(100)  # Уменьшенная высота списка
        # Убедимся, что пароли отображаются полностью
        self.history_list.setWordWrap(True)
        self.history_list.setTextElideMode(Qt.ElideNone)
        history_layout.addWidget(self.history_list)
        
        # Кнопка очистки истории
        clear_history_button = QPushButton("Очистить историю")
        clear_history_button.clicked.connect(self.clear_history)
        clear_history_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        history_layout.addWidget(clear_history_button)
        
        # Добавление секции истории в главный макет
        main_layout.addWidget(history_group)
    
    def generate_password(self):
        """
        Генерирует пароль с текущими настройками и обновляет интерфейс.
        """
        # Получаем текущие настройки
        length = self.length_slider.value()
        mode = self.mode_combo.currentData()
        
        try:
            # Генерируем пароль
            password = self.generator.generate_password(length=length, mode=mode)
            
            # Обновляем поле пароля с анимацией
            self.animate_password_field()
            self.password_field.setText(password)
            
            # Обновляем список истории
            self.update_history_list()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать пароль: {str(e)}")
    
    def animate_password_field(self):
        """
        Анимирует поле пароля при генерации нового пароля.
        """
        # Создаем анимацию изменения цвета фона
        self.password_field.setStyleSheet(f"""
            #passwordField {{
                background-color: {self.PURPLE_LIGHT};
                font-size: 14px;
                font-family: 'Consolas', 'Courier New', monospace;
                border-width: 2px;
                border-color: {self.PURPLE_DARK};
                padding: 10px;
                margin: 4px 0;
                border-radius: 6px;
            }}
        """)
        
        # Возвращаем исходный стиль через 200 мс
        QApplication.processEvents()
        QApplication.instance().processEvents()
        
        # Сбрасываем стиль
        self.password_field.setStyleSheet("")
    
    def adjust_password_font_size(self, password):
        """
        Упрощённый метод для настройки размера шрифта.
        Теперь просто используем стандартный размер для всех паролей.
        
        Args:
            password (str): Пароль для отображения.
        """
        pass  # Больше не меняем размер шрифта в зависимости от длины пароля
    
    def update_length_display(self):
        """
        Обновляет отображение длины пароля при изменении слайдера.
        """
        self.length_display.setText(str(self.length_slider.value()))
    
    def update_length_slider(self):
        """
        Обновляет значение слайдера при изменении поля ввода длины.
        """
        try:
            length = int(self.length_display.text())
            # Ограничиваем значение допустимым диапазоном
            length = max(4, min(32, length))
            self.length_slider.setValue(length)
        except ValueError:
            # Если введено некорректное значение, возвращаем текущее значение слайдера
            self.length_display.setText(str(self.length_slider.value()))
    
    def copy_password(self):
        """
        Копирует текущий пароль в буфер обмена.
        """
        password = self.password_field.text()
        if password:
            pyperclip.copy(password)
            
            # Меняем текст кнопки на "Скопировано!" на короткое время
            original_text = self.copy_button.text()
            # Убираем сохранение иконки
            self.copy_button.setText("Скопировано!")
            self.copy_button.setStyleSheet(f"background-color: {self.PURPLE_VERY_DARK}; color: {self.WHITE};")
            
            # Восстанавливаем текст через 0.5 секунды
            QApplication.instance().processEvents()
            import time
            time.sleep(0.5)
            self.copy_button.setText(original_text)
            self.copy_button.setStyleSheet("")
    
    def update_history_list(self):
        """
        Обновляет список истории паролей.
        """
        # Очищаем текущий список
        self.history_list.clear()
        
        # Добавляем пароли из истории без иконки
        for password in self.generator.get_history():
            item = QListWidgetItem(password)
            self.history_list.addItem(item)
    
    def select_password_from_history(self, item):
        """
        Выбирает пароль из истории при двойном клике.
        
        Args:
            item: Элемент списка, содержащий пароль.
        """
        password = item.text()
        self.password_field.setText(password)
        
        # Анимация выбора пароля
        self.animate_password_field()
    
    def clear_history(self):
        """
        Очищает историю паролей.
        """
        # Запрос подтверждения без иконки
        msg_box = QMessageBox(
            QMessageBox.Question, 
            "Подтверждение", 
            "Вы уверены, что хотите очистить историю паролей?",
            QMessageBox.Yes | QMessageBox.No, 
            self
        )
        msg_box.setDefaultButton(QMessageBox.No)
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            # Очищаем историю
            self.generator.clear_history()
            self.update_history_list() 