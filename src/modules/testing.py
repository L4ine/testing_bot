import logging

from aiogram import Router, types, F

from data.config import STRINGS, TG_ID_BUY_CHAT

from db.db_api import get_test, get_user_test, \
	update_user_test
from db.models import Test

from modules.common.loader import bot
from modules.common.keyboard import get_answer_kb, \
	get_want_full_kb


router = Router(name=__name__)


@router.callback_query(F.data.startswith('answ_'))
async def answer(callback: types.CallbackQuery):
	test_code, question_num, answer = callback.data.split("_")[1:]
	answer = int(answer)

	user_test = await get_user_test(callback.from_user.id, test_code)

	if not user_test:
		return await callback.answer(STRINGS['TEST_ALREADY_COMPLETE_TEXT'])

	if user_test.question_num != int(question_num):
		return await callback.answer(STRINGS['TEST_WRONG_QUESTION_TEXT'])

	test = await get_test(test_code)

	if not test:
		return await callback.answer(STRINGS['TEST_NOT_FOUND'])

	await callback.answer()

	cur_question = test.questions[question_num]

	if test.show_answers:
		await callback.message.answer(cur_question['comment'][answer])

	try:
		await update_user_test(
			callback.from_user.id,
			test_code,
			points=cur_question['points'][answer],
			question_num=int(question_num) + 1,
			is_finished=user_test.question_num == len(test.questions)
		)
	except Exception as exc:
		logging.error(exc)
		return await callback.message.answer(STRINGS['TEST_ERROR_TEXT'])

	if user_test.question_num == len(test.questions):
		await send_final_message(
			callback,
			test,
			user_test.points + cur_question['points'][answer]
		)
	else:
		await send_next_question(callback, test, question_num)


async def send_final_message(
	callback: types.CallbackQuery,
	test: Test,
	points: int
):
	if test.last_message:
		points_scale = STRINGS['TEST_POINTS_SCALE_TEXT'] + '\n'.join(
			f'{value} - {key}' for key, value in test.points_scale.items()
		)

		try:
			last_message = test.last_message.format(
				points=points
			)
		except Exception:
			last_message = test.last_message

		await callback.message.answer(
			last_message + points_scale
		)

		await bot.send_message(
			TG_ID_BUY_CHAT,
			STRINGS['TEST_FINISHED_NOTIFY'].format(
				name=f'{callback.from_user.first_name} {callback.from_user.last_name}',
				username=callback.from_user.username,
				test_name=test.name,
				points=points
			)
		)

	if not test.is_free:
		await callback.message.answer(
			STRINGS['TEST_END_TEXT'],
			reply_markup=await get_want_full_kb(test.code, test.full_by_ref)
		)
	else:
		if test.full_link:
			await callback.message.answer(test.full_link)


async def send_next_question(
	callback: types.CallbackQuery,
	test: Test,
	question_num: int
):
	answers = str()
	next_question_num = str(int(question_num) + 1)
	next_question = test.questions[next_question_num]

	for i, answer in enumerate(next_question['answers'], 1):
		answers += f'<b>{i}.</b> {answer}\n'

	await callback.message.answer(
		f'{next_question_num}. <b>{next_question["question"]}</b>\n\n{answers}',
		reply_markup=await get_answer_kb(test.code, next_question_num),
		parse_mode='HTML'
	)
