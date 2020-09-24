import dialogflow_v2 as dialogflow
import logging
import os
import random
import telebot
import vk_api
import json

from dotenv import load_dotenv
from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"
# credentials_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"


def send_message_vk(text, vk_api, session_id):
    vk_api.messages.send(user_id=session_id, message=text, random_id=random.randint(1, 1000))


def detect_intent_text(text, project_id, session_id, language_code, vk_api):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    if response.query_result.intent.display_name != 'Default Fallback Intent':
        send_message_vk(response.query_result.fulfillment_text, vk_api, session_id)


def send_log_message(telegram_token, telegram_chat_id, text):
    bot = telebot.TeleBot(telegram_token)
    bot.send_message(telegram_chat_id, text)


def main():
    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            send_log_message(telegram_token, telegram_chat_id, log_entry)


    logging.basicConfig(level=10)
    logger = logging.getLogger('TG')
    logger.addHandler(MyLogsHandler())
    while True:
        try:
            logger.warning('Бот запущен! VK')
            logger.warning(credentials)
            logger.warning(service_account_info)
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    detect_intent_text(event.text, project_id, event.user_id, 'RU', vk_api)
        except Exception as err:
            logger.error('Бот VK упал с ошибкой!')
            logger.error(err, exc_info=True)
#             sleep(60)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    main()
