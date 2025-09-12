import gradio as gr

from src.service import process_evaluation
from configs.config import settings


def evaluate_interface(answer, subject):
    """
    Обёртка для запуска процесса оценки ответа студента по заданному предмету.

    Эта функция служит интерфейсом между внешним вызовом (например, API или веб-формой)
    и внутренней логикой обработки. Она передаёт текст ответа и предмет в функцию `process_evaluation`
    и возвращает результат, извлекая его из словаря под ключом 'result'. В случае ошибки или отсутствия
    результата возвращает строку "Ошибка".

    Args:
        answer: Текстовый ответ студента, который необходимо оценить.
        subject: Предмет, по которому дан ответ (например, "Математика", "История").
                 Используется для выбора соответствующих критериев оценки.

    Returns:
        str: Результат оценки (например, JSON-строка с баллами и обратной связью) 
             или сообщение "Ошибка" при неудаче.
    """
    result = process_evaluation(answer, subject)
    return result.get("result", "Ошибка")


demo = gr.Interface(
    fn=evaluate_interface,
    inputs=[
        gr.Textbox(lines=5, placeholder="Введите ответ ученика..."),
        gr.Dropdown(["Математика", "История", "Литература"], label="Предмет")
    ],
    outputs="text",
    title="Auto Reviewer",
    description="Загрузите ответ — получите оценку и фидбэк от ИИ"
)


# Запуск: python gradio_app/gradio_app.py
if __name__ == "__main__":
    demo.launch(server_port=settings.GRADIO_PORT, server_name="0.0.0.0")