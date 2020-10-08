import logging
import os
import random

import telebot
import vk_api

from detect_intent_text import detect_intent_text
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram_logger import MyLogsHandler


logger = logging.getLogger('TG')


def send_message_vk(text, vk_api, session_id):
    vk_api.messages.send(user_id=session_id, message=text, random_id=random.randint(1, 1000))


def send_answer_to_vk(text, session_id, language_code, vk_api):
    answer = detect_intent_text(f'vk-{session_id}', text, language_code)
    if answer.query_result.intent.display_name != 'Default Fallback Intent':
        send_message_vk(answer.query_result.fulfillment_text, vk_api, session_id)


def send_log_message(telegram_token, telegram_chat_id, text):
    bot = telebot.TeleBot(telegram_token)
    bot.send_message(telegram_chat_id, text)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    logging.basicConfig(level=10)
    logger.addHandler(MyLogsHandler())

    while True:
        try:
            logger.warning('Bot VK is working')
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    send_answer_to_vk(event.text, event.user_id, 'RU', vk_api)
        except Exception as err:
            logger.error('Bot VK got an error')
            logger.error(err, exc_info=True)
