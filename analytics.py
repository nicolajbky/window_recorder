# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 08:36:12 2018

@author: Nicolaj Baramsky
"""
import os
import datetime
import pandas as pd
import configparser
import numpy as np
import matplotlib.pyplot as plt


def main():
    analytic = Analytics()
    analytic.analyze_today()



class Analytics():

    def __init__(self):
        config = configparser.ConfigParser()
        path_config = 'categories.dat'
        if not os.path.isfile(path_config):
            with open(path_config, 'w') as file:
                config_template="""[CATEGORIES]
spyder: programming
stackoverflow: programming
stackexchange: programming
github: programming
eingabeaufforderung: programming
texstudio: documents
word: documents
adobe acrobat reader: documents
thunderbird: mail
whatsapp: wasted time
mozilla: wasted time
chrome: wasted time
mingw64: programming
sperrbildschirm: idle"""
                file.write(config_template)

        config.read('categories.dat')
        self.string_cats = config.items('CATEGORIES')


    def analyze_today(self):
        today = datetime.datetime.now()
        folder = 'data/'
        filename = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'
        path = folder + filename
        if not os.path.isfile(path):
            print('start script.py first to generate some data.')
            return


        df = pd.read_csv(path, encoding = "ISO-8859-1", names=['time', 'category', 'duration'])
        u_cats = self.get_unique_categories(self.string_cats) # unique category name
        u_dur = [] # duratio of unice category
        print('')
        print('')
        total_dur = np.sum(df.duration)
        total_hr = int(np.floor(total_dur / 3600))
        total_min = int(np.floor((total_dur-total_hr*3600) / 60))
        total_sec = total_dur%60
        print('Review of {}.{}.{}'.format(today.day, today.month, today.year))
        print('-------------------------------------')
        print('{0: 6}:{1:02}:{2:02} h total'.format(total_hr, total_min, total_sec))
        print('-------------------------------------')

        for u_cat in u_cats:
            temp = df.loc[df.category == u_cat]
            dur = np.sum(temp.duration)
            u_dur.append(dur)
            dur_hr = int(np.floor(dur/3600))
            dur_min = int(np.floor((dur-dur_hr*3600)/60))
            dur_sec = dur%60
            print('{0: 6}:{1:02}:{2:02} h  {3:} '.format(dur_hr, dur_min, dur_sec, u_cat))

        sum_cat_time = total_dur - np.sum(u_dur)
        sum_dur_hr = int(np.floor(sum_cat_time/3600))
        sum_dur_min = int(np.floor((sum_cat_time - sum_dur_hr*3500)/60))
        sum_dur_sec = sum_cat_time%60
        print('-------------------------------------')
        print('{0: 6}:{1:02}:{2:02} h not categorized'.format(sum_dur_hr, sum_dur_min, sum_dur_sec))

        plt.figure()
        plt.pie(u_dur, labels=u_cats, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()


    def get_unique_categories(self, string_cats):
        u_cats = []
        for string, cat in string_cats:
            if cat not in u_cats:
                u_cats.append(cat)

        return u_cats


    def get_cat(self, window):
        for string, category in self.string_cats:
            try:
                if string in window:
                    return category
                    break
            except TypeError:
                pass
        return 'not categorized'


if __name__ == '__main__':
    main()
