import pyautogui
import os
import time
import psutil
def get_screen_shot(path):
    pyautogui.screenshot(path)
    with open(path, 'rb') as file:
        src = file.read()
    return src

def off_pc():
    os.system('shutdown /p /f')

def off_keyboard_mouse():
    ctypes.user32.BlockInput(True)


def on_keyboard_mouse():
    ctypes.user32.BlockInput(False)


def get_process():
    t = []
    for processs in psutil.process_iter():
        t.append(f'{processs.name()} / {processs.status()} \n')
    return t

