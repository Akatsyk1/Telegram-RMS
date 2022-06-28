import keyboard
import pyautogui
import os
import time
import psutil
import ctypes


def get_screen_shot(path):
    pyautogui.screenshot(path)
    with open(path, 'rb') as file:
        src = file.read()
    return src


def off_pc():
    os.system('shutdown /p /f')


def off_keyboard_mouse():
    block = ctypes.windll.user32.BlockInput(True)


def on_keyboard_mouse():
    unlock = ctypes.windll.user32.BlockInput(False)


def get_process():
    t = []
    for processs in psutil.process_iter():
        t.append(f'{processs.name()} / {processs.status()} \n')
    return t


def show_alert(text):
    pyautogui.alert(text)


def refresh_pc():
    os.system('shutdown -r -t 0')


def kill_process(name):
    os.system(f'taskkill /f /im {name}')
