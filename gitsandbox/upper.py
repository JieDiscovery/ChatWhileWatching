#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os

# Credit: http://stackoverflow.com/questions/11540854/ \
#  file-as-command-line-argument-for-argparse-error-message-if-argument-is-not-va

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'rb+')  # return an open file handle

parser = argparse.ArgumentParser(description='upper utility')
parser.add_argument('-f', '--file',
                    dest='file',
                    help='input file', metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))

options = parser.parse_args()

while 1:
    c = options.file.read(1)
    if not c:
        break
    options.file.seek(-1,1)
    options.file.write(c.upper())
    
options.file.close()
