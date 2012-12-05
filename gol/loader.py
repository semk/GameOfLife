#! /usr/bin/env python
#
# Implementation of different Pattern Loaders.
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created on 4th Dec 2012
#
# Licensed under FreeBSD license. Refer COPYING for more info.


import os
import json


class Pattern(object):

    def __init__(self, name=''):
        self.name = name
        self.layout = []
        self.comments = []

    def setName(self, name):
        self.name = name

    def setLayout(self, layout):
        self.layout = layout

    def addRow(self, row):
        self.layout.append(row)

    def addComment(self, comment):
        self.comments.append(comment)


class JSONLoader(object):

    def __init__(self, path):
        self.path = path
        self.pattern = None

    def load(self):
        with open(self.path, 'rb') as f:
            try:
                pattern = json.load(f)
            except Exception, why:
                sys.stderr.write('Ignoring ' + self.path + ':' + str(why) + '\n')

        self.pattern = Pattern(pattern['name'])
        self.pattern.setLayout(pattern['pattern'])
        return self.pattern


class RLELoader(object):

    def __init__(self, path):
        self.path = path
        self.pattern = None

    def load(self):
        self.pattern = Pattern()
        self.currentRow = []
        with open(self.path, 'rb') as f:
            for line in f.readlines():
                if line.startswith('#N'):
                    patternName = line[2:].strip()
                    self.pattern.setName(patternName)
                elif line.startswith('#C'):
                    comment = line[2:].strip()
                    self.pattern.addComment(comment)
                elif not line.startswith('#'):
                    self.loadEncodedLine(line)
                else:
                    pass

        return self.pattern

    def loadEncodedLine(line):
        digit = False
        num = 0
        for char in line:
            if isdigit(char):
                if digit:
                    num = (num * 10) + int(char)
                else:
                    num = int(char)
                digit = True
            else:
                if digit:
                    if char == 'b':
                        self.currentRow += num * [1]
                    elif char == 'o':
                        self.currentRow += num * [0]
                    elif char == '$':
                        self.pattern.addRow(self.currentRow)
                    elif char == '!':
                        break
                digit = False


class PlainTextLoader(object):

    def __init__(self, path):
        self.path = path
        self.pattern = None

    def load(self):
        self.pattern = Pattern()
        with open(self.path, 'rb') as f:
            for line in f.readlines():
                if line.startswith('!'):
                    if line.startswith('!Name:'):
                        patternName = line[6:].strip()
                        self.pattern.setName(patternName)
                        continue
                    self.pattern.addComment(line[1:])
                else:
                    row = []
                    for char in line:
                        if char == '.':
                            row.append(0)
                        elif char == 'O':
                            row.append(1)
                    self.pattern.addRow(row)

        return self.pattern


class PatternLoader(object):

    loaders = {'.json': JSONLoader, '.rle': RLELoader, '.cells': PlainTextLoader}
    
    def __init__(self, path):
        self.path = path
        self.loader_type = os.path.splitext(self.path)[1]

    def load(self):
        loader = self.loaders[self.loader_type](self.path)
        pattern = loader.load()
        return pattern
