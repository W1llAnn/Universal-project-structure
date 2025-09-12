import openai

from configs.prompts import AUTO_EVALUATION_PROMPT
from configs.config import settings
from configs.schemas import EvaluationResult


# Получаем JSON Schema из модели
# Это автоматически генерирует стандарт JSON Schema, понятный LLM
json_schema = EvaluationResult.model_json_schema()


def evaluate_answer(answer: str, subject: str) -> dict:
    """
    Оценивает текстовый ответ ученика с помощью LLM с использованием структурированного вывода (Structured Outputs).

    Функция отправляет ответ студента и предмет в языковую модель через OpenAI-совместимый API (например, vLLM),
    используя параметр `guided_json` для принудительной генерации ответа в формате, соответствующем схеме `EvaluationResult`.
    Это гарантирует получение валидного JSON без необходимости ручной очистки или парсинга.

    Args:
        answer (str): Текст ответа ученика, который необходимо оценить.
        subject (str): Предмет, по которому дан ответ (например, "Математика", "История").

    Returns:
        dict: Результат оценки в виде словаря. При успехе содержит поля:
            - score (int): Оценка по шкале (например, от 1 до 5).
            - feedback (str): Текстовый комментарий учителя.
            - difficulty (str): Уровень сложности ("easy", "medium", "hard").
              В случае ошибки возвращает словарь с ключом "error" и деталями проблемы.
    """

#    Преимущества:
#      - Гарантированно валидный JSON
#      - Нет ошибок парсинга
#      - Чёткая структура ответа
#      - Работает с vLLM, если запущен OpenAI-совместимый сервер
#
#    Требования:
#      - vLLM должен быть запущен с поддержкой guided decoding (xgrammar или outlines)
#      - Модель должна быть способна следовать схеме
#
#    Документация vLLM:
#        https://docs.vllm.ai/en/v0.8.5.post1/features/structured_outputs.html

    prompt = AUTO_EVALUATION_PROMPT.format(subject=subject)
    full_prompt = prompt + "\n\nОтвет ученика:\n" + answer

    client = openai.OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.VLLM_BASE_URL  # Например: "http://localhost:8000/v1"
    )

    try:
        # Отправляем запрос с указанием guided_json
        # vLLM использует эту схему, чтобы "направлять" генерацию
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — строгий учитель. Отвечай ТОЛЬКО в формате JSON, "
                        "соответствующем указанной схеме. Не добавляй пояснений."
                    )
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.3,
            max_tokens=300,
            # Ключевой параметр: принудительный JSON по схеме
            extra_body={
                "guided_json": json_schema  # Гарантирует вывод по схеме EvaluationResult
                # Другие опции (альтернативы):
                # "guided_choice": ["positive", "negative"]
                # "guided_regex": r'\d+/5'
                # "guided_grammar": <your_ebnf_grammar>
            }
        )

        raw_result = response.choices[0].message.content.strip()

        # В идеале — это уже валидный JSON, но всё равно оборачиваем в try
        try:
            from pydantic import TypeAdapter
            # Парсим и валидируем результат как объект EvaluationResult
            result = TypeAdapter(EvaluationResult).validate_json(raw_result)
            return result.model_dump()  # Возвращаем словарь
        except Exception as parse_error:
            return {
                "error": "Failed to parse structured output",
                "raw_response": raw_result,
                "parse_error": str(parse_error)
            }

    except Exception as e:
        return {"error": f"LLM request failed: {str(e)}"}