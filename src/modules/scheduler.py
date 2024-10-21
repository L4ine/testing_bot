import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from data.config import STRINGS

from db.db_api import get_uncompleted_tests

from modules.common.loader import bot
from modules.stats import scheduler_stats


async def check_tests_to_push():
	tests = await get_uncompleted_tests()

	for test in tests:
		try:
			await bot.send_message(
				test.tg_id,
				STRINGS['TEST_UNCOMPLITED_NOTIFY']
			)
		except Exception as exc:
			logging.error(exc)


async def initialize_scheduler():
	scheduler = AsyncIOScheduler()
	scheduler.add_job(scheduler_stats, CronTrigger(hour=0, minute=0))
	scheduler.add_job(check_tests_to_push, CronTrigger(hour=0, minute=0))
	scheduler.start()
