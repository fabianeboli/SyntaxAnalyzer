# Emits VM commands into a file, using the VM command Syntax


class VMWriter:
    def __init__(self, outputFile):
        self.outfile = open(outputFile, 'w')
    
    def writePush(self, segment, index):
        if segment in ('const', 'arg',
        'local', 'static', 'THIS',
        'THAT', 'pointer', 'temp'):
            self.outfile.write(f'push {segment} {index}\n')
    
    def writePop(self, segment, index):
        if segment in ('const', 'arg',
        'local', 'static', 'THIS',
        'THAT', 'pointer', 'temp'):
            self.outfile.write(f'pop {segment} {index}\n')
    
    def writeArithmetic(self, command):
        if command in ('add', 'sub', 'neg', 
                      'eq', 'gt', 'lt', 'and',
                      'or', 'not'):
            self.outfile.write(f'{command}\n')

    def writeLabel(self, string):
        self.outfile.write(f'label {string}\n')
    
    def writeGoto(self, string):
        self.outfile.write(f'goto {string}\n')
    
    def writeCall(self, name, nArgs):
        self.outfile.write(f'call {name} {nArgs}\n')
    
    def writeIf(self, name, nLocals):
        self.outfile.write(f'if-goto {name} {nLocals}\n')

    def writeFunction(self, name, nLocals):
        self.outfile.write(f'function {name} {nLocals}\n')

    def writeReturn(self):
        self.outfile.write(f'return')
    
    def close(self):
        self.outfile.close()
    

