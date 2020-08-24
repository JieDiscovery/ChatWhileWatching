#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

# Set path and import SibylStart
from set_path import set_path
set_path()
from sibyl.main.sibyl_client import SibylStart

# Settings
protocol = 'UDP'
protocolType = 'text'


def create_parser():
    # This funciton is needed by sphing argparse module to wrok correctly
    # Argument parsing
    parser = argparse.ArgumentParser(description='Sibyl Client (' + 
                                      protocol + ' ' + protocolType +
                                     ' Version)')
    parser.add_argument('-p', '--port', dest='serverPort', type=int,
                        help='The port number to be used for listening.',
                        default=1800)
    parser.add_argument('-e', '--debug',
                        dest='debugFlag',
                        help='Raise the log level to debug',
                        action="store_true",
                        default=False)
    parser.add_argument("-m", "--machine", dest="host", type=str,
                        help="the server name or IP address to connect to",
                        default='localhost')

    return parser

if __name__ == '__main__':
    parser = create_parser()
    options = parser.parse_args()

    # Call start function
    SibylStart(protocol, protocolType,
               options.serverPort, options.host,
               options.debugFlag)




