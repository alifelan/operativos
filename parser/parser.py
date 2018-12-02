import ply.yacc as yacc
from .tokenizer import tokens, lexer
from .exceptions import SyntaxErr, EndOfSimulation
from sistema import System


class Parser:
    def __init__(self):
        self.tokens = tokens
        self.parser = yacc.yacc(module=self)
        self.correct = True
        self.system = None

    def p_expression_comment(self, p):
        'expression : expression COMMENT'
        p[0] = p[1]

    def p_expression_politica_memory(self, p):
        'expression : POLITICA STR MEMORY STR'
        if p[2] != 'RR' or p[4] != 'MFU':
            self.correct = False
        if self.correct:
            p[0] = 'Politica de scheduling y de manejo de memoria soportadas'
        else:
            p[0] = 'Politica de scheduling o de manejo de memoria no soportada'

    def p_expression_quantumv(self, p):
        'expression : QUANTUMV FLOAT'
        self.quantum = p[2]
        p[0] = f'Quantum de: {p[2]}'

    def p_expression_realmemory(self, p):
        'expression : REALMEMORY INT'
        self.memory = p[2]
        p[0] = f'Memoria real de: {p[2]}'

    def p_expression_swapmemory(self, p):
        'expression : SWAPMEMORY INT'
        self.swap = p[2]
        p[0] = f'SwapMemory de: {p[2]}'

    def p_expression_pagesize(self, p):
        'expression : PAGESIZE INT'
        self.page_size = p[2]
        self.system = System('RR', 'MFU', self.quantum, self.memory, self.swap, self.page_size)
        p[0] = f'PageSize: {p[2]}'

    def p_expression_create(self, p):
        'expression : CREATE INT'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'
        else:
            p[0] = self.system.createProcess(p[2])

    def p_expression_address(self, p):
        'expression : ADDRESS INT INT'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'
        else:
            p[0] = self.system.getAddress(p[2], p[3])

    def p_expression_createp(self, p):
        'expression : CREATEP INT INT'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'

    def p_expression_quantum(self, p):
        'expression : QUANTUM'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'
        else:
            p[0] = self.system.quantum()

    def p_expression_fin(self, p):
        'expression : FIN INT'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'
        else:
            p[0] = self.system.fin(p[2])

    def p_expression_end(self, p):
        'expression : END'
        if not self.system or not self.correct:
            p[0] = 'Error en el sistema'
        else:
            self.system.end()
        raise EndOfSimulation

    def p_error(self, p):
        raise SyntaxErr("Input malformado")

    def parse(self, call: str) -> str:
        return self.parser.parse(call, lexer=lexer.clone())
