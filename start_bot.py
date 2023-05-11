import multiprocessing
import os
import bot.settings


def telegram_bot():
    os.system(bot.settings.NIX_PATH + "main.py")


def notifier():
    os.system(bot.settings.NIX_PATH + "notif.py")


if __name__ == '__main__':
    p2 = multiprocessing.Process(target=notifier())
    print(1)
    p1 = multiprocessing.Process(target=telegram_bot())
    print(2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
