import ply.yacc as yacc
from .tokenizer import tokens, lexer
from .exceptions import SyntaxErr


def p_expression_comment(p):
    'expression : expression COMMENT'
    p[0] = p[1]


def p_expression_quantumv(p):
    'expression : QUANTUMV FLOAT'
    pass


def p_expression_realmemory(p):
    'expression : REALMEMORY INT'
    pass


def p_expression_swapmemory(p):
    'expression : SWAPMEMORY INT'
    pass


def p_expression_pagesize(p):
    'expression : PAGESIZE INT'
    pass


def p_expression_create(p):
    'expression : CREATE INT'
    pass


def p_expression_address(p):
    'expression : ADDRESS INT INT'
    pass


def p_expression_createp(p):
    'expression : CREATEP INT INT'
    pass


def p_expression_quantum(p):
    'expression : QUANTUM'
    pass


def p_expression_fin(p):
    'expression : FIN INT'
    pass

def p_error(p):
    raise SyntaxErr("Input malformado")

parser = yacc.yacc()


def parse(call: str) -> str:
    return parser.parse(call, lexer=lexer.clone())
