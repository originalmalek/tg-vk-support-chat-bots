# AI Bot telegram/vk.com with DialogFlow
The project makes a telegram/vk.com for user support using DialogFlow


## Description
The code: 
The project gets winner in instagram. 

The project uses:   
 * [Telegram](telegram.org)
 * [Vk.com](https://vk.com/)
 * [DialogFlow](https://dialogflow.cloud.google.com/)
  

## Requirements
Python >=3.7
Dialogflow(Google console) Credentials
Registered bot on  [Telegram](https://t.me/botfather)
Registered account and created public on [vk.com](https://vk.com/).
Registered account in [DialogFlow](https://dialogflow.cloud.google.com/)

 
Create file '.env' and add the code:
```
TELEGRAM_TOKEN = your_telegram_bot_token
VK_TOKEN = your_vk_access_token
DIALOGFLOW_PROJECT_ID = your_dialog_flow_project_id
TELEGRAM_CHAT_ID = your_telegram_chat_id
```

Install requirements modules:
```
pip install -r requirements.txt	
```


### How to use

Install requirements. 
Upload inten to your DialogFlow account 
```
python upload_intent.py
```
Open and run 'tg_bot.py' or/and 'vk_bot.py'.
```
python tg_bot.py
python vk_bot.py
```

### Aditional Information
You have to upload intent f
Get Dialogflow account and credentials [read here](https://cloud.google.com/dialogflow/es/docs/quick/setup).  
Creat Agent for Dialogflow [read here](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).  
For getting key for vk bot: Create public -> Manage -> Api usage -> Create 'Access token'.  
You can get dialogflow project_id from credentionals file.  

Credential must be named 'dialogflow_creds.json'.  

![Alt Text](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

![Alt Text](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_vk_bot.gif)
## Project goal
The code was written for educational purpose on online course for Api developers [Devman](http://dvmn.org). 
