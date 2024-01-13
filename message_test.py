from bs4 import BeautifulSoup
import requests
from datetime import datetime
import telegram
import asyncio
import os 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")
sqr_id = os.environ.get("sqr_id")
group_id = os.environ.get("group_id")

async def sendNotification(message):
    bot = telegram.Bot(token=TOKEN)
    task_message = asyncio.create_task(bot.send_message(chat_id=group_id, text=message))
    res_message = await task_message

asyncio.run(sendNotification("hehe kutas"))