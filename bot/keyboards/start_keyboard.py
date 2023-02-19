from aiogram import types


# создаем кнопку, которая будет располагаться на клавиатуре
set_link_button = types.KeyboardButton('Задать новую ссылку для поиска')
show_link_button = types.KeyboardButton('Посмотреть заданную ссылку')


set_link_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
set_link_keyboard.add(set_link_button)
set_link_keyboard.add(show_link_button)
