# window_recorder


requires the following packages
* pyautogui
* msvcrt
* numpy
* pandas
* configparser
* win32 gui (see below)


install win32 gui from:
    https://stackoverflow.com/questions/20113456/installing-win32gui-python-module#20128310
    Step 1: Download the pywin32....whl
    Step 2: pip install pywin32....whl
    Step 3: C:\python32\python.exe Scripts\pywin32_postinstall.py -install
    Step 4: python


# categories
from 'categories.dat'
```
[CATEGORIES]
spyder: programming
stackoverflow: programming
github: programming
texstudio: latex
mozilla: browsing
chrome: browsing
mingw64: programming
```

# example results

```python
78:5 min total

    59:42 min  programming
     2:11 min  latex
    15:57 min  browsing
```

[pie chart example](/images/example_pie_chart.png)