#!/usr/bin/python
# Finename: cls.py

'''
clear the screen.
'''
import os
import sys

def do_action(cmd,p):
	if sys.platform=='win32':
		os.system('cls')
	else:
		os.system('clear')
