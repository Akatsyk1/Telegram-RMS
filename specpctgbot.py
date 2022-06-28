#╔══╦═══╦═══╦══╦════╦══╦═══╗
#║╔═╣╔═╗║╔══╣╔╗╠═╗╔═╣╔╗║╔═╗║
#║║─║╚═╝║╚══╣╚╝║─║║─║║║║╚═╝║
#║║─║╔╗╔╣╔══╣╔╗║─║║─║║║║╔╗╔╝
#║╚═╣║║║║╚══╣║║║─║║─║╚╝║║║║
#╚══╩╝╚╝╚═══╩╝╚╝─╚╝─╚══╩╝╚╝
#╔══╦╗╔══╦══╦════╦══╦╗╔╦╗╔══╗╔╗
#║╔╗║║║╔═╣╔╗╠═╗╔═╣╔═╣║║║║║╔═╬╝║
#║╚╝║╚╝║─║╚╝║─║║─║╚═╣╚╝║╚╝║─╚╗║
#║╔╗║╔╗║─║╔╗║─║║─╚═╗╠═╗║╔╗║──║║
#║║║║║║╚═╣║║║─║║─╔═╝║╔╝║║║╚═╗║║
#╚╝╚╩╝╚══╩╝╚╝─╚╝─╚══╝╚═╩╝╚══╝╚╝

from specpc import *
import os
import json
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import keyboard

admins = [] # id user admins, example: 871278
bot = Bot(token='', parse_mode=types.ParseMode.HTML) #bot token
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    buttons = ['Get screenshot 💻', 'Switch off pc 🔴', 'Block keyboard, mouse 🐀', 'Unblock keyboard, mouse 🐀',
               'Get list tasks 👦','Restart computer 🖥']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(f'{hbold("Commands: ")} \n {hbold("/alert <message> Displays a dialog box with the message you passed in the argument.")} \n', reply_markup=keyboard)


@dp.message_handler(commands='alert')
async def command_showalert(message: types.Message):
    if message.from_user.id in admins:
        args = message.text.split()
        if len(args) < 2:
            await bot.send_message(message.chat.id, text='Enter the command with at least one argument.')
            return
        show_alert(text=args[1:])
    else:
        return


@dp.message_handler(Text(equals='Restart computer 🖥'))
async def command_refreshcomputer(message: types.Message):
    if message.from_user.id in admins:
        refresh_pc()
    else:
        return


@dp.message_handler(Text(equals='Get list tasks 👦'))
async def command_listtasks(message: types.Message):
    if message.from_user.id in admins:
        print(f"{message.chat.username} get list tasks")
        list_tasks = get_process()
        for task in list_tasks:
            text = hbold(task)
            await bot.send_message(message.chat.id, text=text)
    else:
        return


@dp.message_handler(Text(equals='Switch off pc 🔴'))
async def command_offpc(message: types.Message):
    if message.from_user.id in admins:
        print(f"{message.chat.username} off pc")
        off_pc()
    else:
        return


@dp.message_handler(Text(equals='Block keyboard, mouse 🐀'))
async def block_keyboard_mouse(message: types.Message):
    if message.from_user.id in admins:
        off_keyboard_mouse()
    else:
        return


@dp.message_handler(Text(equals='Unblock keyboard, mouse 🐀'))
async def block_keyboard_mouse(message: types.Message):
    if message.from_user.id in admins:
        on_keyboard_mouse()
    else:
        return


@dp.message_handler(Text(equals='Get screenshot 💻'))
async def command_getscreenshoot(message: types.Message):
    if message.from_user.id in admins:
        print(f"{message.chat.username} get screen")
        photo = get_screen_shot('C:\ProgramData\screen.png')
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        os.remove(path='C:\ProgramData\screen.png')
    else:
        return


if __name__ == '__main__':
    executor.start_polling(dp)
