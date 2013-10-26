__author__ = 'matheus'


class Error(object):

    def __init__(self, outfile):
        self.lineNumber = 0
        self.message = ''
        self.outfile = outfile

    def lexerError(self, message):
        print(message)
        self.outfile.write(message)

    def parserError(self, message):
        print(message)
        self.outfile.write(message)