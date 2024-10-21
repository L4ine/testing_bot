import io
import random
import string
from datetime import datetime

import pandas

from data.config import STRINGS


def format_stats_message(stats):
	return STRINGS['STATS_TEXT'].format(
		date=datetime.now().strftime('%d.%m.%Y'),

		total_users=stats['total_users'],
		day_users=stats['new_users_day'],
		month_users=stats['new_users_month'],

		total_tests=stats['total_finished_tests'],
		day_tests=stats['finished_tests_day'],
		month_tests=stats['finished_tests_month'],

		total_want_buy_full=stats['total_want_buy_full'],
		day_want_buy_full=stats['want_buy_full_day'],
		month_want_buy_full=stats['want_buy_full_month']
	)


def generate_test_code(length=6):
	characters = string.ascii_letters + string.digits
	return ''.join(random.choice(characters) for _ in range(length))


def parse_test(file: io.BytesIO):
	df = pandas.read_excel(file, header=None)

	data = {}
	points_scale = {}
	questions = {}

	points_scale_parse = False
	questions_parse = False
	cur_question = None

	for row in df.itertuples():
		if points_scale_parse:
			if isinstance(row._3, float):
				points_scale_parse = False
				continue
			points_scale[row._3] = row._2

		if questions_parse:
			if isinstance(row._4, float):
				questions_parse = False
				continue
			if row._1 == 'Комментарий, когда выбран ответ':
				questions[cur_question]['comment'] = [row._4, row._5, row._6, row._7]
			elif row._1 == 'Сколько дается баллов за ответ':
				questions[cur_question]['points'] = [row._4, row._5, row._6, row._7]
			elif isinstance(row._2, int):
				cur_question = row._2
				questions[cur_question] = {
					'question': row._3,
					'answers': [row._4, row._5, row._6, row._7]
				}

		if isinstance(row._1, float):
			continue

		elif row._1 == 'Сетка баллов (если меньше или равно указанного значения)':
			points_scale_parse = True
			points_scale[row._3] = row._2

		elif row._1 == 'Номер вопроса':
			questions_parse = True
			cur_question = row._2
			questions[cur_question] = {
				'question': row._3,
				'answers': [row._4, row._5, row._6, row._7]
			}

		elif row._1 == 'Название теста':
			data['name'] = row._2

		elif row._1 == 'Бесплатный тест':
			data['is_free'] = row._2.lower() == 'да'

		elif row._1 == 'Показывать правильный ли ответ был дан?':
			data['show_answers'] = row._2.lower() == 'да'

		elif row._1 == 'Давать ли подробный ответ за приглашение друга в бота?':
			data['full_by_ref'] = row._2.lower() == 'да'

		elif row._1 == 'Уведомлять о прохождении теста в группу?':
			data['notify_admin'] = row._2.lower() == 'да'

		elif row._1 == 'Ссылка на файл с подробным разбором теста':
			data['full_link'] = row._2

		elif row._1 == 'Первое сообщение теста':
			data['first_message'] = row._2

		elif row._1 == 'Завершающее сообщение теста':
			data['last_message'] = row._2

	data['questions'] = questions
	data['points_scale'] = points_scale

	return data
