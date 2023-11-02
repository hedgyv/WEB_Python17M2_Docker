from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re
import difflib
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from abc import ABC, abstractmethod




class ConsoleApplication(ABC):
    def __init__(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.process_user_input()

    @abstractmethod
    def process_user_input(self):
        pass

    def quit(self):
        self.running = False




###Field Based On Field
class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    # Ініціалізація об'єкта Name
    def __init__(self, value):
        self._value = value
        super().__init__(value)#test

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Phone(Field):
    # Ініціалізація об'єкта Phone
    def __init__(self, value):
        self._value = None
        super().__init__(value)

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.match(r'^(\+380\d{9}|0\d{9})$', value):
            self._value = value
        else:
            print("Incorrect phone number format, should be +380638108709 or 0638708106.")


class Email(Field):
    # Ініціалізація об'єкта Email
    def __init__(self, value):
        self._value = None
        super().__init__(value)

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            self._value = value
        else:
            print("Invalid email format.")


class Address(Field):
    # Ініціалізація об'єкта Address
    def __init__(self, value):
        self._value = value
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


class Birthday(Field):
    # Ініціалізація об'єкта Birthday
    def __init__(self, value):
        self._value = None
        super().__init__(value)

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Валідація формату дати
        if re.match(r"\d{2}\.\d{2}\.\d{4}$", value):
            try:
                datetime.strptime(value, "%d.%m.%Y")
                self._value = value
            except ValueError:
                print("Incorrect birthday format, should be DD.MM.YYYY.")
        else:
            print("Incorrect birthday format, should be DD.MM.YYYY.")

###Field Based On Field


class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = ''

    def __str__(self):
        # Перетворення об'єкта контакту в рядок
        phones_str = '; '.join(str(p) for p in self.phones)
        emails_str = '; '.join(str(e) for e in self.emails)
        addresses_str = '; '.join(str(a) for a in self.addresses)

        return f"Contact name: {self.name.value}" + \
            (f", phones: {phones_str}" if len(phones_str) > 0 else "") + \
            (f", emails: {emails_str}" if len(emails_str) > 0 else "") + \
            (f", addresses: {addresses_str}" if len(addresses_str) > 0 else "") + \
            (f", birthday: {self.birthday}" if self.birthday != '' else "")


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except(KeyError, ValueError, IndexError):
            print("Invalid input. Please try again")
        except FileNotFoundError:
            print("File isn't found. Specify the file.")
    return wrapper


class AddressBook(UserDict):
    
    def add_contact(self, text):
        # Додавання контакту
        if len(text) >= 2:
            new_contact = Record(text.title())
            if new_contact.name.value not in list(self.data.keys()):
                self.data[new_contact.name.value] = new_contact
                print(f'Contact {text.title()} added to AddressBook!')
            else:
                print(f'Contact {new_contact.name.value} is already in AddressBook')
        else:
            print("Name of contact is not correct!")
    
    def add_phone_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і номера телефону
        # Якщо після введеня імені не буде вказаний номер телефону то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        phone_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(phone_to_add) >= 1:
            for key, value in self.data.items():
                if key == name_input:
                    if phone_to_add not in list(i.value.lower() for i in self.data[name_input].phones):
                        phone_to_add_new = Phone(phone_to_add)
                        if phone_to_add_new.value is not None:
                            self.data[name_input].phones.append(phone_to_add_new)
                            return print(f'Phone{phone_to_add_new.value} is added for {name_input}')
                        else:
                            return
                    else:
                        return print(f"This phone is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(phone_to_add) == 0:
            print("No phone number!")

    def add_email_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і мейлу
        # Якщо після введеня імені не буде вказаний мейл то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        email_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(email_to_add) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    if email_to_add not in list(i.value.lower() for i in self.data[name_input].emails):
                        email_to_add_new = Email(email_to_add)
                        if email_to_add_new.value is not None:
                            print(f'Email for {name_input} is added!')
                            return self.data[name_input].emails.append(email_to_add_new)
                        else:
                            return
                    else:
                        return print(f"This email is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(email_to_add) == 0:
            print("No email!")

    def add_address_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і адреси
        # Якщо після введеня імені не буде вказана адреса то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        address_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(address_to_add) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    if address_to_add not in list(i.value.lower() for i in self.data[name_input].addresses):
                        print(f'Address for {name_input} is added!')
                        return self.data[name_input].addresses.append(Address(address_to_add))
                    else:
                        return print(f"This address is already entered for this addressbook!")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(address_to_add) == 0:
            print("No address!")

    def add_birthday_to_contact(self, text):
        # Звернення йде шляхом вводу імені контакту і дня народження
        # Якщо після введеня імені не буде вказаний день народження то вийде відповідне повідомлення.
        name_input = text.split(" ")[0].title()
        birthday_to_add = text.removeprefix(name_input.lower()).strip()
        if len(name_input) >= 2 and len(birthday_to_add) == 10:
            for key, value in self.data.items():
                if key == name_input:
                    birthday_to_add_new = Birthday(birthday_to_add)
                    if birthday_to_add_new.value is not None:
                        self.data[name_input].birthday = birthday_to_add_new
                        print(f'Birthday for {name_input} is added!')
                        return
                    else:
                        return
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(birthday_to_add) == 0:
            print("No birthday date!")
        else:
            print("Incorrect birthday format, should be DD.MM.YYYY.")

    def birthday_in(self, days):
        result = []
        date_to_search = datetime.now().date() + timedelta(days=int(days))
        current_year = date_to_search.year
        date_to_search = date_to_search.strftime("%d.%m.%Y")
        for record in self.data.values():
            if record.birthday == '':
                continue
            else:
                edited_birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")\
                                        .replace(year=current_year).date().strftime("%d.%m.%Y")
                if edited_birthday == date_to_search:
                    result.append(record)

        for contact in result:
            print(contact)

    def find_contact_by_name(self, contact_name):  # Пошук контакту
        for key, value in self.data.items():
            if contact_name.title() == key:
                return print(value)

    def search_matches_in_addressbook(self, match):  # Шукаємо збіги в адресній книзі
        found_matches = []

        for name, contact in self.data.items():
            list_of_phones = list(i.value.lower() for i in self.data[name].phones)
            list_of_emails = list(i.value.lower() for i in self.data[name].emails)
            list_of_addresses = list(i.value.lower() for i in self.data[name].addresses)

            if any(match in phone for phone in list_of_phones)\
                    or any(match in email for email in list_of_emails)\
                    or any(match in address for address in list_of_addresses)\
                    or match in contact.birthday.value:
                if contact not in found_matches:
                    found_matches.append(contact)

        for contact in found_matches:
            print(f"{contact}")

    @input_error
    def edit_phone(self, text):
        name_input = text.split(" ")[0].title()
        phone_old = text.split(" ")[1]
        phone_new = text.split(" ")[2]
        if len(name_input) >= 2 and len(phone_old) >= 1 and len(phone_new) >= 1:
            for key, value in self.data.items():
                if key == name_input:
                    list_of_phones = list(i.value.lower() for i in self.data[name_input].phones)
                    for phone in list_of_phones:
                        if phone == phone_old:
                            index = list_of_phones.index(phone)
                            self.data[name_input].phones[index].value = phone_new
                            print(f'Phone for {name_input} is edited!')
                            return
                    return print(f"Phone number '{phone_old}' wasn't found")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(phone_old) == 0:
            print("No old phone number!")
        elif len(phone_new) == 0:
            print("No new phone number!")

    @input_error
    def edit_email(self, text):
        name_input = text.split(" ")[0].title()
        email_old = text.split(" ")[1]
        email_new = text.split(" ")[2]
        if len(name_input) >= 2 and len(email_old) >= 5 and len(email_new) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    list_of_emails = list(i.value.lower() for i in self.data[name_input].emails)
                    for email in list_of_emails:
                        if email == email_old:
                            index = list_of_emails.index(email)
                            self.data[name_input].emails[index].value = email_new
                            print(f'Email for {name_input} is edited!')
                            return
                    return print(f"Email '{email_old}' wasn't found")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(email_old) == 0:
            print("No old email!")
        elif len(email_new) == 0:
            print("No new email!")

    @input_error
    def edit_address(self, text):
        name_input = text.split(" ")[0].title()
        print(name_input)
        address_old = text.removeprefix(name_input.lower()+' ').split(" -")[0]
        print(address_old)
        address_new = text.split("- ")[1]
        print(address_new)
        if len(name_input) >= 2 and len(address_old) >= 5 and len(address_new) >= 5:
            for key, value in self.data.items():
                if key == name_input:
                    list_of_addresses = list(i.value.lower() for i in self.data[name_input].addresses)
                    for address in list_of_addresses:
                        if address == address_old:
                            index = list_of_addresses.index(address)
                            self.data[name_input].addresses[index].value = address_new
                            print(f'Address for {name_input} is edited!')
                            return
                    return print(f"Address '{address_old}' wasn't found")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(address_old) == 0:
            print("No one old address!")
        elif len(address_new) == 0:
            print("No one new address!")

    def delete_contact(self, contact):
        if len(contact) >= 1:
            for key, value in self.data.items():
                if key == contact.title():
                    print(f'User {key} has been deleted from the AddressBook')
                    return self.data.pop(contact.title())
            return print(f"{contact} was not found in AddressBook")
        else:
            print("Enter name of contact to delete")

    def delete_phone(self, text):
        try:
            name_input = text.split(" ")[0].title()
            phone_to_delete = text.split(" ")[1]
            if len(name_input) >= 1 and len(phone_to_delete) >= 1:
                for key, value in self.data.items():
                    if key == name_input:
                        list_of_phones = list(i.value.lower() for i in self.data[name_input].phones)
                        for phone in list_of_phones:
                            if phone == phone_to_delete:
                                index = list_of_phones.index(phone)
                                del self.data[name_input].phones[index]
                                print(f'Phone for {name_input} is deleted!')
                                return
                        return print(f"Phone number '{phone_to_delete}' wasn't found")
                return print(f"{name_input} was not found in addressbook")
            elif len(name_input) == 0:
                print("Enter name of contact!")
            elif len(phone_to_delete) == 0:
                print("No new phone number!")
        except IndexError:
            print(f"You didn't enter a value!")

    def delete_email(self, text):
        try:
            name_input = text.split(" ")[0].title()
            email_to_delete = text.split(" ")[1]
            if len(name_input) >= 1 and len(email_to_delete) >= 1:
                for key, value in self.data.items():
                    if key == name_input:
                        list_of_emails = list(i.value.lower() for i in self.data[name_input].emails)
                        for email in list_of_emails:
                            if email == email_to_delete:
                                index = list_of_emails.index(email)
                                del self.data[name_input].emails[index]
                                print(f'Email for {name_input} is deleted!')
                                return
                        return print(f"Phone number '{email_to_delete}' wasn't found")
                return print(f"{name_input} was not found in addressbook")
            elif len(name_input) == 0:
                print("Enter name of contact!")
            elif len(email_to_delete) == 0:
                print("No one email!")
        except IndexError:
            print(f"You didn't enter a value!")

    def delete_address(self, text):
        name_input = text.split(" ")[0].title()
        address_to_delete = text.split(" ")[1]
        if len(name_input) >= 1 and len(address_to_delete) >= 1:
            for key, value in self.data.items():
                if key == name_input:
                    list_of_addresses = list(i.value.lower() for i in self.data[name_input].addresses)
                    for address in list_of_addresses:
                        if address == address_to_delete:
                            index = list_of_addresses.index(address)
                            del self.data[name_input].addresses[index]
                            print(f'Address for {name_input} is deleted!')
                            return
                    return print(f"Address '{address_to_delete}' wasn't found")
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
        elif len(address_to_delete) == 0:
            print("No one address!")

    def delete_birthday(self, text):
        name_input = text.split(" ")[0].title()
        if len(name_input) >= 1:
            for key, value in self.data.items():
                if key == name_input:
                    self.data[name_input].birthday = None
                    print(f'Birthday for {name_input} is deleted!')
                    return
            return print(f"{name_input} was not found in addressbook")
        elif len(name_input) == 0:
            print("Enter name of contact!")
            
    def save_addressbook(self):
        with open("addressbook.bin", "wb") as f:
            pickle.dump(self.data, f)
            print(f'AddressBook saved!')

    def load_addressbook(self, file):
        with open(file, "rb") as f:
            self.data = pickle.load(f)

    def show_addressbook(self):
        for name, contact in self.data.items():
            print(f"{contact}")


class NoteBook(UserDict):
    # Потрібно для створення унікального неймінгу кожної нотатки
    def __init__(self):
        super().__init__()
        self.__id = 1

    def add_note(self, notes):
        # Додавання нотатки в записник
        if len(notes) >= 1:
            self.data[f"note-{self.__id}"] = Notes(notes)
            print(f'Note is added with title note-{self.__id}')
            self.__id += 1
        else:
            print("Note is empty!")
    
    def search_notes(self, search_match):
        if len(search_match) >= 1:
            # print(self.data['note-1'])
            res = ""
            for key, value in self.data.items():
                # print(type(str(value)))
                # print(str(value))
                if search_match in str(value):
                    res += str(value) + " "
                    print(f'Note "{search_match}" in {key} "{(str(value).split(" ")[0][0].upper() + str(value).split(" ")[0][1:] + str(value)[len(str(value).split(" ")[0]):])}" was found')
    
    def search_notes_by_tag(self, tag):
        found_notes = []
        for name, note in self.data.items():
            if tag in note.tags:
                found_notes.append((name, note))

        found_notes = sorted(found_notes, key=lambda x: x[1].note.split()[0].lower())
        if found_notes:
            print("Notes found:")
            for name, note in found_notes:
                print(f"{name}: {note}")
        else:
            print("No notes found for the tag.")
        return found_notes

    def add_tag(self, text):
        # Звернення йде шляхом вводу імені нотатки і введення тегу для цієї нотатки.
        # Якщо після введеня імені нотатки не буде вказаний тег, функція поверне відповідне повідомлення.
        name_of_note = text.split(" ")[0]
        tag_to_add = text.removeprefix(name_of_note).strip()
        if len(name_of_note) >= 1 and len(tag_to_add) >= 1:
            for key, value in self.data.items():
                if key == name_of_note:
                    if tag_to_add not in self.data[name_of_note].tags:
                        print(f'Tag for {key} is added')
                        return self.data[name_of_note].tags.append(tag_to_add)
                    else:
                        print(f"This tag is already entered for this note!")
            return print(f"{name_of_note} was not found in NoteBook")
        elif len(name_of_note) == 0:
            print("Enter name of note to add tag!")
        elif len(tag_to_add) == 0:
            print("Tag is empty!")

    def edit_note(self, text):
        name_of_note = text.split(" ")[0]
        new_note_text = text.removeprefix(name_of_note).strip()
        if len(name_of_note) >= 1 and len(new_note_text) >= 1:
            for key, value in self.data.items():
                if key == name_of_note:
                    self.data[name_of_note].note = new_note_text
                    return print(f'{name_of_note} edited!')
            return print(f"{new_note_text} was not found in NoteBook")
        elif len(name_of_note) == 0:
            print(f'Enter name of note to edit!')
        elif len(new_note_text) == 0:
            print(f"Enter new text for {name_of_note}")

    def delete_note(self, note_name):
        if len(note_name) >= 1:
            for key, value in self.data.items():
                if key == note_name:
                    return self.data.pop(note_name)
            return print(f"{note_name} was not found in NoteBook")
        else:
            print("Enter name of note to delete")

    def save_notebook(self):
        with open("notebook.bin", "wb") as f:
            pickle.dump((self.data, self.__id), f)
            print("NoteBook saved")

    def load_notebook(self, file):
        with open(file, "rb") as f:
            info_from_file = pickle.load(f)
            self.data = info_from_file[0]
            self.__id = info_from_file[1]

    def show_notebook(self):
        for name, note in self.data.items():
            print(f"{name}: {(str(note).split(' ')[0][0].upper() + str(note).split(' ')[0][1:] + str(note)[len(str(note).split(' ')[0]):])}")


class Notes:
    def __init__(self, note):
        self.note = note
        self.tags = []

    def __str__(self):
        if len(self.tags) == 0:
            return f'{self.note}'
        else:
            return f'{self.note} | Tags are: {self.tags}'
        
class AddressBookApp(ConsoleApplication):
    def __init__(self):
        super().__init__()
        self.contact_book = AddressBook()
        self.list_of_notes = NoteBook()

    def process_user_input(self):
        try:
            self.contact_book.load_addressbook("addressbook.bin")
        except FileNotFoundError:
            self.contact_book = AddressBook()

        try:
            self.list_of_notes.load_notebook("notebook.bin")
        except FileNotFoundError:
            self.list_of_notes = NoteBook()

        all_commands = {
            # General commands
            "hello": lambda: print("Hi! To get commands list print 'info'."),
            "hi": lambda: print("Hi! To get commands list print 'info'."),
            "good bye": lambda: print("Good bye!"),
            "close": lambda: print("Good bye!"),
            "exit": lambda: print("Good bye!"),
            "info": lambda: print(''.join(f"Command list:"), [key for key in all_commands]),
            # AddressBook commands
            "save addressbook": self.contact_book.save_addressbook,
            "load addressbook": lambda: self.contact_book.load_addressbook(text_after_command),
            "add contact": lambda: self.contact_book.add_contact(text_after_command),
            "add phone": lambda: self.contact_book.add_phone_to_contact(text_after_command),
            "add email": lambda: self.contact_book.add_email_to_contact(text_after_command),
            "add address": lambda: self.contact_book.add_address_to_contact(text_after_command),
            "add birthday": lambda: self.contact_book.add_birthday_to_contact(text_after_command),
            "edit phone": lambda: self.contact_book.edit_phone(text_after_command),
            "edit email": lambda: self.contact_book.edit_email(text_after_command),
            "edit address": lambda: self.contact_book.edit_address(text_after_command),
            "delete contact": lambda: self.contact_book.delete_contact(text_after_command),
            "delete phone": lambda: self.contact_book.delete_phone(text_after_command),
            "delete address": lambda: self.contact_book.delete_address(text_after_command),
            "delete email": lambda: self.contact_book.delete_email(text_after_command),
            "delete birthday": lambda: self.contact_book.delete_birthday(text_after_command),
            "show addressbook": lambda: self.contact_book.show_addressbook(),
            "birthdays in": lambda: self.contact_book.birthday_in(text_after_command),
            "find contact": lambda: self.contact_book.find_contact_by_name(text_after_command),
            "find matches": lambda: self.contact_book.search_matches_in_addressbook(text_after_command),
            # NoteBook commands
            "add note": lambda: self.list_of_notes.add_note(text_after_command),
            "add tag": lambda: self.list_of_notes.add_tag(text_after_command),
            "delete note": lambda: self.list_of_notes.delete_note(text_after_command),
            "edit note": lambda: self.list_of_notes.edit_note(text_after_command),
            "search note": lambda: self.list_of_notes.search_notes(text_after_command),
            "search tag": lambda: self.list_of_notes.search_notes_by_tag(text_after_command),
            "save notebook": self.list_of_notes.save_notebook,
            "load notebook": lambda: self.list_of_notes.load_notebook(text_after_command),
            "show notebook": self.list_of_notes.show_notebook,
         }
    
        while True:
            commands = list(all_commands.keys())
            command_completer = WordCompleter(commands)

            closing_words = ["good bye", "close", "exit"]

            command = ""
            text_after_command = ""

            input_your_command = prompt('Enter your command: ', completer=command_completer)

            for i in all_commands.keys():
                if input_your_command.lower().startswith(i):
                    command = i
                    text_after_command = input_your_command.lower().removeprefix(i).strip()
            command_to_check_for_dif = " ".join(input_your_command.split(" ")[0:2])

            if command in closing_words:
                self.list_of_notes.save_notebook()
                self.contact_book.save_addressbook()
                all_commands[command]()
                self.quit()
                break
            elif command in all_commands:
                all_commands[command]()
            else:
                most_similar_command = difflib.get_close_matches(command_to_check_for_dif, commands, n=1)
                print(f"Invalid command. Print 'info' to see list of commands.\n"
                    f"The most similar to command: '{command_to_check_for_dif}' is: '{most_similar_command[0]}'") \
                    if (len(most_similar_command) > 0) \
                    else (print(f"Invalid command. Print 'info' to see list of commands. "))
    

def main():
    app = AddressBookApp()
    app.run()

if __name__ == '__main__':
    main()
