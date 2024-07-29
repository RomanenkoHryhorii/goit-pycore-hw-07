from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    def validate(self, phone):
        return len(phone) == 10 and phone.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.replace(year=today.year)
                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)
                days_until_birthday = (birthday - today).days
                if 0 <= days_until_birthday <= 7:
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday.strftime("%Y.%m.%d")
                    })
        return upcoming_birthdays

# Функція для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
    return inner

# Функції для роботи з адресною книгою
@input_error
def add_contact(args, book):
    name, phone = args
    if name in book.data:
        record = book.data[name]
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def phone_contact(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(p.value for p in record.phones)
    else:
        raise KeyError

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    elif record:
        return f"{name} doesn't have a birthday set."
    else:
        raise KeyError

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return "\n".join(f"{b['name']}: {b['birthday']}" for b in upcoming)
    else:
        return "No upcoming birthdays this week."

@input_error
def show_all(book):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts saved."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").lower().strip()
        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif user_input == "hello":
            print("How can I help you?")
        elif user_input.startswith("add "):
            _, *args = user_input.split(maxsplit=2)
            print(add_contact(args, book))
        elif user_input.startswith("change "):
            _, *args = user_input.split(maxsplit=3)
            print(change_contact(args, book))
        elif user_input.startswith("phone "):
            _, *args = user_input.split(maxsplit=1)
            print(phone_contact(args, book))
        elif user_input.startswith("add-birthday "):
            _, *args = user_input.split(maxsplit=2)
            print(add_birthday(args, book))
        elif user_input.startswith("show-birthday "):
            _, *args = user_input.split(maxsplit=1)
            print(show_birthday(args, book))
        elif user_input == "birthdays":
            print(birthdays(book))
        elif user_input == "all":
            print(show_all(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()