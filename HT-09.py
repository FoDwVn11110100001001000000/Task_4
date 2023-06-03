# Завдання
# Напишіть консольного бота помічника, який розпізнаватиме команди, що вводяться з клавіатури, і відповідати відповідно до введеної команди.

# Бот помічник повинен стати для нас прототипом застосунку-асистента. Застосунок-асистент в першому наближенні повинен вміти працювати з книгою контактів і календарем. У цій домашній роботі зосередимося на інтерфейсі самого бота. Найпростіший і найзручніший на початковому етапі розробки інтерфейс - це консольний застосунок CLI (Command Line Interface). CLI достатньо просто реалізувати. Будь-який CLI складається з трьох основних елементів:

# Парсер команд. Частина, яка відповідає за розбір введених користувачем рядків, виділення з рядка ключових слів та модифікаторів команд.
# Функції обробники команд — набір функцій, які ще називають handler, вони відповідають за безпосереднє виконання команд.
# Цикл запит-відповідь. Ця частина застосунку відповідає за отримання від користувача даних та повернення користувачеві відповіді від функції-handlerа.
# На першому етапі наш бот-асистент повинен вміти зберігати ім'я та номер телефону, знаходити номер телефону за ім'ям, змінювати записаний номер телефону, виводити в консоль всі записи, які зберіг. Щоб реалізувати таку нескладну логіку, скористаємося словником. У словнику будемо зберігати ім'я користувача як ключ і номер телефону як значення.

# Умови
# Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
# Бот завершує свою роботу, якщо зустрічає слова: "good bye", "close", "exit".
# Бот не чутливий до регістру введених команд.
# Бот приймає команди:
# "hello", відповідає у консоль "How can I help you?"
# "add ...". За цією командою бот зберігає у пам'яті (у словнику наприклад) новий контакт. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
# "change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
# "phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту. Замість ... користувач вводить ім'я контакту, чий номер потрібно показати.
# "show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
# "good bye", "close", "exit" за будь-якою з цих команд бот завершує свою роботу після того, як виведе у консоль "Good bye!".
# Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає за повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо. Декоратор input_error повинен обробляти винятки, що виникають у функціях-handler (KeyError, ValueError, IndexError) та повертати відповідну відповідь користувачеві.
# Логіка команд реалізована в окремих функціях і ці функції приймають на вхід один або декілька рядків та повертають рядок.
# Вся логіка взаємодії з користувачем реалізована у функції main, всі print та input відбуваються тільки там.


import sys

contacts = {
    'Alice': '0931112233',
    'Jane': '0504445566',
    'Hugo': '0957778899'
}

def exit_programm(func):
    def wrapper():
        print('Good bye!')
        func()
        sys.exit()
    return wrapper

@exit_programm
def good_bye():
    pass

def hello():
    return 'How can I help you?'

def add(data):
    splitted = data.split()
    if splitted[1].isalpha() and splitted[2].isdigit():
        contacts[splitted[1].title()] = splitted[2]
        return f'Контакт {splitted[1].title()} додано до тел. книжки.'
    elif splitted[1].isdigit() and splitted[2].isalpha():
        contacts[splitted[2].title()] = splitted[1]
        return f'Контакт {splitted[2].title()} додано до тел. книжки.'
    else:
        return 'Некоректні дані для додавання контакту.'


def change(data):
    splitted = data.split()
    if splitted[1].isalpha() and splitted[2].isnumeric():
        contacts[splitted[1].title()] = splitted[2]
        return f'Номер телефону в контакті {splitted[1].title()} змінено.'
    elif splitted[2].isalpha() and splitted[1].isnumeric():
        contacts[splitted[2].title()] = splitted[1]
        return f'Номер телефону в контакті {splitted[2].title()} змінено.'

def phone(data):
    splitted = data.split()
    if splitted[-1].title() in contacts:
        return contacts[splitted[-1].title()]
    else:
        return 'Контакт не знайдено.'

def show_all():
    contacts_list = [f'Name: {name}, Phone: {phone_number}' for name, phone_number in contacts.items()]
    result = '\n'.join(contacts_list)
    return result

def help_lists():
    text = ('Доступні команди для формування запиту:\n'
        '- Hello - навіть наш бот любить ввічливих\n'
        '- Phone - при введенні імені виведе його номер тел. (формат запиту: Phone *User*)\n'
        '- Add - додати контакт (формат запиту: Add *Name* 0500000000)\n'
        '- Change - змінити номер телефону в контакті (формат запиту: Change *Name* 0500000000)\n'
        '- Show all - показати список всіх контактів\n'
        '- Help me - викликати меню команд\n'
        'Для завершення роботи бота введіть "good bye", "close", "exit"'
        )
    return text


commands = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show all': show_all,
    'help me': help_lists,
}


def main():
    print(help_lists())
    while True:
        request = input('Введіть запит: ')
        for key, value in commands.items():
            try:
                if request in ("good bye", "close", "exit"):
                    good_bye()
                elif key in request.lower():
                    print(value(request))
                    break
            except TypeError:
                print(value())
                break
        
                

if __name__ == "__main__":
    main()