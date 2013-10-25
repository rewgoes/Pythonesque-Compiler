__author__ = 'matheus_rafael_thiago_bruno'

from Classes.Token import Token


class Parser(object):

    def __init__(self, lexer):
        # Tokens read from input will populate this list
        # Parser will read this list until it's empty
        # When list is empty, parser will call LexicalAy.getToken()
        self.listToken = []

        # Reference to the lexer object
        self.lexer = lexer

        # This variable stores the current token being analysed
        self.currentToken = Token('a', 'a')

        # This is first-set of non-terminals ("primeiros")
        # It's a dictionary where the non-terminal/terminal is the key
        # And the value is a list with the firsts
        # Use the firstOf method to access the list
        # TODO: Complete the firstSet list, remember to check if the non-terminal you're doing is already in this list
        self.firstSet = \
            {  # Matheus (01-15)
            'programa':  ['algoritmo', 'declare', 'constante', 'tipo', 'procedimento', 'funcao'],
            'declaracoes': ['3', 'declare', 'constante', 'tipo', 'procedimento', 'funcao' ],
            'declaracao_local_global': ['declare', 'constante', 'tipo', 'procedimento', 'funcao' ],
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
            'tipo_basico_ident': ['literal', 'inteiro', 'real', 'logico', 'identificador'],  # How to handle this `IDENT` ?
            'tipo_estendido': ['^', 'literal', 'inteiro', 'real', 'logico', 'identificador'],
             
            # Rafael (16-30)
            'valor_constante': ['cadeia_literal', 'numero_inteiro', 'numero_real', 'verdadeiro', 'falso'],
            'registro': ['registro'],
            'declaracao_global': ['procedimento','funcao'],
            'parametros_opcional': ['3','var','^','identificador'],
            'parametro': ['var','^','identificador'],
            'var_opcional': ['var', '3'],
            'mais_parametros': [',', '3'],
            'declaracoes_locais': ['3', 'declare', 'constante', 'tipo'],
            'corpo': ['leia','escreva','se','caso','para','enquanto','faca','^','identificador','retorne','declare', 'constante', 'tipo','3'],
            'comandos': ['leia','escreva','se','caso','para','enquanto','faca','^','identificador','retorne','3'],
            'cmd': ['leia','escreva','se','caso','para','enquanto','faca','^','identificador','retorne'],
            'mais_expressao': [',','3'],
            'senao_opcional': ['senao','3'],
            'chamada_atribuicao': ['(','.','[','<-'],
            'selecao': ['-', 'numero_inteiro'],
             
            # Thiago (31-44)
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

            # Bruno (45-58)
            'parcela_unario': ['^', 'identificador', 'numero_inteiro', 'numero_real', '('],
            'parcela_nao_unario': ['&', 'cadeia_literal'],
            'outras_parcelas': ['%', '3'],
            'chamada_partes': ['(','.','[','3'],
            'exp_relacional': ['-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
            'op_opcional': ['=', '<>', '>=', '<=', '>', '<', '3'],
            'op_relacional': ['=', '<>', '>=', '<=', '>', '<'],
            'expressao': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
            'op_nao': ['nao', '3'],
            'termo_logico': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
            'outros_termos_logicos': ['ou', '3'],
            'outros_fatores_logicos': ['e', '3'],
            'fator_logico': ['nao', 'verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
            'parcela_logica': ['verdadeiro', 'falso', '-', '^', 'identificador', 'numero_inteiro', 'numero_real', '(', '&', 'cadeia_literal'],
            }

    # Helper methods

    def getToken(self):
        # Obtain the first token on the list
        while not self.listToken:
            self.listToken = self.lexer.getToken()

        self.currentToken = self.listToken.pop()

    def error(self):
        # TODO: Proper error handling
        pass

    def firstOf(self, term):
        if term in self.firstSet:
            # non-terminal
            return self.firstSet.get(term)
        else:
            # terminal
            return term

    # Grammar rules
    # Matheus (01-15)
    def programa(self):
        # <declaracoes> algoritmo <corpo> fim_algoritmo
        self.declaracoes()

        if self.currentToken.name == 'algoritmo':
            self.getToken()
        else:
            self.error()

        self.corpo()

        if self.currentToken.name == 'fim_algoritmo':
            self.getToken()
        else:
            self.error()

    def declaracoes(self):
        # <decl_local_global> <declaracoes> | 3
        while self.currentToken.name in self.firstOf('declaracoes'):  # [?]
            self.getToken()
            self.decl_local_global()
            self.declaracoes()

    def decl_local_global(self):
        # <declaracao_local> | <declaracao_global>
        if self.currentToken.name in self.firstOf('declaracao_local'):
            self.declaracao_local()
        elif self.currentToken.name in self.firstOf('declaracao_global'):
            self.declaracao_global()
        else:
            self.error()

    def declaracao_local(self):
        # declare <variavel>
        # | constante IDENT : <tipo_basico> = <valor_constante>
        # | tipo IDENT : <tipo>
        if self.currentToken.name == 'declare':
            self.getToken()
            self.variavel()
        elif self.currentToken.name == 'constante':
            # TODO: IDENT again, what to do with this?
            self.getToken()
            if self.currentToken.name == ':':
                self.getToken()
                self.tipo_basico()
                if self.currentToken.name == '=':
                    self.getToken()
                    self.valor_constante()
                else:
                    self.error()
            else:
                self.error()

        elif self.currentToken.name == 'tipo':
            # IDENT
            self.getToken()
            if self.currentToken.name == ':':
                self.getToken()
                self.tipo()
            else:
                self.error()
        else:
            self.error()

    def variavel(self):
        # <identificador> <mais_ident> : <tipo>
        if self.currentToken.name in self.firstOf('identificador'):
            self.identificador()
            if self.currentToken.name in self.firstOf('mais_ident'):
                self.mais_ident()
                if self.currentToken.name == ':':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('tipo'):
                        self.tipo()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def identificador(self):
        # <ponteiro_opcional> IDENT <outros_ident> <dimensao>
        if self.currentToken.name in self.firstOf('ponteiro_opcional'):
            self.ponteiro_opcional()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name in self.firstOf('outros_ident'):
                    self.outros_ident()
                    if self.currentToken.name in self.firstOf('dimensao'):
                        self.dimensao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def ponteiro_opcional(self):
        # ^ | 3
        if self.currentToken.name == '^':
            self.getToken()

    def outros_ident(self):
        # . IDENT <outros_ident> | 3
        if self.currentToken.name == '.':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name in self.firstOf('outros_ident'):
                    self.outros_ident()
                else:
                    self.error()
            else:
                self.error()

    def dimensao(self):
        # [ <exp_aritmetica ] <dimensao> | 3
        if self.currentToken.name == '[':
            if self.currentToken.name in self.firstOf('exp_aritmetica'):
                self.exp_aritmetica()
                if self.currentToken.name == ']':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('dimensao'):
                        self.dimensao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()

    def tipo(self):
        # <registro> | <tipo_estendido>
        if self.currentToken.name in self.firstOf('registro'):
            self.registro()
        elif self.currentToken.name in self.firstOf('tipo_estendido'):
            self.tipo_estendido()
        else:
            self.error()

    def mais_ident(self):
        # , <identificador> <mais_ident> | 3
        if self.currentToken.name == ',':
            self.getToken()
            if self.currentToken.name in self.firstOf('identificador'):
                self.identificador()
                if self.currentToken.name in self.firstOf('mais_ident'):
                    self.mais_ident()
                else:
                    self.error()
            else:
                self.error()

    def mais_variaveis(self):
        # <variavel> <mais_variaveis> | 3
        if self.currentToken.name in self.firstOf('variavel'):
            self.variavel()
            if self.currentToken.name in self.firstOf('mais_variaveis'):
                self.mais_variaveis()
            else:
                self.error()

    def tipo_basico(self):
        # literal | inteiro | real | logico
        if self.currentToken.name == 'literal' or self.currentToken.name == 'inteiro' or self.currentToken.name == 'real' or self.currentToken.name == 'logico':
            self.getToken()
        else:
            self.error()

    def tipo_basico_ident(self):
        # <tipo_basico> | IDENT
        if self.currentToken.name in self.firstOf('tipo_basico'):
            self.tipo_basico()
        elif self.currentToken.name == 'identificador':
            self.getToken()
        else:
            self.error()

    def tipo_estendido(self):
        # <ponteiro_opcional> <tipo_basico_ident>
        if self.currentToken.name in self.firstOf('ponteiro_opcional'):
            self.ponteiro_opcional()
            if self.currentToken.name in self.firstOf('tipo_basico_ident'):
                self.tipo_basico_ident()
            else:
                self.error()
        else:
            self.error()

    def corpo(self):
        # <declaracoes_locais> <comandos>
        if self.currentToken.name in self.firstOf('declaracoes_locais'):
            self.declaracoes_locais()
            if self.currentToken.name in self.firstOf('comandos'):
                self.comandos()
            else:
                self.error()
        else:
            self.error()

    def declaracao_global(self):
        # procedimento IDENT ( <parametros_opcional> ) <declaracoes_locais> <comandos> fim_procedimento
        if self.currentToken.name == 'procedimento':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name == '(':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('parametros_opicional'):
                        self.parametros_opicinal()
                        if self.currentToken.name == ')':
                            self.getToken()
                            if self.currentToken.name in self.firstOf('declaracoes_locais'):
                                self.declaracoes_locais()
                                if self.currentToken.name in self.firstOf('comandos'):
                                    self.comandos()
                                    if self.currentToken.name == 'fim_procedimento':
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
                else:
                    self.error()
            else:
                self.error()
            
        # | funcao IDENT ( <parametros_opcional> ) : <tipo_estendido> <declaracoes_locais> <comandos> fim_funcao
        elif self.currentToken.name == 'funcao':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name == '(':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('parametros_opicional'):
                        self.parametros_opicinal()
                        if self.currentToken.name == ')':
                            self.getToken()
                            if self.currentToken.name == ':':
                                self.getToken()
                                if self.currentToken.name in self.firstOf('tipo_estendido'):
                                    self.tipo_estendido()
                                    if self.currentToken.name in self.firstOf('declaracoes_locais'):
                                        self.declaracoes_locais()
                                        if self.currentToken.name in self.firstOf('comandos'):
                                            self.comandos()
                                            if self.currentToken.name == 'fim_funcao':
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

    # Rafael (16-30)
    def valor_constante(self):
        # CADEIA | NUM_INT | NUM_REAL | verdadeiro | falso
        if self.currentToken.name == 'cadeia_literal' or self.currentToken.name == 'numero_inteiro' or self.currentToken.name == 'numero_real' or self.currentToken.name == 'verdadeiro' or self.currentToken.name == 'falso':
            self.getToken()
    
    def registro(self):
        # registro <variavel> <mais_variaveis> fim_registro
        if self.currentToken.name == 'registro':
            self.getToken()
            if self.currentToken.name in self.firstOf('variavel'):
                self.variavel()
                if self.currentToken.name in self.firstOf('mais_variaveis'):
                    self.mais_variaveis()
                    if self.currentToken.name == 'fim_registro':
                        self.getToken()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()
    
    def declaracao_global(self):
        # procedimento IDENT ( <parametros_opcional> ) <declaracoes_locais> <comandos> fim_procedimento
        if self.currentToken.name == 'procedimento':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name == '(':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('parametros_opicional'):
                        self.parametros_opicinal()
                        if self.currentToken.name == ')':
                            self.getToken()
                            if self.currentToken.name in self.firstOf('declaracoes_locais'):
                                self.declaracoes_locais()
                                if self.currentToken.name in self.firstOf('comandos'):
                                    self.comandos()
                                    if self.currentToken.name == 'fim_procedimento':
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
                else:
                    self.error()
            else:
                self.error()
                
        # | funcao IDENT ( <parametros_opcional> ) : <tipo_estendido> <declaracoes_locais> <comandos> fim_funcao
        elif self.currentToken.name == 'funcao':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name == '(':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('parametros_opcional'):
                        self.parametros_opicinal()
                        if self.currentToken.name == ')':
                            self.getToken()
                            if self.currentToken.name == ':':
                                self.getToken()
                                if self.currentToken.name in self.firstOf('tipo_estendido'):
                                    self.tipo_estendido()
                                    if self.currentToken.name in self.firstOf('declaracoes_locais'):
                                        self.declaracoes_locais()
                                        if self.currentToken.name in self.firstOf('comandos'):
                                            self.comandos()
                                            if self.currentToken.name == 'fim_funcao':
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
    
    def parametros_opicinal(self):
        # <parametro> | 3
        if self.currentToken.name in self.firstOf('parametro'):
            self.parametro()
    
    def parametro(self):
        # <var_opcional> <identificador> <mais_ident> : <tipo_estendido> <mais_parametros>
        if self.currentToken.name in self.firstOf('var_opcional'):
            self.var_opicinal()
            if self.currentToken.name in self.firstOf('identificador'):
                self.identificador()
                if self.currentToken.name in self.firstOf('mais_ident'):
                    self.mais_ident()
                    if self.currentToken.name == ':':
                        self.getToken()
                        if self.currentToken.name in self.firstOf('tipo_estendido'):
                            self.tipo_estendido()
                            if self.currentToken.name in self.firstOf('mais_parametros'):
                                self.mais_parametros()
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
        else:
            self.error()
    
    def var_opicinal(self):
        # var | 3
        if self.currentToken.name == 'var':
            self.getToken()
    
    def mais_parametros(self):
        #, <parametro> | 3
        if self.currentToken.name == ',':
            self.getToken()
            if self.currentToken.name in self.firstOf('parametro'):
                self.parametro()
            else:
                self.error()
    
    def declaracoes_locais(self):
        # <declaracao_local> <declaracoes_locais> | 3
        if self.currentToken.name in self.firstOf('declaracao_local'):
            self.declaracao_local()
            if self.currentToken.name in self.firstOf('declaracoes_locais'):
                self.declaracoes_locais()
            else:
                self.error()
    
    def corpo(self):
        # <declaracoes_locais> <comandos>
        if self.currentToken.name in self.firstOf('declaracoes_locais'):
            self.declaracoes_locais()
            if self.currentToken.name in self.firstOf('comandos'):
                self.comandos()
            else:
                self.error()
        else:
            self.error()
    
    def comandos(self):
        # <cmd> <comandos> | 3
        if self.currentToken.name in self.firstOf('cmd'):
            self.cmd()
            if self.currentToken.name in self.firstOf('comandos'):
                self.comandos()
            else:
                self.error()
    
    def cmd(self):
        # leia ( <identificador> <mais_ident> )
        if self.currentToken.name == 'leia':
            self.getToken()
            if self.currentToken.name == '(':
                self.getToken()
                if self.currentToken.name in self.firstOf('identificador'):
                    self.identificador()
                    if self.currentToken.name in self.firstOf('mais_ident'):
                        self.mais_ident()()
                        if self.currentToken.name == ')':
                            self.getToken()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        
        # | escreva ( <expressao> <mais_expressao> )
        elif self.currentToken.name == 'escreva':
            self.getToken()
            if self.currentToken.name == '(':
                self.getToken()
                if self.currentToken.name in self.firstOf('expressao'):
                    self.expressao()
                    if self.currentToken.name in self.firstOf('mais_expressao'):
                        self.mais_expressao()()
                        if self.currentToken.name == ')':
                            self.getToken()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        
        # | se <expressao> entao <comandos> <senao_opcional> fim_se
        elif self.currentToken.name == 'se':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name == 'entao':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('comandos'):
                        self.comandos()
                        if self.currentToken.name in self.firstOf('senao_opicional'):
                            self.senao_opcional()
                            if self.currentToken.name == 'fim_se':
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
                
        # | caso <exp_aritmetica> seja <selecao> <senao_opcional> fim_caso
        elif self.currentToken.name == 'caso':
            self.getToken()
            if self.currentToken.name in self.firstOf('exp_aritmetica'):
                self.exp_aritmetica()
                if self.currentToken.name == 'seja':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('selecao'):
                        self.selecao()
                        if self.currentToken.name in self.firstOf('senao_opcional'):
                            self.senao_opcional()
                            if self.currentToken.name == 'fim_caso':
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
                
        # | para IDENT <- <exp_aritmetica> ate <exp_aritmetica> faca <comandos> fim_para
        elif self.currentToken.name == 'para':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name == '<-':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('exp_aritmetica'):
                        self.exp_aritmetica()
                        if self.currentToken.name == 'ate':
                            self.getToken()
                            if self.currentToken-name in self.firstOf('exp_aritmetica'):
                                self.exp_aritmetica()
                                if self.currentToken.name == 'faca':
                                    self.getToken()
                                    if self.currentToken.name in self.firstOf('comandos'):
                                        self.comandos()
                                        if self.currentToken.name == 'fim_para':
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
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
            
            
        # | enquanto <expressao> faca <comandos> fim_enquanto
        elif self.currentToken.name == 'enquanto':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name == 'faca':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('comandos'):
                        self.comandos()
                        if self.currentToken.name == 'fim_enquanto':
                            self.getToken()
                        else:
                            self.error()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
            
            
        # | faca <comandos> ate <expressao>
        elif self.currentToken.name == 'faca':
            self.getToken()
            if self.currentToken.name in self.firstOf('comandos'):
                self.comandos()
                if self.currentToken.name == 'ate':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('expressao'):
                        self.expressao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
            
            
        # | ^ IDENT <outros_ident> <dimensao> <- <expressao>
        elif self.currentToken.name == '^':
            self.getToken()
            if self.currentToken.name == 'identificador':
                if self.currentToken.name in self.firstOf('outros_ident'):
                    self.outros_ident()
                    if self.currentToken.name in self.firstOf('dimensao'):
                        self.dimensao()
                        if self.currentToken.name == '<-':
                            self.getToken()
                            if self.currentToken.name in self.firstOf('expressao'):
                                self.expressao()
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
            
            
        # | IDENT <chamada_atribuicao>
        elif self.currentToken.name == 'identificador':
            self.getToken()
            if self.currentToken.name in self.firstOf('chamada_atribuicao'):
                self.chamada_atribuicao()
            else:
                self.error()
        
        # | retorne <expressao>
        elif self.currentToken.name == 'retorne':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
            else:
                self.error()
        else:
            self.error()
    
    def mais_expressao(self):
        # , <expressao> <mais_expressao> | 3
        if self.currentToken.name == ',':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name in self.firstOf('mais_expressao'):
                    self.mais_expressao()
                else:
                    self.error()
            else:
                self.error()
    
    def senao_opcional(self):
        # senao <comandos> | 3
        if self.currentToken.name == 'senao':
            self.getToken()
            if self.currentToken.name in self.firstOf('comandos'):
                self.comandos()
            else:
                self.error()
    
    def chamada_atribuicao(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> <- <expressao>
        if self.currentToken.name == '(':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name in self.firstOf('mais_expressao'):
                    self.mais_expressao()
                    if self.currentToken.name == ')':
                        self.getToken()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        
        elif self.currentToken.name in self.firstOf('outros_ident'):
            self.outros_ident()
            if self.currentToken.name in self.firstOf('dimensao'):
                self.dimensao()
                if self.currentToken.name == '<-':
                    self.getToken()
                    if self.currentToken.name in self.firstOf('expressao'):
                        self.expressao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
            
        else:
            self.error()
    
    def selecao(self):
        # <constantes> : <comandos> <mais_selecao>
        if self.currentToken.name in self.firstOf('constantes'):
            self.constantes()
            if self.currentToken.name == ':':
                self.getToken()
                if self.currentToken.name in self.firstOf('comandos'):
                    self.comandos()
                    if self.currentToken.name in self.firstOf('mais_selecao'):
                        self.mais_selecao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    # Thiago (31-44)
    def mais_selecao(self):
        # <selecao> | 3
        if self.currentToken.name in self.firstOf('selecao'):
            self.selecao()
    
    def constantes(self):
        # <numero_intervalo> <mais_constantes>
        if self.currentToken.name in self.firstOf('numero_intervalo'):
            self.numero_intervalo()
            if self.currentToken.name in self.firstOf('constantes'):
                self.mais_constantes()
            else:
                self.error()
        else:
            self.error()
    
    def mais_constantes(self):
        # , <constantes> | 3
        if self.currentToken.name == ',':
            self.getToken()
            if self.currentToken.name in self.firstOf('constantes'):
                self.mais_constantes()
            else:
                self.error()
    
    def numero_intervalo(self):
        # <op_unario> NUM_INT <intervalo_opicional>
        if self.currentToken.name in self.firstOf('op_unario'):
            self.op_unario()
            if self.currentToken.name == 'numero_inteiro':
                self.getToken()
                if self.currentToken.name in self.firstOf('intervalo_opicional'):
                    self.intervalo_opcional()
            else:
                self.error()
        else:
            self.error()
    
    def intervalo_opcional(self):
        # .. <op_unario> NUM_INT | 3
        if self.currentToken.name == '..':
            self.getToken()
            if self.currentToken.name in self.firstOf('op_unario'):
                self.op_unario()
                if self.currentToken.name == 'numero_inteiro':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()
    
    def op_unario(self):
        # - | 3
        if self.currentToken.name == '-':
            self.getToken()
    
    def exp_aritmetica(self):
        # <termo> <outros_termos>
        if self.currentToken.name in self.firstOf('termo'):
            self.termo()
            if self.currentToken.name in self.firstOf('outros_termos'):
                self.outros_termos()
            else:
                self.error()
        else:
            self.error()
    
    def op_multiplicacao(self):
        # * | /
        if self.currentToken.name == '*' or self.currentToken.name == '/':
            self.getToken()
        else:
            self.error()
    
    def op_adicao(self):
        # + | -
        if self.currentToken.name == '+' or self.currentToken.name == '-':
            self.getToken()
        else:
            self.error() 
    
    def termo(self):
        # <fator> <outros_fatores>
        if self.currentToken.name in self.firstOf('fator'):
            self.fator()
            if self.currentToken.name in self.firstOf('outros_fatores'):
                self.outros_fatores()
            else:
                self.error()
        else:
            self.error()
    
    def outros_termos(self):
        # <op_adicao> <termo> <outros_termos> | 3
        while self.currentToken.name in self.firstOf('op_adicao'):
            self.op_adicao()
            if self.currentToken.name in self.firstOf('termo'):
                self.termo()
            else:
                self.error()
            
    
    def fator(self):
        # <parcela> <outras_parcelas>
        if self.currentToken.name in self.firstOf('parcela'):
            self.parcela()
            if self.currentToken.name in self.firstOf('outras_parcelas'):
                self.outras_parcelas()
            else:
                self.error()
        else:
            self.error()
    
    def outros_fatores(self):
        # <op_multiplicacao> <fator> <outros_termos> | 3
        while self.currentToken.name in self.firstOf('op_multiplicacao'):
            self.op_multiplicacao()
            if self.currentToken.name in self.firstOf('fator'):
                self.fator()
                if self.currentToken.name in self.firstOf('outros_termos'):
                    self.outros_termos()
                else:
                    self.error()
            else:
                self.error()
    
    def parcela(self):
        # <op_unario> <parcela_unario> | <parcela_nao_unario>
        if self.currentToken.name in self.firstOf('op_unario'):
            self.op_unario()
            if self.currentToken.name in self.firstOf('parcela_unario'):
                self.parcela_unario()
            else:
                self.error()
        elif self.currentToken.name in self.firstOf('parcela_nao_unario'):
            self.parcela_nao_unario()
        else:
            self.error()
            

    # Bruno (45-58)
    def parcela_unario(self):
        # ^ IDENT <outros_ident> <dimensao> | IDENT <chamada_partes> | NUM_INT | NUM_REAL | ( <expressao> )
        if self.currentToken.name == '^':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name in self.firstOf('outros_ident'):
                    self.outros_ident()
                    if self.currentToken.name in self.firstOf('dimensao'):
                        self.dimensao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        
        elif self.currentToken.name == 'identificador':
            self.getToken()
            if self.currentToken.name in self.firstOf('chamada_partes'):
                self.chamada_partes()
            else:
                self.error()
        
        elif self.currentToken.name == 'numero_inteiro' or self.currentToken.name == 'numero_real':
            self.getToken()
            
        elif self.currentToken.name == '(':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name == ')':
                    self.getToken()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    def parcela_nao_unario(self):
        # & IDENT <outros_ident> <dimensao> | CADEIA
        if self.currentToken.name == '&':
            self.getToken()
            if self.currentToken.name == 'identificador':
                self.getToken()
                if self.currentToken.name in self.firstOf('outros_ident'):
                    self.outros_ident()
                    if self.currentToken.name in self.firstOf('dimensao'):
                        self.dimensao()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        elif self.currentToken.name == 'cadeia_literal':
            self.getToken()
        else:
            self.error()

    def outras_parcelas(self):
        # % <parcela> <outras_parcelas> | 3
        if self.currentToken.name == '%':
            self.getToken()
            if self.currentToken.name in self.firstOf('parcela'):
                self.parcela()
                if self.currentToken.name in self.firstOf('outras_parcelas'):
                    self.outras_parcelas()
                else:
                    self.error()
            else:
                self.error()
        

    def chamada_partes(self):
        # ( <expressao> <mais_expressao> ) | <outros_ident> <dimensao> | 3
        if self.currentToken.name == '(':
            self.getToken()
            if self.currentToken.name in self.firstOf('expressao'):
                self.expressao()
                if self.currentToken.name in self.firstOf('mais_expressao'):
                    self.mais_expressao()
                    if self.currentToken.name == ')':
                        self.getToken()
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        elif self.currentToken.name in self.firstOf('outros_ident'):
            self.outros_ident()
            if self.currentToken.name in self.firstOf('dimensao'):
                self.dimensao()
            else:
                self.error()

    def exp_relacional(self):
        # <exp_aritmetica> <op_opcional>
        if self.currentToken.name in self.firstOf('exp_aritmetica'):
            self.exp_aritmetica()
            if self.currentToken.name in self.firstOf('op_opcional'):
                self.op_opcional()
            else:
                self.error()
        else:
            self.error()

    def op_opcional(self):
        # <op_relacional> <exp_aritmetica> | 3
        if self.currentToken.name in self.firstOf('op_relacional'):
            self.op_relacional()
            if self.currentToken.name in self.firstOf('exp_aritmetica'):
                self.exp_aritmetica()
            else:
                self.error()

    def op_relacional(self):
        # = | <> | >= | <= | > | <
        if self.currentToken.name == '=' or self.currentToken.name == '<>' or self.currentToken.name == '>=' or self.currentToken.name == '<=' or self.currentToken.name == '>' or self.currentToken.name == '<':
            self.getToken()
        else:
            self.error()

    def expressao(self):
        # <termo_logico> <outros_termos_logicos>
        if self.currentToken.name in self.firstOf('termo_logico'):
            self.termo_logico()
            if self.currentToken.name in self.firstOf('outros_termos_logicos'):
                self.outros_termos_logicos()
            else:
                self.error()
        else:
            self.error()

    def op_nao(self):
        # nao | 3
        if self.currentToken.name == 'nao':
            self.getToken()

    def termo_logico(self):
        # <fator_logico> <outros_fatores_logicos>
        if self.currentToken.name in self.firstOf('fator_logico'):
            self.fator_logico()
            if self.currentToken.name in self.firstOf('outros_fatores_logicos'):
                self.outros_fatores_logicos()
            else:
                self.error()
        else:
            self.error()

    def outros_termos_logicos(self):
        # ou <termo_logico> <outros_termos_logicos> | 3
        if self.currentToken.name == 'ou':
            self.getToken()
            if self.currentToken.name in self.firstOf('termo_logico'):
                self.termo_logico()
                if self.currentToken.name in self.firstOf('outros_termos_logicos'):
                    self.outros_termos_logicos()
                else:
                    self.error()
            else:
                self.error()

    def outros_fatores_logicos(self):
        # e <fator_logico> <outros_fatores_logicos> | 3
        if self.currentToken.name == 'e':
            self.getToken()
            if self.currentToken.name in self.firstOf('fator_logico'):
                self.fator_logico()
                if self.currentToken.name in self.firstOf('outros_fatores_logicos'):
                    self.outros_fatores_logicos()
                else:
                    self.error()
            else:
                self.error()

    def fator_logico(self):
        # <op_nao> <parcela_logica>
        if self.currentToken.name in self.firstOf('op_nao'):
            self.op_nao()
            if self.currentToken.name in self.firstOf('parcela_logica'):
                self.parcela_logica()
            else:
                self.error()
        else:
            self.error()

    def parcela_logica(self):
        # verdadeiro | falso | <exp_relacional>
        if self.currentToken.name == 'verdadeiro' or self.currentToken.name == 'falso':
            self.getToken()
        elif self.currentToken.name in self.firstOf('exp_relacional'):
            self.exp_relacional()
        else:
            self.error()

    # TODO: other methods, remove 'pass' if writing in one of these