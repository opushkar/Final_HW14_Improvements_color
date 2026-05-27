import re
from datetime import datetime


class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not self._validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    def _validate(self, value: str) -> bool:
        return bool(re.match(r"^\d{10}$", value))


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""
    def __init__(self, value: str) -> None:
        try:
            # Перевірка коректності дати та конвертація в об'єкт datetime
            self.date_object: datetime = datetime.strptime(value, "%d.%m.%Y")
            # Зберігаємо у початковому текстовому форматі для сумісності з Field
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Email(Field):
    """Клас для Email з валідацією формату."""
    def __init__(self, value: str) -> None:
        if not self._validate(value):
            raise ValueError("Invalid email format. Example: user@example.com")
        super().__init__(value)

    def _validate(self, value: str) -> bool:
        # Простий та надійний регулярний вираз для валідації пошти
        pattern = r"^[a-zA-Z0-8_.+-]+@[a-zA-Z0-8-]+\.[a-zA-Z0-8-.]+$"
        return bool(re.match(pattern, value))


class Address(Field):
    """Клас для зберігання фізичної адреси контакту."""
    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())