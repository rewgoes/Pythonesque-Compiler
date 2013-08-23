__author__ = 'Matheus'

import sys
from Classes.LexicalAy import LexicalAy
from Classes.SymTable import SymTable


# List of reserved words
keywords = ['algoritmo', 'fim_algoritmo', 'declare', 'literal', 'inteiro', 'real',
            'logico', 'leia', 'escreva', 'se', 'entao', 'senao', 'fim_se', 'caso',
            'seja', 'fim_caso', 'tipo', 'para', 'ate', 'faca', 'fim_para', 'enquanto',
            'fim_enquanto', 'procedimento', 'fim_procedimento', 'funcao', 'fim_funcao',
            'ou', 'e', 'nao', 'registro', 'fim_registro', 'var', 'constante', 'verdadeiro',
            'falso', 'retorne']

# List of reserved symbols
symbols = [':', ',', '^', '(', ')', '-', '%', '*', '/', '+', '&', '=', '<', '>', '.',
           '[', ']', '<-', '<>', '<=', '>=', '..']


def main(infile):
    # Create reserved words and symbols table
    """

    :param infile:
    """
    global keywords, symbols
    # Class that creates the symbol table
    symtable = SymTable(keywords, symbols)

    # Open input file
    f = open(infile)

    # Instantiate the Lexical Analyser Class and assigns the keytable and symtable to it
    ly = LexicalAy(symtable)
    ly.symtable = symtable

    # Read line from file and send it to LexicalAy.getToken() method
    for line in f.readline():
        ly.getToken(line)

        # TODO - Print tokens on outfile


if __name__ == '__main__':
    # Get command line argument
    infile = sys.argv[0]

    # Calls main function
    main(infile)
