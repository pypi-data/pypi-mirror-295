# yaroslavslogger/greetings.py

import ctypes
import os

def say_hello(name):
    # Определяем путь к текущей директории, где находится модуль
    current_dir = os.path.dirname(__file__)

    # Путь к библиотеке будет внутри пакета, а не на уровне выше
    if os.name == 'nt':  # Для Windows
        lib_path = os.path.join(current_dir, "compiled_libraries", "string_length.dll")
    else:  # Для Linux и macOS
        lib_path = os.path.join(current_dir, "compiled_libraries", "libstring_length.so")

    # Проверяем, существует ли библиотека по указанному пути
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"Library not found: {lib_path}")

    # Загружаем библиотеку
    lib = ctypes.CDLL(lib_path)

    # Определяем аргументы и возвращаемый тип функции
    lib.string_length.argtypes = [ctypes.c_char_p]
    lib.string_length.restype = ctypes.c_int

    # Преобразуем Python-строку в байты для C
    name_bytes = name.encode('utf-8')

    # Вызываем C-функцию
    length = lib.string_length(name_bytes)

    # Возвращаем результат
    return f"Hello, {name}! Your name has {length} characters."

