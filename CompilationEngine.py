# Compilation Engine that that parses the JackTokenizer into XML file
import sys
import re
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:

    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, inputFile, outputFile, outputFile2):
        # Syntax tokenizer modules
        self.inF = open(inputFile, 'r')
        self.opF = open(outputFile, 'w')
        self.Jt = []
        self.JtIndex = 1
        # Compilation module
        self.vmWr = VMWriter(outputFile2)
        self.symTab = SymbolTable()
        # parse the result of the tokenizer into a list
        for line in self.inF:
            self.Jt.append(line)
        self.compileProgram()

    def readLine(self):
        return self.Jt[self.JtIndex]

    def hasMoreTokens(self):
        return self.JtIndex != len(self.Jt) - 2

    def advance(self):
        if self.hasMoreTokens():
            self.JtIndex += 1

    def retract(self):
        self.JtIndex -= 1

    def compileProgram(self):
        # self._ParseTokens()
        structures = {'class': self.compileClass,
                      'static': self.CompileClassVarDec,
                      'field': self.CompileClassVarDec,
                      'constructor': self.CompileSubroutine,
                      'function': self.CompileSubroutine,
                      'method': self.CompileSubroutine,
                      'var': self.compileVarDec,
                      'let': self.compileLet,
                      'if': self.compileIf,
                      'while': self.compileWhile,
                      'do': self.compileDo,
                      'return': self.compileReturn}
        if self.readLine().split()[1] in structures:
            structures[self.readLine().split()[1]]()
            self.compileProgram()
        else:
            self._ParseTokens()
            self.compileProgram()

    def compileClass(self):
        self.opF.write('<class> \n')
        self._ParseTokens(3)  # class classname {
        while 'static' in self.readLine().split()[1] or 'field' in self.readLine().split()[1]:
            self.CompileClassVarDec()
        # while is subroutine dec
        while 'constructor' in self.readLine().split()[1] or 'function' in self.readLine().split()[1] or 'method' in self.readLine().split()[1]:
            self.CompileSubroutine()
        self._ParseTokens()     # }
        # Close
        self.opF.write('</class> \n')
        # self.vmWr.close()
        self.symTab.print()

    def CompileClassVarDec(self):
        # ('static' | 'field') type varName (',' varName)* ';'
        self.opF.write('<classVarDec> \n')
        self._ParseTokens(3)
        while ';' not in self.readLine().split()[1]:
            self._ParseTokens()
        self._ParseTokens()  # ;
        self.opF.write('</classVarDec> \n')

    def CompileSubroutine(self):
        # { 'constructor | function | method'}
        # 'void | type' subroutineName '(' parameterList ')' subroutineBody
        self.opF.write('<subroutineDec> \n')
        self._ParseTokens(4)  # confunmeth void | type  subName parList )
        self.compileParameterList()
        self._ParseTokens()  # )
        # compile subroutine body
        self.opF.write('<subroutineBody> \n')
        self._ParseTokens()  # {

        while 'var' in self.readLine():
            self.compileVarDec()
        self.compileStatements()
        self._ParseTokens()  # }
        self.opF.write('</subroutineBody> \n')
        self.opF.write('</subroutineDec> \n')

    def compileParameterList(self):
        self.opF.write('<parameterList> \n')
        while ')' not in self.readLine().split()[1]:
            self._ParseTokens()
        # self._ParseTokens() Commented because ')'  should be between symbols
        self.opF.write('</parameterList> \n')

    def compileVarDec(self):
        self.opF.write('<VarDec> \n')
        # var -> type
        self._ParseTokens(3)
        # varName -> *(, -> varname)* until ';' is met
        while ';' not in self.readLine().split()[1]:
            self._ParseTokens()
        self._ParseTokens()
        self.opF.write('</VarDec>\n')

    def compileStatements(self):
        statements = {'let': self.compileLet, 'if': self.compileIf,
                      'while': self.compileWhile, 'do': self.compileDo,
                      'return': self.compileReturn}
        self.opF.write('<statements> \n')
        while self.readLine().split()[1] in statements:
            statements[self.readLine().split()[1]]()
        self.opF.write('</statements> \n')

    def compileDo(self):
        self.opF.write('<doStatement> \n')
        self._ParseTokens(2)  # do (subroutineName | className | varName)
        if '.' in self.readLine():
            self._ParseTokens(2)  # . surbroutineName
        self._ParseTokens()
        self.CompileExpressionList()
        self._ParseTokens(2)
        self.opF.write('</doStatement> \n')

    def compileLet(self):
        self.opF.write('<letStatement> \n')
        # keyword(let) -> identifier -> symbol
        self._ParseTokens(2)
        if '[' in self.readLine():  # gitCode
            self._ParseTokens()
            self.compileExpression()
            self._ParseTokens()
        self._ParseTokens()
        self.compileExpression()
        self._ParseTokens()   # ;
        self.opF.write('</letStatement> \n')

    def compileWhile(self):
        self.opF.write('<whileStatement> \n')
        # keyword(while) -> symbol(()
        self._ParseTokens(2)
        self.compileExpression()
        # symbol()) -> symbol({)
        self._ParseTokens(2)
        self.compileStatements()
        self._ParseTokens()
        self.opF.write('</whileStatement> \n')

    def compileReturn(self):
        self.opF.write('<returnStatement> \n')
        self._ParseTokens()  # return
        if ';' not in self.readLine():
            self.compileExpression()
        self._ParseTokens()  # ';'
        self.opF.write('</returnStatement> \n')

    def compileIf(self):
        self.opF.write('<ifStatement> \n')
        self._ParseTokens(2)  # if -> (
        self.compileExpression()
        self._ParseTokens(2)  # ) -> {
        self.compileStatements()
        self._ParseTokens()  # }
        if 'else' in self.readLine().split()[1]:
            self._ParseTokens(2)  # else -> {
            self.compileStatements()  # statements
            self._ParseTokens()  # }
        self.opF.write('</ifStatement> \n')

    def compileExpression(self, token=None):  # CHECK
        self.opF.write('<expression> \n')
        self.compileTerm()
        while self.readLine().split()[1] in self.binaryOp:
            self._ParseTokens()  # op
            self.compileTerm()  # term
            self.vmWr.writeArithmetic(token)
        self.opF.write('</expression> \n')

    def compileTerm(self, token=None):
        # Syntax Analyzer
        # self.opF.write('<term> \n')
        # if self.readLine().split()[1] in self.unaryOp:
        #     self._ParseTokens()  # ~ or - unaryOP
        #     self.compileTerm()
        # elif '(' in self.readLine().split()[1]:
        #     self._ParseTokens()  # (
        #     self.compileExpression()
        #     self._ParseTokens()  # )
        # else:
        #     self._ParseTokens()  # identifier
        #     if '[' in self.readLine().split()[1]:
        #         self._ParseTokens()  # [
        #         self.compileExpression()
        #         self._ParseTokens()  # ]
        #     elif '.' in self.readLine().split()[1]:
        #         self._ParseTokens(3)  # . subroutineName (
        #         self.CompileExpressionList()
        #         self._ParseTokens()
        #     elif '(' in self.readLine().split()[1]:
        #         self._ParseTokens()
        #         self.CompileExpressionList()
        #         self._ParseTokens()
        # self.opF.write('</term> \n')
        # Compiler 
        currentToken = self.currentToken()
        if currentToken.isdigit():
            self.vmWr.writePush('constant', token)
        elif currentToken[0] == '"':
            currentToken = currentToken[0:-2]
            self.vmWr.writePush('constant', currentToken)
            self.vmWr.writeCall('String', 'new', 1)
            for idx in range(1, len(token) - 1):
                self.vmWr.writePush('constant', ord(token[idx]))
                self.vmWr.writeCall('String', 'appendChar', 2)
        elif currentToken == 'true':
            self.vmWr.writePush('constant', '1')
            #self.vmWr.writeArithmetic('-', 'NEG')
            self.vmWr.writeArithmetic('neg')
        elif currentToken in ['false', 'null']:
            self.vmWr.writePush('constant', '0')
        elif currentToken == 'this':
            self.vmWr.writePush('constant', '0')
        elif currentToken == '-':
            return self.CompileNegOperator(token)
        elif currentToken == '~':
            return self.CompileNotOperator(token)
        elif currentToken == '(':
            self._ParseTokens()
            currentToken = self.currentToken() # termToken
            currentToken = self.compileExpression() #  )
        elif currentToken == '[':
            segment = self.symTab.kindOf(token)
            index = self.symTab.indexOf(token)
            self.vmWr.writePush(segment, index)
            self._ParseTokens()
            self.vmWr.writeArithmetic('+')
            self.vmWr.writePop('pointer', '1')
            self.vmWr.writePush('that', '0')
        elif currentToken == '.':
            self._ParseTokens() # . methOrFunc ( CHECK IT
            methOrFunc = self.currentToken()
            self._ParseTokens(3)
            currentToken = self.currentToken()
            numArg = 0
            className = token
            idType = self.symTab.typeOf(token)
            if idType is not None:
                segment = self.symTab.kindOf(token)
                index = self.symTab.kindOf(token)
                self.vmWr.writePush(segment, index)
                numArg += 1
                className = idType
            if token != ')':
                numArg = self.CompileExpressionList(token)
                self.vmWr.writeCall(className, methOrFunc, numArg)

    def CompileNegOperator(self, token=None):
        self._ParseTokens()
        token = self.currentToken()
        token = self.compileTerm(token) 
        # self.vmWr.writeArithmetic('-', 'NEG')
        self.vmWr.writeArithmetic('neg')
        return token
    
    def CompileNotOperator(self, token=None):
        self._ParseTokens()
        token = self.currentToken()
        if token != '(':
            token = self.CompileTerm(token)
        else:
            self._ParseTokens()
            token = self.currentToken()
            self.compileExpression(token)
            self._ParseTokens()
            token = self.currentToken()
        
        self.vmWr.writeArithmetic('~')
        return token

    def CompileExpressionList(self):
        self.opF.write('<expressionList> \n')
        if ')' not in self.readLine():
            self.compileExpression()
        while ')' not in self.readLine().split()[1]:  # GirCode
            self._ParseTokens()
            self.compileExpression()
        self.opF.write('</expressionList> \n')

    def _ParseTokens(self, amount=1):
        for i in range(amount):
            if self.hasMoreTokens():
                self.opF.write(self.readLine())
                self.advance()
            else:
                self.opF.write(self.readLine())
                self.opF.write('</class> \n')
                print(f'Program compiled')
                sys.exit('Done!')

    def is_op(self):
        return re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', self.readLine())
    
    def currentToken(self):
        return self.readLine().split()[1]



inputFile = '/home/Nand2TetrisCourse/nand2tetris/projects/10/SyntaxAnalyser/TokenizedFile.xml'
outputFile = './ParsedFile.xml'
outputFile2 = './CompiledFile.vm'
test = CompilationEngine(inputFile, outputFile, outputFile2)