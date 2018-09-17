# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 08:29:50 2018

@author: Nicolaj Baramsky
install win32 gui from:
    https://stackoverflow.com/questions/20113456/installing-win32gui-python-module#20128310
    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32

    Step 1: Download the pywin32....whl
    Step 2: pip install pywin32....whl
    Step 3: C:\python32\python.exe Scripts\pywin32_postinstall.py -install
    Step 4: python
"""
import os
import sys
import win32gui
import time
import datetime
import pyautogui
import msvcrt
import configparser
import numpy as np
import csv
from analytics import Analytics

last_time_key_pressed = time.time()
last_time_mouse_moved = time.time()
last_mouse_coords = [0, 0]
start_of_event = time.time()
last_window = 'start tracking'
last_event = ''
idle_time = 5*60
html_update_time = time.time() + 60

config = configparser.ConfigParser()
try:
    print(config.read('config.dat'))
    string_cats = config.items('CATEGORIES')
except Exception as e:
    print(e)
    print('Press ENTER to quit ...')
    input()


def main():
    global start_of_event
    global last_window
    global last_event
    global html_update_time

    analytic = Analytics()

    print("""
---------------------------------------
TRACK YOUR TIME - DON'T WASTE IT!
---------------------------------------

  TIME           CATEGORY""")

    while True:
        mouse_idle = is_mouse_idle()
        keyboard_idle = is_keyboard_idle(0.01)

        current_window = get_window_name()
        idle = mouse_idle and keyboard_idle

        if idle:
            current_event = 'idle'
        else:
            current_event = current_window


        if current_event != last_event:
            if last_event == 'idle':
                category = 'idle'
            else:
                category = analytic.get_cat(last_window)

            duration = time.time() - start_of_event
            if duration > 2:


                save_data([time.time(), category, int(duration)])
                try:
                    if sys.version_info.major >2:
                        mins = int(np.floor(duration/60))
                        secs = int(np.floor(duration - mins*60))
                        print("{0: 3}:{1:02} min\t".format(mins, secs),
                              "{}\t".format(category),
                              "({})".format(last_event[:30]))
                except UnicodeDecodeError:
                    print("{0: 5.0f} s\t".format(duration), "UNICODE DECODE ERROR")

            last_window = current_window
            start_of_event = time.time()
            last_event = current_event

        if time.time() > html_update_time:
            analytic.create_html()
            html_update_time = time.time()+ 60

def is_idle_category(window):
    """
    returns True if the window title can be categorized as an idle window
    """
    for string, cat in string_cats:
        if string in window:
            if cat == 'idle':
                return True
    return False


def save_data(data):
    today = datetime.datetime.now()
    folder = 'data/'
    filename = '{0:d}-{1:02d}-{2:02d}.csv'.format(today.year, today.month, today.day)
    #filename = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'
    path = folder + filename
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=',', lineterminator="\r")
        writer.writerow(data)


def is_mouse_idle():
    global last_time_mouse_moved
    global last_mouse_coords
    global idle_time

    try:
        x, y = pyautogui.position()
        mouse_coords = [x,y]
    except:
        pass

    if mouse_coords != last_mouse_coords:
        last_mouse_coords = [x, y]
        last_time_mouse_moved = time.time()
    elif time.time() > last_time_mouse_moved + idle_time:
        return True

    return False


def get_window_name():
    try:
        parent = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(parent).lower()
        window_name = window_name.replace(',', '')
        window_name = window_name.lower().encode("latin_1", "ignore")
        window_name = window_name.lower().decode("latin_1", "ignore")
        return window_name
    except win32gui.error as E:
        print(E)


def is_keyboard_idle(sleep_duration):
    global last_time_key_pressed
    global idle_time

    time.sleep(sleep_duration)
    key_pressed = msvcrt.kbhit()

    if key_pressed:
        #keys = msvcrt.getch() # reads the keys and resets kbhit()
        last_time_key_pressed = time.time()

    if time.time() > last_time_key_pressed + idle_time:
        return True
    return False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Process interrupted.')
    except Exception as e:
        print (e)
    finally:
        print('Press ENTER to quit ...')
        input()
