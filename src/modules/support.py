import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from data.config import ADMIN_IDS, STRINGS, TG_ID_SUPPORT_CHAT
from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter


router = Router(name=__name__)


class Support(StatesGroup):
	question = State()


@router.message(Command('help'), ChatTypeFilter('private'))
async def support(message: types.Message, state: FSMContext):
	await state.set_state(Support.question)
	await message.answer(STRINGS['SUPPORT_TEXT'])


@router.message(Support.question, ChatTypeFilter('private'))
async def send_question(message: types.Message, state: FSMContext):
	forwarded_message = await message.copy_to(TG_ID_SUPPORT_CHAT)

	user_info = f'\n\n{message.from_user.id} | @{message.from_user.username}'

	try:
		if message.caption:
			await bot.edit_message_caption(
				chat_id=TG_ID_SUPPORT_CHAT,
				message_id=forwarded_message.message_id,
				caption=message.caption + user_info,
			)
		else:
			await bot.edit_message_text(
				chat_id=TG_ID_SUPPORT_CHAT,
				message_id=forwarded_message.message_id,
				text=message.text + user_info,
			)
	except Exception as exc:
		logging.error(exc)

	await state.clear()


@router.message(ChatTypeFilter('support'))
async def send_answer(message: types.Message):
	if message.from_user.id not in ADMIN_IDS:
		return

	if not message.reply_to_message:
		return

	try:
		replied_message = message.reply_to_message

		if replied_message.caption:
			user_id = int(replied_message.caption.split('\n')[-1].split('|')[0])
		else:
			user_id = int(replied_message.text.split('\n')[-1].split('|')[0])

		await message.copy_to(user_id)
	except Exception as exc:
		logging.error(exc)
