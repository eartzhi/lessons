import asyncio
import logging
import os
import annoy
import pickle
import string
import json
import pandas as pd
import numpy as np

from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from gensim.models import Word2Vec
from sklearn import linear_model
from pymorphy3 import MorphAnalyzer
from stop_words import get_stop_words

# Все нижеследующее можно разбить на несколько фалов, но в учебных целях этого делать не будем.
BASE_DIR = Path(__file__).resolve().parent

index = annoy.AnnoyIndex(100 ,'angular')
product_index = annoy.AnnoyIndex(100 ,'angular')

model = Word2Vec.load("pda_01/w2v_model")
index.load('pda_01/speaker.ann')
product_index.load('pda_01/product.ann')

with open('pda_01/index_map.json', 'r') as f:
    index_map = json.load(f)
    
with open('pda_01/product_index_map.json', 'r') as f:
    product_index_map = json.load(f)


morpher = MorphAnalyzer()
sw = set(get_stop_words("ru"))
exclude = set(string.punctuation)
products = pd.read_csv('pda_01/data/vector_products.csv')

with open('pda_01/log_model.pkl', 'rb') as file:
    log_model = pickle.load(file)

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

my_formatter = logging.Formatter(
    '%(filename)s %(asctime)s %(levelname)s %(message)s')

logging.basicConfig(level=logging.INFO)
info_logger = logging.getLogger()
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(os.path.join(BASE_DIR, 'bot.log'), 'w', 'utf-8')
info_handler.setFormatter(my_formatter)
info_logger.addHandler(info_handler)

TOKEN = os.getenv("TOKEN")
dp = Dispatcher()


def preprocess_txt(line):
    spls = "".join(i for i in line.strip() if i not in exclude).split()
    spls = [morpher.parse(i.lower())[0].normal_form for i in spls]
    spls = [i for i in spls if i not in sw and i != ""]
    return spls


def find_answer(vector):
    answer_index = index.get_nns_by_vector(vector, 1)
    return index_map[str(answer_index[0])]


def find_product(vector):
    # print(vector)
    answer_index = product_index.get_nns_by_vector(vector, 1)
    return product_index_map[str(answer_index[0])]


def get_answer(question):
    question = preprocess_txt(question)
    n_w2v = 0
    vector = np.zeros(100)
    for word in question:
        if word in model.wv:
            vector += model.wv[word]
            n_w2v += 1
    if n_w2v > 0:
        vector = vector / n_w2v
    # print(vector)
    # vector = pd.DataFrame(vector, columns=[f'elem_{elem}' for elem in range(100)])
    direction = log_model.predict(vector.reshape(1, -1))
    if direction:
        return find_product(vector)
    else:
        return find_answer(vector)
        


@dp.message(Command('start', 'help'))
async def command_handler(message: Message) -> None:
    info_logger.info(f'Боту пришло сообщение: "{message.text}'
                     f' от {message.from_user.first_name}"')
    answer = f'Приветствую, {message.from_user.first_name}! ' \
             f'Я помогу тебе подобрать товар ' \
             f'Введи название или описание товара и я подберу его для тебя' 
    await message.reply(answer)
    info_logger.info(f'Бот ответил: "{answer}"')

@dp.message()
async def message_handler(message: types.Message) -> None:
    info_logger.info(f'Боту пришло сообщение: "{message.text}'
                     f' от {message.from_user.first_name}"')
    answer = get_answer(message.text)
    await message.reply(answer)
    info_logger.info(f'Бот ответил: "{answer}"')



async def main() -> None:
    # bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())