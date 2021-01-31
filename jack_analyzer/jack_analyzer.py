import os
import sys
import jack_tokenizer as jt
import jack_compilation_engine as jce

from pathlib import Path
import glob

class JackAnalyzer:
    def __init__(self, jack_file):
        self.jack_file = jack_file
        if os.path.isdir(jack_file):
            self.jack_files = list(glob.glob(f"{jack_file}/*.jack"))
        else:
            self.jack_files = [jack_file]

    def main(self):
        for file in self.jack_files:
            out_file = os.path.splitext(file)[0] + ".xml"
            tokenizer = jt.JackTokenizer(file)
            compilation_engine = jce.CompilationEngine(out_file, tokenizer)
            compilation_engine.main()
            #compilation_engine.test()
            tokenizer.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python jack_analyzer.py <filename.jack> | <directory>")
        sys.exit(0)
    else:
        jack_file = sys.argv[1]
        if not Path(jack_file).is_file() and not Path(jack_file).is_dir():
            print("File not found!")
            sys.exit(0)
    
    analyzer = JackAnalyzer(jack_file)
    analyzer.main()
