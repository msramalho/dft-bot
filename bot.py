import asyncio
import os
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from dotenv import load_dotenv

import datetime
from dft_bot.callers.caller import BotType
from dft_bot.db.crud import init_db, insert_active_user, is_user_active
from dft_bot.db.models import UserTypeEnum
from dft_bot.security import valid_login

#### Access credentials
load_dotenv()
API_ID = os.environ.get("API_ID")  # get the api id
API_HASH = os.environ.get("API_HASH")  # get the api hash
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # get the bot token

client = TelegramClient("./secrets/anon", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


### Start command
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    sender = await event.get_sender()
    sender_id = sender.id
    text = "Docker Bot 🤖 ready\nHello! I'm answering you from Docker!"
    await client.send_message(sender_id, text, parse_mode="HTML")

    markup = client.build_reply_markup(Button.text('/time', single_use=True))
    await client.send_message(sender_id, "Click it", buttons=markup)


### First command, get the time and day
@client.on(events.NewMessage(pattern="/(?i)time"))
async def time(event):
    # Get the sender of the message
    sender = await event.get_sender()
    sender_id = sender.id
    text = "Received! Day and time: " + str(datetime.datetime.now())
    await client.send_message(sender_id, text, parse_mode="HTML")

import re
login_pattern = r"^/login (.+?)( (\d{6})|)$"
@client.on(events.NewMessage(pattern=login_pattern))
async def _login(event):
    # expects "/login API_KEY OTP_TOKEN" with optional OTP_TOKEN
    sender = await event.get_sender()
    sender_id = sender.id
    match = re.search(login_pattern, event.raw_text)
    if valid_login(match.group(1), match.group(2)):
        insert_active_user(sender_id, UserTypeEnum.telegram)
        await client.send_message(sender_id, "Login success.", parse_mode="HTML")
    else:
        await client.send_message(sender_id, "Invalid credentials, please send <code>/login (API_KEY) (OTP_CODE)</code> <a href='/login'>login<a/>", parse_mode="HTML")


### EMAIL PATTERN
from dft_bot.callers.email.holehe_caller import HoleheCaller
from dft_bot.callers.email.ghunt_caller import GHuntCaller
from dft_bot.callers.aleph_caller import AlephCaller
from dft_bot.utils import ToolResponse

email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
@client.on(events.NewMessage(pattern=email_pattern))
async def _email_check(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if not is_user_active(sender_id, UserTypeEnum.telegram):
        await client.send_message(sender_id, "Please /login first.", parse_mode="HTML")
        return
    email = event.raw_text
    main_r = ToolResponse("email")
    
    callers = [
        # HoleheCaller({"email": email}, {"client": client, "sender_id": event.sender_id}, BotType.telethon),
        # GHuntCaller({"email": email}, {"client": client, "sender_id": event.sender_id}, BotType.telethon),
        AlephCaller({"email": email}, {"client": client, "sender_id": event.sender_id}, BotType.telethon),
    ]

    start_message = await client.send_message(sender_id, "loading...", parse_mode="HTML")
    await asyncio.gather(*[caller.call() for caller in callers])
    await client.send_message(sender_id, f"Done in {main_r.get_total_time_seconds()}s.", parse_mode="HTML")
    await client.delete_messages(sender_id, [start_message.id])

### URL PATTERN
# from dft_bot.callers.url.unfurl_caller import UnfurlCaller
# from dft_bot.callers.url.subdomain_caller import SubdomainCaller
# url_pattern = r"^/url (.+)$"
# @client.on(events.NewMessage(pattern=url_pattern))
# async def _url_check(event):
#     print("URL")
#     sender = await event.get_sender()
#     sender_id = sender.id
#     main_r = ToolResponse("email")

#     url = re.search(url_pattern, event.raw_text).group(1)
#     callers = [
#         UnfurlCaller({"url": url}, {"client": client, "sender_id": event.sender_id}, BotType.telethon),
#         SubdomainCaller({"url": url}, {"client": client, "sender_id": event.sender_id}, BotType.telethon),
#     ]

#     start_message = await client.send_message(sender_id, "loading...", parse_mode="HTML")
#     await asyncio.gather(*[caller.call() for caller in callers])
#     await client.send_message(sender_id, f"Done in {main_r.get_total_time_seconds()}s.", parse_mode="HTML")
#     await client.delete_messages(sender_id, [start_message.id])

    
# from maigret import 
import subprocess
username_pattern = r"^/user (.+)$"
@client.on(events.NewMessage(pattern=username_pattern))
async def _username_check(event):
    print("USERNAME")
    username = re.search(username_pattern, event.raw_text).group(1)
    command = f"maigret {username} --html --pdf --csv"
    cli_output = subprocess.check_output(
        command, shell=True, stderr=subprocess.STDOUT, text=True
    )
    print(cli_output)


### MAIN
if __name__ == "__main__":
    init_db()
    print("DB Init!")
    client.run_until_disconnected()
    print("Bot Started!")
