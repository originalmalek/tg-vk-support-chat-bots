import dialogflow_v2 as dialogflow
import os

from dotenv import load_dotenv
from google.oauth2 import service_account

load_dotenv()
dialogflow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
credentials = service_account.Credentials.from_service_account_file("google-credentials.json")

def detect_intent_text(chat_id, text, language_code):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(dialogflow_project_id, chat_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response
