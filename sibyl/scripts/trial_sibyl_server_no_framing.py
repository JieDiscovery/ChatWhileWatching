#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import copy
import os
import sys

# Set path and import SibylStart
from set_path import set_path
stockrsm_path = set_path()

def main():
    trial_class = 'sibyl.test.sibyl_server_test.SibylServerTestCase'
    cmdLine = ['trial',
               trial_class + '.test_sibyl_no_framing']
    
    os.environ['STOCKRSMPATH'] = stockrsm_path
    
    sys.argv.append(trial_class + '.test_sibyl_no_framing')
        
    sys.path.insert(0, os.path.abspath(os.getcwd()))
    from twisted.scripts.trial import run
    run()

if __name__ == '__main__':
    main()
