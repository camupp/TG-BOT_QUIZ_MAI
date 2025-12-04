import telebot, json, os
from telebot import types
from random import choice
import time

# Инициализация бота и переводчика
bot = telebot.TeleBot('8387186945:AAEYOlEYq89-R1L7vg4Jv-zdHh5V_bnnUMU')


def get_random_theory(theme):
    markup = types.InlineKeyboardMarkup()
    btn_next_theory = types.InlineKeyboardButton('Следующая', callback_data=f'{theme}')
    btn_return_to_theory = types.InlineKeyboardButton('Назад', callback_data='theory')
    markup.add(btn_next_theory, btn_return_to_theory)
    with open('theory.json', 'r', encoding='utf-8') as theory_file:
        info = json.load(theory_file)
        current_theory = choice(info[f'{theme}'])
        return current_theory['name'], current_theory['definition'], markup
    
def get_random_practice(theme):
    markup = types.InlineKeyboardMarkup()
    btn_next_practice = types.InlineKeyboardButton('Следующая', callback_data=f'{theme}')
    btn_return_to_practice = types.InlineKeyboardButton('Назад', callback_data='practice')
    markup.add(btn_next_practice, btn_return_to_practice)
    task_answer = choice(os.listdir(f'practice/{theme}'))[:-4]
    task_path = f'practice/{theme}/' + task_answer + '.png'
    return task_path, task_answer, markup





@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_theory = types.InlineKeyboardButton('Теория', callback_data='theory')
    btn_practice = types.InlineKeyboardButton('Практика', callback_data='practice')
    markup.add(btn_theory, btn_practice)
    bot.send_message(message.chat.id, '<b>Привет, дорогой студент!</b> ✨\n\nНа связи твой личный помощник по повторению матана по лекциям <b>Ю.И. Битюкова</b> с помощью флеш-карточек.\n\n🎯 <b>Я предлагаю два вида повторения:</b>\n\n📚 <b>Теория</b>\nПовторяй теоретический материал, который пригодится на сессии\n\n🔢 <b>Практика</b>\nРешай простые типовые задачки для закрепления материала\n\n<b>Начни свой путь в матанализе прямо сейчас!</b>\nВыбери интересующий тебя раздел и погрузись в мир математического анализа с удовольствием! 🚀', reply_markup=markup, parse_mode='html')

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # Разделы теории
    if callback.data == 'theory':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_complex = types.InlineKeyboardButton('Комплексные числа', callback_data='complex_t')
        btn_sets = types.InlineKeyboardButton('Множества', callback_data='sets')
        btn_limits = types.InlineKeyboardButton('Пределы', callback_data='limits_t')
        btn_continuity = types.InlineKeyboardButton('Непрерывность', callback_data='continuity')
        btn_derivative = types.InlineKeyboardButton('Производные', callback_data='derivatives_t')
        btn_return_to_start = types.InlineKeyboardButton('Назад', callback_data='return_to_main_menu')
        markup.add(btn_complex, btn_sets, btn_limits, btn_continuity, btn_derivative, btn_return_to_start)
        bot.send_message(callback.message.chat.id, 'Выбери подраздел теории', reply_markup=markup)
    elif callback.data == 'practice':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_complex = types.InlineKeyboardButton('Комплексные числа', callback_data='complex_p')
        btn_limits = types.InlineKeyboardButton('Пределы', callback_data='limits_p')
        btn_derivative = types.InlineKeyboardButton('Производные', callback_data='derivatives_p')
        btn_return_to_start = types.InlineKeyboardButton('Назад', callback_data='return_to_main_menu')
        markup.add(btn_complex, btn_limits, btn_derivative, btn_return_to_start)
        bot.send_message(callback.message.chat.id, 'Выбери подраздел практики', reply_markup=markup)
    # ТЕОРИЯ карточки
    # Карточки с пределами
    elif callback.data == 'limits_t':
        name, definiton, markup = get_random_theory('limits_t')
        bot.send_message(callback.message.chat.id, f'Раздел - Пределы:\n\n{name}:\n\n<tg-spoiler>{definiton}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # Карточки с комплексными числами
    elif callback.data == 'complex_t':
        name, definiton, markup = get_random_theory('complex_t')
        bot.send_message(callback.message.chat.id, f'Раздел - Комплексные числа:\n\n{name}:\n\n<tg-spoiler>{definiton}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # Карточки с непрерывностью
    elif callback.data == 'continuity':
        name, definiton, markup = get_random_theory('continuity')
        bot.send_message(callback.message.chat.id, f'Раздел - Непрерывность:\n\n{name}:\n\n<tg-spoiler>{definiton}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # Карточки с производными
    elif callback.data == 'derivatives_t':
        name, definiton, markup = get_random_theory('derivatives_t')
        bot.send_message(callback.message.chat.id, f'Раздел - Производные:\n\n{name}:\n\n<tg-spoiler>{definiton}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # Карточки со множествами
    elif callback.data == 'sets':
        name, definiton, markup = get_random_theory('sets')
        bot.send_message(callback.message.chat.id, f'Раздел - Множества:\n\n{name}:\n\n<tg-spoiler>{definiton}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # ПРАКТИКА карточки
    elif callback.data == 'limits_p':
        path, answer, markup = get_random_practice('limits_p')
        with open(path, 'rb') as task:
            bot.send_photo(callback.message.chat.id, task)
            bot.send_message(callback.message.chat.id, f'Посмотреть правильный ответ:\n\n<tg-spoiler>{answer}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    elif callback.data == 'derivatives_p':
        path, answer, markup = get_random_practice('derivatives_p')
        with open(path, 'rb') as task:
            bot.send_photo(callback.message.chat.id, task)
            bot.send_message(callback.message.chat.id, f'Посмотреть правильный ответ:\n\n<tg-spoiler>{answer}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    elif callback.data == 'complex_p':
        path, answer, markup = get_random_practice('complex_p')
        with open(path, 'rb') as task:
            bot.send_photo(callback.message.chat.id, task)
            bot.send_message(callback.message.chat.id, f'Посмотреть правильный ответ:\n\n<tg-spoiler>{answer}</tg-spoiler>', parse_mode='html', reply_markup=markup)
    # Возврат в меню
    elif callback.data == 'return_to_main_menu':
        start(callback.message)

bot.polling(none_stop=True)