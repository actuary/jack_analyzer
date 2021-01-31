import jack_tokenizer as jt

class CompileError(Exception):
    pass

JACK_OPS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
JACK_UNARY_OPS = ["-", "~"]
JACK_KEYWORD_CONSTS = ["true", "false", "null", "this"]

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
        self.write_open_tag("class")

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
            
        self.write_close_tag("class")

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
            self.write_terminal_tag() # ,
            self.tokenizer.advance()
            
            self.write_terminal_tag() # varName
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
        self.write_open_tag("varDec")
        
        self.write_terminal_tag() # var
        self.tokenizer.advance()
        
        self.write_terminal_tag() # type
        self.tokenizer.advance()
        
        self.write_terminal_tag() # varName
        self.tokenizer.advance()
        
        while self.tokenizer.current_token == ",":
            self.write_terminal_tag() #varName
            self.tokenizer.advance()

        self.write_terminal_tag() #;
        self.tokenizer.advance()
        
        self.write_close_tag("varDec")
        

    def compile_statements(self):
        self.write_open_tag("statements")

        while self.current_token in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.current_token == "let":
                self.compile_let()
            elif self.tokenizer.current_token == "do":
                self.compile_do()
            elif self.tokenizer.current_token == "while":
                self.compile_while()
            elif self.tokenizer.current_token == "if":
                self.compile_if()
            elif self.tokenizer.current_token == "return":
                self.compile_return()
            else:
                raise CompileError

        self.write_close_tag("statements")

    def compile_do(self):
        self.write_open_tag("do")
        
        self.write_terminal_tag() #do
        self.tokenizer.advance()

        self.write_terminal_tag() #subroutineCall
        self.tokenizer.advance()

        self.write_terminal_tag() #;
        self.tokenizer.advance()
        
        self.write_close_tag("do")

    def compile_let(self):
        self.write_open_tag("let")

        self.write_terminal_tag() #let
        self.tokenizer.advance()

        self.write_terminal_tag() #varName
        self.tokenizer.advance()

        if self.tokenizer.current_token == "[":
            self.write_terminal_tag() #[
            self.tokenizer.advance()

            self.compile_expression() #expression

            self.write_terminal_tag() #]
            self.tokenizer.advance()
        
        self.write_terminal_tag() #=
        self.tokenizer.advance()
        
        self.compile_expression()
        
        self.write_terminal_tag() #;
        self.tokenizer.advance()
        
        self.write_close_tag("let")

    def compile_while(self):
        self.write_open_tag("while")

        self.write_terminal_tag() #while
        self.tokenizer.advance()

        self.write_terminal_tag() #(
        self.tokenizer.advance()

        self.compile_expression()

        self.write_terminal_tag() #)
        self.tokenizer.advance()

        self.write_terminal_tag() #{
        self.tokenizer.advance()

        self.compile_statements()

        self.write_terminal_tag() #}
        self.tokenizer.advance()
        
        self.write_close_tag("while")
        
    def compile_return(self):
        self.write_open_tag("return")

        self.write_terminal_tag() #return
        self.tokenizer.advance()

        if self.tokenizer.current_token != ";":
            self.compile_expression()

        self.write_terminal_tag() #;
        self.tokenizer.advance()
        
        self.write_close_tag("return")

    def compile_if(self):
        self.write_open_tag("if")

        self.write_terminal_tag() #if
        self.tokenizer.advance()

        self.write_terminal_tag() #(
        self.tokenizer.advance()

        self.compile_expression()

        self.write_terminal_tag() #)
        self.tokenizer.advance()

        self.write_terminal_tag() #{
        self.tokenizer.advance()

        self.compile_statements()

        self.write_terminal_tag() #}
        self.tokenizer.advance()

        if self.tokenizer.current_token == "else":
            self.write_terminal_tag() #else
            self.tokenizer.advance()

            self.write_terminal_tag() #{
            self.tokenizer.advance()

            self.compile_statements()

            self.write_terminal_tag() #}
            self.tokenizer.advance()
        
        self.write_close_tag("if")

    def compile_expression(self):
        self.write_open_tag("expression")

        self.compile_term()

        if self.current_token in JACK_OPS:
            self.write_terminal_tag() # op
            self.tokenizer.advance()

            self.compile_term()
        
        
        self.write_close_tag("expression")

    def compile_term(self):
        self.write_open_tag("term")

        if self.tokenizer.current_token in JACK_UNARY_OPS:
            self.write_terminal_tag() # ~ or -
            self.tokenizer.advance()

        if self.tokenizer.current_token == "(":
            self.write_terminal_tag() #(
            self.tokenizer.advance()

            self.compile_expression

            self.write_terminal_tag() #)
            self.tokenizer.advance()
            
        else:
            self.write_terminal_tag() #varName
            self.tokenizer.advance()

            if self.tokenizer.current_token == "(":
                # subroutine Call
                self.write_terminal_tag() #(
                self.tokenizer.advance()
                
                self.compile_expression()

                while self.tokenizer.current_token == ",":
                    self.compile_expression()

                self.write_terminal_tag() #)
                self.tokenizer.advance()

            elif self.tokenizer.current_token == ".":
                # subroutineCall - class/var
                self.write_terminal_tag() #.
                self.tokenizer.advance()

                self.write_terminal_tag() #subroutineName
                self.tokenizer.advance()

                self.write_terminal_tag() #(
                self.tokenizer.advance()
                
                self.compile_expression()

                while self.tokenizer.current_token == ",":
                    self.compile_expression()

                self.write_terminal_tag() #)
                self.tokenizer.advance()
                
            elif self.tokenizer.current_token == "[":
                # array expression
                self.write_terminal_tag() #[
                self.tokenizer.advance()

                self.compile_expression()

                self.write_terminal_tag() #]
                self.tokenizer.advance()
        
        self.write_close_tag("term")

    

if __name__ == "__main__":
    print("JackParser")
