import logging

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from data.config import STRINGS

from db.db_api import user_exists, add_user, \
	get_test, add_user_test, user_test_exists, \
	get_user_test, get_ref_test, update_user_test

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter
from modules.common.keyboard import get_answer_kb


router = Router(name=__name__)


@router.message(Command('start'), ChatTypeFilter('private'))
async def start(message: types.Message, command: CommandObject):
	test_code = referrer = campaign = None

	if not command.args:
		await message.answer(STRINGS['START_ERROR_TEXT'])
	else:
		args = command.args.split('_')

		test_code = args[0]

		if len(args) > 2:
			if args[1] == 'r':
				referrer = args[2]
			elif args[1] == 'c':
				campaign = args[2]

	if not await user_exists(message.from_user.id):
		await add_user(
			message.from_user.id,
			message.from_user.username,
			message.from_user.first_name,
			message.from_user.last_name,
			referrer,
			campaign
		)

		if referrer and test_code:
			try:
				test = await get_test(test_code)
			except Exception as exc:
				logging.error(exc)
				return await message.answer(STRINGS['START_ERROR_TEXT'])

			user_test = await get_ref_test(referrer, test_code)

			if user_test:
				await bot.send_message(referrer, test.full_link)

				await update_user_test(referrer, test_code, full_via_ref=True)

	if test_code:
		try:
			test = await get_test(test_code)
		except Exception as exc:
			logging.error(exc)
			return await message.answer(STRINGS['START_ERROR_TEXT'])

		answers = str()

		if await user_test_exists(message.from_user.id, test_code):
			user_test = await get_user_test(message.from_user.id, test_code)
			question_num = str(user_test.question_num)
			question = test.questions[question_num]

			for i, answer in enumerate(question['answers'], 1):
				answers += f'<b>{i}.</b> {answer}\n'

			await message.answer(
				f'<b>{question_num}. {question["question"]}</b>\n\n{answers}',
				reply_markup=await get_answer_kb(test_code, question_num),
				parse_mode='HTML'
			)

		else:
			question = test.questions['1']

			for i, answer in enumerate(question['answers'], 1):
				answers += f'<b>{i}.</b> {answer}\n'

			await message.answer(test.first_message)
			await message.answer(
				f'<b>1. {question["question"]}</b>\n\n{answers}',
				reply_markup=await get_answer_kb(test_code, 1),
				parse_mode='HTML'
			)

			await add_user_test(message.from_user.id, test_code)
