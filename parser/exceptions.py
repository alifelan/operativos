class ParserException(Exception):
    pass

class LexerError(ParserException):
    pass

class SyntaxErr(ParserException):
    pass
