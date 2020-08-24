#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Set path and import SibylStart
from set_path import set_path
set_path()

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

from sibyl.main.sibyl_server import SibylStart

# Settings
protocol = 'TCP'
protocolType = 'binary'

# Argument parsing
parser = argparse.ArgumentParser(description='Sibyl Server (UDP Text Version)')
parser.add_argument('-p', '--port', dest='server_port', type=int,
                    help='The port number to be used for listening.',
                    default=1800)
parser.add_argument('-e', '--debug',
                    dest='debugFlag',
                    help='Raise the log level to debug',
                    action="store_true",
                    default=False)

argcomplete.autocomplete(parser)

options = parser.parse_args()


# Call start function
SibylStart(protocol, protocolType,
           options.server_port, 
           options.debugFlag)
