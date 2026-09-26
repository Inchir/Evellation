import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Функция для настройки разных логгеров в разные файлы"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler(log_file, encoding="UTF-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = True  # Предотвращает дублирование в root логгере
    return logger