__author__ = 'matheus'

import sys


class Error(object):

    def __init__(self, outfile):
        self.lineNumber = 0
        self.message = ''
        self.outfile = outfile

    def lexerError(self, message):
        #print(message + '\nFim da compilacao')
        self.outfile.write(message)
        self.outfile.write('\nFim da compilacao\n')
        sys.exit(0)

    def parserError(self, message):
        #print(message + '\nFim da compilacao')
        self.outfile.write(message)
        self.outfile.write('\nFim da compilacao\n')
        sys.exit(0)