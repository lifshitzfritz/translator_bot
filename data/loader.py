import os
from dotenv import load_dotenv
from telebot import TeleBot
from googletrans import Translator

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = TeleBot(token=BOT_TOKEN,
              parse_mode='HTML')

translator = Translator()
print(translator)