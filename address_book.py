import os
import pickle 

from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from record import Record
from colorama import Fore, Style

class AddressBook(UserDict):
    """Клас для зберігання записів та керування ними."""
    
    def add_record(self, record: Record) -> None:
        """Додає запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Шукає запис за іменем."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за іменем."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

    def search(self, query: str) -> List[Record]:
        """Шукає збіги за частиною імені, телефону або нотаток."""
        query = query.lower()
        results = []
        for record in self.data.values():
            name_match = query in record.name.value.lower()
            phone_match = any(query in phone.value for phone in record.phones)
            notes_match = any(query in note.lower() for note in record.notes)
            
            if name_match or phone_match or notes_match:
                results.append(record)
        return results
    
    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        """Повертає список користувачів, яких потрібно привітати на наступному тижні."""
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            # Перевіряємо, чи у контакту взагалі вказано день народження
            if not record.birthday:
                continue
            
            # Беремо дату з нашого об'єкта Birthday (отримуємо чистий .date())
            birthday_date = record.birthday.date_object.date()
            
            # Визначаємо день народження в поточному році
            try:
                birthday_this_year = birthday_date.replace(year=today.year)
            except ValueError:
                # Обробка для 29 лютого, якщо поточний рік не високосний -> переносимо на 1 березня
                birthday_this_year = datetime(today.year, 3, 1).date()

            # Якщо день народження вже минув у цьому році, переносимо на наступний
            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday_date.replace(year=today.year + 1)
                except ValueError:
                    # Обробка для 29 лютого, якщо наступний рік не високосний -> переносимо на 1 березня
                    birthday_this_year = datetime(today.year + 1, 3, 1).date()

            # Перевіряємо, чи дата народження потрапляє в інтервал наступних 7 днів
            if today <= birthday_this_year <= end_date:
                congratulation_date = birthday_this_year
                
                # Якщо день народження випадає на суботу (5) або неділю (6), переносимо на понеділок
                if congratulation_date.weekday() in (5, 6):
                    days_until_monday = 7 - congratulation_date.weekday()
                    congratulation_date += timedelta(days=days_until_monday)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y") # Формат DD.MM.YYYY для уніфікації
                })

        return upcoming_birthdays
    
    # --- Красиве виведення у вигляді таблиці ---
    def get_table_view(self, records_list: Optional[List[Record]] = None) -> str:
        """Повертає кольорову текстову таблицю списку контактів."""
        target_records = records_list if records_list is not None else list(self.data.values())
        if not target_records:
            return f"{Fore.YELLOW}Address book is empty / No records to display."


        # Обов'язково перевірте, щоб тут було написано назву header_text:
        header_text = f"{'Name':<12} | {'Phones':<23} | {'Birthday':<10} | {'Email':<20} | {'Address':<20} | {'Notes':<15}"
        separator = "-" * len(header_text)
        
        
        # Тепер ця змінна буде успішно знайдена Python:
        header = f"{Fore.CYAN}{Style.BRIGHT}{header_text}"
        lines = [separator, header, separator]

        for index, r in enumerate(target_records):
            phones = ", ".join(p.value for p in r.phones) or "None"
            birthday = r.birthday.value if r.birthday else "None"
            email = r.email.value if r.email else "None"
            address = r.address.value if r.address else "None"
            notes = "; ".join(r.notes) or "None"

            # Обрізаємо занадто довгі значення для збереження структури таблиці
            row_text = (
                f"{r.name.value[:12]:<12} | {phones[:23]:<23} | {birthday:<10} | "
                f"{email[:20]:<20} | {address[:20]:<20} | {notes[:15]:<15}"
            )

            # Якщо індекс парний — жовтий колір, якщо непарний — звичайний білий
            if index % 2 == 0:
                lines.append(f"{Fore.YELLOW}{row_text}")
            else:
                lines.append(f"{Fore.WHITE}{row_text}")
        
        lines.append(separator)
        return "\n".join(lines)

    # --- Керування збереженням у будь-яку папку ---
    def save_to_file(self, folder_path: str, filename: str = "addressbook.pkl") -> str:
        """Зберігає копію адресної книги у вказану папку."""
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "wb") as file:
                pickle.dump(self, file)
            return f"Data successfully saved to: {full_path}"
        except Exception as e:
            return f"Error while saving data: {e}"

    @classmethod
    def load_from_file(cls, filename: str = "addressbook.pkl") -> "AddressBook":
        """Автоматично завантажує базу з поточної папки при запуску програми."""
        try:
            with open(filename, "rb") as file:
                print(f"Data successfully restored from local {filename}.")
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("No local saved data found. Starting with an empty address book.")
            return cls()

    