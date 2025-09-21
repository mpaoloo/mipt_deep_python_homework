"""Модуль для фильтрации файлов по ключевым словам"""


def filter_file(
    file_,
    search_words,
    stop_words,
):
    """Фильтрует строки файла по заданным словам."""

    search_lower = [word.lower() for word in search_words]
    stop_lower = [word.lower() for word in stop_words]

    need_to_close_file = False
    file_object = None

    try:
        if isinstance(file_, str):
            # pylint: disable=consider-using-with
            file_object = open(file_, "r", encoding="utf-8")
            need_to_close_file = True
        else:
            file_object = file_
            need_to_close_file = False

        for line in file_object:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            words_in_line = line_stripped.lower().split()

            if any(stop_word in words_in_line for stop_word in stop_lower):
                continue

            if any(
                search_word in words_in_line for search_word in search_lower
            ):
                yield line
    finally:
        if need_to_close_file and file_object and not file_object.closed:
            file_object.close()
