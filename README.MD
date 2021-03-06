# AI Bot telegram/vk.com with DialogFlow
The project makes a telegram/vk.com bot for user support using DialogFlow.
The bots can answer for user requests in telegram/vk.com.


## Description
The code: 
Create a chat bot for user support. The bot can answer on user question automatically. 

The project uses:   
 * [Telegram](telegram.org)
 * [Vk.com](https://vk.com/)
 * [DialogFlow](https://dialogflow.cloud.google.com/)
  

## Requirements
Python >=3.7  
Dialogflow(Google console) Credentials.  
Registered bot on  [Telegram](https://t.me/botfather).  
Registered account and created public on [vk.com](https://vk.com/).  
Registered account in [DialogFlow](https://dialogflow.cloud.google.com/).  

 
Create file '.env' and add the code:
```
TELEGRAM_TOKEN=your_telegram_bot_token
VK_TOKEN=your_vk_access_token
DIALOGFLOW_PROJECT_ID=your_dialog_flow_project_id
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Install requirements modules:
```
pip install -r requirements.txt	
```

You have to upload intent first.
Get Dialogflow account and credentials [read here](https://cloud.google.com/dialogflow/es/docs/quick/setup).  
Creat Agent for Dialogflow [read here](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).  
For getting key for vk bot: Create public -> Manage -> Api usage -> Create 'Access token'.  
You can get dialogflow project_id from credentionals file.  


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

### Program example
![tg bot](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

![vk bot](https://dvmn.org/media/filer_public/1e/f6/1ef61183-56ad-4094-b3d0-21800bdb8b09/demo_vk_bot.gif)
## Project goal
The code was written for educational purpose on online course for Api developers [Devman](http://dvmn.org). 
