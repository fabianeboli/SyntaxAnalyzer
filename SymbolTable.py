# Provides snall Table abstraction


class SymbolTable:
    def __init__(self):
        self.classSymTable = []
        self.subSymTable = []
        self.staticIndex = 0
        self.fieldIndex = 0
        self.argumentIndex = 0
        self.varIndex = 0
        self.subroutineIndentifier = 0

    def startSubroutine(self):
        self.subSymTable = []
        self.subIdentifier  # CHECK
        self.subArgumentIndex = 0
        self.subVarIndex = 0

    def Define(self, name, type, kind):
        if kind in ('static', 'field', 'arg', 'var'):
            if kind == 'static':
                self.classSymTable.append((name, type, kind, self.staticIndex))
                self.staticIndex += 1
            else:
                self.classSymTable.append((name, type, kind, self.fieldIndex))
                self.varIndex += 1
        else:
            if kind == 'local':
                self.subSymTable.append((name, type, kind, self.varIndex))
                self.varIndex += 1
            elif kind == 'argument':
                self.subSymTable.append((name, type, kind, self.argumentIndex))
                self.argumentIndex += 1
        #     self.symTable.append([name, type, kind])
        #     print(self.symTable)
        # else: 
        #     return print('wrong kind of variable')

    def varCount(self, kind):
            count = {'static': self.staticIndex,
                    'field': self.fieldIndex,
                    'argument': self.argumentIndex,
                    'local': self.varIndex}
            if kind in count:
                return count[kind]

    def KindOf(self, string):            
            kind = [None if string not in sym[2] else string for sym in self.classSymTable]
            if string == 'field':
                return 'this'
            elif string in self.classSymTable:
                return [None if string not in sym[2] else string for sym in self.subSymTable]

    def TypeOf(self, string):
        return [None if string not in sym[1] else string for sym in self.classSymTable]
        return [None if string not in sym[0] else string for sym in self.subSymTable]

    def IndexOf(self, string):
        return [None if string not in sym[0] else string for sym in self.classSymTable]
        return [None if string not in sym[0] else string for sym in self.subSymTable]
    
    def print(self):
        print('----------Class------------')
        print('  name', '  type', '  kind', '  #')
        print('--------------------------')
        print(self.classSymTable)
        print('---------Subroutine-------')
        print(self.classSymTable)
        print('--------------------------')


test = SymbolTable()
test.Define('test', 'int', 'field')
