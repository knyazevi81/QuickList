# aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
# AI
import openai

# Modules
import settings
from read_database import Database

""" First settings. """
bot = Bot(settings.TELEG_TOKEN)
dp = Dispatcher(bot)
db = Database(settings.PATH_TO_DB)

# openai.api_key = config.ai_token
model_engine = 'text-davinci-003'
max_tokens = 128


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
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),  # нет
            InlineKeyboardButton(text='🚬 все задачи', callback_data='all_task'),  # нет
            InlineKeyboardButton(text='👥 о нас', callback_data='about_us'),  # нет
            InlineKeyboardButton(text='📍 Админ панель', callback_data='admin')   # нет
        )
    else:
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
            InlineKeyboardButton(text='👥 о нас', callback_data='about_us'),
            InlineKeyboardButton(text='🚬 Все задачи', callback_data='all_task')
        )


# Основные хэндлер
@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    if db.quest_user_in_db(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "Что такое Quicklist",
            reply_markup=double_main_button()
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f'🧩 Привет {message.from_user.username}!\n'
            f'Для того чтобы зарегист'
            f'рироватся нажми на кнопку',
            reply_markup=auth_keyboad()
        )


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
    await bot.edit_message_text(message_id=callback.message.message_id,
                                chat_id=callback.from_user.id,
                                text="🗿 Для того чтобы зарегистрировать"
                                     "ся введите токен аунтетификации: "
                                     f"{callback.message.message_id}")


@dp.callback_query_handler(text="add_task", )
async def add_task_def(call: types.CallbackQuery):
    await bot.send_message(
        call.message.chat.id,
        'уцацуа'.format(call.data),
        reply_markup=double_main_button()
    )


@dp.callback_query_handler(text="double_main")
async def double_main(call: types.CallbackQuery):
    type_user = {
        1: "✅",
        0: "⛔"
    }
    data = f"**Основное меню Бота**\n" \
           f"режим администрaтора:  " \
           f"{type_user[int(db.is_admin(call.from_user.id))]}\n" \
           f"ассистент:  " \
           f"{type_user[int(db.is_ai_assistent(call.from_user.id))]}\n" \

    await bot.send_message(
        call.message.chat.id,
        data.format(call.data),
        parse_mode="MarkdownV2",
        reply_markup=main_button(call.from_user.id)
    )


if __name__ == '__main__':
    executor.start_polling(dp)
