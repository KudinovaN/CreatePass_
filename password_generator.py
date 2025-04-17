#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль генератора паролей.

Этот модуль содержит класс PasswordGenerator, который позволяет
генерировать пароли с различными настройками и режимами.
"""

import random
import string
from typing import List, Optional


class PasswordGenerator:
    """
    Класс для генерации паролей с различными настройками.
    
    Attributes:
        password_history (List[str]): История сгенерированных паролей.
        max_history_size (int): Максимальный размер истории паролей.
    """
    
    # Константы для режимов генерации
    MODE_LETTERS_ONLY = "только_буквы"
    MODE_LETTERS_DIGITS = "буквы_цифры"
    MODE_FULL = "полный"
    MODE_READABLE = "читаемый"
    
    def __init__(self, max_history_size: int = 10):
        """
        Инициализирует генератор паролей.
        
        Args:
            max_history_size (int, optional): Максимальный размер истории паролей. 
                По умолчанию 10.
        """
        self.password_history: List[str] = []
        self.max_history_size = max_history_size
    
    def generate_password(self, length: int = 12, mode: str = "полный") -> str:
        """
        Генерирует пароль заданной длины в соответствии с указанным режимом.
        
        Args:
            length (int, optional): Длина пароля. По умолчанию 12.
            mode (str, optional): Режим генерации пароля:
                - "только_буквы": только буквы верхнего и нижнего регистра
                - "буквы_цифры": буквы и цифры
                - "полный": буквы, цифры и специальные символы
                - "читаемый": легко читаемый пароль без похожих символов
                По умолчанию "полный".
        
        Returns:
            str: Сгенерированный пароль.
            
        Raises:
            ValueError: Если указан неверный режим или длина пароля меньше 4.
        """
        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов")
        
        # Определяем набор символов в зависимости от режима
        if mode == self.MODE_LETTERS_ONLY:
            chars = string.ascii_letters
        elif mode == self.MODE_LETTERS_DIGITS:
            chars = string.ascii_letters + string.digits
        elif mode == self.MODE_FULL:
            chars = string.ascii_letters + string.digits + string.punctuation
        elif mode == self.MODE_READABLE:
            # Исключаем символы, которые могут быть похожи: i, l, 1, I, 0, O, o, и т.д.
            chars = ''.join(set(string.ascii_letters + string.digits) - 
                           set('il1IoO0'))
        else:
            raise ValueError(f"Неизвестный режим генерации: {mode}")
        
        # Генерируем пароль
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Добавляем пароль в историю
        self._add_to_history(password)
        
        return password
    
    def _add_to_history(self, password: str) -> None:
        """
        Добавляет пароль в историю с учетом максимального размера истории.
        
        Args:
            password (str): Пароль для добавления в историю.
        """
        # Добавляем пароль в начало истории
        self.password_history.insert(0, password)
        
        # Если история превысила максимальный размер, удаляем последний элемент
        if len(self.password_history) > self.max_history_size:
            self.password_history.pop()
    
    def get_history(self) -> List[str]:
        """
        Возвращает историю сгенерированных паролей.
        
        Returns:
            List[str]: Список сгенерированных паролей.
        """
        return self.password_history
    
    def clear_history(self) -> None:
        """
        Очищает историю сгенерированных паролей.
        """
        self.password_history.clear()
    
    def get_available_modes(self) -> List[str]:
        """
        Возвращает список доступных режимов генерации паролей.
        
        Returns:
            List[str]: Список доступных режимов.
        """
        return [
            self.MODE_LETTERS_ONLY,
            self.MODE_LETTERS_DIGITS,
            self.MODE_FULL,
            self.MODE_READABLE
        ]
    
    def get_mode_description(self, mode: str) -> Optional[str]:
        """
        Возвращает описание режима генерации пароля.
        
        Args:
            mode (str): Режим генерации пароля.
            
        Returns:
            Optional[str]: Описание режима или None, если режим не найден.
        """
        descriptions = {
            self.MODE_LETTERS_ONLY: "Только буквы верхнего и нижнего регистра",
            self.MODE_LETTERS_DIGITS: "Буквы и цифры",
            self.MODE_FULL: "Буквы, цифры и специальные символы",
            self.MODE_READABLE: "Легко читаемые символы (без похожих символов)"
        }
        
        return descriptions.get(mode)


if __name__ == "__main__":
    # Пример использования
    generator = PasswordGenerator()
    
    # Генерация паролей в разных режимах
    print("Пример паролей:")
    print(f"Только буквы: {generator.generate_password(mode=PasswordGenerator.MODE_LETTERS_ONLY)}")
    print(f"Буквы и цифры: {generator.generate_password(mode=PasswordGenerator.MODE_LETTERS_DIGITS)}")
    print(f"Полный: {generator.generate_password(mode=PasswordGenerator.MODE_FULL)}")
    print(f"Читаемый: {generator.generate_password(mode=PasswordGenerator.MODE_READABLE)}")
    
    # Вывод истории
    print("\nИстория паролей:")
    for password in generator.get_history():
        print(f"- {password}") 