import sys
from Classes import Parser
from Classes.LexicalAy import LexicalAy
from Classes.SymTable import SymTable
from Classes.Parser import Parser
from Classes.Error import Error
from Classes.CodeGenerator import CodeGenerator


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
    """
    :param infile: input file path
    :param outfile: output file path
    """
    
    global keywords, symbols

     # Open output file
    out = open(outfile, "w")
    
    # Class that creates the symbol table
    symtable = SymTable(keywords, symbols)

    # Instantiate Error class
    error = Error(out)

    # Instantiate the Lexical Analyser Class and assigns the keytable and symtable to it
    ly = LexicalAy(symtable, infile, error)

    # Instantiate Parser class
    parser = Parser(ly, symtable, error)

    # Parse!
    parser.parse()


    # Instantiate Code Generator class
    #ly2 = LexicalAy(symtable, infile, error)
    #codegenerator = CodeGenerator(ly2, out)

    # Generator Code
   # code = codegenerator.code()

    #for c in code:
    #    out.write(c)

    # Close output file
    # (input file doesn't need to be closed since we're using linecache)
    out.close()


if __name__ == '__main__':
    # Get command line arguments
    infile = sys.argv[1]
    outfile = sys.argv[2]

    # Calls main function
    main(infile, outfile)
