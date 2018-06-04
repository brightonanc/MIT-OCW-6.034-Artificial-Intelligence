rem Author: Brighton Ancelin
rem Updates all .py files in directory from Python 2 to Python 3 using 2to3.py
for /r %%f in (*.py) do (
    2to3 -w "%%f"
)