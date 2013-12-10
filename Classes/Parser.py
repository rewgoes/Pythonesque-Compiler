from symtable import symtable

__author__ = 'bruno_matheus_rafael_thiago'

from Classes.Token import Token
from Classes.SymTable import SymTable


class Parser(object):
    def __init__(self, lexer, symtable, error):
        """
        :param lexer: instance of lexer class
        :param error: instance of error class
        """
        # Tokens read from input will populate this list
        # Parser will read this list until it's empty
        # When list is empty, parser will call LexicalAy.getToken()
        self.listToken = []

        # Reference to the lexer object
        self.lexer = lexer

        # This variable stores the current token being analysed
        self.currentToken = Token('', '')

        # Reference to the symble table
        self.symtable = symtable

        # Error instance
        self.errorRef = error

        # identifier temp
        self.tempIdent = []
        self.ponteiroOpc = False
        self.declaring = False
        self.returnType = ""
        self.returnVar = ""
        self.regVar = []
        self.regName = ""
        self.isProcedure = False
        self.param = False
        self.paramProc = []
        self.nameProc = ""
        self.localIdent = []
        self.lastIdent = ""
        # keeps the scope of the program, as it can have global variables
        self.scope = "global"

        # Error list
        self.listError = []

        # This is first-set of non-terminals ("primeiros")
        # It's a dictionary where the non-terminal/terminal is the key
        # And the value is a list with the firsts
        # Use the firstOf method to access the list
        self.firstSet = \
            {'programa': ['algoritmo', 'declare', 'constante', 'tipo', 'procedimento', 'funcao'],
             'declaracoes': ['3', 'declare', 'constante', 'tipo', 'procedimento', 'funcao'],
             'declaracao_local_global': ['declare', 'constante', 'tipo', 'procedimento', 'funcao'],
             'declaracao_global': ['procedimento', 'funcao'],
             'declaracao_local': ['declare', 'constante', 'tipo'],
             'variavel': ['^', 'identificador'],
             'identificador': ['^', 'identificador'],
             'ponteiro_opcional': ['^', '3'],
             'outros_ident': ['.', '3'],
             'dimensao': ['[', '3'],
             'tipo': ['registro', '^', 'literal', 'inteiro', 'real', 'logico', 'identificador'],
             'registro': ['registro'],
             'mais_ident': [',', '3'],
             'mais_variaveis': ['^', 'identificador', '3'],
             'tipo_basico': ['literal', 'inteiro', 'real', 'logico'],
             'tipo_basico_ident': ['literal', 'inteiro', 'real', 'logico', 'identificador'],
             'tipo_estendido': ['^', 'literal', 'inteiro', 'real', 'logico', 'identificador'],
             'valor_constante': ['cadeia_literal', 'numero_inteiro', 'numero_real', 'verdadeiro', 'falso'],
             'parametros_opcional': ['3', 'var', '^', 'identificador'],
             'parametro': ['var', '^', 'identificador'],
             'var_opcional': ['var', '3'],
             'mais_parametros': [',', '3'],
             'declaracoes_locais': ['3', 'declare', 'constante', 'tipo'],
             'corpo': ['leia', 'escreva', 'se', 'caso', 'para', 'enquanto', 'faca', '^', 'identificador', 'retorne',
                       'declare', 'constante', 'tipo', '3'],
             'comandos': ['leia', 'escreva', 'se', 'caso', 'para', 'enquanto', 'faca', '^', 'identificador', 'retorne',
                          '3'],
             'cmd': ['leia', 'escreva', 'se', 'caso', 'para', 'enquanto', 'faca', '^', 'identificador', 'retorne'],
             'mais_expressao': [',', '3'],
             'senao_opcional': ['senao', '3'],
             'chamada_atribuicao': ['(', '.', '[', '<-'],
             'selecao': ['-', 'numero_inteiro'],
             'mais_selecao': ['-', 'numero_inteiro', '3'],
             'constantes': ['-', 'numero_inteiro'],
             'mais_constantes': [',', '3'],
             'numero_intervalo': ['-', 'numero_inteiro'],
             'intervalo_opcional': ['..', '-', 'numero_inteiro', '3'],
             'op_unario': ['-', '3'],
             'exp_aritmetica': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
             'op_multiplicacao': ['*', '/'],
             'op_adicao': ['+', '-'],
             'termo': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
             'outros_termos': ['+', '-', '3'],
             'fator': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
             'outros_fatores': ['*', '/', '3'],
             'parcela': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
             'parcela_unario': ['^', 'identificador', 'numero_inteiro', 'numero_real', '('],
             'parcela_nao_unario': ['&', 'cadeia_literal'],
             'outras_parcelas': ['%', '3'],
             'chamada_partes': ['(', '.', '[', '3'],
             'exp_relacional': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
             'op_opcional': ['=', '<>', '>=', '<=', '>', '<', '3'],
             'op_relacional': ['=', '<>', '>=', '<=', '>', '<'],
             'expressao': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real',
                           '(', '&', 'cadeia_literal'],
             'op_nao': ['nao', '3'],
             'termo_logico': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real',
                              '(', '&', 'cadeia_literal'],
             'outros_termos_logicos': ['ou', '3'],
             'outros_fatores_logicos': ['e', '3'],
             'fator_logico': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real',
                              '(', '&', 'cadeia_literal'],
             'parcela_logica': ['verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(',
                                '&', 'cadeia_literal'],
             }

    # Main method
    def parse(self):
        self.getToken()
        self.programa()
        if self.listError:
            self.errorRef.semanticError(self.listError)

    # Helper methods
    def getToken(self):
        # Obtain the first token on the list
        while not self.listToken:
            self.listToken = self.lexer.getToken()

        self.currentToken = self.listToken.pop(0)

    def error(self):
        lineN = str(self.lexer.lineNumber)
        self.errorRef.parserError('Linha ' + lineN + ': erro sintatico proximo a ' + self.currentToken.name)

    def firstOf(self, term):
        if term in self.firstSet:
            # non-terminal
            return self.firstSet.get(term)
        else:
            # terminal
            return term

    # Grammar rules
    # 1
    def programa(self):
        # <declaracoes> algoritmo <corpo> fim_algoritmo
        self.declaracoes()

        if self.currentToken.token == 'algoritmo':
            self.scope = "local"
            self.getToken()
        else:
            self.error()

        self.corpo()

        if self.currentToken.token == 'fim_algoritmo':
            pass
        else:
            self.error()

    # 2
    def declaracoes(self):
        # <decl_local_global> <declaracoes> | 3
        while self.currentToken.token in self.firstOf('declaracoes'):  # [?]
            self.decl_local_global()
            self.declaracoes()

    # 3
    def decl_local_global(self):
        # <declaracao_local> | <declaracao_global>
        if self.currentToken.token in self.firstOf('declaracao_local'):
            self.declaracao_local()
        elif self.currentToken.token in self.firstOf('declaracao_global'):
            self.declaracao_global()
        else:
            self.error()

    # 4
    def declaracao_local(self):
        # declare <variavel>
        # | constante IDENT : <tipo_basico> = <valor_constante>
        # | tipo IDENT : <tipo>
        if self.currentToken.token == 'declare':
            self.getToken()
            self.declaring = True
            self.variavel()
            self.declaring = False
        elif self.currentToken.token == 'constante':
            self.getToken()

            if self.currentToken.token == 'identificador':
                nameConst = self.currentToken.name
                self.getToken()

                if self.currentToken.token == ':':
                    self.getToken()
                    ttipo = self.currentToken.name
                    self.tipo_basico()

                    if self.currentToken.token == '=':
                        self.getToken()
                        self.symtable.insertSymbol(nameConst, (nameConst, 'identificador', 'constante', ttipo, self.currentToken.name, 'global', []))
                        self.valor_constante()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()

        elif self.currentToken.token == 'tipo':
            self.getToken()
            if self.currentToken.token == 'identificador':
                self.getToken()
                if self.currentToken.token == ':':
                    self.getToken()
                    self.tipo()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    # 5
    def variavel(self):
        # <identificador> <mais_ident> : <tipo>
        self.identificador()
        self.mais_ident()

        if self.currentToken.token == ':':
            self.getToken()
            self.tipo()
        else:
            self.error()
    
    # 6
    def identificador(self):
        # <ponteiro_opcional> IDENT <outros_ident> <dimensao>
        self.ponteiro_opcional()
        if self.currentToken.token == 'identificador':
            # insert symbol in symbol table
            if self.declaring:

                if self.regVar:
                    for r in self.regVar:
                        ok = self.symtable.insertSymbol(r + "." + self.currentToken.name, (r + "." + self.currentToken.name, self.currentToken.token, 'variavel', '', '', self.scope, []))
                        if not ok:
                            self.listError.append('Linha ' + str(self.lexer.lineNumber) + ': identificador ' + r + "." + self.currentToken.name + ' ja declarado anteriormente')
                        self.tempIdent.append(r + "." + self.currentToken.name)
                else:
                    ok = self.symtable.insertSymbol(self.currentToken.name, (self.currentToken.name, self.currentToken.token, 'variavel', '', '', self.scope, []))
                    if not ok:
                        self.listError.append('Linha ' + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' ja declarado anteriormente')
                    # add to tempIndent list
                    self.tempIdent.append(self.currentToken.name)
                    self.lastIdent = self.currentToken.name

                if self.isProcedure:
                    self.localIdent.append(self.currentToken.name)
            else:
                if self.currentToken.name not in self.symtable.table:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' nao declarado')

            self.getToken()
            self.outros_ident()
            self.dimensao()
        else:
            self.error()

    # 7
    def ponteiro_opcional(self):
        # ^ | 3
        if self.currentToken.token == '^':
            self.ponteiroOpc = True
            self.getToken()

    # 8
    def outros_ident(self):
        # . IDENT <outros_ident> | 3
        if self.currentToken.token == '.':
            self.getToken()

            if self.currentToken.token == 'identificador':
                if self.returnVar != "":
                    self.returnVar += "." + self.currentToken.name
                    if self.returnVar not in self.symtable.table:
                        self.listError.append("Linha " + str(self.lexer.lineNumber) + ": identificador " + self.returnVar + "nao declarado")
                    else:
                        self.returnType = self.symtable.table[self.returnVar]['type']
                self.getToken()
                self.outros_ident()
            else:
                self.error()
    
    # 9
    def dimensao(self):
        # [ <exp_aritmetica ] <dimensao> | 3
        if self.currentToken.token == '[':
            self.getToken()
            if self.returnVar != "":
                self.returnVar += "["+self.currentToken.name+"]"
            self.exp_aritmetica()

            if self.lastIdent in self.symtable.table:
                self.symtable.table[self.lastIdent]['category'] = "vetor"

            if self.currentToken.token == ']':
                self.getToken()
                self.dimensao()
            else:
                self.error()

    # 10
    def tipo(self):
        # <registro> | <tipo_estendido>
        if self.currentToken.token in self.firstOf('registro'):
            self.registro()
        elif self.currentToken.token in self.firstOf('tipo_estendido'):
            self.tipo_estendido()
        else:
            self.error()
    
    # 11
    def mais_ident(self):
        # , <identificador> <mais_ident> | 3
        if self.currentToken.token == ',':
            self.getToken()
            self.identificador()
            self.mais_ident()

    # 12
    def mais_variaveis(self):
        # <variavel> <mais_variaveis> | 3
        if self.currentToken.token in self.firstOf('variavel'):
            self.variavel()
            self.mais_variaveis()

    # 13
    def tipo_basico(self):
        # literal | inteiro | real | logico
        if self.currentToken.token == 'literal' or self.currentToken.token == 'inteiro' or \
                self.currentToken.token == 'real' or self.currentToken.token == 'logico':
            # run through the tempIdent list to add types to the variables
            for e in self.tempIdent:
                if self.ponteiroOpc:
                    self.symtable.table[e]['category'] = "ponteiro"
                self.symtable.table[e]['type'] = self.currentToken.token
            self.tempIdent = []

            self.getToken()
        else:
            self.error()
    
    # 14
    def tipo_basico_ident(self):
        if self.param:
            self.paramProc.append(self.currentToken.name)

        # <tipo_basico> | IDENT
        if self.currentToken.token in self.firstOf('tipo_basico'):
            self.tipo_basico()
        else:
            if self.currentToken.token == 'identificador':
                # Checks whether the identifier is in the symtable
                if self.currentToken.name not in self.symtable.table:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ": tipo " + self.currentToken.name + " nao declarado")

                # run through tempIdent
                for e in self.tempIdent:
                    if self.ponteiroOpc:
                        self.symtable.table[e]['category'] = "ponteiro"
                    else:
                        self.symtable.table[e]['category'] = "variavel"
                    self.symtable.table[e]['type'] = self.currentToken.token
                    if self.param:
                        self.paramProc.append(self.currentToken.token)

                self.ponteiroOpc = False
                self.tempIdent = []

                self.getToken()
            else:
                self.error()
    
    # 15
    def tipo_estendido(self):
        # <ponteiro_opcional> <tipo_basico_ident>
        self.ponteiro_opcional()
        self.tipo_basico_ident()

    # 16
    def valor_constante(self):
        # CADEIA | NUM_INT | NUM_REAL | verdadeiro | falso
        if self.currentToken.token == 'cadeia_literal' or self.currentToken.token == 'numero_inteiro' or \
                        self.currentToken.token == 'numero_real' or self.currentToken.token == 'verdadeiro' or \
                        self.currentToken.token == 'falso':
            self.getToken()
        else:
            self.error()
    
    # 17
    def registro(self):
        # registro <variavel> <mais_variaveis> fim_registro
        if self.currentToken.token == 'registro':
            self.getToken()

            for e in self.tempIdent:
                self.symtable.table[e]['type'] = "registro"

            self.regVar = self.tempIdent
            self.tempIdent = []

            self.variavel()
            self.mais_variaveis()

            if self.currentToken.token == 'fim_registro':
                self.regVar = []
                self.getToken()
            else:
                self.error()
        else:
            self.error()
    
    # 18
    def declaracao_global(self):
        # procedimento IDENT ( <parametros_opcional> ) <declaracoes_locais> <comandos> fim_procedimento
        if self.currentToken.token == 'procedimento':
            self.getToken()
            if self.currentToken.token == 'identificador':

                # insert symbol in symbol table
                if not self.symtable.insertSymbol(self.currentToken.name, (self.currentToken.name, self.currentToken.token, 'procedimento', '', '', self.scope, [])):
                    self.listError.append('Linha ' + self.lexer.lineNumber + ': identificador ' + self.currentToken.name + ' ja declarado anteriormente')

                self.isProcedure = True
                self.nameProc = self.currentToken.name

                self.getToken()
                if self.currentToken.token == '(':
                    self.getToken()
                    self.parametros_opcional()

                    self.symtable.table[self.nameProc]['param'] = self.paramProc
                    self.paramProc = []

                    if self.currentToken.token == ')':
                        self.getToken()
                        self.declaracoes_locais()
                        self.comandos()

                        if self.currentToken.token == 'fim_procedimento':
                            for l in self.localIdent:
                                self.symtable.removeSymbol(l)
                            self.isProcedure = False
                            self.localIdent=[]
                            self.nameProc=""
                            self.paramProc = []

                            self.getToken()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()

        # | funcao IDENT ( <parametros_opcional> ) : <tipo_estendido> <declaracoes_locais> <comandos> fim_funcao
        elif self.currentToken.token == 'funcao':
            self.getToken()

            if self.currentToken.token == 'identificador':

                # insert symbol in symbol table
                if not self.symtable.insertSymbol(self.currentToken.name, (self.currentToken.name, self.currentToken.token, 'funcao', '', '', self.scope, [])):
                    self.listError.append('Linha ' + self.lexer.lineNumber + ': identificador ' + self.currentToken.name + ' ja declarado anteriormente')

                self.isProcedure = True
                self.nameProc = self.currentToken.name

                self.getToken()
                if self.currentToken.token == '(':
                    self.getToken()
                    self.parametros_opcional()

                    self.symtable.table[self.nameProc]['param'] = self.paramProc
                    self.paramProc = []

                    if self.currentToken.token == ')':
                        self.getToken()
                        if self.currentToken.token == ':':
                            self.getToken()
                            self.tipo_estendido()
                            self.declaracoes_locais()
                            self.comandos()

                            if self.currentToken.token == 'fim_funcao':
                                for l in self.localIdent:
                                    self.symtable.removeSymbol(l)
                                self.isProcedure = False
                                self.localIdent = []
                                self.nameProc = ""
                                self.paramProc = []

                                self.getToken()
                            else:
                                self.error()
                        else:
                            self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()
    
    # 19
    def parametros_opcional(self):
        # <parametro> | 3
        if self.currentToken.token in self.firstOf('parametro'):
            self.parametro()

    # 20
    def parametro(self):
        # <var_opcional> <identificador> <mais_ident> : <tipo_estendido> <mais_parametros>

        self.declaring = True
        self.var_opcional()
        self.identificador()
        self.mais_ident()

        if self.currentToken.token == ':':
            self.getToken()
            self.param = True
            self.tipo_estendido()
            self.mais_parametros()
            self.declaring = False
            self.param = False
        else:
            self.error()

    # 21
    def var_opcional(self):
        # var | 3
        if self.currentToken.token == 'var':
            self.getToken()

    # 22
    def mais_parametros(self):
        # , <parametro> | 3
        if self.currentToken.token == ',':
            self.getToken()
            self.parametro()

    # 23
    def declaracoes_locais(self):
        # <declaracao_local> <declaracoes_locais> | 3
        if self.currentToken.token in self.firstOf('declaracao_local'):
            self.declaracao_local()
            self.declaracoes_locais()

    # 24
    def corpo(self):
        # <declaracoes_locais> <comandos>
        self.declaracoes_locais()
        self.comandos()

    # 25
    def comandos(self):
        # <cmd> <comandos> | 3
        while self.currentToken.token in self.firstOf('cmd'):
            self.cmd()
    
    # 26 
    def cmd(self):
        # leia ( <identificador> <mais_ident> )
        if self.currentToken.token == 'leia':
            self.getToken()
            if self.currentToken.token == '(':
                self.getToken()
                self.identificador()
                self.mais_ident()

                if self.currentToken.token == ')':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | escreva ( <expressao> <mais_expressao> )
        elif self.currentToken.token == 'escreva':
            self.getToken()
            if self.currentToken.token == '(':
                self.getToken()
                self.expressao()
                self.mais_expressao()

                if self.currentToken.token == ')':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | se <expressao> entao <comandos> <senao_opcional> fim_se
        elif self.currentToken.token == 'se':
            self.getToken()
            self.expressao()

            if self.currentToken.token == 'entao':
                self.getToken()
                self.comandos()
                self.senao_opcional()

                if self.currentToken.token == 'fim_se':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | caso <exp_aritmetica> seja <selecao> <senao_opcional> fim_caso
        elif self.currentToken.token == 'caso':
            self.getToken()
            self.exp_aritmetica()

            if self.currentToken.token == 'seja':
                self.getToken()
                self.selecao()
                self.senao_opcional()

                if self.currentToken.token == 'fim_caso':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | para IDENT <- <exp_aritmetica> ate <exp_aritmetica> faca <comandos> fim_para
        elif self.currentToken.token == 'para':
            self.getToken()

            if self.currentToken.token == 'identificador':
                self.getToken()

                if self.currentToken.token == '<-':
                    self.getToken()
                    self.exp_aritmetica()

                    if self.currentToken.token == 'ate':
                        self.getToken()
                        self.exp_aritmetica()

                        if self.currentToken.token == 'faca':
                            self.getToken()
                            self.comandos()

                            if self.currentToken.token == 'fim_para':
                                self.getToken()
                            else:
                                self.error()

                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()

        # | enquanto <expressao> faca <comandos> fim_enquanto
        elif self.currentToken.token == 'enquanto':
            self.getToken()
            self.expressao()

            if self.currentToken.token == 'faca':
                self.getToken()
                self.comandos()

                if self.currentToken.token == 'fim_enquanto':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | faca <comandos> ate <expressao>
        elif self.currentToken.token == 'faca':
            self.getToken()
            self.comandos()

            if self.currentToken.token == 'ate':
                self.getToken()
                self.expressao()
            else:
                self.error()

        # | ^ IDENT <outros_ident> <dimensao> <- <expressao>
        elif self.currentToken.token == '^':
            self.getToken()
            if self.currentToken.token == 'identificador':
                if self.currentToken.name not in self.symtable.table:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' nao declarado')
                else:
                    self.returnType = self.symtable.table[self.currentToken.name]['type']
                    self.returnVar = self.currentToken.name
                self.getToken()
                self.outros_ident()
                self.dimensao()

                if self.currentToken.token == '<-':
                    lineN = self.lexer.lineNumber
                    self.getToken()
                    if self.expressao() == "error":
                        self.listError.append("Linha " + str(lineN) + ": atribuicao nao compativel para ^" + self.returnVar)

                    self.returnType = ""
                    self.returnVar = ""
                else:
                    self.error()

            else:
                self.error()

        # | IDENT <chamada_atribuicao>
        elif self.currentToken.token == 'identificador':
            if self.currentToken.name not in self.symtable.table:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' nao declarado')
            else:
                if self.symtable.table[self.currentToken.name]['category'] == "ponteiro":
                    self.returnType = "endereco"
                else:
                    self.returnType = self.symtable.table[self.currentToken.name]['type']
                self.returnVar = self.currentToken.name
            lineN = self.lexer.lineNumber
            self.getToken()
            ret = self.chamada_atribuicao()
            if ret != self.returnType:
                if ret == "inteiro" and self.returnType == "real":
                    pass
                else:
                    if self.returnVar != "":
                        self.listError.append("Linha " + str(lineN) + ": atribuicao nao compativel para " + self.returnVar)
            self.returnType = ""
            self.returnVar = ""

        # | retorne <expressao>
        elif self.currentToken.token == 'retorne':
            self.getToken()
            self.expressao()
        else:
            self.error()

    # 27
    def mais_expressao(self):
        # , <expressao> <mais_expressao> | 3
        if self.currentToken.token == ',':
            self.getToken()
            self.expressao()
            self.mais_expressao()
    
    # 28
    def senao_opcional(self):
        # senao <comandos> | 3
        if self.currentToken.token == 'senao':
            self.getToken()
            self.comandos()
    
    # 29
    def chamada_atribuicao(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> <- <expressao>
        if self.currentToken.token == '(':
            self.getToken()
            self.expressao()
            self.mais_expressao()

            if self.currentToken.token == ')':
                self.getToken()
            else:
                self.error()

        else:
            self.outros_ident()
            self.dimensao()

            if self.currentToken.token == '<-':
                self.getToken()
                return self.expressao()
            else:
                self.error()
    
    # 30
    def selecao(self):
        # <constantes> : <comandos> <mais_selecao>
        self.constantes()

        if self.currentToken.token == ':':
            self.getToken()
            self.comandos()
            self.mais_selecao()
        else:
            self.error()

    # 31
    def mais_selecao(self):
        # <selecao> | 3
        if self.currentToken.token in self.firstOf('selecao'):
            self.selecao()

    # 32
    def constantes(self):
        # <numero_intervalo> <mais_constantes>
        self.numero_intervalo()
        self.mais_constantes()

    # 33
    def mais_constantes(self):
        # , <constantes> | 3
        if self.currentToken.token == ',':
            self.getToken()
            self.mais_constantes()

    # 34
    def numero_intervalo(self):
        # <op_unario> NUM_INT <intervalo_opcional>
        self.op_unario()

        if self.currentToken.token == 'numero_inteiro':
            self.getToken()
            self.intervalo_opcional()
        else:
            self.error()

    # 35
    def intervalo_opcional(self):
        # .. <op_unario> NUM_INT | 3
        if self.currentToken.token == '..':
            self.getToken()
            self.op_unario()

            if self.currentToken.token == 'numero_inteiro':
                self.getToken()
            else:
                self.error()

    # 36
    def op_unario(self):
        # - | 3
        if self.currentToken.token == '-':
            self.getToken()

    # 37
    def exp_aritmetica(self):
        # <termo> <outros_termos>
        ret1 = self.termo()
        ret2 = self.outros_termos()
        if ret2 == "error":
            return "error"
        else:
            return ret1

    # 38
    def op_multiplicacao(self):
        # * | /
        if self.currentToken.token == '*' or self.currentToken.token == '/':
            self.getToken()
        else:
            self.error()

    # 39
    def op_adicao(self):
        # + | -
        if self.currentToken.token == '+' or self.currentToken.token == '-':
            self.getToken()
        else:
            self.error()

    # 40
    def termo(self):
        # <fator> <outros_fatores>
        ret1 = self.fator()
        ret2 = self.outros_fatores()
        if ret2 == "error":
            return "error"
        else:
            return ret1

    # 41
    def outros_termos(self):
        # <op_adicao> <termo> <outros_termos> | 3
        retf = ""
        while self.currentToken.token in self.firstOf('op_adicao'):
            self.op_adicao()
            ret2 = self.termo()
            if ret2 == "error":
                retf = "error"
        return retf

    # 42
    def fator(self):
        # <parcela> <outras_parcelas>
        ret1 = self.parcela()
        ret2 = self.outras_parcelas()
        if ret2 == "error":
            return "error"
        else:
            return ret1

    # 43
    def outros_fatores(self):
        # <op_multiplicacao> <fator> <outros_termos> | 3
        retf = ""
        while self.currentToken.token in self.firstOf('op_multiplicacao'):
            self.op_multiplicacao()
            ret1 = self.fator()
            ret2 = self.outros_termos()
            if ret1 == "error" or ret2 == "error":
                retf = "error"
        return retf

    # 44
    def parcela(self):
        # <op_unario> <parcela_unario> | <parcela_nao_unario>
        if self.currentToken.token in self.firstOf("parcela_nao_unario"):
            return self.parcela_nao_unario()
        else:
            self.op_unario()
            return self.parcela_unario()

    # 45
    def parcela_unario(self):
        # ^ IDENT <outros_ident> <dimensao> | IDENT <chamada_partes> | NUM_INT | NUM_REAL | ( <expressao> )
        if self.currentToken.token == '^':
            self.getToken()
            if self.currentToken.token == 'identificador':
                self.getToken()
                self.outros_ident()
                self.dimensao()
            else:
                self.error()

        elif self.currentToken.token == 'identificador':
            ok = True
            if self.currentToken.name not in self.symtable.table:
                self.listError.append("Linha " + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' nao declarado')
                ok = False
            tmpToken = self.currentToken.name

            if self.isProcedure:
                self.paramProc.append(self.symtable.table[tmpToken]['type'])

            if tmpToken in self.symtable.table and (self.symtable.table[tmpToken]['category'] == "procedimento" or self.symtable.table[tmpToken]['category'] == "funcao"):
                self.paramProc = []
                self.isProcedure = True
            self.getToken()
            self.chamada_partes()

            if self.isProcedure and (self.symtable.table[tmpToken]['category'] == "procedimento" or self.symtable.table[tmpToken]['category'] == "funcao"):
                self.isProcedure = False
                if self.paramProc != self.symtable.table[tmpToken]['param']:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ": incompatibilidade de parametros na chamada de " + tmpToken)
                self.paramProc = []
            if ok:
                if self.returnType == "real" and (self.symtable.table[tmpToken]['type'] == "real" or self.symtable.table[tmpToken]['type'] == "inteiro"):
                    return self.symtable.table[tmpToken]['type']
                elif self.returnType == self.symtable.table[tmpToken]['type']:
                    return self.symtable.table[tmpToken]['type']
                else:
                    return "error"
            else:
                return ""

        elif self.currentToken.token == 'numero_inteiro':
            self.getToken()
            if self.returnType == "real" or self.returnType == "inteiro":
                return "inteiro"
            else:
                return "error"

        elif self.currentToken.token == 'numero_real':
            self.getToken()
            if self.returnType == "real":
                return "real"
            else:
                return "error"

        elif self.currentToken.token == '(':
            self.getToken()
            ret = self.expressao()

            if self.currentToken.token == ')':
                self.getToken()
                return ret
            else:
                self.error()
        else:
            self.error()
    
    # 46
    def parcela_nao_unario(self):
        # & IDENT <outros_ident> <dimensao> | CADEIA
        if self.currentToken.token == '&':
            self.getToken()

            if self.currentToken.token == 'identificador':
                if self.currentToken.name not in self.symtable.table:
                    self.listError.append("Linha " + str(self.lexer.lineNumber) + ': identificador ' + self.currentToken.name + ' nao declarado')
                self.getToken()
                self.outros_ident()
                self.dimensao()
                if self.returnType == "endereco":
                    return "endereco"
                else:
                    return "error"
            else:
                self.error()

        elif self.currentToken.token == 'cadeia_literal':
            self.getToken()
            if self.returnType == "literal":
                return "literal"
            else:
                return "error"
        else:
            self.error()

    # 47
    def outras_parcelas(self):
        # % <parcela> <outras_parcelas> | 3
        if self.currentToken.token == '%':
            self.getToken()
            self.parcela()
            self.outras_parcelas()
            return "inteiro"

    # 48
    def chamada_partes(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> | 3
        if self.currentToken.token == '(':
            self.getToken()

            ret1 = self.expressao()
            ret2 = self.mais_expressao()



            if self.currentToken.token == ')':
                self.getToken()
                if ret1 == "error":
                    return "error"
                else:
                    return ret1
            else:
                self.error()

        elif self.currentToken.token in self.firstOf('outros_ident') or\
                self.currentToken.token in self.firstOf('dimensao'):
            self.outros_ident()
            self.dimensao()

    # 49
    def exp_relacional(self):
        # <exp_aritmetica> <op_opcional>
        ret1 = self.exp_aritmetica()
        ret2 = self.op_opcional()
        if ret2 == "logico":
            return "logico"
        else:
            return ret1

    # 50
    def op_opcional(self):
        # <op_relacional> <exp_aritmetica> | 3
        if self.currentToken.token in self.firstOf('op_relacional'):
            self.op_relacional()
            self.exp_aritmetica()
            if self.returnType == "logico":
                return "logico"
            else:
                return "error"
        return ""

    # 51
    def op_relacional(self):
        # = | <> | >= | <= | > | <
        if self.currentToken.token == '=' or self.currentToken.token == '<>' or \
                        self.currentToken.token == '>=' or self.currentToken.token == '<=' or \
                        self.currentToken.token == '>' or self.currentToken.token == '<':

            self.getToken()
        else:
            self.error()

    # 52
    def expressao(self):
        # <termo_logico> <outros_termos_logicos>
        ret1 = self.termo_logico()
        ret2 = self.outros_termos_logicos()
        if self.isProcedure and ret1!="error":
                self.paramProc.append(ret1)
        if ret2 == "error":
            return "error"
        else:
            return ret1
    
    # 53
    def op_nao(self):
        # nao | 3
        if self.currentToken.token == 'nao':
            self.getToken()
            if self.returnType == "logico":
                return "logico"
            else:
                return "error"
    
    # 54
    def termo_logico(self):
        # <fator_logico> <outros_fatores_logicos>
        ret1 = self.fator_logico()
        ret2 = self.outros_fatores_logicos()
        if ret2 == "error":
            return "error"
        else:
            return ret1

    # 55
    def outros_termos_logicos(self):
        # ou <termo_logico> <outros_termos_logicos> | 3
        if self.currentToken.token == 'ou':
            self.getToken()
            self.termo_logico()
            self.outros_termos_logicos()
            if self.returnType == "logico":
                return "logico"
            else:
                return "error"

    # 56
    def outros_fatores_logicos(self):
        # e <fator_logico> <outros_fatores_logicos> | 3
        if self.currentToken.token == 'e':
            self.getToken()
            self.fator_logico()
            self.outros_fatores_logicos()
            if self.returnType == "logico":
                return "logico"
            else:
                return "error"

    # 57
    def fator_logico(self):
        # <op_nao> <parcela_logica>
        ret1 = self.op_nao()
        ret2 = self.parcela_logica()
        if ret1 == "error":
            return "error"
        else:
            return ret2

    # 58
    def parcela_logica(self):
        # verdadeiro | falso | <exp_relacional>
        if self.currentToken.token == 'verdadeiro' or self.currentToken.token == 'falso':
            self.getToken()
            if self.returnType == "logico":
                return "logico"
            else:
                return "error"
        elif self.currentToken.token in self.firstOf('exp_relacional'):
            return self.exp_relacional()
        else:
            self.error()
