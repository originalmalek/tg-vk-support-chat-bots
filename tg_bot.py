import dialogflow_v2 as dialogflow
import os
import telebot
import logging

from google.oauth2 import service_account
from dotenv import load_dotenv

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token)


def detect_intent_text(dialogflow_project_id, chat_id, text, language_code):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(dialogflow_project_id, chat_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    bot.send_message(chat_id=chat_id, text=response.query_result.fulfillment_text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, чем я могу вам помочь?")


@bot.message_handler(content_types='text')
def send_question_to_dialogflow(message):
    detect_intent_text(dialogflow_project_id, message.chat.id, message.text, 'RU')


def send_log_message(telegram_token, telegram_chat_id, text):
    bot = telebot.TeleBot(telegram_token)
    bot.send_message(telegram_chat_id, text)


if __name__ == '__main__':
    load_dotenv()

    credentials = service_account.Credentials.from_service_account_file("google-credentials.json")
    dialogflow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            send_log_message(telegram_token, telegram_chat_id, log_entry)

    logging.basicConfig(level=10)
    logger = logging.getLogger('TG')
    logger.addHandler(MyLogsHandler())

    while True:
        try:
            logger.warning('Bot TG is working')
            bot.polling()
        except Exception as err:
            logger.error('Bot TG got error')
            logger.error(err, exc_info=True)
