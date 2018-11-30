import ply.lex as lex
import re
from .exceptions import LexerError

tokens = ('COMMENT', 'INT', 'FLOAT', 'QUANTUMV', 'REALMEMORY', 'SWAPMEMORY',
          'PAGESIZE', 'CREATE', 'ADDRESS', 'CREATEP', 'QUANTUM', 'FIN',
          'POLITICA', 'MEMORY', 'END', 'C')

t_COMMENT = r'//.*'
t_QUANTUMV = r'QuantumV'
t_REALMEMORY = r'RealMemory'
t_SWAPMEMORY = r'SwapMemory'
t_PAGESIZE = r'PageSize'
t_CREATE = r'Create'
t_ADDRESS = r'Address'
t_CREATEP = r'CreateP'
t_QUANTUM = r'Quantum'
t_POLITICA = r'Politicas\sscheduling'
t_MEMORY = r'Memory'
t_FIN = r'Fin'
t_END = r'End'
t_C = r'.'

def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_error(t):
    raise LexerError(t.value)


t_ignore = ' \r\n\t'

lexer = lex.lex()
