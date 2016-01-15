#!/usr/bin/env python3

import os
import sys

class BadFile(Exception):
    pass

def makeFileNameList(pathLocation, extension):
    '''Returns a list of the absolute filenames ending with the 'extension' in the path and subfolders of the path specified in 'pathLocation'.'''
    fnl = []
    for root, dirs, files in os.walk(pathLocation):
        for file in files:
            if file.endswith(extension):
                 fnl.append(os.path.join(root, file))
    return fnl

def cff(fNm): # Contents from filename
    """Contents from filename. This method opens a file sent to it as 'fNm', and returns the contents"""
    f = open(fNm)
    c = f.read()
    f.close()
    return c

def processHTML(fc):
    """Takes the contents of an HTML file as fc (file contents), and runs some tests on the HTML. If it passes, returns 'pass' if it fails, returns 'fail'."""
    if fc.count('<') != fc.count('>'):
        return 'fail'
    else:
        return 'pass'

def processCSS(fc):
    """Takes the contents of a CSS file as fc (file contents), and runs some tests on the HTML. If it passes, returns 'pass' if it fails, returns 'fail'."""
    if fc.count('{') != fc.count('}'):
        return 'fail'
    else:
        return 'pass'


htmlList = makeFileNameList(sys.path[0], '.html')  # Get a list of the HTML Files' Filenames

# Open those filenames, as files, and then process the files' contents
for fName in htmlList:
    contents = cff(fName) # Get contents from filename
    if processHTML(contents) == 'fail':
        raise BadFile(fName + " Failed. Details: '<': " + str(contents.count('<')) + " '>': " + str(contents.count('>')))
    else:
        print(fName, "Passed.")



cssList = makeFileNameList(sys.path[0], '.css')

for fName in cssList:
    contents = cff(fName) # Get contents from filename
    if processCSS(contents) == 'fail':
        raise BadFile(fName + " Failed. Details: '{': " + str(contents.count('{')) + " '}': " + str(contents.count('}')))
    else:
        print(fName + "Passed.")




    
