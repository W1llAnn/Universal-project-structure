import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Конфигурационный класс для хранения и валидации настроек приложения.

    Загружает параметры из переменных окружения (и файла .env), обеспечивая централизованное управление
    конфигурацией сервиса. Включает настройки API-ключей, сетевых параметров, модели LLM,
    подключения к базе данных и режимов работы. Использует Pydantic BaseSettings для автоматической
    валидации типов и безопасной загрузки чувствительных данных.

    Args:
        BaseSettings (pydantic.BaseSettings): Базовый класс Pydantic для управления настройками через переменные окружения.
    """

    # === API КЛЮЧИ ===
    # Эти переменные берутся из .env. Никогда не коммить их в Git!
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    # Опциональный ключ для Anthropic (Claude). Может быть пустым.
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")

    # === СЕТЕВЫЕ НАСТРОЙКИ ===
    # Хост, на котором будет слушать приложение (внутри контейнера)
    APP_HOST: str = os.getenv("APP_HOST")  # 0.0.0.0 = доступен извне контейнера
    # Порт для FastAPI (должен совпадать с внутренним портом в docker-compose.yml)
    APP_PORT: int = int(os.getenv("APP_PORT"))
    # Порт для Gradio (если используется)
    GRADIO_PORT: int = int(os.getenv("GRADIO_PORT"))

    # === МОДЕЛЬ LLM ===
    # Какую модель использовать (например: gpt-3.5-turbo, gpt-4o-mini, claude-3-haiku)
    LLM_MODEL: str = os.getenv("LLM_MODEL")

    # === БАЗА ДАННЫХ ===
    # Строка подключения к БД. Пример для PostgreSQL:
    # postgresql://user:password@db:5432/mydatabase
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # ВАЖНО: если DATABASE_URL не задан — приложение упадёт при запуске
    # Чтобы сделать обязательным полем, можно убрать значение по умолчанию

    # === РЕЖИМ ОТЛАДКИ ===
    # DEBUG=True — больше логов, auto-reload, детальные ошибки
    # Значение по умолчанию: False (безопасно для продакшена)
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    # Объяснение: os.getenv возвращает строку → приводим к bool через сравнение

    # === ДРУГИЕ НАСТРОЙКИ (примеры) ===
    # Максимальная длина текста для обработки
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", 10000))
    # Таймаут запроса к LLM (в секундах)
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", 30))

    # Настройка Pydantic для работы с .env
    class Config:
        env_file = ".env"           # Указывает, откуда читать переменные окружения
        env_file_encoding = "utf-8" # Кодировка файла (если в .env есть кириллица)
        # Дополнительно (Pydantic v1): можно добавить
        # case_sensitive = False    # Игнорировать регистр (RELOAD и reload — одно и то же)

# Создаём ЕДИНСТВЕННЫЙ экземпляр настроек
# Теперь в любом файле проекта можно писать:
#   from configs.config import settings
#   if settings.DEBUG: ...
settings = Settings()