# создать виртуальное окружение
# активировать его
# добавить интерпретатор
# скачать библиотеки
# python-dotenv pytelegrambotapi googletrans==4.0.0rc1

import handlers
from data.loader import bot
from database.main import create_users_table, create_translations_table


create_users_table('translations.db')
create_translations_table('translations.db')
bot.polling(none_stop=True)


# TODO:
# в амдминистрацию
# Муслима Рахимжонова
# Фаррух Иззатуллоев
# Диёржон Зокиров
# Асадбек Абдуллаев
