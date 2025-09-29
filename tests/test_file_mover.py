"""
Для запуска теста - ввести pytest -s
"""
import os
import tempfile
import pytest
from src.file_mover import move_file_interactive


def test_move_txt_file_to_documents():
    """
    Проверяет, что текстовый файл корректно перемещается в папку 'Documents'
    с учётом нового порядка вопросов (множественный выбор, вопрос о кастомных папках).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "test.txt"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("Hello")

        # 1 — выбрать файл с индексом 1
        # n — не добавлять пользовательские папки
        # 2 — выбор 'Documents'
        inputs = iter(["1", "n", "2"])
        outputs = []

        move_file_interactive(
            folder_path=temp_dir,
            input_func=lambda _: next(inputs),
            print_func=lambda msg: outputs.append(msg),
        )

        dest_path = os.path.join(temp_dir, "Documents", test_filename)

        assert not os.path.exists(test_filepath), "Файл не был удалён из исходной папки"
        assert os.path.exists(dest_path), "Файл не появился в целевой папке"
        assert any("Перемещено файлов: 1" in line for line in outputs)
        assert any(f"- {test_filename} -> Documents" in line for line in outputs)


def test_create_destination_folders():
    """
    Проверяет, что целевая папка создаётся автоматически, если её не было,
    и корректное перемещение mp3-файла в 'Music'.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "song.mp3"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("music content")

        # 1 — выбрать файл, n — не добавлять пользовательские папки, 3 — Music
        inputs = iter(["1", "n", "3"])
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
        assert any("Перемещено файлов: 1" in line for line in outputs)
        assert any(f"- {test_filename} -> Music" in line for line in outputs)


def test_invalid_folder_number():
    """
    Проверяет, что ввод несуществующего номера папки не вызывает исключение,
    а приводит к печати сообщения и завершению без перемещения.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = "file.exe"
        test_filepath = os.path.join(temp_dir, test_filename)
        with open(test_filepath, "w") as f:
            f.write("executable")

        # 1 — выбрать файл, n — не добавлять пользовательские папки, 228 — неверная папка
        inputs = iter(["1", "n", "228"])
        outputs = []

        move_file_interactive(
            folder_path=temp_dir,
            input_func=lambda _: next(inputs),
            print_func=lambda msg: outputs.append(msg),
        )

        # Файл должен остаться на месте
        assert os.path.exists(test_filepath), "Файл не должен был быть перемещён"
        assert any("Неверный номер папки" in line for line in outputs), "Ожидалось сообщение об ошибке номера папки"
        