# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 07:37:39 2022

def printUnicode():
    print(u"\u2b1c")
    print(u"\u1f7e8")
    print(u"\u1f7e9")
printUnicode()

@author: jacks
"""


"""    
import unicodedata   # access to the Unicode Character Database

def check_unicode(s):
    print(len(s), s)
    for char in s:
        print( char, '{:04x}'.format( ord(char)), 
               unicodedata.category( char),
               unicodedata.name( char, '(unknown)') )
check_unicode( u"\u2b1c\U0001f7e8\U0001f7e9") # adjusted string literals
"""

def printUnicode():
    print(u"\U0001F7EB")
    print(u"\U0001f7e8")
    print(u"\U0001f7e9")
printUnicode()