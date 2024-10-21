import json


with open('settings.json', 'r') as file:
    settings = json.load(file)

DATABASE_HOST: str = settings['DATABASE_HOST']
DATABASE_NAME: str = settings['DATABASE_NAME']
DATABASE_USER: str = settings['DATABASE_USER']
DATABASE_PASS: str = settings['DATABASE_PASS']

DATABASE_URL = 'postgresql+asyncpg://{user}:{passw}@{host}/{name}'.format(
    user=DATABASE_USER,
    passw=DATABASE_PASS,
    host=DATABASE_HOST,
    name=DATABASE_NAME
)

BOT_TOKEN: str = settings['BOT_TOKEN']
BOT_USERNAME: str = settings['BOT_USERNAME']

ADMIN_IDS: list[int] = settings['ADMIN_IDS']

TG_ID_BUY_CHAT: int = settings['TG_ID_BUY_CHAT']
TG_ID_SUPPORT_CHAT: int = settings['TG_ID_SUPPORT_CHAT']

STRINGS: dict[str, str] = settings['STRINGS']
