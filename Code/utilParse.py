# -*- coding: utf-8 -*-

# removes control characters from a string
def removeControlCharacters(string):
    bytesArr = (str(string)).encode("utf-8")
    newString = ""
    for i in range(len(bytesArr)):
        if bytesArr[i] >= 32:
            newString = newString+string[i]
    return newString