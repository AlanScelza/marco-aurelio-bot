#!/usr/bin/python3

import telebot
from telebot import types
import time
import logging
import os
import sys
import storages
import re
import random
from pymongo import MongoClient

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

storage_type = getattr(sys.modules[storages.__name__], os.environ.get("STORAGE_TYPE"))
storage = storage_type()


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
    
def meditacion_aleatoria():
    client = MongoClient("mongodb://mongo:27017/")
    db = client["meditaciones"]
    collection = db["meditaciones"]

    random_id = random.randint(1, 485)
    meditacion = collection.find_one({"_id": random_id})

    logger.info(f'Meditacion seleccionada: {random_id}')

    mensaje = f"LIBRO {meditacion['libro'].split()[-1]}\n\n{meditacion['numero']}: {meditacion['texto']}"

    return mensaje

@bot.message_handler(commands=['start'])
def accesoalprograma(message):
    bot.send_message(message.chat.id, f"¡Bienvenid@ {message.from_user.first_name}! Envía /estoico para leer una meditación.")

@bot.message_handler(commands=['estoico'])
def estoico(message):
    Id = message.chat.id
    mensaje = meditacion_aleatoria()

    try:
        bot.send_message(Id, mensaje)
        logger.info("Meditacion enviada.")

    except Exception as e:
        logger.error(f'No fue posible enviar meditación: {e}')
        bot.send_message(Id, f'Mmm, tuve problema para recordar alguna frase. ¿Quieres intentar nuevamente?')

logger.info('Iniciando bot...')
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, none_stop=True)
    except Exception as e:
        logger.error(f"Error en infinity polling: {e}")
        time.sleep(5)
