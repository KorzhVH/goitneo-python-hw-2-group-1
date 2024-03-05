from collections import UserDict
from error_manager import input_error

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        if name != '':
            super().__init__(name)
        else:
            raise ValueError


class Phone(Field):
    def __init__(self, phone):
        if 0 < len(phone) <= 10:
            super().__init__(phone)
        else:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    @input_error
    def add_phone(self, phone):
        self.phones.append(phone)
    @input_error
    def find_phone(self, phone):
        return self.phones[self.phones.index(phone)]
    @input_error
    def edit_phone(self, old_phone, new_phone):
        self.phones[self.phones.index(old_phone)] = new_phone
    @input_error
    def remove_phone(self, phone):
        return self.phones.pop(self.phones.index(phone))

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    @input_error
    def add_record(self, record):
        to_update = {record.name.__str__(): record}
        self.data.update(to_update)
        print(f'Contact {record.name} was added!')
    @input_error
    def find(self, name):
        return self.data[name]
    @input_error
    def delete(self, name):
        user = self.data.pop(name)
        return f'{user.name} was removed from your contacts!'


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


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
            name, *user_phones = args
            username = Name(name)
            user_record = Record(username)
            for i in user_phones:
                user_phone = Phone(i).__str__()
                user_record.add_phone(user_phone)
            book.add_record(user_record)

        elif command == "find":
            name = args[0]   # It always makes name a list, and I have no idea how to go around it without this. I NEED HELP!
            print(book.find(name))
        elif command == "delete":
            name = args[0]
            print(book.delete(name))
        elif command == "show_all":
            for name, record in book.data.items():
                print(record)

        elif command == "add_phone":
            name, phone = args
            user_record = book.find(name)
            phone_to_add = Phone(phone).__str__()
            user_record.add_phone(phone_to_add)
            print(user_record)
        elif command == "edit_phone":
            name, old_phone, new_phone = args
            user_record = book.find(name)
            phone1 = Phone(old_phone).__str__()
            phone2 = Phone(new_phone).__str__()
            user_record.edit_phone(phone1, phone2)
            print(user_record)
        elif command == "find_phone":
            name, phone = args
            user_record = book.find(name)
            phone_to_find = Phone(phone).__str__()
            phone_found = user_record.find_phone(phone_to_find)
            print(f'{user_record.name}: {phone_found}')

        elif command == "remove_phone":
            name, phone = args
            user_record = book.find(name)
            phone_to_delete = Phone(phone).__str__()
            user_record.remove_phone(phone_to_delete)
            print(user_record)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
