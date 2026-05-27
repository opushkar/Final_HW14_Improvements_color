import os
from typing import List, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox

from address_book import AddressBook
from record import Record
from errors import input_error


FILENAME = "addressbook.pkl"
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Папка проекту для збереження за замовчуванням


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Розбирає введення користувача на команду та аргументи."""
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def show_birthdays(book: AddressBook) -> str:
    """Виводить список найближчих днів народження."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    
    result = "Upcoming birthdays for the next week:\n"
    for user in upcoming:
        result += f"🎂 {user['name']}: Congratulate on {user['congratulation_date']}\n"
    return result.strip()

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    """Додає контакт або новий телефон до контакту."""
    if len(args) < 2:
        raise ValueError("Enter user name and phone number.")
    name, phone = args[0], args[1]
    
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact '{name}' added with phone {phone}."
    else:
        message = f"Phone {phone} added to contact '{name}'."
        
    record.add_phone(phone)
    
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return message

@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    """Замінює старий номер телефону на новий."""
    if len(args) < 3:
        raise ValueError("Enter user name, old phone, and new phone.")
    name, old_phone, new_phone = args[0], args[1], args[2]
    
    record = book.find(name)
    if record is None:
        raise KeyError(name)
        
    record.edit_phone(old_phone, new_phone)
    
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Phone number updated for contact '{name}'."

@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    """Показує всі номери телефонів для контакту."""
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0]
    
    record = book.find(name)
    if record is None:
        raise KeyError(name)
        
    if not record.phones:
        return f"Contact '{name}' has no phone numbers saved."
        
    # Збираємо лише номери через кому
    phones_str = '; '.join(p.value for p in record.phones)
    return f"{name}'s phones: {phones_str}"

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    """Додає день народження до контакту."""
    if len(args) < 2:
        raise ValueError("Enter user name and birthday date (DD.MM.YYYY).")
    name, birthday = args[0], args[1]
    
    record = book.find(name)
    if record is None:
        raise KeyError(name)
        
    record.add_birthday(birthday)
    
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Birthday added for contact '{name}'."

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    """Показує дату народження для вказаного контакту."""
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0]
    
    record = book.find(name)
    if record is None:
        raise KeyError(name)
        
    if record.birthday:
        return f"Contact '{name}' birthday: {record.birthday.value}"
    return f"Contact '{name}' does not have a birthday specified."

@input_error
def add_email(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Enter user name and email.")
    name, email = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.add_email(email)
    
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Email '{email}' added to contact '{name}'."

@input_error
def add_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Enter user name and address.")
    name = args[0]
    address_text = " ".join(args[1:])  # Адреса може містити пробіли
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.add_address(address_text)
    
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Address added to contact '{name}'."

@input_error
def add_note(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Enter user name and note text/tag.")
    name = args[0]
    note_text = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.add_note(note_text)
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Note added to contact '{name}'."

@input_error
def search_contacts(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Enter search query.")
    query = args[0]
    found = book.search(query)
    return book.get_table_view(found)


@input_error
def delete_contact(args: List[str], book: AddressBook) -> str:
    """Повністю видаляє контакт із книги."""
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0]
    book.delete(name)
    book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    return f"Contact '{name}' successfully deleted."

def show_all(book: AddressBook) -> str:
    """Виводить на екран усі записи в адресній книзі."""
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())

def main() -> None:
    # При запуску автозавантаження шукає файл у поточній папці проекту
    book = AddressBook.load_from_file(FILENAME)

    print("\nWelcome to the Final Assistant Bot!")
    
    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            # Автозбереження у папку проекту перед виходом
            book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
            
             # ІМПРУВМЕНТ: Запит y/n через графічне вікно Windows після закриття
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            
            # Показуємо стандартне вікно запиту Так/Ні
            choice = messagebox.askyesno(
                title="Save backup", 
                message="База збережена локально. Бажаєте додатково зберегти копію файлу на комп'ютері?"
            )
            
            if choice:  # Якщо користувач обрав 'Yes' (Y)
                selected_folder = filedialog.askdirectory(title="Оберіть репозиторій/папку для збереження копії")
                if selected_folder:
                    print(book.save_to_file(selected_folder, FILENAME))
                else:
                    print("Saving backup cancelled. No folder was selected.")
            
            root.destroy()
            print("Good bye!")
            break
        
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":  
            print(show_phone(args, book))
        elif command == "add-birthday":  
            print(add_birthday(args, book))
        elif command == "show-birthday": 
            print(show_birthday(args, book))
        elif command == "birthdays":  
            print(show_birthdays(book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "add-note":
            print(add_note(args, book))
        elif command == "search":
            print(search_contacts(args, book))
        elif command == "all":
            print(book.get_table_view())
        elif command == "delete":  
            print(delete_contact(args, book))
        elif command == "":
            continue
        else:
            print("Unknown command. Use add, change, phone, add-birthday, show-birthday, birthdays, add-email, add-address, add-note, search, all, delete, exit.")
        
if __name__ == "__main__":
    main()
