import logging

from aiogram import Router, types
from aiogram.filters import Command

from data.config import STRINGS, ADMIN_IDS, BOT_USERNAME

from db.db_api import add_test

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter
from modules.utils import parse_test, generate_test_code


router = Router(name=__name__)


@router.message(Command('create_test'), ChatTypeFilter('private'))
async def create_test(message: types.Message):
	if message.from_user.id not in ADMIN_IDS:
		return

	if not message.reply_to_message:
		return await message.answer(STRINGS['CREATE_TEST_REPLY_TEXT'])

	if not message.reply_to_message.document:
		return await message.answer(STRINGS['CREATE_TEST_REPLY_TEXT'])

	await message.answer(STRINGS['CREATE_TEST_START_TEXT'])

	file = await bot.download(message.reply_to_message.document)
	test = parse_test(file)
	code = generate_test_code()

	try:
		await add_test(
			test['name'],
			code,
			test['is_free'],
			test['show_answers'],
			test['full_by_ref'],
			test['notify_admin'],
			test['first_message'],
			test['last_message'],
			test['full_link'],
			test['points_scale'],
			test['questions']
		)
	except Exception as exc:
		logging.error(exc)
		return await message.answer(
			STRINGS['CREATE_TEST_ERROR_TEXT'].format(
				error=exc
			)
		)

	await message.answer(
		STRINGS['CREATE_TEST_RESULT_TEXT'].format(
			username=BOT_USERNAME,
			test_code=code
		)
	)
