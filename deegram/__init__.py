import logging
import os
import sys
import time

import deethon
from dotenv import load_dotenv
from telethon import TelegramClient, functions, types
from telethon.events import NewMessage

formatter = logging.Formatter(
    '%(levelname)s %(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler(f'{__name__}.log', 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.WARNING)
telethon_logger.addHandler(ch)
telethon_logger.addHandler(fh)

botStartTime = time.time()

load_dotenv()

try:
    API_ID = int(os.environ["2156559"])
    API_HASH = os.environ["fea80bd8ede83bcb1a3290c43e5691bd"]
    BOT_TOKEN = os.environ["1440547253:AAEuCMcYuGQUeJQZwM-LNnWn8EhZaOteulg"]
    DEEZER_TOKEN = os.environ["2370c3c0c13737598e7643fb1c144e9c44df67645b0d7f728e77d33db050012d197225658d682c30d9d89ae7ff10e825f471de952d17d96037b2e2447094bbb9ac32a11325cff4bb00549e06d5975eb2cd00e5b55edef37af5a7c54c030b2d3f"]
    OWNER_ID = int(os.environ["1492235056"])
except KeyError:
    logger.error("One or more environment variables are missing! Exiting now…")
    sys.exit(1)

deezer = deethon.Session(DEEZER_TOKEN)
logger.debug(f'Using deethon v{deethon.__version__}')

bot = TelegramClient(__name__, API_ID, API_HASH,
                     base_logger=telethon_logger).start(bot_token=BOT_TOKEN)
logger.info("Bot started")

# Saving user preferences locally
users = {}

bot.loop.run_until_complete(
    bot(functions.bots.SetBotCommandsRequest(
        commands=[
            types.BotCommand(
                command='start',
                description='Get the welcome message'),
            types.BotCommand(
                command='help',
                description='How to use the bot'),
            types.BotCommand(
                command='settings',
                description='Change your preferences'),
            types.BotCommand(
                command='info',
                description='Get some useful information about the bot'),
            types.BotCommand(
                command='stats',
                description='Get some statistics about the bot'),
        ]
    ))
)


@bot.on(NewMessage())
async def init_user(event: NewMessage.Event):
    if event.chat_id not in users.keys():
        users[event.chat_id] = {
            "quality": "FLAC"
        }
