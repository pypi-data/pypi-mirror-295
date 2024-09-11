import csv
import os

class NameRecognizer:
    def __init__(self):
        # Поддерживаемые страны и их базы данных
        self.name_databases = {
            "RU": "names_ru.csv",
            # В будущем можно добавить другие страны
        }
    
    def _load_names(self, country_code):
        # Проверяем, поддерживается ли код страны
        if country_code not in self.name_databases:
            raise ValueError(f"Страна с кодом {country_code} не поддерживается.")
        
        # Получаем путь к CSV файлу для данной страны
        csv_filename = self.name_databases[country_code]
        csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
        
        name_dict = {}
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                name_detector = row['Имя-детектор'].strip().lower()
                input_name = row['Вводимое имя'].strip().lower()
                name_dict[name_detector] = input_name
        
        return name_dict

    def recognize_name(self, country_code: str, dirty_string: str) -> str:
        # Загружаем базу имен для указанной страны
        name_dict = self._load_names(country_code)
        
        # Приводим строку к нижнему регистру и убираем лишние символы
        cleaned_string = ''.join([c for c in dirty_string.lower() if c.isalnum() or c.isspace()]).strip()
        
        # Ищем совпадение с именем в словаре
        for name_detector, full_name in name_dict.items():
            if name_detector in cleaned_string:
                return full_name

        # Если имя не распознано, возвращаем сообщение
        return "Имя не распознано"
