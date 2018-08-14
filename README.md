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

```
-------------------------------------
   121:06 min total
-------------------------------------
    88:43 min  programming
     7:29 min  latex
     4:38 min  wasted time
     7:14 min  wasted time (mozilla)
    11:05 min  wasted time (chrome)
-------------------------------------
     1:57 min  not categorized
```

![pie chart example](/images/example_pie_chart.png)
