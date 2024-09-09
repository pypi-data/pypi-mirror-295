import multiprocessing
import os
import subprocess
import sys
import wx
import TestWXPython


def call_first_script():
	print('Main: attempting to call the UI code...')
	os.system(f'TestWXPython.py')
	print('Main: ...completed call if the UI code')
	
if __name__ == "__main__":
	#check_python_installation()
	app = wx.App(False)
	print('Main: calling UI code... ')
	frame = TestWXPython.SpreadsheetApp(None, "Spreadsheet App")
	app.MainLoop()

