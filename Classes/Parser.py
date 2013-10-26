__author__ = 'matheus_rafael_thiago_bruno'

from Classes.Token import Token


class Parser(object):
    def __init__(self, lexer, error):
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

        # Error instance
        self.errorRef = error

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

        if self.currentToken.category == 'algoritmo':
            self.getToken()
        else:
            self.error()

        self.corpo()

        if self.currentToken.category == 'fim_algoritmo':
            pass
        else:
            self.error()

    # 2
    def declaracoes(self):
        # <decl_local_global> <declaracoes> | 3
        while self.currentToken.category in self.firstOf('declaracoes'):  # [?]
            self.decl_local_global()
            self.declaracoes()

    # 3
    def decl_local_global(self):
        # <declaracao_local> | <declaracao_global>
        if self.currentToken.category in self.firstOf('declaracao_local'):
            self.declaracao_local()
        elif self.currentToken.category in self.firstOf('declaracao_global'):
            self.declaracao_global()
        else:
            self.error()

    # 4
    def declaracao_local(self):
        # declare <variavel>
        # | constante IDENT : <tipo_basico> = <valor_constante>
        # | tipo IDENT : <tipo>
        if self.currentToken.category == 'declare':
            self.getToken()
            self.variavel()

        elif self.currentToken.category == 'constante':
            self.getToken()

            if self.currentToken.category == 'identificador':
                self.getToken()

                if self.currentToken.category == ':':
                    self.getToken()
                    self.tipo_basico()

                    if self.currentToken.category == '=':
                        self.getToken()
                        self.valor_constante()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()

        elif self.currentToken.category == 'tipo':
            self.getToken()
            if self.currentToken.category == 'identificador':
                self.getToken()
                if self.currentToken.category == ':':
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

        if self.currentToken.category == ':':
            self.getToken()
            self.tipo()
        else:
            self.error()
    
    # 6
    def identificador(self):
        # <ponteiro_opcional> IDENT <outros_ident> <dimensao>
        self.ponteiro_opcional()
        if self.currentToken.category == 'identificador':
            self.getToken()
            self.outros_ident()
            self.dimensao()
        else:
            self.error()

    # 7
    def ponteiro_opcional(self):
        # ^ | 3
        if self.currentToken.category == '^':
            self.getToken()

    # 8
    def outros_ident(self):
        # . IDENT <outros_ident> | 3
        if self.currentToken.category == '.':
            self.getToken()

            if self.currentToken.category == 'identificador':
                self.getToken()
                self.outros_ident()
            else:
                self.error()
    
    # 9
    def dimensao(self):
        # [ <exp_aritmetica ] <dimensao> | 3
        if self.currentToken.category == '[':
            self.getToken()
            self.exp_aritmetica()

            if self.currentToken.category == ']':
                self.getToken()
                self.dimensao()
            else:
                self.error()

    # 10
    def tipo(self):
        # <registro> | <tipo_estendido>
        if self.currentToken.category in self.firstOf('registro'):
            self.registro()
        elif self.currentToken.category in self.firstOf('tipo_estendido'):
            self.tipo_estendido()
        else:
            self.error()
    
    # 11
    def mais_ident(self):
        # , <identificador> <mais_ident> | 3
        if self.currentToken.category == ',':
            self.getToken()
            self.identificador()
            self.mais_ident()

    # 12
    def mais_variaveis(self):
        # <variavel> <mais_variaveis> | 3
        if self.currentToken.category in self.firstOf('variavel'):
            self.variavel()
            self.mais_variaveis()

    # 13
    def tipo_basico(self):
        # literal | inteiro | real | logico
        if self.currentToken.category == 'literal' or self.currentToken.category == 'inteiro' or \
                self.currentToken.category == 'real' or self.currentToken.category == 'logico':
            self.getToken()
        else:
            self.error()
    
    # 14
    def tipo_basico_ident(self):
        # <tipo_basico> | IDENT
        if self.currentToken.category in self.firstOf('tipo_basico'):
            self.tipo_basico()
        else:
            if self.currentToken.category == 'identificador':
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
        if self.currentToken.category == 'cadeia_literal' or self.currentToken.category == 'numero_inteiro' or \
                        self.currentToken.category == 'numero_real' or self.currentToken.category == 'verdadeiro' or \
                        self.currentToken.category == 'falso':
            self.getToken()
        else:
            self.error()
    
    # 17
    def registro(self):
        # registro <variavel> <mais_variaveis> fim_registro
        if self.currentToken.category == 'registro':
            self.getToken()
            self.variavel()
            self.mais_variaveis()

            if self.currentToken.category == 'fim_registro':
                self.getToken()
            else:
                self.error()
        else:
            self.error()
    
    # 18
    def declaracao_global(self):
        # procedimento IDENT ( <parametros_opcional> ) <declaracoes_locais> <comandos> fim_procedimento
        if self.currentToken.category == 'procedimento':
            self.getToken()
            if self.currentToken.category == 'identificador':
                self.getToken()
                if self.currentToken.category == '(':
                    self.getToken()
                    self.parametros_opcional()

                    if self.currentToken.category == ')':
                        self.getToken()
                        self.declaracoes_locais()
                        self.comandos()

                        if self.currentToken.category == 'fim_procedimento':
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
        elif self.currentToken.category == 'funcao':
            self.getToken()
            if self.currentToken.category == 'identificador':
                self.getToken()
                if self.currentToken.category == '(':
                    self.getToken()
                    self.parametros_opcional()

                    if self.currentToken.category == ')':
                        self.getToken()
                        if self.currentToken.category == ':':
                            self.getToken()
                            self.tipo_estendido()
                            self.declaracoes_locais()
                            self.comandos()

                            if self.currentToken.category == 'fim_funcao':
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
        if self.currentToken.category in self.firstOf('parametro'):
            self.parametro()

    # 20
    def parametro(self):
        # <var_opcional> <identificador> <mais_ident> : <tipo_estendido> <mais_parametros>
        self.var_opcional()
        self.identificador()
        self.mais_ident()

        if self.currentToken.category == ':':
            self.getToken()
            self.tipo_estendido()
            self.mais_parametros()
        else:
            self.error()

    # 21
    def var_opcional(self):
        # var | 3
        if self.currentToken.category == 'var':
            self.getToken()

    # 22
    def mais_parametros(self):
        # , <parametro> | 3
        if self.currentToken.category == ',':
            self.getToken()
            self.parametro()

    # 23
    def declaracoes_locais(self):
        # <declaracao_local> <declaracoes_locais> | 3
        if self.currentToken.category in self.firstOf('declaracao_local'):
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
        while self.currentToken.category in self.firstOf('cmd'):
            self.cmd()
    
    # 26 
    def cmd(self):
        # leia ( <identificador> <mais_ident> )
        if self.currentToken.category == 'leia':
            self.getToken()
            if self.currentToken.category == '(':
                self.getToken()
                self.identificador()
                self.mais_ident()

                if self.currentToken.category == ')':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | escreva ( <expressao> <mais_expressao> )
        elif self.currentToken.category == 'escreva':
            self.getToken()
            if self.currentToken.category == '(':
                self.getToken()
                self.expressao()
                self.mais_expressao()

                if self.currentToken.category == ')':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | se <expressao> entao <comandos> <senao_opcional> fim_se
        elif self.currentToken.category == 'se':
            self.getToken()
            self.expressao()

            if self.currentToken.category == 'entao':
                self.getToken()
                self.comandos()
                self.senao_opcional()

                if self.currentToken.category == 'fim_se':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | caso <exp_aritmetica> seja <selecao> <senao_opcional> fim_caso
        elif self.currentToken.category == 'caso':
            self.getToken()
            self.exp_aritmetica()

            if self.currentToken.category == 'seja':
                self.getToken()
                self.selecao()
                self.senao_opcional()

                if self.currentToken.category == 'fim_caso':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | para IDENT <- <exp_aritmetica> ate <exp_aritmetica> faca <comandos> fim_para
        elif self.currentToken.category == 'para':
            self.getToken()

            if self.currentToken.category == 'identificador':
                self.getToken()

                if self.currentToken.category == '<-':
                    self.getToken()
                    self.exp_aritmetica()

                    if self.currentToken.category == 'ate':
                        self.getToken()
                        self.exp_aritmetica()

                        if self.currentToken.category == 'faca':
                            self.getToken()
                            self.comandos()

                            if self.currentToken.category == 'fim_para':
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
        elif self.currentToken.category == 'enquanto':
            self.getToken()
            self.expressao()

            if self.currentToken.category == 'faca':
                self.getToken()
                self.comandos()

                if self.currentToken.category == 'fim_enquanto':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()

        # | faca <comandos> ate <expressao>
        elif self.currentToken.category == 'faca':
            self.getToken()
            self.comandos()

            if self.currentToken.category == 'ate':
                self.getToken()
                self.expressao()
            else:
                self.error()

        # | ^ IDENT <outros_ident> <dimensao> <- <expressao>
        elif self.currentToken.category == '^':
            self.getToken()
            if self.currentToken.category == 'identificador':
                self.getToken()
                self.outros_ident()
                self.dimensao()

                if self.currentToken.category == '<-':
                    self.getToken()
                    self.expressao()
                else:
                    self.error()

            else:
                self.error()

        # | IDENT <chamada_atribuicao>
        elif self.currentToken.category == 'identificador':
            self.getToken()
            self.chamada_atribuicao()

        # | retorne <expressao>
        elif self.currentToken.category == 'retorne':
            self.getToken()
            self.expressao()
        else:
            self.error()

    # 27
    def mais_expressao(self):
        # , <expressao> <mais_expressao> | 3
        if self.currentToken.category == ',':
            self.getToken()
            self.expressao()
            self.mais_expressao()
    
    # 28
    def senao_opcional(self):
        # senao <comandos> | 3
        if self.currentToken.category == 'senao':
            self.getToken()
            self.comandos()
    
    # 29
    def chamada_atribuicao(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> <- <expressao>
        if self.currentToken.category == '(':
            self.getToken()
            self.expressao()
            self.mais_expressao()

            if self.currentToken.category == ')':
                self.getToken()
            else:
                self.error()

        else:
            self.outros_ident()
            self.dimensao()

            if self.currentToken.category == '<-':
                self.getToken()
                self.expressao()
            else:
                self.error()
    
    # 30
    def selecao(self):
        # <constantes> : <comandos> <mais_selecao>
        self.constantes()

        if self.currentToken.category == ':':
            self.getToken()
            self.comandos()
            self.mais_selecao()
        else:
            self.error()

    # 31
    def mais_selecao(self):
        # <selecao> | 3
        if self.currentToken.category in self.firstOf('selecao'):
            self.selecao()

    # 32
    def constantes(self):
        # <numero_intervalo> <mais_constantes>
        self.numero_intervalo()
        self.mais_constantes()

    # 33
    def mais_constantes(self):
        # , <constantes> | 3
        if self.currentToken.category == ',':
            self.getToken()
            self.mais_constantes()

    # 34
    def numero_intervalo(self):
        # <op_unario> NUM_INT <intervalo_opcional>
        self.op_unario()

        if self.currentToken.category == 'numero_inteiro':
            self.getToken()
            self.intervalo_opcional()
        else:
            self.error()

    # 35
    def intervalo_opcional(self):
        # .. <op_unario> NUM_INT | 3
        if self.currentToken.category == '..':
            self.getToken()
            self.op_unario()

            if self.currentToken.category == 'numero_inteiro':
                self.getToken()
            else:
                self.error()

    # 36
    def op_unario(self):
        # - | 3
        if self.currentToken.category == '-':
            self.getToken()

    # 37
    def exp_aritmetica(self):
        # <termo> <outros_termos>
        self.termo()
        self.outros_termos()

    # 38
    def op_multiplicacao(self):
        # * | /
        if self.currentToken.category == '*' or self.currentToken.category == '/':
            self.getToken()
        else:
            self.error()

    # 39
    def op_adicao(self):
        # + | -
        if self.currentToken.category == '+' or self.currentToken.category == '-':
            self.getToken()
        else:
            self.error()

    # 40
    def termo(self):
        # <fator> <outros_fatores>
        self.fator()
        self.outros_fatores()

    # 41
    def outros_termos(self):
        # <op_adicao> <termo> <outros_termos> | 3
        while self.currentToken.category in self.firstOf('op_adicao'):
            self.op_adicao()
            self.termo()

    # 42
    def fator(self):
        # <parcela> <outras_parcelas>
        self.parcela()
        self.outras_parcelas()

    # 43
    def outros_fatores(self):
        # <op_multiplicacao> <fator> <outros_termos> | 3
        while self.currentToken.category in self.firstOf('op_multiplicacao'):
            self.op_multiplicacao()
            self.fator()
            self.outros_termos()

    # 44
    def parcela(self):
        # <op_unario> <parcela_unario> | <parcela_nao_unario>
        if self.currentToken.category in self.firstOf("parcela_nao_unario"):
            self.parcela_nao_unario()
        else:
            self.op_unario()
            self.parcela_unario()

    # 45
    def parcela_unario(self):
        # ^ IDENT <outros_ident> <dimensao> | IDENT <chamada_partes> | NUM_INT | NUM_REAL | ( <expressao> )
        if self.currentToken.category == '^':
            self.getToken()
            if self.currentToken.category == 'identificador':
                self.getToken()
                self.outros_ident()
                self.dimensao()
            else:
                self.error()

        elif self.currentToken.category == 'identificador':
            self.getToken()
            self.chamada_partes()

        elif self.currentToken.category == 'numero_inteiro' or self.currentToken.category == 'numero_real':
            self.getToken()

        elif self.currentToken.category == '(':
            self.getToken()
            self.expressao()

            if self.currentToken.category == ')':
                self.getToken()
            else:
                self.error()
        else:
            self.error()
    
    # 46
    def parcela_nao_unario(self):
        # & IDENT <outros_ident> <dimensao> | CADEIA
        if self.currentToken.category == '&':
            self.getToken()

            if self.currentToken.category == 'identificador':
                self.getToken()
                self.outros_ident()
                self.dimensao()
            else:
                self.error()

        elif self.currentToken.category == 'cadeia_literal':
            self.getToken()
        else:
            self.error()

    # 47
    def outras_parcelas(self):
        # % <parcela> <outras_parcelas> | 3
        if self.currentToken.category == '%':
            self.getToken()
            self.parcela()
            self.outras_parcelas()

    # 48
    def chamada_partes(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> | 3
        if self.currentToken.category == '(':
            self.getToken()
            self.expressao()
            self.mais_expressao()

            if self.currentToken.category == ')':
                self.getToken()
            else:
                self.error()

        elif self.currentToken.category in self.firstOf('outros_ident') or\
                self.currentToken.category in self.firstOf('dimensao'):
            self.outros_ident()
            self.dimensao()

    # 49
    def exp_relacional(self):
        # <exp_aritmetica> <op_opcional>
        self.exp_aritmetica()
        self.op_opcional()
    
    # 50
    def op_opcional(self):
        # <op_relacional> <exp_aritmetica> | 3
        if self.currentToken.category in self.firstOf('op_relacional'):
            self.op_relacional()
            self.exp_aritmetica()
    
    # 51
    def op_relacional(self):
        # = | <> | >= | <= | > | <
        if self.currentToken.category == '=' or self.currentToken.category == '<>' or \
                        self.currentToken.category == '>=' or self.currentToken.category == '<=' or \
                        self.currentToken.category == '>' or self.currentToken.category == '<':
            self.getToken()
        else:
            self.error()

    # 52
    def expressao(self):
        # <termo_logico> <outros_termos_logicos>
        self.termo_logico()
        self.outros_termos_logicos()
    
    # 53
    def op_nao(self):
        # nao | 3
        if self.currentToken.category == 'nao':
            self.getToken()
    
    # 54
    def termo_logico(self):
        # <fator_logico> <outros_fatores_logicos>
        self.fator_logico()
        self.outros_fatores_logicos()

    # 55
    def outros_termos_logicos(self):
        # ou <termo_logico> <outros_termos_logicos> | 3
        if self.currentToken.category == 'ou':
            self.getToken()
            self.termo_logico()
            self.outros_termos_logicos()

    # 56
    def outros_fatores_logicos(self):
        # e <fator_logico> <outros_fatores_logicos> | 3
        if self.currentToken.category == 'e':
            self.getToken()
            self.fator_logico()
            self.outros_fatores_logicos()

    # 57
    def fator_logico(self):
        # <op_nao> <parcela_logica>
        self.op_nao()
        self.parcela_logica()

    # 58
    def parcela_logica(self):
        # verdadeiro | falso | <exp_relacional>
        if self.currentToken.category == 'verdadeiro' or self.currentToken.category == 'falso':
            self.getToken()
        elif self.currentToken.category in self.firstOf('exp_relacional'):
            self.exp_relacional()
        else:
            self.error()
