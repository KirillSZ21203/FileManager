import os
import shutil
from typing import Callable


def move_file_interactive(
    folder_path: str,
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> None:
    """
    Перемещает выбранные пользователем файлы из указанной папки в одну из целевых категорий.

    :param folder_path: Путь к папке, где находятся файлы
    :param input_func: Функция для получения пользовательского ввода (по умолчанию input)
    :param print_func: Функция для вывода информации пользователю (по умолчанию print)
    """
    dest_folders = {
        "1": "Images",
        "2": "Documents",
        "3": "Music",
        "4": "Torrent files",
        "5": "Executable files",
        "6": "Archive files",
    }

    # Создаем папки назначения, если их нет
    for folder in dest_folders.values():
        os.makedirs(os.path.join(folder_path, folder), exist_ok=True)

    # Получаем список файлов в указанной папке
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    if not files:
        print_func("Нет доступных файлов для перемещения.")
        return

    # Выводим список файлов
    for i, file in enumerate(files, 1):
        print_func(f"{i}. {file}")

    # Запрашиваем номера файлов (поддержка: 1,3-5 или 'all')
    selection_raw = input_func(
        "Введите номера файлов (через запятую или диапазоны, например: 1,3-5, или 'all'): "
    ).strip()

    if selection_raw.lower() == "all":
        selected_indices = list(range(len(files)))
    else:
        parts = [p.strip() for p in selection_raw.split(",") if p.strip()]
        selected_indices = []
        for p in parts:
            if "-" in p:
                a, b = p.split("-", 1)
                if not a.isdigit() or not b.isdigit():
                    print_func(f"Некорректный диапазон: {p}")
                    return
                start, end = int(a), int(b)
                if start < 1 or end < 1 or start > len(files) or end > len(files) or start > end:
                    print_func(f"Диапазон вне допустимых границ: {p}")
                    return
                selected_indices.extend([i - 1 for i in range(start, end + 1)])
            else:
                if not p.isdigit():
                    print_func(f"Некорректный номер: {p}")
                    return
                idx = int(p)
                if idx < 1 or idx > len(files):
                    print_func(f"Номер вне допустимых границ: {p}")
                    return
                selected_indices.append(idx - 1)
        # Удаляем дубликаты, сохраняя порядок
        seen = set()
        selected_indices = [x for x in selected_indices if not (x in seen or seen.add(x))]

    if not selected_indices:
        print_func("Не выбрано ни одного файла.")
        return

    selected_files = [files[i] for i in selected_indices]

    print_func(
        "Куда переместить? "
        "1 - Images, "
        "2 - Documents, "
        "3 - Music, "
        "4 - Torrent files, "
        "5 - Executable files, "
        "6 - Archive files"
    )
    folder_num = input_func("Введите номер папки: ").strip()

    # Проверка на корректность номера папки
    if folder_num not in dest_folders:
        print_func(f"Неверный номер папки: {folder_num}")
        return

    def unique_destination_path(dst_dir: str, filename: str) -> str:
        base, ext = os.path.splitext(filename)
        candidate = os.path.join(dst_dir, filename)
        counter = 1
        while os.path.exists(candidate):
            candidate = os.path.join(dst_dir, f"{base} ({counter}){ext}")
            counter += 1
        return candidate

    # Перемещаем выбранные файлы
    dst_dir = os.path.join(folder_path, dest_folders[folder_num])
    os.makedirs(dst_dir, exist_ok=True)

    moved = []
    for fname in selected_files:
        source = os.path.join(folder_path, fname)
        destination = unique_destination_path(dst_dir, fname)
        shutil.move(source, destination)
        moved.append(os.path.basename(destination))

    print_func(f"Перемещено файлов: {len(moved)}")
    for nm in moved:
        print_func(f"- {nm} -> {dest_folders[folder_num]}")


if __name__ == "__main__":
    # Пример: путь по умолчанию — загрузки текущего пользователя (можно изменить на свой путь)
    default_download_path = os.path.join(os.path.expanduser("~"), "Desktop")
    print(f"Используется папка: {default_download_path}")
    move_file_interactive(default_download_path)
