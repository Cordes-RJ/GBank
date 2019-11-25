# -*- coding: utf-8 -*-

import os

# checks if file exists, returns a bool
def Exists(path): # string -> bool
    return os.path.isfile(path)

# erases contents at path
def Erase(path):
    if Exists(path):
        open(path, 'w').close()
        
def Create(path):
    open(path, 'a').close()
    
