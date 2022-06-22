from random import choice
import telebot


token = '5267627441:AAFJIhlGbYyRP05AXiG1g0W3E0UaaaPxBlg'

bot = telebot.TeleBot(token)

RANDOM_TASKS = ['Помыть машину', 'Купить цветы', 'Посмотреть сериал', 'Поцеловать жену/мужа', 'Позвонить подруге/другу',
                'Купить торт и побаловать себя']
todos = dict()

HELP = '''
Список доступных команд:
/help - напечатать справку по программе
/add - добавить задачу в список 
/show - напечатать все добавленные задачи
/random - добавить случайную задачу на дату сегодня
'''


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня!')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}!')


@bot.message_handler(commands=['show'])
def print_(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет!'
    bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)
