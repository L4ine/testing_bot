from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.config import STRINGS


async def get_answer_kb(
	test_code: str,
	question_num: int | str
) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for i in range(4):
		builder.button(
			text=f"{i+1}",
			callback_data=f"answ_{test_code}_{question_num}_{i}"
		)
	return builder.as_markup()


async def get_want_full_kb(
	test_code: str,
	full_by_ref: bool
) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=STRINGS["BUY_BUTTON"],
		callback_data=f"buy_{test_code}"
	)
	if full_by_ref:
		builder.button(
			text=STRINGS["REF_BUTTON"],
			callback_data=f"ref_{test_code}"
		)
	return builder.as_markup()


async def get_buy_kb(
	test_code: str
) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=STRINGS["DONE_BUTTON"],
		callback_data=f"done_{test_code}"
	)
	return builder.as_markup()


async def get_send_full_kb(
	test_code: str
) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=STRINGS["SEND_BUTTON"],
		callback_data=f"send_{test_code}"
	)
	return builder.as_markup()
