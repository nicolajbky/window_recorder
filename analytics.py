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
    analytic.print_review()
    #analytic.print_pi_chart()
    analytic.create_html()
    pass


class Analytics():

    def __init__(self):
        self.path_data = 'data'
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
        if not os.path.isdir('figs'):
            os.mkdir('figs')
        config.read('categories.dat')
        self.string_cats = config.items('CATEGORIES')


    def analyze(self, logfile=''):
        if logfile == '':
            today = datetime.datetime.now()
            filename = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'
            path = self.path_data + '/' + filename
            if not os.path.isfile(path):
                print('start script.py first to generate some data.')
                return
        else:
            filename = logfile
        path = self.path_data + '/' + filename
        date = datetime.datetime.strptime(filename[:-4], '%Y-%m-%d')

        df = pd.read_csv(path, encoding = "ISO-8859-1", names=['time', 'category', 'duration'])
        u_cats = self.get_unique_categories(self.string_cats) # unique category name
        u_dur = [] # duratio of unice category
        for u_cat in u_cats:
            temp = df.loc[df.category == u_cat]
            dur = np.sum(temp.duration)
            u_dur.append(dur)
        return u_cats, u_dur, date, df


    def print_pi_chart(self, logfile=''):

        if logfile == '':
            date = datetime.datetime.today()
        else:
            date = date = datetime.datetime.strptime(logfile[:-4], '%Y-%m-%d')

        filename = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '.png'
        u_cats, u_dur, date, df = self.analyze(logfile)
        total_dur = np.sum(u_dur)
        total_hr = int(np.floor(total_dur / 3600))
        total_min = int(np.floor((total_dur-total_hr*3600) / 60))
        total_sec = int(total_dur%60)

        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.title('{0:02}.{1:02}.{2:04} - {3:02}:{4:02}:{5:02} h'\
                  .format(date.day, date.month, date.year,
                          total_hr, total_min, total_sec))
        plt.pie(u_dur, labels=u_cats, autopct='%1.1f%%')
        plt.axis('equal')
        path = 'figs/'+filename
        plt.savefig(path)
        plt.show()
        plt.close()
        print('Figure saved as {}'.format(path))


    def print_review(self, logfile=''):
        u_cats, u_dur, date, df = self.analyze(logfile)
        print('')
        print('')
        total_dur = np.sum(df.duration)
        total_hr = np.floor(total_dur / 3600)
        total_min = np.floor((total_dur-total_hr*3600) / 60)
        total_sec = total_dur%60
        print('Review of {0:02}.{1:02}.{2:04}'.format(date.day, date.month, date.year))
        print('-------------------------------------')
        print('{0: 6}:{1:02}:{2:02} h total'.format(int(total_hr), int(total_min), int(total_sec)))
        print('-------------------------------------')

        for idx in range(len(u_dur)):
            dur = u_dur[idx]
            cat = u_cats[idx]
            if dur > 0:
                dur_hr = int(np.floor(dur/3600))
                dur_min = int(np.floor((dur-dur_hr*3600)/60))
                dur_sec = int(dur%60)
                print('{0: 6}:{1:02}:{2:02} h  {3:} '.format(dur_hr, dur_min, dur_sec, cat))

        sum_cat_time = total_dur - np.sum(u_dur)
        sum_dur_hr = int(np.floor(sum_cat_time/3600))
        sum_dur_min = int(np.floor((sum_cat_time - sum_dur_hr*3500)/60))
        sum_dur_sec = sum_cat_time%60
        print('-------------------------------------')
        print('{0: 6}:{1:02}:{2:02} h not categorized'.format(sum_dur_hr, sum_dur_min, sum_dur_sec))


    def get_log_list(self):
        log_list = os.listdir(self.path_data)
        date_list = []
        for log in log_list:
            date_list.append(datetime.datetime.strptime(log[:-4], '%Y-%m-%d'))
        return log_list, date_list


    def get_unique_categories(self, string_cats=''):
        if string_cats == '':
            string_cats = self.string_cats
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


    def create_html(self, logfile=''):
        _, u_dur, date, df = self.analyze(logfile)
        log_list, date_list = self.get_log_list()
        u_cats = self.get_unique_categories()
        with open('html/head.txt', 'r') as file:
            head = file.readlines()
        with open('html/tail.txt', 'r') as file:
            tail = file.read()


        with open('html/index.html', 'w') as file:

            # TABLE
            file.writelines(head)
            row = '<table>\n'
            row += '<tr>\n<td></td>'
            for cat in u_cats:
                row += '<td><b>{}</b></td>\n'.format(cat)
            row += '</tr>'

            for log in log_list:
                print(log)
                self.print_pi_chart(log)
                row += '<tr>\n\t<td>'
                u_cat, u_dur, date, df = self.analyze(log)
                date = datetime.datetime.strptime(log[:-4], '%Y-%m-%d')
                row += '<b>{0:02}.{1:02}.{2:04}</b>'.format(date.day, date.month, date.year)
                row += '</td>'
                for dur in u_dur:
                    dur_hr = int(np.floor(dur/3600))
                    dur_min = int(np.floor((dur-dur_hr*3600)/60))
                    dur_sec = int(dur%60)
                    row += '<td>'
                    row += '{0: 6}:{1:02}:{2:02}'.format(dur_hr, dur_min, dur_sec)
                    row += '</td>\n'
                row += '</tr>\n'
            file.write(row)
            file.write('</table>\n')

            # images
            file.write('<div class="gallery">\n')
            img_list = os.listdir('figs')
            for img in img_list:
                img_row = '<img src="../figs/{}" width=500></br>\n'.format(img)
                file.write(img_row)
            file.write('</div>\n')
            file.writelines(tail)
        pass


if __name__ == '__main__':
    main()
