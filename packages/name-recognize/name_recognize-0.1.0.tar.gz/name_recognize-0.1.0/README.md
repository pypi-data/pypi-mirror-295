# Name Recognize

**Name Recognize** — это библиотека для распознавания и нормализации русских имен с поддержкой выбора страны. Она использует таблицу соответствий форм имен для получения правильного полного имени.

## Установка

Для установки библиотеки локально:

```bash
pip install name_recognize
```
## Пример использования
```python
from name_recognize import NameRecognizer

# Создание экземпляра класса
recognizer = NameRecognizer()

# Распознавание имени для России (код страны: "RU")
name = recognizer.recognize_name("RU", "Настя")
print(name)  # Вывод: анастасия
```

## Функции
### recognize_name(country_code: str, dirty_string: str) -> str
*Описание: Функция принимает код страны и "грязную" строку, содержащую имя. Она возвращает нормализованное имя или сообщение, что имя не распознано.*

**Параметры:**
```

country_code (строка): Код страны (например, "RU" для России).
dirty_string (строка): "Грязная" строка с именем.
Возвращаемое значение:

Чистое, нормализованное имя (строка).
Если имя не распознано, возвращается строка: "Имя не распознано".
```

**Структура проекта**
```
name_recognize/
│
├── name_recognize/
│   ├── __init__.py
│   ├── name_recognizer.py
│   ├── names_ru.csv
│
├── setup.py
├── README.md
├── tests/
│   ├── test_name_recognizer.py
```
## Тестирование

### Для запуска тестов:

```bash
python -m unittest discover
```