

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
        self.vm_file.write(f"{label}\n")

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, num_args):
        pass

    def write_function(self, name, num_locals):
        pass

    def write_return(self):
        pass

    def close(self):
        self.vm_file.close()
