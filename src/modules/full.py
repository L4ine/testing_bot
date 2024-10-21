from aiogram import Router, types, F

from data.config import STRINGS, BOT_USERNAME, \
	TG_ID_BUY_CHAT

from db.db_api import get_test, update_user_test

from modules.common.loader import bot
from modules.common.keyboard import get_buy_kb, \
	get_send_full_kb


router = Router(name=__name__)


@router.callback_query(F.data.startswith('buy_'))
async def buy(callback: types.CallbackQuery):
	test_code = callback.data.split("_")[1]

	await callback.message.answer(
		STRINGS['BUY_TEXT'],
		reply_markup=await get_buy_kb(test_code)
	)

	await callback.answer()

	test = await get_test(test_code)

	await bot.send_message(
		TG_ID_BUY_CHAT,
		STRINGS['WANT_BUY_NOTIFY'].format(
			name=f'{callback.from_user.first_name} {callback.from_user.last_name}',
			username=callback.from_user.username,
			test_name=test.name,
		)
	)

	await update_user_test(
		callback.from_user.id,
		test_code,
		want_buy_full=True
	)


@router.callback_query(F.data.startswith('ref_'))
async def ref(callback: types.CallbackQuery):
	test_code = callback.data.split("_")[1]

	await callback.message.answer(
		STRINGS['REF_TEXT'].format(
			username=BOT_USERNAME,
			test_code=test_code,
			user_id=callback.from_user.id
		)
	)

	await callback.answer()


@router.callback_query(F.data.startswith('done_'))
async def done(callback: types.CallbackQuery):
	test_code = callback.data.split("_")[1]

	await callback.answer(
		STRINGS['WAIT_CALLBACK'],
		show_alert=True
	)

	test = await get_test(test_code)

	await bot.send_message(
		TG_ID_BUY_CHAT,
		STRINGS['BUY_NOTIFY'].format(
			name=f'{callback.from_user.first_name} {callback.from_user.last_name}',
			username=callback.from_user.username,
			test_name=test.name,
		) + f'\n\nUser ID: {callback.from_user.id}',
		reply_markup=await get_send_full_kb(test_code)
	)


@router.callback_query(F.data.startswith('send_'))
async def send(callback: types.CallbackQuery):
	test_code = callback.data.split("_")[1]

	test = await get_test(test_code)

	await update_user_test(
		callback.from_user.id,
		test_code,
		full_via_buy=True
	)

	chat_id = int(callback.message.text.split('\n')[-1].split(':')[-1])

	await bot.send_message(
		chat_id,
		test.full_link,
	)

	await callback.answer(
		STRINGS['SENDED_CALLBACK'],
		show_alert=True
	)
