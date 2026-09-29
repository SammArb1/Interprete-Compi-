# ANALIZADOR LEXICO

from tokens import Token, lookup_ident, EQ, ASSIGN, PLUS, MINUS, BANG, NOT_EQ
from tokens import SLASH, POW, ASTERISK, LTE, LT, GTE, GT, SEMICOLON, COMMA
from tokens import LPAREN, RPAREN, LBRACE, RBRACE, LBRACKET, RBRACKET, EOF, ILLEGAL, INT, STRING

class Lexer:
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.read_position = 0
        self.ch = ''
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = ''
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self):
        if self.read_position >= len(self.input):
            return ''
        return self.input[self.read_position]

    def next_token(self):
        self.skip_whitespace()
        tok = None

        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(EQ, ch + self.ch)
            else:
                tok = Token(ASSIGN, self.ch)
        elif self.ch == '+':
            tok = Token(PLUS, self.ch)
        elif self.ch == '-':
            tok = Token(MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(NOT_EQ, ch + self.ch)
            else:
                tok = Token(BANG, self.ch)
        elif self.ch == '/':
            tok = Token(SLASH, self.ch)
        elif self.ch == '*':
            if self.peek_char() == '*':
                ch = self.ch
                self.read_char()
                tok = Token(POW, ch + self.ch)
            else:
                tok = Token(ASTERISK, self.ch)
        elif self.ch == '<':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(LTE, ch + self.ch)
            else:
                tok = Token(LT, self.ch)
        elif self.ch == '>':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(GTE, ch + self.ch)
            else:
                tok = Token(GT, self.ch)
        elif self.ch == ';':
            tok = Token(SEMICOLON, self.ch)
        elif self.ch == ',':
            tok = Token(COMMA, self.ch)
        elif self.ch == '(':
            tok = Token(LPAREN, self.ch)
        elif self.ch == ')':
            tok = Token(RPAREN, self.ch)
        elif self.ch == '{':
            tok = Token(LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(RBRACE, self.ch)
        elif self.ch == '[':
            tok = Token(LBRACKET, self.ch)
        elif self.ch == ']':
            tok = Token(RBRACKET, self.ch)
        elif self.ch == '"' or self.ch == "'":
            tok = Token(STRING, self.read_string(self.ch))
        elif self.ch == '':
            tok = Token(EOF, "")
        else:
            if self.is_letter(self.ch):
                literal = self.read_identifier()
                type = lookup_ident(literal)
                return Token(type, literal)
            elif self.is_digit(self.ch):
                return Token(INT, self.read_number())
            else:
                tok = Token(ILLEGAL, self.ch)

        self.read_char()
        return tok

    def skip_whitespace(self):
        while self.ch in [' ', '\t', '\n', '\r']:
            self.read_char()

    def is_letter(self, ch):
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'

    def is_digit(self, ch):
        return '0' <= ch <= '9'

    def read_identifier(self):
        pos = self.position
        while self.is_letter(self.ch) or self.is_digit(self.ch):
            self.read_char()
        return self.input[pos:self.position]

    def read_number(self):
        pos = self.position
        while self.is_digit(self.ch):
            self.read_char()
        return self.input[pos:self.position]

    def read_string(self, quote_type):
        pos = self.position + 1
        self.read_char()
        while self.ch != quote_type and self.ch != '':
            self.read_char()
        return self.input[pos:self.position]
