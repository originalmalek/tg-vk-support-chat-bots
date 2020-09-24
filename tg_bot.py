import dialogflow_v2 as dialogflow
import os
import telebot

from dotenv import load_dotenv


load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow_creds.json"
dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
telegram_token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(telegram_token)


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


def main():
    while True:
        bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
