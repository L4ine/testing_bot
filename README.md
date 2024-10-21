# Testing Bot
Бот используется для проведения простых линейных тестов с 4-мя вариантами ответов. Это могут быть тесты на ЕГЭ, психологические тесты, любые классические тесты с вариантами ответа.

За каждый ответ начисляется определенное кол-во баллов, в конце баллы суммируются и согласно таблице очков определяется результат теста.

## Запуск
Для запуска достаточно иметь установленный Git, Docker и docker-compose.

Пошаговый мануал:

1. `git clone https://github.com/L4ine/bc_testing_bot.git`

2. `cd bc_testing_bot/deploy`.

3. `cp .env.example .env` и отредактируйте по необходимости.

4. Заполните settings.json по [примеру](#пример-settingsjson).

5. Если изменяли `deploy/.env`, то отредактируйте `sqlalchemy.url` в `src/db/alembic.ini`.

    Формат: `postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@testing_bot_db/{POSTGRES_DB}`

6. `docker-compose up --build -d`

7. Выполните команду [для обновления БД](#миграция-в-бд).

Поздравляю, бот запущен!

## Пример settings.json
```JSON
{
	"DATABASE_HOST": "testing_bot_db",
	"DATABASE_NAME": "Здесь {POSTGRES_DB}",
	"DATABASE_USER": "Здесь {POSTGRES_USER}",
	"DATABASE_PASS": "Здесь {POSTGRES_PASSWORD}",

	"BOT_TOKEN": "123456789:AAEEQQDDFFGGEEWD...",
	"BOT_USERNAME": "testing_bot",

	"ADMIN_IDS": [123456789, 987654321],

	"TG_ID_BUY_CHAT": -123456789,
	"TG_ID_SUPPORT_CHAT": -123456789,

    "STRINGS": {
        "Если где-то есть {такие скобки}": "То они должны быть в этом сообщении, если их убрать, что-нибудь {сломается}"
    }
}
```

## Миграция в БД
После обновления моделей, необходимо провести миграцию и обновить БД. Запустите контейнер с обновленными моделями и выполните следующую команду:

`docker exec -it testing_bot bash -c "cd db && python3 -m alembic revision --autogenerate && python3 -m alembic upgrade head"`

Если все сделано правильно, то в ответ выйдут только INFO логи, в случае ERROR логов проведите дебаг.

## Логи
Все важные события и ошибки логгируются. Для просмотра логов выполните:

`docker logs testing_bot`

Учтите, что при перезапуске контейнера логи также перезаписываются!