from data.loader import bot, translator
from keyboards.reply import show_start_kb, show_languages_kb
from keyboards.inline import show_langs_kb
from telebot import types
from database.main import add_user, add_translation, get_user_translations
from googletrans import LANGCODES, LANGUAGES


@bot.message_handler(commands=['start'])
def handle_command_start(message: types.Message):
    chat_id = message.chat.id
    add_user('translations.db', chat_id=chat_id)
    text = f'Привет, <i>{message.from_user.username}</i>'
    bot.send_message(chat_id, text, reply_markup=show_start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Перевод')
def handle_translation_start(message: types.Message):
    chat_id = message.chat.id
    text = 'Выберите язык, с которого хотите сделать перевод'
    bot.send_message(chat_id, text, reply_markup=show_languages_kb())
    bot.register_next_step_handler(message, get_lang_from)

@bot.message_handler(func=lambda msg: msg.text in LANGUAGES.values())
def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    text = 'Выберите язык, на который хотите сделать перевод'
    bot.send_message(chat_id, text, reply_markup=show_languages_kb())
    bot.register_next_step_handler(message, get_lang_to, message.text)


@bot.message_handler(func=lambda msg: msg.text in LANGUAGES.values())
def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    text = "Напишите текст для перевода"
    bot.send_message(chat_id, text, reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id
    code_from = LANGCODES[lang_from]
    code_to = LANGCODES[lang_to]

    translated = translator.translate(message.text, code_to, code_from).text

    msg = f"""
FROM: <i>{lang_from}</i>
TO: <i>{lang_to}</i>
ORIGINAL: <i>{message.text}</i>
TRANSLATED: <i>{translated}</i>
"""
    add_translation('translations.db', code_from, code_to, message.text, translated, chat_id)
    bot.send_message(chat_id, msg)


@bot.message_handler(func=lambda msg: msg.text == 'История переводов')
def handle_translation_history(message: types.Message):
    chat_id = message.chat.id
    text = 'Ваша история переводов'
    translations = get_user_translations('translations.db', chat_id)
    print(translations)
    bot.send_message(chat_id, text)




# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith('prev_page')
# )
# def answer_callback(call: types.CallbackQuery):
#     _, page, start, finish, translation_id = call.data.split(':')
#     if int(page) == 1:
#         return bot.answer_callback_query(
#             callback_query_id=call.id,
#             text='Вы уже на первой странице',
#             show_alert=True
#         )
#
#     bot.edit_message_reply_markup(
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id,
#         reply_markup=show_langs_kb(
#             page=int(page)-1,
#             start=int(start)-9,
#             finish=int(finish)-9
#         )
#     )
#
#
# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith('next_page')
# )
# def answer_callback(call: types.CallbackQuery):
#     data = call.data
#     print(data)
#     _, page, start, finish, total_pages = data.split(':')
#     if int(page) == int(total_pages):
#         bot.answer_callback_query(call.id, 'Это последняя страница',
#                                   show_alert=True)
#         return
#
#     bot.edit_message_reply_markup(
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id,
#         reply_markup=show_langs_kb(
#             start=int(start) + 9,
#             finish=int(finish) + 9,
#             page=int(page) + 1
#         )
#     )
#
#
# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith('lang')
# )
# def answer_callback(call: types.CallbackQuery):
#     _, lang = call.data.split(':')
#
#     bot.edit_message_text(
#         text='Выберите язык на который хотите сделать перевод',
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id,
#         reply_markup=show_langs_kb(
#             is_from=False
#         )
#     )
#     bot.register_next_step_handler(call.message, next_step_1, lang)
#
#
# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith('lang_to')
# )
# def next_step_1(call: types.CallbackQuery, lang_from):
#     print(lang_from)
# # сделать обработку клика по языку и по кнопке следующая страница
