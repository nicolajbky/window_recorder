# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 08:29:50 2018

@author: Nicolaj Baramsky
install win32 gui from:
    https://stackoverflow.com/questions/20113456/installing-win32gui-python-module#20128310

    Step 1: Download the pywin32....whl
    Step 2: pip install pywin32....whl
    Step 3: C:\python32\python.exe Scripts\pywin32_postinstall.py -install
    Step 4: python
"""

import win32gui
import time
import pyautogui
import keyboard



def main():
    for _ in range(100):
        print(get_window_name())
        get_mouse_coord()
        get_key_pressed()
        time.sleep(1)

    print('done')


def get_key_pressed():
    try: #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):#if key 'q' is pressed
            print('You Pressed A Key!')
        else:
            pass
    except:
        pass


def get_mouse_coord():
    try:
        x, y = pyautogui.position()
        #positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        return x, y
    except:
        pass



def get_window_name():
    try:
        parent = win32gui.GetForegroundWindow()
        fg_window_name = win32gui.GetWindowText(parent).lower()
        return fg_window_name
    except win32gui.error as E:
        print(E)



if __name__ == '__main__':
    main()