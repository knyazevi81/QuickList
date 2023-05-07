# aigram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

# Modules
import settings
from read_database import Database

""" First settings. """
storage = MemoryStorage()
bot = Bot(settings.TELEG_TOKEN)
dp = Dispatcher(bot, storage)
db = Database(settings.PATH_TO_DB)


# _______Keyboards_______
def auth_keyboad() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Зарегистрироваться', callback_data='add_user')
    )


# ______Machine__________
class Auth(StatesGroup):
    token = State()


# Основные хэндлер
@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    if db.quest_user_in_db(message.from_user.id):
        pass
    else:
        await bot.send_message(message.from_user.id, f'🧩 Привет {message.from_user.username}!\n'
                                                     f'Для того чтобы зарегист'
                                                     f'рироватся нажми на кнопку', reply_markup=auth_keyboad())
        settings.LAST_MESSAGE.append(message.message_id + 1)
        settings.LAST_USER.append(message.from_user.id)


@dp.message_handler(content_types=["token"], state=Auth)
async def get_token(message: types.Message, state: FSMContext):
    if message.text == settings.AUTH_TOKEN:
        await bot.send_message(message.from_user.id, 'Nice')
    else:
        await bot.send_message(message.from_user.id, 'Not Nice')


# INLINE HANDLERS
@dp.callback_query_handler(text="add_user")
async def send_auth(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=settings.LAST_MESSAGE[-1],
                                chat_id=settings.LAST_USER[-1],
                                text="🗿 Для того чтобы зарегистрировать"
                                     "ся введите токен аунтетификации: ")
    await Auth.token.set()  # set token to auth


if __name__ == '__main__':
    executor.start_polling(dp)
