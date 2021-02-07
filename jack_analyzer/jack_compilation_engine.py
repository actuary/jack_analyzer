import jack_tokenizer as jt
from jack_symbol_table import SymbolTable, JackSymbolNotFound
from vm_writer import VMWriter

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

JACK_OP_TO_VM = {
    "+" : "add",
    "-" : "sub",
    "&" : "and",
    "|" : "or",
    "<" : "lt",
    ">" : "gt",
    "=" : "eq",
    "*" : "call Math.multiply 2",
    "/" : "call Math.divide 2"
}

JACK_UNARY_OP_TO_VM = {
    "-" : "neg",
    "~" : "not"
}

class CompilationEngine:
    def __init__(self, output_filepath, tokenizer):
        self.vm_writer = VMWriter(output_filepath)
        self.tokenizer = tokenizer
        
        self.symtab = SymbolTable()
        self.class_symtab = SymbolTable()
        
        self.class_name = ""
        self.memory_chunks = 0

    def main(self):
        self.tokenizer.advance()
        self.compile_class()
        self.vm_writer.close()

    def compile_class(self):
        self.vm_writer.write_comment("class")
        self.tokenizer.advance() #class
        self.class_name = self.tokenizer.current_token
        self.tokenizer.advance_n(2) #className {

        while self.tokenizer.current_token in ["static", "field"]:
            self.compile_class_var_dec()
            
        while self.tokenizer.current_token in ["function", "constructor", "method"]:
            self.compile_subroutine()

        self.tokenizer.advance() #} end
        self.vm_writer.close()

    def compile_class_var_dec(self):
        
        kind = self.tokenizer.current_token #field|static
        self.tokenizer.advance()

        type_of = self.tokenizer.current_token
        self.tokenizer.advance()

        name = self.tokenizer.current_token
        self.tokenizer.advance()

        #think I only need to do this on call?
        self.class_symtab.define({"name" : name,
                                  "type" : type_of,
                                  "kind" : kind})

        self.memory_chunks += 1
        while self.tokenizer.current_token == ",":
            self.tokenizer.advance()
            name = self.tokenizer.current_token
            self.class_symtab.define({"name" : name,
                                       "type" : type_of,
                                       "kind" : kind})
            self.tokenizer.advance()
            self.memory_chunks += 1

        self.tokenizer.advance()
            
    def compile_subroutine(self):
        self.vm_writer.write_comment("subroutine")
        #clear old symbol table
        self.if_counter = -1
        self.while_counter = -1
        
        self.symtab = SymbolTable()

        #counters for labels

        self.sub_keyword = self.tokenizer.current_token
        self.tokenizer.advance() #keyword
        #!!!
        # we need to do different things depending on what this keyword is
        # if its a method - then set base of the this segment to argument 0
        # if its a constructor - then must allocate a memory block for this object and then set the base of this segment this to the new objects address
        # and must return the base address to the caller, (but we always return this so should be ok)
        # we'll do this in the body...
            
        self.tokenizer.advance() #type
        sub_name = self.tokenizer.current_token
        self.tokenizer.advance() #subRoutineName
        self.tokenizer.advance() #(

        self.subroutine_name = f"{self.class_name}.{sub_name}"
        self.compile_parameter_list()

        self.tokenizer.advance() #)
        
        self.compile_subroutine_body()
        

    def compile_parameter_list(self):
        if self.tokenizer.current_token == ")":
            return

        type_of = self.tokenizer.current_token
        self.tokenizer.advance() #type 
        
        name = self.tokenizer.current_token
        self.tokenizer.advance() #varName
        #we make sure this index starts at 1 in the symbol table class        
        new_symbol = {"name" : name,
                      "type" : type_of,
                      "kind" : "argument"}

        if self.sub_keyword == "method":
            self.symtab.define({"name": "this_pointer",
                                "type": "int",
                                "kind": "argument"})
            
        
        self.symtab.define(new_symbol)
        
        while self.tokenizer.current_token == ",":
            self.tokenizer.advance() #,

            type_of = self.tokenizer.current_token
            self.tokenizer.advance() #type
            name = self.tokenizer.current_token
            new_symbol = {"name" : name,
                          "type" : type_of,
                          "kind" : "argument"}
            self.symtab.define(new_symbol)
                
            self.tokenizer.advance() #varName

    def compile_subroutine_body(self):
        self.tokenizer.advance() #{
        local_vars = 0
        while self.tokenizer.current_token == "var":
            local_vars += self.compile_var_dec()

        self.vm_writer.write_function(self.subroutine_name, local_vars) #function declaration
        if self.sub_keyword == "method":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)
        elif self.sub_keyword == "constructor":
            #pop a newly allocated memory block into this
            self.vm_writer.write_push("constant", self.memory_chunks)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)       
            
        while self.tokenizer.current_token in ["let", "if", "while", "do", "return"]:
            self.compile_statements()

        self.tokenizer.advance() #}
    
    def compile_var_dec(self):
        local_vars = 1
        self.tokenizer.advance() #var 
        type_of = self.tokenizer.current_token

        self.tokenizer.advance() #type
        name = self.tokenizer.current_token

        new_symbol = {"name" : name,
                      "type" : type_of,
                      "kind" : "local"}
        self.symtab.define(new_symbol)
        self.tokenizer.advance() #varName
        
        while self.tokenizer.current_token == ",":
            self.tokenizer.advance() #,
            name = self.tokenizer.current_token
            new_symbol = {"name" : name,
                          "type" : type_of,
                          "kind" : "local"}
            self.symtab.define(new_symbol)
            self.tokenizer.advance() #varName
            local_vars += 1
        self.tokenizer.advance() #;
        return local_vars

    def compile_statements(self):
        self.vm_writer.write_comment("(statements)")
        
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

    def compile_do(self):
        self.vm_writer.write_comment("do")
        
        self.tokenizer.advance() #do
        self.compile_subroutine_call()

        #we also need to pop the top value off the stack into temp as it's 0 and useless!
        self.vm_writer.write_pop("temp", 0)
        self.tokenizer.advance() #;

    def compile_let(self):
        self.vm_writer.write_comment("let")

        self.tokenizer.advance() #let
        name = self.tokenizer.current_token
        token_type = self.tokenizer.token_type()
        self.tokenizer.advance() #varName

        if self.tokenizer.current_token == "[":
            #an array, so push base address, index, add then pop that into pointer 1
            self.tokenizer.advance() #[
            self.compile_expression() #expression
            self.find_segment_and_push(name, token_type)
            self.vm_writer.write_arithmetic("add")
            self.tokenizer.advance() #]
            self.tokenizer.advance() #=
            self.compile_expression()
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)
            self.tokenizer.advance() #;
        else:
            self.tokenizer.advance() #=
            self.compile_expression()
            self.tokenizer.advance() #;
            #pop top of stack whatever into assigned var
            self.find_segment_and_pop(name)
            

    def find_segment_and_pop(self, name):
        #pop off whatever into assigned var
        try:
            segment = self.symtab.kind_of(name)
            index = self.symtab.index_of(name)
        except JackSymbolNotFound:
            if self.class_symtab.kind_of(name)== "field":
                segment = "this"
            else:
                segment = self.class_symtab.kind_of(name)
            index = self.class_symtab.index_of(name)
            
        self.vm_writer.write_pop(segment, index)

    def find_segment_and_push(self, name, token_type):
        #pop off whatever into assigned var
        # !!! we need to handle all the keywords here
        # e.g. this, null 0, false 0, true -1,
        # StringConstants
        if token_type == jt.JackTokenType.KEYWORD:
            if name == "null":
                self.vm_writer.write_push("constant", 0)
            elif name == "true":
                self.vm_writer.write_push("constant", 1)
                self.vm_writer.write_arithmetic("neg")
            elif name == "false":
                self.vm_writer.write_push("constant", 0)
            elif name == "this":
                self.vm_writer.write_push("pointer", 0)
            else:
                raise CompileError
                
        elif token_type == jt.JackTokenType.INT_CONST:
            self.vm_writer.write_push("constant", name)
        elif token_type == jt.JackTokenType.STRING_CONST:
            string = name[1:-1]
            self.vm_writer.write_push("constant", len(string))
            self.vm_writer.write_call("String.new", 1)

            for c in string:
                self.vm_writer.write_push("constant", ord(c))
                self.vm_writer.write_call("String.appendChar", 2)
        else:
            try:
                segment = self.symtab.kind_of(name)
                index = self.symtab.index_of(name)
            except JackSymbolNotFound:
                segment = self.class_symtab.kind_of(name)
                if segment == "field":
                    segment = "this"

                index = self.class_symtab.index_of(name)

            self.vm_writer.write_push(segment, index)
   
    def compile_while(self):
        self.vm_writer.write_comment("while")
        self.while_counter += 1
        self.tokenizer.advance_n(2) #while(

        #push the condition to top of stack
        while_counter = self.while_counter
        self.vm_writer.write_label(f"WHILE_EXP{while_counter}")
        
        self.compile_expression()
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(f"WHILE_END{while_counter}")
        
        self.tokenizer.advance_n(2) #){

        self.compile_statements()

        self.vm_writer.write_goto(f"WHILE_EXP{while_counter}")
        self.vm_writer.write_label(f"WHILE_END{while_counter}")

        self.tokenizer.advance() #}
        
    def compile_return(self):
        self.vm_writer.write_comment("return")
        self.tokenizer.advance() #return

        if self.tokenizer.current_token != ";":
            #push expression to stack
            self.compile_expression()
        else:
            self.vm_writer.write_push("constant", 0)

        self.vm_writer.write_return()
        self.tokenizer.advance() #;

    def compile_if(self):
        self.vm_writer.write_comment("if")
        self.if_counter += 1
        self.tokenizer.advance_n(2) #if(

        self.compile_expression()
        #self.vm_writer.write_arithmetic("not")
        
        self.tokenizer.advance_n(2) #){
        #self.vm_writer.write_if(f"{self.subroutine_name}.ELSE.{self.if_counter}")
        if_counter = self.if_counter
        self.vm_writer.write_if(f"IF_TRUE{if_counter}")
        self.vm_writer.write_goto(f"IF_FALSE{if_counter}")
        self.vm_writer.write_label(f"IF_TRUE{if_counter}")
            
        self.compile_statements()
        self.vm_writer.write_goto(f"IF_END{if_counter}")
        self.tokenizer.advance() #}
        self.vm_writer.write_label(f"IF_FALSE{if_counter}")
        
        if self.tokenizer.current_token == "else":
            self.tokenizer.advance_n(2) #else{
            self.compile_statements()
            self.tokenizer.advance() #}

        self.vm_writer.write_label(f"IF_END{if_counter}")

    def compile_expression(self):
        self.vm_writer.write_comment("(expression)")
        self.compile_term()

        if self.tokenizer.current_token in JACK_OPS:
            op = self.tokenizer.current_token #this needs to go last
            self.tokenizer.advance() #op
            self.compile_term()
            self.vm_writer.write_arithmetic(JACK_OP_TO_VM[op]) #also handles * and /
        

    def compile_term(self):
        self.vm_writer.write_comment("term")

        if self.tokenizer.current_token in JACK_UNARY_OPS:
            unary_op = self.tokenizer.current_token
            self.tokenizer.advance() #unary_up
            self.compile_term()
            self.vm_writer.write_arithmetic(JACK_UNARY_OP_TO_VM[unary_op])
            
        elif self.tokenizer.current_token == "(":
            self.tokenizer.advance() #(
            self.compile_expression()
            self.tokenizer.advance() #)
            
        else:
            name = self.tokenizer.current_token
            token_type = self.tokenizer.token_type()
            self.tokenizer.advance() #varName

            if self.tokenizer.current_token == "(":
                self.vm_writer.write_comment("(subroutine call - no class specified")
                #subroutineCall
                #if its a method need to push base address
                # assume it's always a method if no name before .
                self.vm_writer.write_push("pointer", 0)
                self.tokenizer.advance() #(
                num_args = self.compile_expression_list() + 1

                self.vm_writer.write_call(f"{self.class_name}.{name}", num_args)
                self.tokenizer.advance() #)

            elif self.tokenizer.current_token == ".":
                self.vm_writer.write_comment("(subroutine call)")

                num_args = 0
                if not (self.symtab.exists(name) or self.class_symtab.exists(name)):
                    #then must be a function call, or constructor, don't push the object
                    class_name = name
                else:
                    #its a method! push address to stack
                    num_args += 1
                    self.find_segment_and_push(name, "")
                    try:
                        class_name = self.symtab.type_of(name)
                    except:
                        class_name = self.class_symtab.type_of(name)
                        
                self.tokenizer.advance() #.
                sub_name = self.tokenizer.current_token
                self.tokenizer.advance() #name

                self.tokenizer.advance() #(
                num_args += self.compile_expression_list()
                self.tokenizer.advance() #)

                self.vm_writer.write_call(f"{class_name}.{sub_name}", num_args) #need to convert name to type_of if not class
                
            elif self.tokenizer.current_token == "[":
                # array expression
                self.tokenizer.advance() #[
                self.compile_expression() #expression
                self.find_segment_and_push(name, token_type)
                self.vm_writer.write_arithmetic("add")
                self.vm_writer.write_pop("pointer", 1)
                self.tokenizer.advance() #]
                self.vm_writer.write_push("that", 0)

            else:
                self.find_segment_and_push(name, token_type)

    def compile_subroutine_call(self):
        # this is just a do call
        num_args = 0
        name = self.tokenizer.current_token

        self.tokenizer.advance() #class/subrotuineName
        if self.tokenizer.current_token == ".":
            if not (self.symtab.exists(name) or self.class_symtab.exists(name)):
                #then must be a function call, or constructor, don't push the object
                class_name = name
            else:
                #its a method!
                num_args += 1
                self.find_segment_and_push(name, "")
                try:
                    class_name = self.symtab.type_of(name)
                except:
                    class_name = self.class_symtab.type_of(name)
            
            self.tokenizer.advance() #.
            name = self.tokenizer.current_token
            self.tokenizer.advance() #methodName
        else:
            #its this class method
            self.vm_writer.write_push("pointer", 0)
            num_args += 1
            class_name = self.class_name

        self.tokenizer.advance() #(
        num_args += self.compile_expression_list()

        self.vm_writer.write_call(f"{class_name}.{name}", num_args)
        self.tokenizer.advance() #)

    def compile_expression_list(self):
        self.vm_writer.write_comment("(expression list)")

        num_args = 0
        if self.tokenizer.current_token != ")":
            self.compile_expression()
            num_args += 1
            while self.tokenizer.current_token == ",":
                self.tokenizer.advance() #,
                self.compile_expression()
                num_args += 1

        return num_args
    

if __name__ == "__main__":
    print("Jack Compilation Engine")
