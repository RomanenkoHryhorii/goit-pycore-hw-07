# Функція для розбору введеної користувачем команди
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Декоратор для обробки помилок введення
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

# Функція для зміни номера телефону контакту
@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."
    else:
        raise KeyError("Contact not found.")

# Функція для відображення номера телефону контакту
@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter the name please.")
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(p.value for p in record.phones)
    else:
        raise KeyError("Contact not found.")

# Функція для відображення всіх контактів
@input_error
def show_all(book):
    if book.data:
        return '\n'.join(str(record) for record in book.data.values())
    else:
        return "No contacts saved."

# Функція для додавання дня народження контакту
@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError("Contact not found.")

# Функція для відображення дня народження контакту
@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter the name please.")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return f"{name} doesn't have a birthday set."
    else:
        raise KeyError("Contact not found.")

# Функція для відображення найближчих днів народження
@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return '\n'.join(f"{b['name']}: {b['birthday']}" for b in upcoming)
    else:
        return "No upcoming birthdays this week."

# Головна функція програми
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
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

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

# Точка входу в програму
if __name__ == "__main__":
    main()