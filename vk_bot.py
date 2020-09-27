import dialogflow_v2 as dialogflow
import logging
import os
import random
import telebot
import vk_api

from google.oauth2 import service_account
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

credentials = service_account.Credentials.from_service_account_file("google-credentials.json")


def send_message_vk(text, vk_api, session_id):
    vk_api.messages.send(user_id=session_id, message=text, random_id=random.randint(1, 1000))


def detect_intent_text(text, project_id, session_id, language_code, vk_api):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    if response.query_result.intent.display_name != 'Default Fallback Intent':
        send_message_vk(response.query_result.fulfillment_text, vk_api, session_id)


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
    
    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            send_log_message(telegram_token, telegram_chat_id, log_entry)

    logging.basicConfig(level=10)
    logger = logging.getLogger('TG')
    logger.addHandler(MyLogsHandler())
    while True:
        try:
            logger.warning('Bot VK is working')
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    detect_intent_text(event.text, project_id, event.user_id, 'RU', vk_api)
        except Exception as err:
            logger.error('Bot VK got an error')
            logger.error(err, exc_info=True)
