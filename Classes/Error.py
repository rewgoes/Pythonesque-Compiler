__author__ = 'matheus'

import sys


class Error(object):

    # This class is being used for Error handling, because we do not have
    # proper error recovery, we exit the application after 1 error is found
    def __init__(self, outfile):
        """
        :param outfile: output file to write error messages
        """
        self.lineNumber = 0
        self.message = ''
        self.outfile = outfile

    def lexerError(self, message):
        """
        :param message: message to be written in file
        """
        self.outfile.write(message)
        self.outfile.write('\nFim da compilacao\n')
        sys.exit(0)

    def parserError(self, message):
        """
        :param message: message to be written in file
        """
        self.outfile.write(message)
        self.outfile.write('\nFim da compilacao\n')
        sys.exit(0)

    def semanticError(self, listError):
        for msg in listError:
            self.outfile.write(msg + '\n')
        self.outfile.write('Fim da compilacao\n')