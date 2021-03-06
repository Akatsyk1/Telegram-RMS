from specpc import *
import os
import json
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import keyboard

admins = [] # admin IDs
bot = Bot(token='', parse_mode=types.ParseMode.HTML) # token bot
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    buttons = ['Get screenshot 💻', 'Switch off pc 🔴', 'Block keyboard, mouse 🐀', 'Unblock keyboard, mouse 🐀',
               'Get list tasks 👦', 'Restart computer 🖥']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(f'{hbold("Commands: ")} \n' \
                         f'{hbold("/alert <message> Displays a dialog box with the message you passed in the argument. ")} \n' \
                         f'{hbold("/killp <process> Terminates a process.")} \n', reply_markup=keyboard)


@dp.message_handler(commands='killp')
async def command_killprocess(message: types.Message):
    if message.from_user.id in admins:
        args = message.text.split()
        if args == 0:
            await bot.send_message(message.chat.id, text=f'{hbold("More than one process cannot be allowed.")}')
            return
        elif len(args) > 2:
            await bot.send_message(message.chat.id, text=f'{hbold("Only one process can be terminated")}')
            return
        try:
            kill_process(args[1])
        except Exception:
            await bot.send_message(message.chat.id, text='There is no such process.')
            return


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
            await bot.send_message(message.chat.id, text=text, disable_notification=True)
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
