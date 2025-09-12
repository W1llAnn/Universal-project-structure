# Universal Project Structure

Универсальный шаблон для микросервисов на Python: API (FastAPI), Gradio-интерфейсы, обработка текстов с LLM, работа с базами данных.

Этот шаблон создан для **единообразия проектов** в команде. Он помогает:

- Быстро стартовать новый сервис
- Поддерживать чистую и понятную архитектуру
- Обеспечить безопасность (ключи в `.env`, не в коде)
- Гарантировать структурированный вывод от LLM
- Упростить разработку, тестирование и деплой

> Совместим с vLLM, OpenAI, Anthropic  
> Поддерживает Docker, Docker Compose, FastAPI, Gradio  
> Использует Pydantic для валидации и структурированного вывода

---

## Структура проекта

```
Universal-project-structure/
├── configs/                  # Конфиги, промпты, схемы
│   ├── config.py             # Настройки из .env
│   ├── prompts.py            # Промпты для LLM
│   ├── schemas.py            # Pydantic-модели для валидации
│   └── utils.py              # Вспомогательные функции (логгеры, утилиты)
├── gradio_app/               # Визуальный интерфейс (опционально)
│   ├── gradio_app.py         # Запуск Gradio
│   └── utils.py              # Помощь для интерфейса
├── src/                      # Основная логика приложения
│   ├── evaluator.py          # Вызов LLM, обработка ответов
│   └── service.py            # Бизнес-логика: валидация, вызовы, логирование
├── tests/                    # Автотесты
│   └── test_service.py       # Примеры unit-тестов
├── .env                      # Переменные окружения (не коммитится!)
├── .gitignore                # Защита чувствительных файлов
├── Dockerfile                # Сборка образа
├── docker-compose.yml        # Запуск сервисов (API, Gradio, БД)
├── requirements.txt          # Зависимости
├── main.py                   # Точка входа: API (FastAPI)
└── README.md                 # Эта инструкция
```


## Переменные окружения

Все ключи, порты и настройки вынесены в `.env`.  
Никогда не коммить этот файл в Git!

1. Отредактируйте .env, указав свои значения (возьмите env-file как пример):
```
OPENAI_API_KEY или другой LLM-ключ
Порты (API_PORT, GRADIO_PORT)
Настройки БД (если используется)
```
Добавьте .env в .gitignore! 
     

## Ключевые возможности 
**Структурированный вывод от LLM (Structured Outputs)**

1. Используется vLLM  с guided_json для гарантированного получения валидного JSON. 

Пример:  
```
extra_body={"guided_json": EvaluationResult.model_json_schema()}
```
Это исключает ошибки парсинга и делает интеграцию с бэкендом надёжной.


2. Валидация данных через Pydantic  
- schemas.py — определяет формат запросов и ответов  
- main.py — автоматически проверяет вход и выход  
- /docs — генерирует интерактивную документацию  

3. Централизованная конфигурация   
Все настройки — в configs/config.py. Поддерживаются:   
- API-ключи  
- Порты  
- Модель LLM  
- Режим отладки  
- Подключение к БД  

4. Логирование и безопасность 
- Все чувствительные данные — в .env
- Логгеры настраиваются через configs/utils.py
- Минимальный образ Docker (python:3.10-slim)

## Полезные ссылки 
- [vLLM: Structured Outputs](https://docs.vllm.ai/en/v0.8.5.post1/features/structured_outputs.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/?spm=a2ty_o01.29997173.0.0.2037c921x7IrPK)
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/?spm=a2ty_o01.29997173.0.0.2037c921x7IrPK)
- [Docker Compose Reference](https://docs.docker.com/reference/compose-file/)