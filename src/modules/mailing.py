import asyncio

from aiogram import Router, types
from aiogram.filters import Command

from data.config import STRINGS, ADMIN_IDS

from db.db_api import get_users

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter


router = Router(name=__name__)


@router.message(Command('send'), ChatTypeFilter('private'))
async def notify(message: types.Message):
	if message.from_user.id not in ADMIN_IDS:
		return

	if not message.reply_to_message:
		return await message.answer(STRINGS['MAILING_REPLY_TEXT'])

	await message.answer(STRINGS['MAILING_CREATED_TEXT'])

	succeses = 0
	errors = 0

	users = await get_users()

	for user in users:
		try:
			await bot.copy_message(
				from_chat_id=message.chat.id,
				chat_id=user.tg_id,
				message_id=message.reply_to_message.message_id
			)
			succeses += 1
		except Exception:
			errors += 1

		asyncio.sleep(0.5)

	await message.answer(
		STRINGS['MAILING_RESULT_TEXT'].format(
			total=len(users),
			succeses=succeses,
			errors=errors
		)
	)
