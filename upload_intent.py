import os
import dialogflow_v2 as dialogflow
import requests
from dotenv import load_dotenv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow_creds.json"


def structure_training_phases(dialogflow_question_phases):
    training_phases = []
    for question_phase in dialogflow_question_phases:
        training_phases.append({'parts': [{'text': question_phase}]})
    return training_phases


def get_intent_phases():
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response_phases = requests.get(url)
    response_phases.raise_for_status()
    return response_phases.json()


def upload_intent(intent, project_id):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    client.create_intent(parent, intent)


def create_intent_file(project_id):
    training_phases = get_intent_phases()
    intent = {}
    for display_name in training_phases:
        dialogflow_answer_phases = training_phases[display_name]['answer']
        dialogflow_question_phases = training_phases[display_name]['questions']
        intent.update({'display_name': display_name,
                       'messages': [{'text': {'text': [dialogflow_answer_phases]}}],
                       'training_phrases': structure_training_phases(dialogflow_question_phases)
                       })

        upload_intent(intent, project_id)


def main():
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    create_intent_file(project_id)


if __name__ == '__main__':
    main()
