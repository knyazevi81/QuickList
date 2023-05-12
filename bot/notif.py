import notifiers
import time
import settings
import read_database


def how_hours(hours: int):
    return hours * 3600


def up_notification():
    curs = read_database.Database(settings.PATH_TO_DB)
    while True:
        telegram = notifiers.get_notifier('telegram')
        time.sleep(4)
        telegram.notify(
            token=settings.TELEG_TOKEN,
            chat_id=settings.ADMIN_ID,
            message='бот успешно работает!'
        )
        data_users: list = curs.all_user_to_notifier()
        for users in data_users:
            how_tasks: int = curs.now_tasks_num(users[0])
            if how_tasks > 0:
                telegram.notify(token=settings.TELEG_TOKEN,
                                chat_id=(users[0]),
                                message=f'❗ у вас {curs.now_tasks_num(users[0])} '
                                        f'нерешенных задач'
                                )


if __name__ == '__main__':
    up_notification()
