import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\3.6\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\3.6\\tcl\\tk8.6'

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("masterGUI.py", base=base)]

cx_Freeze.setup(name="EBook Manager", options = {"build_exe":{"packages":["tkinter", "datetime", "time", "checkout", "EBookAPI", "fileAPI", "lateBooksAPI", "studentAPI"], "include_files":["saveData.config","tcl86t.dll","tk86t.dll"]}}, executables=executables)
#Packages = modules
#include files = files use in script
