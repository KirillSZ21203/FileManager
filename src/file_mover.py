import os
import shutil
from typing import Callable


def move_file_interactive(
    folder_path: str,
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print
) -> None:
    """
    Перемещает выбранный пользователем файл из указанной папки в одну из целевых категорий.

    :param folder_path: Путь к папке, где находятся файлы
    :param input_func: Функция для получения пользовательского ввода (по умолчанию input)
    :param print_func: Функция для вывода информации пользователю (по умолчанию print)
    """
    dest_folders = {
        "1": "Images",
        "2": "Documents",
        "3": "Music",
        "4": "Torrent files",
        "5": "Executable files"
    }

    # Создаем папки назначения, если их нет
    for folder in dest_folders.values():
        os.makedirs(os.path.join(folder_path, folder), exist_ok=True)

    # Получаем список файлов в указанной папке
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        print_func("Нет доступных файлов для перемещения.")
        return

    # Выводим список файлов
    for i, file in enumerate(files, 1):
        print_func(f"{i}. {file}")

    # Запрашиваем номер файла и номер папки
    file_num = int(input_func("Выберите номер файла: ")) - 1
    file_to_move = files[file_num]

    print_func("Куда переместить? 1 - Images, 2 - Documents, 3 - Music, 4 - Torrent files, 5 - Executable files")
    folder_num = input_func("Введите номер папки: ")

    # Проверка на корректность номера папки
    if folder_num not in dest_folders:
        raise KeyError(f"Неверный номер папки: {folder_num}")

    # Перемещаем файл
    source = os.path.join(folder_path, file_to_move)
    destination = os.path.join(folder_path, dest_folders[folder_num], file_to_move)
    shutil.move(source, destination)

    print_func(f"Файл {file_to_move} перемещен в {dest_folders[folder_num]}")


if __name__ == "__main__":
    # Пример: путь по умолчанию — загрузки текущего пользователя (можно изменить)
    default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"Используется папка: {default_download_path}")
    move_file_interactive(default_download_path)
