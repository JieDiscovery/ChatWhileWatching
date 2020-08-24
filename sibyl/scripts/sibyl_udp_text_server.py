#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

# Set path and import SibylStart
from set_path import set_path
set_path()
from sibyl.main.sibyl_server import SibylStart

# Settings
protocol = 'UDP'
protocolType = 'text'


def create_parser():
    # This is needed for the argparse sphinx module to work
    parser = argparse.ArgumentParser(description='Sibyl Server (UDP Text Version)')
    parser.add_argument('-p', '--port', dest='server_port', type=int,
                    help='The port number to be used for listening.',
                    default=1800)
    parser.add_argument('-e', '--debug',
                    dest='debugFlag',
                    help='Raise the log level to debug',
                    action="store_true",
                    default=False)
    print(type(parser))
    return parser


if __name__ == '__main__':
    # Argument parsing
    parser = create_parser()

    options = parser.parse_args()

    # Call start function
    SibylStart(protocol, protocolType,
               options.server_port,
               options.debugFlag)

