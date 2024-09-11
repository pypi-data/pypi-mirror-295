import unittest
from name_recognize.name_recognizer import NameRecognizer

class TestNameRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = NameRecognizer()

    def test_known_name_ru(self):
        self.assertEqual(self.recognizer.recognize_name("RU", "Настя"), "анастасия")
        self.assertEqual(self.recognizer.recognize_name("RU", "Саша"), "александр")

    def test_unknown_name(self):
        self.assertEqual(self.recognizer.recognize_name("RU", "Марс"), "Имя не распознано")

    def test_invalid_country_code(self):
        with self.assertRaises(ValueError):
            self.recognizer.recognize_name("US", "John")

if __name__ == '__main__':
    unittest.main()
