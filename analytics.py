# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 08:36:12 2018

@author: Nicolaj Baramsky
"""

import pandas as pd
import configparser
import numpy as np
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read('categories.dat')
string_cats = config.items('CATEGORIES')


def main():
    df = pd.read_csv('data/log.csv', encoding = "ISO-8859-1", names=['time', 'window', 'duration'])
    df['category'] = df.window.apply(get_cat)
    u_cats = get_unique_categories(string_cats) # unique category name
    u_dur = [] # duratio of unice category
    print('')
    print('')
    print('{} min total'.format(np.sum(df.duration)%60))
    print('')

    for u_cat in u_cats:
        temp = df.loc[df.category == u_cat]
        dur = np.sum(temp.duration)
        u_dur.append(dur)
        print('{1: 6} min  {0:} '.format(u_cat, dur%60))

    plt.figure()
    plt.pie(u_dur, labels=u_cats, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()


def get_unique_categories(string_cats):
    u_cats = []

    for string, cat in string_cats:
        if cat not in u_cats:
            u_cats.append(cat)

    return u_cats


def get_cat(window):
    for string, category in string_cats:
        if string in window:
            return category
            break
    return ''


if __name__ == '__main__':
    main()
