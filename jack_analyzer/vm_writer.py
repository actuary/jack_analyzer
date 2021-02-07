

class VMWriter(object):
    def __init__(self, output_file):
        self.vm_file = open(output_file, "w")

    def write_push(self, segment, index):
        self.vm_file.write(f"push {segment} {index}\n")

    def write_pop(self, segment, index):
        self.vm_file.write(f"pop {segment} {index}\n")
        
    def write_arithmetic(self, command):
        self.vm_file.write(f"{command}\n")

    def write_label(self, label):
        self.vm_file.write(f"label {label}\n")

    def write_goto(self, label):
        self.vm_file.write(f"goto {label}\n")

    def write_if(self, label):
        self.vm_file.write(f"if-goto {label}\n")

    def write_call(self, name, num_args):
        self.vm_file.write(f"call {name} {num_args}\n")

    def write_function(self, name, num_locals):
        self.vm_file.write(f"function {name} {num_locals}\n")

    def write_return(self):
        self.vm_file.write(f"return\n")

    def write_comment(self, comment):
        #self.vm_file.write(f"\n// {comment}\n")
        pass
    def close(self):
        self.vm_file.close()
