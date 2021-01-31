import jack_tokenizer as jt

class CompileError(Exception):
    pass

JACK_OPS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
JACK_UNARY_OPS = ["-", "~"]
JACK_KEYWORD_CONSTS = ["true", "false", "null", "this"]

XML_RESERVED_WORDS = {
    '<' : '&lt;',
    '>' : '&gt;',
    '"' : '&quot;',
    "&" : '&amp;'
}
class CompilationEngine:
    def __init__(self, output_filepath, tokenizer):
        self.output_file = open(output_filepath, "w")
        self.tokenizer = tokenizer

    def test(self):
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        self.output_file.close()
        
    def main(self):
        self.tokenizer.advance()
        self.compile_class()
        self.output_file.close()

    def write_tag_and_advance(self):
        self.write_terminal_tag()
        self.tokenizer.advance()
        
    def write_terminal_tag(self):
        jack_token_map = {
            jt.JackTokenType.KEYWORD: "keyword",
            jt.JackTokenType.SYMBOL: "symbol",
            jt.JackTokenType.INT_CONST: "integerConstant",
            jt.JackTokenType.STRING_CONST: "stringConstant",
            jt.JackTokenType.IDENTIFIER: "identifier",
        }
        self.write_open_tag(jack_token_map[self.tokenizer.token_type()], "")
        if self.tokenizer.current_token in XML_RESERVED_WORDS.keys():
            self.output_file.write(f" {XML_RESERVED_WORDS[self.tokenizer.current_token]} ")
        else:    
            if self.tokenizer.token_type() == jt.JackTokenType.STRING_CONST:
                self.output_file.write(f" {self.tokenizer.current_token[1:-1]} ")
            else:
                self.output_file.write(f" {self.tokenizer.current_token} ")
        self.write_close_tag(jack_token_map[self.tokenizer.token_type()])

    def write_open_tag(self, tag_name, tag_terminator="\n"):
        self.output_file.write(f"<{tag_name}>{tag_terminator}")

    def write_close_tag(self, tag_name):
        self.output_file.write(f"</{tag_name}>\n")
            
    def compile_class(self):
        self.write_open_tag("class")

        self.write_tag_and_advance() #class
        self.write_tag_and_advance() #className
        self.write_tag_and_advance() #{

        while self.tokenizer.current_token in ["static", "field"]:
            self.compile_class_var_dec()
            
        while self.tokenizer.current_token in ["function", "constructor", "method"]:
            self.compile_subroutine()

        self.write_tag_and_advance() #end of program
            
        self.write_close_tag("class")

    def compile_class_var_dec(self):
        self.write_open_tag("classVarDec")
        
        self.write_tag_and_advance() #field|static
        self.write_tag_and_advance() #type
        self.write_tag_and_advance() #varName

        while self.tokenizer.current_token == ",":
            self.write_tag_and_advance() #,
            self.write_tag_and_advance() #varName

        self.write_tag_and_advance() #;
        
        self.write_close_tag("classVarDec")
            
    
    def compile_subroutine(self):
        self.write_open_tag("subroutineDec")
        
        self.write_tag_and_advance() #keyword
        self.write_tag_and_advance() #type
        self.write_tag_and_advance() #subroutineName
        self.write_tag_and_advance() #(

        self.compile_parameter_list()

        self.write_tag_and_advance() #)
        
        self.compile_subroutine_body()
        
        self.write_close_tag("subroutineDec")

    def compile_parameter_list(self):
        self.write_open_tag("parameterList")

        if self.tokenizer.current_token == ")":
            self.write_close_tag("parameterList")
            return

        self.write_tag_and_advance() #type
        self.write_tag_and_advance() #varName

        while self.tokenizer.current_token == ",":
            self.write_tag_and_advance() #,
            self.write_tag_and_advance() #type
            self.write_tag_and_advance() #varName

        self.write_close_tag("parameterList")

    def compile_subroutine_body(self):
        self.write_open_tag("subroutineBody")

        self.write_tag_and_advance() #{

        while self.tokenizer.current_token == "var":
            self.compile_var_dec()

        while self.tokenizer.current_token in ["let", "if", "while", "do", "return"]:
            self.compile_statements()

        self.write_tag_and_advance() #}
        
        self.write_close_tag("subroutineBody")
    
    def compile_var_dec(self):
        self.write_open_tag("varDec")

        self.write_tag_and_advance() #var
        self.write_tag_and_advance() #type
        self.write_tag_and_advance() #varName
        
        while self.tokenizer.current_token == ",":
            self.write_tag_and_advance() #,
            self.write_tag_and_advance() #varName

        self.write_tag_and_advance() #;
        
        self.write_close_tag("varDec")
        

    def compile_statements(self):
        self.write_open_tag("statements")

        while self.tokenizer.current_token in ["let", "if", "while", "do", "return"]:
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
        self.write_open_tag("doStatement")

        self.write_tag_and_advance() #do
        
        self.compile_subroutine_call()

        self.write_tag_and_advance() #;
        
        self.write_close_tag("doStatement")

    def compile_let(self):
        self.write_open_tag("letStatement")

        self.write_tag_and_advance() #let
        self.write_tag_and_advance() #varName

        if self.tokenizer.current_token == "[":
            self.write_tag_and_advance() #[
            self.compile_expression() #expression
            self.write_tag_and_advance() #]
        
        self.write_tag_and_advance() #=
        
        self.compile_expression()
        
        self.write_tag_and_advance() #;
        
        self.write_close_tag("letStatement")

    def compile_while(self):
        self.write_open_tag("whileStatement")

        self.write_tag_and_advance() #while
        self.write_tag_and_advance() #(
        self.compile_expression()
        self.write_tag_and_advance() #)
        self.write_tag_and_advance() #{
        self.compile_statements()
        self.write_tag_and_advance #}
        
        self.write_close_tag("whileStatement")
        
    def compile_return(self):
        self.write_open_tag("returnStatement")

        self.write_tag_and_advance() #return

        if self.tokenizer.current_token != ";":
            self.compile_expression()

        self.write_tag_and_advance() #;
        
        self.write_close_tag("returnStatement")

    def compile_if(self):
        self.write_open_tag("ifStatement")

        self.write_tag_and_advance() #if
        self.write_tag_and_advance() #(
        self.compile_expression()
        self.write_tag_and_advance() #)
        self.write_tag_and_advance() #{
        self.compile_statements()
        self.write_tag_and_advance() #}

        if self.tokenizer.current_token == "else":
            self.write_tag_and_advance() #else
            self.write_tag_and_advance() #{
            self.compile_statements()
            self.write_tag_and_advance() #}
        
        self.write_close_tag("ifStatement")

    def compile_expression(self):
        self.write_open_tag("expression")

        self.compile_term()

        if self.tokenizer.current_token in JACK_OPS:
            self.write_tag_and_advance() #op
            self.compile_term()
        
        
        self.write_close_tag("expression")

    def compile_term(self):
        self.write_open_tag("term")

        if self.tokenizer.current_token in JACK_UNARY_OPS:
            self.write_tag_and_advance() #unary op
            self.compile_term()

        elif self.tokenizer.current_token == "(":
            self.write_tag_and_advance() #(
            self.compile_expression()
            self.write_tag_and_advance() #)
            
        else:
            self.write_tag_and_advance() #varName

            if self.tokenizer.current_token == "(":
                #subroutineCall
                self.write_tag_and_advance() #(
                self.compile_expression_list()
                self.write_tag_and_advance() #)

            elif self.tokenizer.current_token == ".":
                # subroutineCall - class/var
                self.write_tag_and_advance()#.
                self.compile_subroutine_call()
                
            elif self.tokenizer.current_token == "[":
                # array expression
                self.write_tag_and_advance() #[
                self.compile_expression()
                self.write_tag_and_advance()() #]
        
        self.write_close_tag("term")

    def compile_subroutine_call(self):
        self.write_tag_and_advance() #class/subroutineName

        if self.tokenizer.current_token == ".":
            self.write_tag_and_advance() #.
            self.write_tag_and_advance() #methodName

        self.write_tag_and_advance() #(
        self.compile_expression_list()
        self.write_tag_and_advance() #)

    def compile_expression_list(self):
        self.write_open_tag("expressionList")

        if self.tokenizer.current_token != ")":
            self.compile_expression()

            while self.tokenizer.current_token == ",":
                self.write_tag_and_advance() #,
                self.compile_expression()

        self.write_close_tag("expressionList")
    

if __name__ == "__main__":
    print("Jack Compilation Engine")
