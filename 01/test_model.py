"""Тесты для модуля model"""

import unittest
from unittest.mock import patch
from model import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    """Тесты для функции predict_message_mood."""

    @patch("model.SomeModel.predict")
    def test_bad_mood_message(self, predict_mock):
        """Тест неудовлетворительного настроения сообщения"""
        predict_mock.return_value = 0.27
        result = predict_message_mood("хорошо")
        self.assertEqual(result, "неуд")

    @patch("model.SomeModel.predict")
    def test_good_mood_message(self, predict_mock):
        """Тест отличного настроения сообщения."""
        predict_mock.return_value = 0.82
        self.assertEqual(predict_message_mood("хорошо1"), "отл")

    @patch("model.SomeModel.predict")
    def test_normal_mood_message(self, predict_mock):
        """Тест нормального настроения сообщения."""
        predict_mock.return_value = 0.61
        self.assertEqual(predict_message_mood("хорошо2"), "норм")

    @patch("model.SomeModel.predict")
    def test_normal_border_mood_message(self, predict_mock):
        """Тест пограничного нормального настроения"""
        predict_mock.return_value = 0.3
        self.assertEqual(predict_message_mood("хорошо3"), "норм")

    @patch("model.SomeModel.predict")
    def test_good_border_mood_message(self, predict_mock):
        """Тест пограничного нормального настроения"""
        predict_mock.return_value = 0.8
        self.assertEqual(predict_message_mood("хорошо3"), "норм")

    @patch("model.SomeModel.predict")
    def test_new_normal_mood_message(self, predict_mock):
        """Тест нормального настроения с новыми порогами"""
        predict_mock.return_value = 0.95
        self.assertEqual(
            predict_message_mood(
                "хорошо3", bad_thresholds=0.4, good_thresholds=0.95
            ),
            "норм",
        )

    @patch("model.SomeModel.predict")
    def test_new_bad_mood_message(self, predict_mock):
        """Тест неудовлетворительного настроения с новыми порогами"""
        predict_mock.return_value = 0.21
        self.assertEqual(
            predict_message_mood(
                "хорошо3", bad_thresholds=0.21, good_thresholds=0.78
            ),
            "норм",
        )


if __name__ == "__main__":
    unittest.main()
