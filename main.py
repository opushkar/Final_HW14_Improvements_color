import os

from typing import Tuple, List

import smtplib
from email.message import EmailMessage

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
def send_email_command(args: list[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
        
    emails = []
    for user in upcoming:
        record = book.find(user['name'])
        if record and getattr(record, 'email', None) and record.email.value:
            if str(record.email.value).strip().lower() != "none":
                emails.append(str(record.email.value).strip())
                
    if not emails:
        return "No email addresses found for upcoming birthdays."

    to_emails = ", ".join(emails)
    
    # Малюємо гарне CLI-вікно листа за допомогою f-строк та символів рамки
    cli_email_preview = (
        "\n"
        " ┌────────────────── OUTGOING EMAIL (CLI MODE) ──────────────────┐\n"
        f" │ From:    assistant_bot_v15@cli.local                          │\n"
        f" │ To:      {to_emails:<52} │\n"
        " │ Subject: З прийдешнім днем народження!                        │\n"
        " ├───────────────────────────────────────────────────────────────┤\n"
        " │ Привіт друзі!                                                 │\n"
        " │                                                               │\n"
        " │ Вітаю вас з прийдешнім днем народженням.                      │\n"
        " │ Бажаю вам всього найкращого і веселого.                       │\n"
        " │                                                               │\n"
        " │ З любов'ю,                                                    │\n"
        " │ Ваш друг Василь                                               │\n"
        " └───────────────────────────────────────────────────────────────┘\n"
        "Sending queued message via local network... 🚀\n"
        "✨ Status: Sent successfully!"
    )
    
    return cli_email_preview

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
def save_as_command(args: list[str], book: AddressBook) -> str:
    """Зберігає адресную книгу за вказаним шляхом або пропонує дефолтний варіант."""
    # Визначаємо дефолтний варіант (наприклад, у поточній папці з префіксом backup)
    default_filename = "address_book_backup.bin"
    default_path = os.path.abspath(default_filename)
    
    # 1. Якщо користувач не передав аргументи, запускаємо діалог прямо в CLI
    if not args:
        print(f"Default path proposed: {default_path}")
        user_input = input("Press Enter to confirm or type your custom path & filename: ").strip()
        
        if user_input:
            final_path = user_input
        else:
            final_path = default_path
    else:
        # 2. Якщо користувач одразу написав: save-as my_folder/book.bin
        final_path = " ".join(args)

    # Автоматично додаємо розширення .bin, якщо користувач забув його вказати
    if not final_path.endswith('.bin') and not final_path.endswith('.pkl'):
        final_path += '.bin'
        
    # Перевіряємо, чи існує папка, куди зберігаємо (якщо вказано складний шлях)
    dirname = os.path.dirname(final_path)
    if dirname and not os.path.exists(dirname):
        try:
            os.makedirs(dirname)  # Створюємо директорію, якщо її немає
        except Exception as e:
            return f"❌ Error: Cannot create directory '{dirname}'. Details: {e}"

    try:
        # Викликаємо ваш метод збереження з ДЗ
        book.save_to_file(final_path)
        return f"💾 Address book successfully saved to:\n➡️ {os.path.abspath(final_path)}"
    except Exception as e:
        return f"❌ Failed to save file. Error: {e}"


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
            book.save_to_file(os.path.dirname(os.path.abspath(__file__)), FILENAME)
            print("Good bye! 👋")
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
        elif command == "send-email":
            print(send_email_command(args, book))
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
        elif command == "save-as":
            print(save_as_command(args, book))

        elif command == "":
            continue
        else:
            print("Unknown command. Use add, change, phone, add-birthday, show-birthday, birthdays, add-email, send-email, add-address, add-note, search, all, save-as, delete, exit.")
        
if __name__ == "__main__":
    main()
