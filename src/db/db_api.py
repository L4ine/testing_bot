from typing import Optional

import logging

from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from data.config import DATABASE_URL

from db.models import User, UserTest, Test


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)


async def get_user(tg_id: int) -> Optional[User]:
	async with async_session() as session:
		query = select(User).where(User.tg_id == tg_id)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)


async def get_users() -> list[User]:
	async with async_session() as session:
		query = select(User)

		try:
			res = await session.execute(query)
			return res.scalars().all()
		except Exception as exc:
			logging.error(exc)
			return []


async def user_exists(tg_id: int) -> bool:
	return not not await get_user(tg_id)


async def add_user(
	tg_id: int,
	username: str,
	first_name: str,
	last_name: str,
	referrer: str,
	campaign: str,
) -> None:
	async with async_session() as session:
		new_user = User(
			tg_id=tg_id,
			username=username,
			first_name=first_name,
			last_name=last_name,
			referrer=referrer,
			campaign=campaign,
		)

		session.add(new_user)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def get_test(code: str) -> Optional[Test]:
	async with async_session() as session:
		query = select(Test).where(Test.code == code)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)
			return None


async def test_exists(code: int) -> bool:
	return not not await get_test(code)


async def add_test(
	name: str,
	code: str,
	is_free: bool,
	show_answers: bool,
	full_by_ref: bool,
	notify_admin: bool,
	first_message: str,
	last_message: str,
	full_link: Optional[str],
	points_scale: dict,
	questions: dict,
) -> None:
	async with async_session() as session:
		new_test = Test(
			name=name,
			code=code,
			is_free=is_free,
			show_answers=show_answers,
			full_by_ref=full_by_ref,
			notify_admin=notify_admin,
			first_message=first_message,
			last_message=last_message,
			full_link=full_link,
			points_scale=points_scale,
			questions=questions
		)

		session.add(new_test)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
			raise exc


async def get_user_test(tg_id: int, test_code: str) -> Optional[UserTest]:
	async with async_session() as session:
		query = select(UserTest).where(
			UserTest.tg_id == tg_id,
			UserTest.test_code == test_code,
			UserTest.is_finished == False
		)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)


async def get_ref_test(ref_id: int, test_code: str) -> Optional[UserTest]:
	async with async_session() as session:
		query = select(UserTest).where(
			UserTest.tg_id == ref_id,
			UserTest.test_code == test_code,
			UserTest.is_finished == True,
			UserTest.full_via_ref == False,
			UserTest.full_via_buy == False
		)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)


async def get_uncompleted_tests() -> list[UserTest]:
	async with async_session() as session:
		boundary_time = datetime.now() - timedelta(hours=24)

		query = select(UserTest).where(
			UserTest.is_finished == False,
			UserTest.updated_at < boundary_time
		)

		try:
			res = await session.execute(query)
			return res.scalars().all()
		except Exception as exc:
			logging.error(exc)
			return []


async def user_test_exists(tg_id: int, test_code: str) -> bool:
	return not not await get_user_test(tg_id, test_code)


async def add_user_test(
	tg_id: int,
	test_code: str,
) -> None:
	async with async_session() as session:
		new_user_test = UserTest(
			tg_id=tg_id,
			test_code=test_code
		)

		session.add(new_user_test)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
			raise exc


async def update_user_test(
	tg_id: int,
	test_code: str,
	question_num: Optional[int] = None,
	points: Optional[int] = None,
	is_finished: Optional[datetime] = None,
	want_buy_full: Optional[bool] = None,
	full_via_buy: Optional[bool] = None,
	full_via_ref: Optional[bool] = None,
) -> None:
	async with async_session() as session:
		query = select(UserTest).where(
			UserTest.tg_id == tg_id,
			UserTest.test_code == test_code,
			UserTest.is_finished == False
		)

		try:
			result = await session.execute(query)
			user_test: UserTest = result.scalars().first()

			if user_test is None:
				return

			if question_num:
				user_test.question_num = question_num

			if points:
				user_test.points = user_test.points + points

			if is_finished:
				user_test.is_finished = is_finished
				user_test.finished_at = datetime.now()

			if want_buy_full:
				user_test.want_buy_full = want_buy_full

			if full_via_buy:
				user_test.full_via_buy = full_via_buy

			if full_via_ref:
				user_test.full_via_ref = full_via_ref

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
			raise exc


async def get_stats() -> dict:
	async with async_session() as session:
		stats = {}

		yesterday = datetime.now() - timedelta(days=1)
		month_ago = datetime.now() - timedelta(days=30)

		# Общее количество пользователей
		query = select(func.count(User.id))
		stats['total_users'] = (await session.execute(query)).scalar()

		# Новые пользователи за сутки
		query = select(func.count(User.id)).where(User.created_at >= yesterday)
		stats['new_users_day'] = (await session.execute(query)).scalar()

		# Новые пользователи за месяц
		query = select(func.count(User.id)).where(User.created_at >= month_ago)
		stats['new_users_month'] = (await session.execute(query)).scalar()

		# Количество пройденных тестов за все время
		query = select(func.count(UserTest.id))
		stats['total_finished_tests'] = (await session.execute(query)).scalar()

		# Количество пройденных тестов за сутки
		query = (
			select(func.count(UserTest.id))
			.where(UserTest.finished_at >= yesterday)
		)
		stats['finished_tests_day'] = (await session.execute(query)).scalar()

		# Количество пройденных тестов за последние 30 дней
		query = (
			select(func.count(UserTest.id))
			.where(UserTest.finished_at >= month_ago)
		)
		stats['finished_tests_month'] = (await session.execute(query)).scalar()

		# Количество тестов с want_buy_full = True за все время
		query = select(func.count(UserTest.id)).where(
			UserTest.want_buy_full == True
		)
		stats['total_want_buy_full'] = (await session.execute(query)).scalar()

		# Количество тестов с want_buy_full = True за сутки
		query = select(func.count(UserTest.id)).where(
			UserTest.finished_at >= yesterday,
			UserTest.want_buy_full == True
		)
		stats['want_buy_full_day'] = (await session.execute(query)).scalar()

		# Количество тестов с want_buy_full = True за последние 30 дней
		query = select(func.count(UserTest.id)).where(
			UserTest.finished_at >= month_ago,
			UserTest.want_buy_full == True
		)
		stats['want_buy_full_month'] = (await session.execute(query)).scalar()

		return stats
