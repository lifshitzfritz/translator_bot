from googletrans import LANGCODES
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def show_langs_kb(start=0, finish=9, page=1, is_from=True, translation_id=None):
    kb = InlineKeyboardMarkup()
    languages = LANGCODES.items()
    total_pages = round(len(languages)/9)
    buttons = []
    for lang, lang_code in list(languages)[start:finish]:
        callback = f'lang:{lang_code}:{translation_id}' if is_from else f'lang_to:{lang_code}:{translation_id}'
        buttons.append(
            InlineKeyboardButton(
                text=lang,
                callback_data=callback
            ))
    kb.add(*buttons)
    kb.row(
        InlineKeyboardButton("◀", callback_data=f'prev_page:{page}:{start}:{finish}:{translation_id}'),
        InlineKeyboardButton(f"{page}/{total_pages}", callback_data=f'page'),
        InlineKeyboardButton("▶", callback_data=f'next_page:{page}:{start}:{finish}:{total_pages}:{translation_id}'),
    )
    return kb
