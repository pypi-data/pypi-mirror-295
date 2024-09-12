#!/usr/bin/env python3
from pynput import keyboard
from datetime import datetime

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            keys_pressed.add(keyboard.Key.ctrl_l)
        elif key == keyboard.KeyCode.from_char('d'):
            keys_pressed.add(keyboard.KeyCode.from_char('d'))

        if keyboard.Key.ctrl_l in keys_pressed and keyboard.KeyCode.from_char('d') in keys_pressed:
            type_datetime()
            keys_pressed.clear()
    except AttributeError:
        pass

def on_release(key):
    try:
        if key in keys_pressed:
            keys_pressed.remove(key)
    except AttributeError:
        pass

def type_datetime():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    controller.type(current_time)

keys_pressed = set()
controller = keyboard.Controller()

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
