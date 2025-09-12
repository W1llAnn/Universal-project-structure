import logging


def setup_logger(name: str, level=logging.INFO):
    """
    Настраивает и возвращает логгер с указанным именем и уровнем.

    Создаёт логгер с заданным именем и добавляет к нему StreamHandler для вывода сообщений в stdout.
    Настраивает формат сообщений: дата-время, имя логгера, уровень и само сообщение.
    Проверяет наличие обработчиков, чтобы избежать дублирования при многократном вызове.

    Args:
        name (str): Имя логгера (обычно используется имя модуля).
        level (_int_, optional): Уровень логирования (например, logging.INFO, logging.DEBUG). По умолчанию — logging.INFO.

    Returns:
        logging.Logger: Настроенный экземпляр логгера.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


def truncate_text(text: str, max_len: int = 500) -> str:
    """
    Обрезает текст до указанной максимальной длины с добавлением суффикса "..." если необходимо.

    Полезна для ограничения объёма отображаемых данных в логах или интерфейсе,
    предотвращая переполнение и улучшая читаемость.

    Args:
        text (str): Исходный текст для обрезки.
        max_len (int, optional): Максимально допустимая длина текста перед обрезкой. По умолчанию — 500.

    Returns:
        str: Обрезанный текст, если исходный длиннее max_len, иначе — исходный текст без изменений.
    """
    return text[:max_len] + "..." if len(text) > max_len else text