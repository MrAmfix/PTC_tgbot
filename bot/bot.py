from aiogram import Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN
from database.base import DataBase


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
rt = Router()


@rt.message(Command('start'))
async def start(msg: Message):
    await msg.reply('Привет!')
    try:
        # Сейчас делаю так, так как пока у нас всего 1 параметр
        userid = msg.text.split()[1].split('=')[1]
        if not DataBase.add_tgid_to_user(userid, msg.from_user.id):
            await msg.reply('Простите, но указанного пользователя не существует')
        else:
            await msg.reply('Телеграм аккаунт успешно привязан!')
    except IndexError:
        pass


@rt.message(Command('send_notification'))
async def send_notification(msg: Message):
    # Как будем вводить данные? Пока просто через пробел оставлю
    # /send_notification uid text
    try:
        datas = msg.text.split(maxsplit=2)
        tgid = DataBase.get_user_tgid(datas[1])
        if tgid is None:
            await msg.reply('Такого пользователя не существует или у него не привязан telegram')
        else:
            await bot.send_message(int(tgid), datas[2])
            await msg.reply('Уведомление отправлено!')
    except IndexError:
        pass


@rt.message(Command('add'))
async def add(msg: Message):
    DataBase.add_userid(msg.text.split()[1])
    await msg.reply('Ok!')
