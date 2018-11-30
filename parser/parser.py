import ply.yacc as yacc
from .tokenizer import tokens, lexer
from .exceptions import SyntaxErr


class Parser:
    def __init__(self):
        self.tokens = tokens
        self.parser = yacc.yacc(module=self)

    def p_expression_comment(self, p):
        'expression : expression COMMENT'
        p[0] = p[1]

    def p_expression_quantumv(self, p):
        'expression : QUANTUMV FLOAT'
        pass

    def p_expression_realmemory(self, p):
        'expression : REALMEMORY INT'
        pass

    def p_expression_swapmemory(self, p):
        'expression : SWAPMEMORY INT'
        pass

    def p_expression_pagesize(self, p):
        'expression : PAGESIZE INT'
        pass

    def p_expression_create(self, p):
        'expression : CREATE INT'
        pass

    def p_expression_address(self, p):
        'expression : ADDRESS INT INT'
        pass

    def p_expression_createp(self, p):
        'expression : CREATEP INT INT'
        pass

    def p_expression_quantum(self, p):
        'expression : QUANTUM'
        pass

    def p_expression_fin(self, p):
        'expression : FIN INT'
        pass

    def p_error(self, p):
        raise SyntaxErr("Input malformado")

    def parse(self, call: str) -> str:
        return self.parser.parse(call, lexer=lexer.clone())
