from sqlalchemy import Column, Integer, BigInteger, \
	String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)

	username = Column(String, nullable=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=True)

	referrer = Column(String, nullable=True)
	campaign = Column(String, nullable=True)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class UserTest(Base):
	__tablename__ = 'user_tests'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)
	test_code = Column(String, nullable=False)

	question_num = Column(Integer, default=1)
	points = Column(Integer, default=0)

	is_finished = Column(Boolean, default=False)
	finished_at = Column(DateTime, nullable=True)

	want_buy_full = Column(Boolean, default=False)  # Нажал "Получить разбор"
	full_via_buy = Column(Boolean, default=False)  # Получил разбор покупкой
	full_via_ref = Column(Boolean, default=False)  # Получил разбор рефералом

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Test(Base):
	__tablename__ = 'tests'

	id = Column(Integer, primary_key=True)

	name = Column(String, nullable=False)
	code = Column(String, nullable=False)

	is_free = Column(Boolean, default=False)
	show_answers = Column(Boolean, default=False)
	full_by_ref = Column(Boolean, default=False)
	notify_admin = Column(Boolean, default=False)

	first_message = Column(String, nullable=False)
	last_message = Column(String, nullable=False)

	full_link = Column(String, nullable=True)

	points_scale = Column(JSON, nullable=False)
	questions = Column(JSON, nullable=False)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
