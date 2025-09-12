from fastapi import FastAPI, HTTPException

from configs.schemas import EvaluateRequest, EvaluateResponse
from src.service import process_evaluation
from configs.config import settings


app = FastAPI(
    title="API",
    description="""
    API для автоматической оценки текстовых ответов студентов с помощью LLM.

    Особенности:
    - Поддержка структурированного вывода (JSON по схеме)
    - Совместимость с vLLM и OpenAI
    - Валидация входных/выходных данных
    - Полная документация по /docs

    Документация vLLM по structured outputs:
    https://docs.vllm.ai/en/v0.8.5.post1/features/structured_outputs.html
    """,
    version="1.0.0"
)


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest):
    """
    Обработчик POST-запроса для оценки ответа студента по заданному предмету.

    Принимает запрос с текстом ответа и предметом, запускает процесс оценки через LLM
    с использованием структурированного вывода (guided_json), валидирует результат
    и возвращает ответ в строгом соответствии со схемой `EvaluateResponse`.

    Args:
        request (EvaluateRequest): Объект запроса, содержащий:
            - answer (str): Текст ответа студента.
            - subject (str): Предмет, по которому дан ответ.
            - criteria (Optional[List[str]]): Дополнительные критерии оценки (необязательно).

    Raises:
        HTTPException: С кодом 500, если произошла ошибка при обработке оценки.
        HTTPException: С кодом 500, если ответ модели не соответствует ожидаемой схеме.
        HTTPException: С кодом 500, если возникла любая другая непредвиденная ошибка.

    Returns:
        dict: Результат оценки в формате словаря, соответствующем модели `EvaluateResponse`,
              содержащий поля `score` и `feedback`. Возвращается как JSON-ответ.
    """
    try:
        result = process_evaluation(request.answer, request.subject)

        # Проверяем, есть ли ошибка от сервиса
        if "error" in result:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при оценке: {result['error']}"
            )

        # Гарантируем, что выход соответствует схеме EvaluateResponse
        # Это защита от "почти JSON" или неправильных полей
        try:
            validated_response = EvaluateResponse(**result)
            return validated_response.model_dump()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка формата ответа LLM: {str(e)}. "
                       f"Получено: {result}"
            )

    except HTTPException:
        raise  # Перебрасываем дальше
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def health():
    """
    Корневой эндпоинт для проверки работоспособности и получения информации о состоянии сервиса.

    Используется для health check, мониторинга и диагностики. Возвращает основные параметры конфигурации.

    Returns:
        dict: Информация о текущем состоянии сервиса, включая:
            - status (str): Общий статус ("ok").
            - debug (bool): Включен ли режим отладки.
            - model (str): Имя используемой языковой модели.
            - api_port (int): Порт, на котором работает API.
            - app_host (str): Хост приложения.
            - message (str): Приветственное сообщение.
    """
    return {
        "status": "ok",
        "debug": settings.DEBUG,
        "model": settings.LLM_MODEL,
        "api_port": settings.APP_PORT,
        "app_host": settings.APP_HOST,
        "message": "Сервис готов к оценке ответов!"
    }