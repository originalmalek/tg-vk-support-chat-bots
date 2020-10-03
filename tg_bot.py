import logging
import os

import telebot

from detect_intent_text import detect_intent_text
from dotenv import load_dotenv
from telegram_logger import MyLogsHandler

logger = logging.getLogger('TG')

load_dotenv()
telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, чем я могу вам помочь?")


def send_answer_to_telegram(chat_id, text, language_code):
    answer = detect_intent_text(chat_id, text, language_code)
    bot.send_message(chat_id=chat_id, text=answer.query_result.fulfillment_text)

@bot.message_handler(content_types='text')
def send_question_to_dialogflow(message):
    send_answer_to_telegram(message.chat.id, message.text, 'RU')


if __name__ == '__main__':
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
   
    logging.basicConfig(level=10)
    logger.addHandler(MyLogsHandler())

    while True:
        try:
            logger.warning('Bot TG is working')
            bot.polling()
        except Exception as err:
            logger.error('Bot TG got error')
            logger.error(err, exc_info=True)
