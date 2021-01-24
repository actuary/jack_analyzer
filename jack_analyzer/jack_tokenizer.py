import os
import sys
from enum import Enum

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



class JackTokenizer:
    def __init__(self, jack_filepath):
        self.jack_file = open(jack_filepath, 'r')

    def has_more_tokens(self):
        return True

    def advance(self):
        pass

    def token_type(self):
        return JackTokenType.KEYWORD
    
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
