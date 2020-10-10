import argparse
import os

import dialogflow_v2 as dialogflow
import requests

from dotenv import load_dotenv
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file("google-credentials.json")


def structure_training_phases(dialogflow_question_phases):
    training_phases = []
    for question_phase in dialogflow_question_phases:
        training_phases.append({'parts': [{'text': question_phase}]})
    return training_phases


def get_intent_phases(url):
    response_phases = requests.get(url)
    response_phases.raise_for_status()
    return response_phases.json()


def create_intent_dict(url):
    training_phases = get_intent_phases(url)
    intent = {}
    for display_name in training_phases:
        dialogflow_answer_phases = training_phases[display_name]['answer']
        dialogflow_question_phases = training_phases[display_name]['questions']
        intent.update({'display_name': display_name,
                       'messages': [{'text': {'text': [dialogflow_answer_phases]}}],
                       'training_phrases': structure_training_phases(dialogflow_question_phases)
                       })

    return intent


def upload_intent(dialogflow_project_id, url):
    intent = create_intent_dict(url)
    client = dialogflow.IntentsClient(credentials=credentials)
    parent = client.project_agent_path(dialogflow_project_id)
    client.create_intent(parent, intent)


def main():
    parser = argparse.ArgumentParser(description='The programm upload intent to Google DialogFlow')
    parser.add_argument('url', help='Enter url to json file or enter\n "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"\n for uploading default intent')
    args = parser.parse_args()
    url = args.url

    load_dotenv()
    dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    upload_intent(dialogflow_project_id, url)


if __name__ == '__main__':
    main()
