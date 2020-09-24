import dialogflow_v2 as dialogflow
import os
import telebot
import logging

from dotenv import load_dotenv
from time import sleep

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"



dialogflow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token)
telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']


def detect_intent_text(dialogflow_project_id, chat_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
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
            logger.warning('Бот запущен! TG')
            bot.polling()
            logger.warning('bot poll')
        except Exception as err:
            logger.error('Бот TG упал с ошибкой!')
            logger.error(err, exc_info=True)
            sleep(60)


if __name__ == '__main__':
    main()
