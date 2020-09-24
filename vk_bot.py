import os
import dialogflow_v2 as dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import random


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow_creds.json"


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


def main():
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_text(event.text, project_id, event.user_id, 'RU', vk_api)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    main()
