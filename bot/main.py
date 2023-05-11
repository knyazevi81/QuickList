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

bot = Bot(settings.TELEG_TOKEN, proxy=settings.PROXY_URL)
dp = Dispatcher(bot)
db = Database(settings.PATH_TO_DB)

openai.api_key = settings.OPEN_AI_TOKEN
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
            InlineKeyboardButton(text='🗣️ Ассистент', callback_data='ai'),
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
            InlineKeyboardButton(text='➖ Решить задачу', callback_data='kill_task'),
            InlineKeyboardButton(text='🚬 Задачи', callback_data='all_task'),
            InlineKeyboardButton(text='📍 Админ панель', callback_data='admin')   # нет
        )
    else:
        if db.is_ai_assistent(user_id):
            return InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='🗣️ Ассистент', callback_data='ai'),
                InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
                InlineKeyboardButton(text='➖ Решить задачу', callback_data='kill_task'),
                InlineKeyboardButton(text='🚬 Задачи', callback_data='all_task'),
                InlineKeyboardButton(text='👥 О нас', callback_data='about_us')
            )
        else:
            return InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='🗣️ получить ассистента', callback_data='how_ai'),
                InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
                InlineKeyboardButton(text='➖ Решить задачу', callback_data='kill_task'),
                InlineKeyboardButton(text='🚬 Задачи', callback_data='all_task'),
                InlineKeyboardButton(text='👥 О нас', callback_data='about_us')
            )


# Основные хэндлер
@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    if db.quest_user_in_db(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "Что такое Quicklist  это бот ассистент с искуственным интеллекто"
            "м ChatGPT, записывайте задачи и следите за их выполнением\n\n"
            "Идеи для доработки:\n"
            "~Добавить ии~\n"
            "Уведомление сделать нормально\n"
            "настроки уведомлений\n"
            "**************************************\n"
            "чтобы отключить или включить уведомления нажмите /updatenotifies",
            parse_mode="MarkdownV2",
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


@dp.message_handler(commands="uptask")
async def add_task_db(message: types.Message):
    if len(message.text.split()) == 1 and db.quest_user_in_db(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            " ⛔ Вы забыли ввести задание",
            reply_markup=double_main_button()
        )
    elif len(message.text.split()) != 1 and db.quest_user_in_db(message.from_user.id):
        db.add_task(message.from_user.id, str(message.text[8:]))
        await bot.send_message(
            message.from_user.id,
            '✅ задача успешно записана',
            reply_markup=double_main_button()
        )


@dp.message_handler(commands="deltask")
async def del_task_db(message: types.Message):
    if len(message.text.split()) == 1 and db.quest_user_in_db(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            " ⛔ Вы забыли ввести задание",
            reply_markup=double_main_button()
        )
    elif len(message.text.split()) != 1 and db.quest_user_in_db(message.from_user.id):
        try:
            if isinstance(int(message.text.split()[1]), int) and db.del_task(message.from_user.id, message.text.split()[1]):
                await bot.send_message(
                    message.from_user.id,
                    '✅ задача успешно удалена',
                    reply_markup=double_main_button()
                )
            else:
                await bot.send_message(
                    message.from_user.id,
                    '⛔ Вы не имеете доступ к этому задачи'
                )
        except ValueError:
            await bot.send_message(
                message.from_user.id,
                " ⛔ Неверно указан id",
                reply_markup=double_main_button()
            )


@dp.message_handler(commands="updatenotifies")
async def del_task_db(message: types.Message):
    if db.update_notifier(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "🔔 уведомления включены",
            reply_markup=double_main_button()
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "🔕 уведомления выключены",
            reply_markup=double_main_button()
        )


@dp.message_handler()
async def main_handler(message: types.Message):
    if message.text.split()[0] == settings.AUTH_TOKEN and not db.quest_user_in_db(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(
            message.from_user.id,
            " ✅ Вы успешно зарегистрировались!\n"
            "нажмите -> /menu"
        )
    elif message.text.split()[0] == settings.ADMIN_TOKEN and db.quest_user_in_db(
            message.from_user.id) and not db.is_admin(message.from_user.id):
        db.add_admin(message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            " ✅ Режим администратора активирован!\n"
            "Нажмите -> /menu"
        )
    elif message.text[0:3] == 'tok' and message.chat.type == 'private':
        if db.get_ai(message.from_user.id, message.text):
            await bot.send_message(
                message.from_user.id,
                " ✅ Вы успешно активировали ассистента",
                reply_markup=double_main_button())
        else:
            await bot.send_message(
                message.from_user.id,
                " ⛔ Токен не работает",
                reply_markup=double_main_button()
            )
    else:
        if db.is_ai_assistent(message.from_user.id):
            await bot.send_message(
                message.from_user.id,
                '💤💤Запрос выполнятеся, подождите немного...',
                reply_to_message_id=message.message_id
            )
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=message.text,
                max_tokens=1024,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            await bot.edit_message_text(
                message_id=message.message_id + 1,
                chat_id=message.from_user.id,
                text=str(completion.choices[0].text),
                reply_markup=double_main_button()
            )

        else:
            await bot.send_message(message.from_user.id,
                                   ' ⛔ У вас нет доступа к ассистенту',
                                   reply_markup=double_main_button()
                                   )


# INLINE HANDLERS
@dp.callback_query_handler(text="add_user")
async def send_auth(call: types.CallbackQuery):
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.from_user.id,
                                text="🗿 Для того чтобы зарегистрировать"
                                     "ся введите токен аунтетификации: "
                                )


@dp.callback_query_handler(text="add_task", )
async def add_task_def(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text='*Для того чтобы добавить задачу, напишите*\n\n'
        '*пример:*\n'
        '/uptask купить курицу к дню рождению\n'
        '/uptask сделать плов \n\n'
        'Нажмите на команду чтобы ее скопировать\n'
        'куда нажимать    ➡️   ```/uptask```     '.format(call.data),
        parse_mode="MarkdownV2",
        reply_markup=double_main_button()
    )


@dp.callback_query_handler(text="kill_task", )
async def add_task_def(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text='*Для того чтобы удалить задачу, напишите\n'
        '/deltask и айди задачи*\n\n'
        '*пример:*\n'
        '/deltask 1\n'
        '/deltask 8 \n\n'
        'Нажмите на команду чтобы ее скопировать\n'
        'куда нажимать    ➡️   ```/deltask```     '.format(call.data),
        parse_mode="MarkdownV2",
        reply_markup=double_main_button()
    )


@dp.callback_query_handler(text="double_main")
async def double_main(call: types.CallbackQuery):
    type_user = {
        1: "✅",
        0: "⛔"
    }
    data = f"*Основное меню Бота*\n" \
           f"*режим администрaтора:*  " \
           f"{type_user[int(db.is_admin(call.from_user.id))]}\n" \
           f"*ассистент GPT:*  " \
           f"{type_user[int(db.is_ai_assistent(call.from_user.id))]}\n" \

    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"‼️ {call.from_user.first_name} на данный\n"
        f"момент у тебя {db.now_tasks_num(call.from_user.id)} зада"
        f"ч"
    )

    await bot.send_message(
        call.message.chat.id,
        data.format(call.data),
        parse_mode="MarkdownV2",
        reply_markup=main_button(call.from_user.id)
    )


@dp.callback_query_handler(text="all_task")
async def about(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    data = db.how_undone_tasks(call.from_user.id)
    out_data = "--id--|-----description-----\n"
    for id_task, text_task in data:
        out_data += f"[{id_task}]-🟥: {text_task}\n"
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=out_data,
        reply_markup=double_main_button()
        )


@dp.callback_query_handler(text="ai")
async def about(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f'Знакомься @{call.from_user.first_name} это ИИ ChatGPT(3.5)\n'
        f'---------------------------------\n'
        f'❗ Старайтесь оканчивать ваши запросы к боту '
        f'восклицаетльным или вопросительным '
        f'знаком, иначе бот продолжит ваш вопрос'
        f'и ответит сам на себя\n'
        f'❗ GPT-3.5 плох в математике, относитесь к'
        f' его ответам с сомнением!\n'
        f'---------------------------------\n'
        f'Для того чтобы пообщаться с ним просто напиши в чат свой вопрос',
        reply_markup=double_main_button()
    )


@dp.callback_query_handler(text="how_ai")
async def about(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=f"{call.from_user.first_name} для того того чтобы получить доступ к и"
        f"и напиши @ilpdakz",
        reply_markup=double_main_button()
    )


@dp.callback_query_handler(text="about_us")
async def about(call: types.CallbackQuery):
    await bot.delete_message(message_id=call.message.message_id - 1, chat_id=call.from_user.id)
    await bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text="Меня зовут Хасан и я являюсь разработчиком Телеграмм-бота. Мой бот пр"
        "едназначен для помощи в организации вашей деятельности. Бот помогает "
        "вам отслеживать ваши результаты и достигать ваших целей а также может"
        " вам помочь в решении задач с помощью chat-gpt. Я постоянно работаю н"
        "ад улучшением и добавлением новых функций в бота, чтобы он мог предос"
        "тавлять вам лучший опыт. Если у вас есть какие-либо вопросы или предл"
        "ожения, пожалуйста, свяжитесь со мной. Я буду рад помочь вам. @ilpdak"
        "z",
        reply_markup=double_main_button()
    )


if __name__ == '__main__':
    executor.start_polling(dp)
