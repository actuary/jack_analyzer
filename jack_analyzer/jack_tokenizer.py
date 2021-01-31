import os
import sys
import re
from enum import Enum
import pdb
import io

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

JACK_KEYWORDS = ["class", "constructor", "function", "method",
                 "field", "static", "var", "int", "char",
                 "boolean", "void", "true", "false", "null",
                 "let", "do", "if", "else", "while", "return", "this"]

JACK_SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
                "+", "-", "*", "/", "&", "|", "<", ">", "=",
                "~"]

class JackTokenizer:
    
    identifier_matcher = re.compile("^[a-zA-Z_][a-zA-Z0-9\_]*$")
    
    def __init__(self, jack_filepath):
        self.jack_file = io.open(jack_filepath, "rb")
        self.is_more_tokens = True
        self.current_token = ""

    def has_more_tokens(self):
        return self.is_more_tokens

    def get_next_char(self):
        c = self.jack_file.read(1)
        return c.decode("utf-8")

    def go_back_chars(self, back_steps = 1):
       self.jack_file.seek(self.jack_file.tell() - back_steps, os.SEEK_SET) 

    def advance(self):
        c = self.get_next_char()
        if not c:
            self.is_more_tokens = False
        elif c == "/":
            is_comment = self._advance_past_comments()
            if is_comment:
                self.advance()
            else:
                self.current_token = c
        elif c.isspace():
            self.advance()
        elif c == '"':
            self.current_token = c
            c = self.get_next_char()
            while c != '"':
                self.current_token += c
                c = self.get_next_char()
            self.current_token += c
        # catch symbols
        elif c in JACK_SYMBOLS:
            self.current_token = c
        else:
            # otherwise it's gotta be an identifer, const or keyword
            # so eat that up
            self.current_token = ""
            while c and c not in JACK_SYMBOLS and not c.isspace():
                self.current_token += c
                c = self.get_next_char()
            if c:
                self.go_back_chars(1)

    def _advance_past_comments(self):
        c = self.get_next_char()
        # in-line comment
        is_comment = True
        if c == "/":
            # in-line comment
            while c and c != "\n":

                c = self.get_next_char()
        elif c == "*":
            # comment until closing ignore diff between it and API comment
            c = self.get_next_char()
            while c:
                if c == "*":
                    c = self.get_next_char()
                    if c == "/":
                        break
                else:
                    c = self.get_next_char()
        else:
            is_comment = False
            self.go_back_chars(1)
        return is_comment

                    
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
        
    def close(self):
        self.jack_file.close()

if __name__ == "__main__":
    print("Tokenizer")
