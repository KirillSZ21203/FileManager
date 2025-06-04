"""
Для запуска теста - ввести pytest -s
os — используется для работы с файловой системой (создание путей, проверка существования файлов).
tempfile — используется для создания временных директорий, чтобы не работать с реальной файловой системой.
pytest — основной тестовый фреймворк.
from file_mover import move_file_interactive — импорт тестируемой функции из модуля,
где находится логика перемещения файлов.
"""

import os
import tempfile
import pytest
from src.file_mover import move_file_interactive


def test_move_txt_file_to_documents():
    """
    Проверяет, что текстовый файл корректно перемещается в папку 'Documents'.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "test.txt"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("Hello")

        inputs = iter(["1", "2"])  # 1 — выбрать файл, 2 — Documents
        outputs = []

        move_file_interactive(
            folder_path=temp_dir,
            input_func=lambda _: next(inputs),
            print_func=lambda msg: outputs.append(msg),
        )

        dest_path = os.path.join(temp_dir, "Documents", test_filename)

        assert not os.path.exists(test_filepath), "Файл не был удалён из исходной папки"
        assert os.path.exists(dest_path), "Файл не появился в целевой папке"
        assert any("перемещен в Documents" in line for line in outputs)


def test_create_destination_folders():
    """
    Проверяет, что целевая папка создаётся автоматически, если её не было.
    Также проверяет корректное перемещение mp3-файла в 'Music'.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "song.mp3"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("music content")

        inputs = iter(["1", "3"])  # 1 — выбрать файл, 3 — Music
        outputs = []

        move_file_interactive(
            folder_path=temp_dir,
            input_func=lambda _: next(inputs),
            print_func=lambda msg: outputs.append(msg),
        )

        dest_folder = os.path.join(temp_dir, "Music")
        dest_path = os.path.join(dest_folder, test_filename)

        assert os.path.isdir(dest_folder), "Целевая папка 'Music' не была создана"
        assert os.path.exists(dest_path), "Файл не переместился в 'Music'"


def test_invalid_folder_number():
    """
    Проверяет, что ввод несуществующего номера папки вызывает KeyError.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "file.exe"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("executable")

        inputs = iter(["1", "228"])  # 1 — выбрать файл, 228 — неверная папка

        with pytest.raises(KeyError):
            move_file_interactive(
                folder_path=temp_dir,
                input_func=lambda _: next(inputs),
                print_func=lambda msg: None,
            )
