#!usr/bin/python
# Finename: Console.py

import sys
import ctypes


IS_WIN32 = sys.platform=='win32'

class Console:
	STD_INPUT_HANDLE = -10  
	STD_OUTPUT_HANDLE= -11  
	STD_ERROR_HANDLE = -12  

	def __init__(self):
		if IS_WIN32:
			self.std_out_handle=ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

	def _write(self,str,color=None,new_line=True):
		if color==None:
			if new_line:
				print str
			else:
				print str,
		else:
			if IS_WIN32:
				self.__setWin32Color(color)
				if not new_line:
					print str,
				else:
					print str
				self.__resetWin32Color()
			else:
				str = color+str+ForeColor.END
				if not new_line:
					print str,
				else:
					print str

	def write(self,str,color=None):
		self._write(str,color,new_line=False)

	def write_line(self,str,color=None):
		self._write(str,color,True)

	def red(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_RED,new_line)

	def green(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_GREEN,new_line)

	def blue(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_BLUE,new_line)

	def yellow(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_YELLOW,new_line)

	def purple(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_PURPLE,new_line)

	def cyan(self,str,new_line=True):
		self._write(str,ForeColor.INTENSITY_CYAN,new_line)

	def __setWin32Color(self,color):
		return ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, color)

	def __resetWin32Color(self):
		self.__setWin32Color(ForeColor.WHITE)

class ForeColor:
	if IS_WIN32:
		BLACK = 0x0  
		BLUE = 0x01 # text color contains blue.  
		GREEN = 0x02 # text color contains green.  
		RED = 0x04 # text color contains red.  
		YELLOW = RED | GREEN
		PURPLE = RED | BLUE
		CYAN = GREEN | BLUE
		WHITE = GREEN | RED | BLUE
		INTENSITY = 0x08 # text color is intensified.
		INTENSITY_RED=INTENSITY | RED
		INTENSITY_BLUE=INTENSITY | BLUE
		INTENSITY_BLACK=INTENSITY | BLACK
		INTENSITY_GREEN=INTENSITY | GREEN
		INTENSITY_YELLOW = INTENSITY | YELLOW
		INTENSITY_PURPLE = INTENSITY | PURPLE
		INTENSITY_CYAN = INTENSITY | CYAN		
		END=None
	else:
		BLACK = '\033[30m'  
		BLUE = '\033[34m'  # text color contains blue.  
		GREEN= '\033[32m'  # text color contains green.  
		RED = '\033[31m'  # text color contains red.  
		YELLOW = '\033[33m'
		PURPLE = '\033[35m'
		CYAN = '\033[36m'
		WHITE = '\033[37m'
		INTENSITY = None	 # text color is intensified.
		INTENSITY_RED='\033[91m'
		INTENSITY_BLUE='\033[94m'
		INTENSITY_BLACK='\033[90m'
		INTENSITY_GREEN='\033[92m'
		INTENSITY_YELLOW = '\033[93m'
		INTENSITY_PURPLE = '\033[95m'
		INTENSITY_CYAN = '\033[96m'	
		END= '\033[0m'
class BackColor:
	if IS_WIN32:		
		BLUE = 0x10 # background color contains blue.  
		GREEN= 0x20 # background color contains green.  
		RED = 0x40 # background color contains red.  
		INTENSITY = 0x80 # background color is intensified.  
	else:
		BLUE = '\033[44m' # background color contains blue.  
		GREEN= '\033[42m' # background color contains green.  
		RED = '\033[41m' # background color contains red.  
		END = '\033[0m' # background color is intensified.