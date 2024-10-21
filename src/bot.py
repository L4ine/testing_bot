import asyncio
import logging

from modules.common.loader import dp, bot

from modules.full import router as full_router
from modules.start import router as start_router
from modules.stats import router as stats_router
from modules.support import router as support_router
from modules.mailing import router as mailing_router
from modules.testing import router as testing_router
from modules.create_test import router as create_test_router

from modules.scheduler import initialize_scheduler


if __name__ == "__main__":
	try:
		logging.basicConfig(
			format=u'%(filename)s [LINE:%(lineno)d] \
				#%(levelname)-8s [%(asctime)s]  %(message)s',
			level=logging.INFO,
		)

		loop = asyncio.new_event_loop()

		loop.create_task(initialize_scheduler())

		dp.include_router(full_router)
		dp.include_router(start_router)
		dp.include_router(stats_router)
		dp.include_router(support_router)
		dp.include_router(mailing_router)
		dp.include_router(testing_router)
		dp.include_router(create_test_router)

		loop.create_task(dp.start_polling(bot))
		logging.info('The bot is running...')

		loop.run_forever()

	except (KeyboardInterrupt, SystemExit):
		logging.error('Bot stopped!')
	except Exception as exc:
		logging.error(exc)
