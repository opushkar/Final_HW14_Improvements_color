from typing import List, Optional
from fields import Name, Phone, Birthday, Email, Address

class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.notes: List[str] = []  # Список текстових нотаток/тегів

    def add_birthday(self, birthday_date: str) -> None:
        """Додає або перезаписує день народження контакту."""
        self.birthday = Birthday(birthday_date)

    def add_phone(self, phone_number: str) -> None:
        if self.find_phone(phone_number):
            print(f"Phone {phone_number} already exists.")
            return
        self.phones.append(Phone(phone_number))

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """Замінює старий номер телефону на новий."""
        phone_to_edit = self.find_phone(old_number)
        if not phone_to_edit:
            raise ValueError(f"Phone {old_number} not found.")
        
        # Створюємо новий об'єкт Phone для валідації 10 цифр перед заміною
        new_phone = Phone(new_number)
        phone_to_edit.value = new_phone.value

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    # --- Нові поля та нотатки (Фінал) ---
    def add_birthday(self, birthday_date: str) -> None:
        self.birthday = Birthday(birthday_date)

    def add_email(self, email_address: str) -> None:
        self.email = Email(email_address)

    def add_address(self, physical_address: str) -> None:
        self.address = Address(physical_address)

    def add_note(self, text: str) -> None:
        """Додає нову замітку або тег."""
        if text.strip():
            self.notes.append(text.strip())

    def clear_notes(self) -> None:
        """Видаляє всі нотатки контакту."""
        self.notes.clear()

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones) or 'None'
        birthday_str = self.birthday.value if self.birthday else "None"
        email_str = self.email.value if self.email else "None"
        address_str = self.address.value if self.address else "None"
        notes_str = ' | '.join(self.notes) or 'None'
        
        return (f"Contact: {self.name.value} | Phones: {phones_str} | "
                f"Birthday: {birthday_str} | Email: {email_str} | "
                f"Address: {address_str} | Notes: {notes_str}")





    #def __str__(self) -> str:
    #    phones_str = '; '.join(p.value for p in self.phones)
    #    birthday_str = self.birthday.value if self.birthday else "Not specified"
    #    return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"
