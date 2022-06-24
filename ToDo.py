from random import choice
import telebot

token = 'secret_token'

bot = telebot.TeleBot(token)


RANDOM_TASKS = ['Umýt auto', 'Кoupit květiny pro manželku', 'Vzít si volno v práci'
                'Jít s kamarádkou/kamarádem na pivo', 'Zajít do cukrárny']

todos = {}


HELP = '''
Seznam dostupných příkazů:
/add  - zobrazit všechny úkoly na zadaný den
/todo - přidat úkol
/random - přidat na dnešní den náhodný úkol
/help - zobrazení informací
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
    add_todo('dnes', task)
    bot.send_message(message.chat.id, f'Úkol {task} přidán na dnes')


@bot.message_handler(commands=['add'])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command([1]).lower()
    task = command([2])
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Úkol {task} přidán na datum {date}!')



@bot.message_handler(commands=['show'])
def print_(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Datum neexistuje!'
    bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)
