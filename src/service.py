from src.evaluator import evaluate_answer
from configs.utils import setup_logger


logger = setup_logger("service")


def process_evaluation(answer: str, subject: str):
    """
    Обрабатывает запрос на оценку ответа студента по заданному предмету.

    Функция выполняет предварительную валидацию входного текста (проверка на минимальную длину),
    логирует начало и завершение процесса, а затем вызывает основную функцию `evaluate_answer`
    для получения структурированной оценки от языковой модели. Используется как центральная точка
    обработки, объединяющая проверку, логирование и непосредственную оценку.

    Args:
        answer (str): Текст ответа студента, который необходимо оценить.
        subject (str): Предмет, по которому дан ответ (например, "Математика", "История").
                      Используется для формирования контекста оценки.

    Returns:
        dict: Словарь с результатом оценки. При успешной обработке содержит поля:
            - score (int): Оценка по шкале.
            - feedback (str): Текстовый комментарий учителя.
            - difficulty (str): Уровень сложности ("easy", "medium", "hard").
              В случае ошибки (например, слишком короткий ответ) возвращает словарь с ключом "error".
    """
    logger.info(f"Processing evaluation for subject: {subject}")

    if len(answer.strip()) < 10:
        return {"error": "Ответ слишком короткий"}

    result = evaluate_answer(answer, subject)
    logger.info("Evaluation completed")
    return result