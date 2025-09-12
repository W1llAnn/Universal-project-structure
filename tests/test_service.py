import pytest

from src.service import process_evaluation


def test_short_answer():
    """
    Тестирует обработку слишком короткого ответа.

    Проверяет, что функция `process_evaluation` корректно отклоняет ответы,
    длина которых меньше минимально допустимой (10 символов), и возвращает словарь с ключом "error".
    """
    result = process_evaluation("OK", "Математика")
    assert "error" in result


def test_long_answer():
    """
    Тестирует обработку длинного ответа.

    Проверяет, что функция `process_evaluation` принимает достаточно длинный текст,
    успешно передает его на оценку и возвращает результат, который либо содержит оценку,
    либо не помечен как ошибка (предполагая успешную обработку).
    """
    long_answer = "Я думаю, что теорема Пифагора важна, потому что..."
    result = process_evaluation(long_answer, "Математика")
    assert "result" in result or "error" not in result