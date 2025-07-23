from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from googletrans import LANGUAGES


def show_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton(text='Перевод'),
        KeyboardButton(text='История переводов'),
    )
    return kb


def show_languages_kb():
    # создать переменную для клавиатуры
    # создать пустой список кнопок
    # написать цикл по значениям словаря
    # добавить кнопку в список кнопок
    # вернуть клавиатуру
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []

    for value in LANGUAGES.values():
        buttons.append(
            KeyboardButton(text=value)
        )
    kb.add(*buttons)
    return kb



def show_translated_items_kb():
    pass