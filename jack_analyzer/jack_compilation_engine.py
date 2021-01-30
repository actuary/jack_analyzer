import jack_tokenizer as jt

class CompileError(Exception):
    pass
class CompilationEngine:
    def __init__(jack_filepath, output_filepath):
        self.jack_filepath = jack_filepath
        self.output_file = open(output_filepath, "w")
        self.tokenizer = jt.JackTokenizer(jack_filepath) 
        self.compile_class()

    def write_terminal_tag(self):
        jack_token_map = {
            jt.JackTokenType.KEYWORD: "kyword",
            jt.JackTokenType.SYMBOL: "symbol",
            jt.JackTokenType.INT_CONST: "integerConstant",
            jt.JackTokenType.STRING_CONST: "stringConstant",
            jt.JackTokenType.IDENTIFIER: "identifier",
        }
        self.write_open_tag(jack_token_map[self.tokenizer.token_type()], "")
        self.write(f" {self.tokenizer.current_token} ")
        self.write_close_tag(jack_token_map[self.tokenizer.token_type()])

    def write_open_tag(self, tag_name, tag_terminator="\n"):
        self.output_file.write(f"<{tag_name}>{tag_terminator}")

    def write_close_tag(self, tag_name):
        self.output_file.write(f"</{tag_name}>\n")
            
    def compile_class(self):
        
        self.output_file.write("<class>\n")
        self.tokenizer.advance()
        self.write_terminal_tag() #class
        self.tokenizer.advance() 
        self.write_terminal_tag() #className
        self.tokenizer.advance()  
        self.write_terminal_tag() # {
        self.tokenizer.advance()

        while self.tokenizer.current_token in ["static", "field"]:
            self.compile_class_var_dec()
            
        while self.tokenizer.current_token in ["function", "constructor", "method"]:
            self.compile_subroutine()

        self.write_terminal_tag() # }
            
        self.output_file.write("</class>\n")

    def compile_class_var_dec(self):
        self.write_open_tag("classVarDec")
        self.write_terminal_tag() # keyword
        self.tokenizer.advance()
        self.write_terminal_tag() # identifier or keyword
        self.tokenizer.advance()
        self.write_terminal_tag() # varName
        self.tokenizer.advance()

        while self.tokenizer.current_token == ",":
            self.write_terminal_tag() # ,
            self.tokenizer.advance()
            self.write_terminal_tag() # varName
            self.tokenizer.advance()

        self.write_terminal_tag() # ;
        self.advance()
        self.write_close_tag("classVarDec")
            
    
    def compile_subroutine(self):
        self.write_open_tag("subroutineDec")
        self.write_terminal_tag() # keyword
        self.tokenizer.advance()
        self.write_terminal_tag() #void/type
        self.tokenizer.advance()
        self.write_terminal_tag() # subroutineName
        self.tokenizer.advance() 
        self.write_terminal_tag() # (
        self.tokenizer.advance()

        if self.tokenizer.current_token != ")":
            self.compile_parameter_list()

        self.write_terminal_tag() # )
        self.tokenizer.advance()

        self.compile_subroutine_body()
        
        self.write_close_tag("subroutineDec")

    def compile_parameter_list(self):
        self.write_open_tag("parameterList")

        self.write_terminal_tag() # type
        self.tokenizer.advance()
        self.write_terminal_tag() # varName
        self.tokenizer.advance()

        while self.tokenizer.current_token == ",":
            self.write_terminal_tag()
            self.tokenizer.advance()
            self.write_terminal_tag()
            self.tokenizer.advance()

        self.write_close_tag("parameterList")

    def compile_subroutine_body(self):
        self.write_open_tag("subroutineBody")
        self.write_terminal_tag() # {
        self.tokenizer.advance()

        while self.current_token == "var":
            self.compile_var_dec()

        while self.current_token in ["let", "if", "while", "do", "return"]:
            self.compile_statements()

        self.write_terminal_tag() # }
        self.tokenizer.advance()
        self.write_close_tag("subroutineBody")
    
    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expresson(self):
        pass

    def compile_term(self):
        pass

    def compile_expression(self):
        pass
    

if __name__ == "__main__":
    print("JackParser")
