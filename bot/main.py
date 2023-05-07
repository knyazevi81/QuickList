# aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

# Modules
import settings
from read_database import Database

""" First settings. """
bot = Bot(settings.TELEG_TOKEN)
dp = Dispatcher(bot)
db = Database(settings.PATH_TO_DB)


# _______Keyboards_______
def auth_keyboad() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='👥Зарегистрироваться', callback_data='add_user')
    )


def double_main_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='главное меню', callback_data='double_main')
    )


def main_button(user_id: int) -> InlineKeyboardMarkup:
    if db.is_admin(user_id):
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
            InlineKeyboardButton(text='🚬 все задачи', callback_data='all_task'),
            InlineKeyboardButton(text='📍 Админ панель', callback_data='admin')
        )
    else:
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
            InlineKeyboardButton(text='🚬 Все задачи', callback_data='all_task')
        )


# Основные хэндлер
@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    if db.quest_user_in_db(message.from_user.id):
        await bot.send_message(message.from_user.id, f"👤 Привет @{message.from_user.username}"
                                                     f"🅰 режим администартора - {None}",
                               reply_markup=main_button(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f'🧩 Привет {message.from_user.username}!\n'
                                                     f'Для того чтобы зарегист'
                                                     f'рироватся нажми на кнопку', reply_markup=auth_keyboad())
    settings.LAST_MESSAGE.append(message.message_id + 1)
    settings.LAST_USER.append(message.from_user.id)


@dp.message_handler()
async def main_handler(message: types.Message):
    if message.text.split()[0] == settings.AUTH_TOKEN and not db.quest_user_in_db(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.from_user.id, "✅ Вы успешно зарегистрировались!\n"
                                                     "нажмите -> /menu")
    elif message.text.split()[0] == settings.ADMIN_TOKEN and db.quest_user_in_db(
            message.from_user.id) and not db.is_admin(message.from_user.id):
        db.add_admin(message.from_user.id)
        await bot.send_message(message.from_user.id, "✅ Режим администратора активирован!\n"
                                                     "Нажмите -> /menu")


# INLINE HANDLERS
@dp.callback_query_handler(text="add_user")
async def send_auth(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=settings.LAST_MESSAGE[-1],
                                chat_id=settings.LAST_USER[-1],
                                text="🗿 Для того чтобы зарегистрировать"
                                     "ся введите токен аунтетификации: ")


@dp.callback_query_handler(text="add_task")
async def add_task_def(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=settings.LAST_MESSAGE[-1],
                                chat_id=settings.LAST_USER[-1],
                                text="ТЕСТ")


@dp.callback_query_handler(text="double_main")
async def double_main(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=settings.LAST_MESSAGE[-1],
                                chat_id=settings.LAST_USER[-1],
                                text=f"👤 Привет @{message.from_user.username}"
                                     f"🅰 режим администартора - {None}")


if __name__ == '__main__':
    executor.start_polling(dp)
