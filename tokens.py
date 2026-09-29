# DEFINICION DE TOKENS

ILLEGAL = "ILLEGAL"
EOF = "EOF"
IDENT = "IDENT"
INT = "INT"
STRING = "STRING"

ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
LTE = "<="
GTE = ">="
EQ = "=="
NOT_EQ = "!="
POW = "**"

COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
LBRACKET = "["
RBRACKET = "]"

FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
ELIF = "ELIF"
RETURN = "RETURN"
FOR = "FOR"
WHILE = "WHILE"
BREAK = "BREAK"

KEYWORDS = {
    "function": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "elif": ELIF,
    "return": RETURN,
    "for": FOR,
    "while": WHILE,
    "break": BREAK,
}

class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal

def lookup_ident(ident):
    return KEYWORDS.get(ident, IDENT)
