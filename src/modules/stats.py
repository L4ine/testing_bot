import logging

from aiogram import Router, types
from aiogram.filters import Command

from data.config import ADMIN_IDS, TG_ID_BUY_CHAT

from db.db_api import get_stats

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter
from modules.utils import format_stats_message


router = Router(name=__name__)


@router.message(Command('stats'), ChatTypeFilter('private'))
async def stats(message: types.Message):
	if message.from_user.id not in ADMIN_IDS:
		return

	stats = await get_stats()

	await message.answer(format_stats_message(stats))


async def scheduler_stats():
	stats = await get_stats()
	stats_text = format_stats_message(stats)

	try:
		await bot.send_message(
			TG_ID_BUY_CHAT,
			stats_text
		)
	except Exception as exc:
		logging.error(exc)
