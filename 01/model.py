"""Модуль редсказания модели"""


class SomeModel:
    # pylint: disable=too-few-public-methods
    """Класс модели"""

    def predict(self, message: str) -> float:
        """Делает предсказание модели"""
        word_count = len(message.split())
        return min(1.0, word_count / 10.0)


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """Определяет настроение сообщения по оценке."""
    model = SomeModel()
    result = model.predict(message)

    if result < bad_thresholds:
        return "неуд"
    if result > good_thresholds:
        return "отл"
    return "норм"
