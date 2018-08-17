# Monitor the time you spend
1. run 'script.py' in background
2. run 'analytics.py' to see where you waisted your time
3. have fun

## requirements
requires the following packages
* pyautogui
* msvcrt
* numpy
* pandas
* configparser
* win32 gui (see below)


### install win32 gui from:
Details from [satackoverflow](https://stackoverflow.com/questions/20113456/installing-win32gui-python-module#20128310)
1. Download the pywin32....whl from [pythonlibs](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32)
2. pip install pywin32....whl
3. C:\python32\python.exe Scripts\pywin32_postinstall.py -install

more details under [Module win32gui](http://timgolden.me.uk/pywin32-docs/win32gui.html)


## categories
the program will log the window title that you have in focus every time you change the focussed window.
in the 'categories.dat' file you can name a string as key (left of the ':') and correspond it to a categorie  (right of the ':'). The file will be read from top to bottom. So if you use 'stackoverflow' and correspond that with the categoriey 'programming' than this will be prioritized against the string 'chrome', which might also appear on a visited website.

from 'categories.dat'
```
[CATEGORIES]
spyder: programming
stackoverflow: programming
github: programming
eingabeaufforderung: programming
texstudio: latex
whatsapp: wasted time
mozilla: wasted time (mozilla)
chrome: wasted time (chrome)
mingw64: programming
```

## example results
run 'analytics.py' to get a summary table and a pie chart of your data.
Only the data for today will be shown

```
Review of 15.8.2018
-------------------------------------
     7:50:39 h total
-------------------------------------
     4:53:10 h  programming
     0:57:42 h  documents
     0:14:49 h  mail
     1:09:24 h  wasted time
-------------------------------------
     0:35:34 h not categorized
```

![pie chart example](/images/example_pie_chart.png)

## Website shows results of all data in "data"
open html/index.html and see the beauty of your recorded data
every 60 seconds, the script will automaticall refresh the source code for the html page
![html preview](/images/html_preview.PNG)

# todo
- adding "projects" as a separate measure next to categories
- read the parent process and not only the window title
