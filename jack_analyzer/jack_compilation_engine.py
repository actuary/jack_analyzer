
class CompilationEngine:
    def __init__(jack_filepath, output_filepath):
        self.jack_filepath = jack_filepath
        self.output_file = open(output_filepath, "w")

        self.compile_class()

    def compile_class(self):
        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

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
