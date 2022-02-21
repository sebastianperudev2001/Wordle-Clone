# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 07:37:39 2022

@author: jacks
"""
import colored
from colored import stylize, fg,bg,attr

print(stylize("This is green.", colored.bg("dark_gray")+ colored.fg("black")))
print(stylize("This is green.", colored.bg("light_gray") + colored.fg("black")))
print(stylize("This is green.", colored.bg("white") + colored.fg("black")  )  )

print("This is not.")

angry = colored.fg("red") + colored.attr("bold")
print(stylize("This is angry text.", colored.attr("bold") + colored.fg("red")))


print(stylize("This is VERY angry text.", angry + colored.attr("underlined")))
print("But this is not.")
