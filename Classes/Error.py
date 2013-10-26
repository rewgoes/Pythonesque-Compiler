__author__ = 'matheus'

import sys


class Error(object):

    def __init__(self, outfile):
        self.lineNumber = 0
        self.message = ''
        self.outfile = outfile

    def lexerError(self, message):
        print(message)
        self.outfile.write(message)
        sys.exit(0)

    def parserError(self, message):
        print(message)
        self.outfile.write(message)
        sys.exit(0)