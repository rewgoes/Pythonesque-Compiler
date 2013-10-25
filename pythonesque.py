import sys
from Classes import Parser
from Classes.LexicalAy import LexicalAy
from Classes.SymTable import SymTable
from Classes.Parser import Parser


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


def main(infile, outfile):
    """(file) -> None
    
    Create reserved words and symbols table 
    
    :param infile:
    :param outfile
    """
    
    global keywords, symbols
    messageList = []
    
    # Class that creates the symbol table
    symtable = SymTable(keywords, symbols)

    # Instantiate the Lexical Analyser Class and assigns the keytable and symtable to it
    ly = LexicalAy(symtable, infile, messageList)
    parser = Parser(ly, messageList)
    parser.parse()

    # Read line from file and send it to LexicalAy.getToken() method
    #for line in f :
    #    tmpList = ly.getToken()
    #    for token in tmpList:
    #        listTokens.append(token)

    # Open output file
    out = open(outfile, "w")

    # Write on the output file
    for message in messageList:
        print(message)
            
    # Close input and output file
    #f.close()
    out.close()

    #ly.symtable.printTable()

if __name__ == '__main__':
    # Get command line arguments
    infile = sys.argv[1]
    outfile = sys.argv[2]

    # Calls main function
    main(infile, outfile)
