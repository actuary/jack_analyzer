import os
import sys
import re
from enum import Enum

class InvalidToken(Exception):
    def __init(self, token):
        self.token = token
        self.message = f"Could not parse given token: {token}"
        super().__init__(self.message)
        
class JackTokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

class JackKeyword(Enum):
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 16
    WHILE = 17
    RETURN = 18
    TRUE = 19
    FALSE = 20
    NULL = 21
    THIS = 23

JACK_KEYWORDS = ["class", "constructor", "function", "method",
                 "field", "static", "var", "int", "char",
                 "boolean", "void", "true", "false", "null",
                 "let", "do", "if", "else", "while", "return"]

JACK_SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
                "+", "-", "*", "/", "&", "|", "<", ">", "=",
                "~"]

class JackTokenizer:
    
    identifier_matcher = re.compile("^[a-zA-Z_][a-zA-Z0-9\_]*$")
    
    def __init__(self, jack_filepath):
        self.jack_file = open(jack_filepath, 'r')
        self.buffer = ""
        if self.has_more_tokens():
            self.advance()
        

    def has_more_tokens(self):
        return True

    def advance(self):
        # need to read a char, keep reading until:
        #   - a symbol
        #   - a keyword followed by a space
        c = self.jack_file.read(1)

        # Comments
        if c == "/":
            c = self._advance_past_comments
            
        # ignore whitespace
        while c and c.isspace():
            c = self.jack_file.read(1)

        # catch symbols
        if c in JACK_SYMBOLS:
            self.current_token = c
        else:
            # otherwise it's gotta be an identifer, const or keyword
            # so eat that up
            self.current_token = c
            while c and c not in JACK_SYMBOLS and c != " ":
                self.current_token += c                        

    def _advance_past_comments(self):
        c = self.jack_file.read(1)
        # in-line comment
        if c == "/":
            # in-line comment
            while c and c != "\n":
                c = self.jack_file.read(1)

        elif c == "*":
            # comment until closing ignore diff between it and API comment
            while c:
                c = self.jack_file.read(1)
                if c == "*" and self.jack_file.read(1) == "/":
                    break

        return c
                    
    def _set_current_token(self, token):
        # for testing
        self.current_token = token
    
    def token_type(self):
        if self.current_token in JACK_KEYWORDS:
            return JackTokenType.KEYWORD
        elif self.current_token in JACK_SYMBOLS:
            return JackTokenType.SYMBOL
        elif self.current_token.isnumeric():
            return JackTokenType.INT_CONST
        elif self.current_token[0]==self.current_token[-1]=='"':
            return JackTokenType.STRING_CONST
        elif self._valid_identifier(self.current_token):
            return JackTokenType.IDENTIFIER
        else:
            raise InvalidToken(self.current_token)

    def _valid_identifier(self, token):
        return token != "" and JackTokenizer.identifier_matcher.match(token)
        
    def key_word(self):
        return JackKeyWord.CLASS

    def symbol(self):
        return ""

    def identifier(self):
        return ""

    def int_val(self):
        return 0

    def string_val(self):
        return ""
    
    def close(self):
        self.jack_file.close()

if __name__ == "__main__":
    print("Tokenizer")
