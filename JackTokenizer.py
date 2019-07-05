# Removes all comments and white space from the input stream
# and breaks it into Jack-Language tokens, as specified
# by the Jack grammer.
from enum import Enum
import re


class TokenType(Enum):
    Keyword = 'keyword'
    Symbol = 'symbol'
    Identifier = 'identifier'
    Int_Const = 'integerConstant'
    String_Const = 'stringConstant'


class JackTokenizer:
    def __init__(self, inputFile):
        self.Tokens = []
        self.TokensWTypes = []
        self.currTokenIndex = 0
        self.currToken = None
        self.fileToTokenize = open(inputFile, 'r')
        self.TokenizedFile = open('./TokenizedFile.xml', 'w')
        # split file in lines and then split those lines by commands
        for line in self.fileToTokenize:
            splittedLine = line.split()
            for token in splittedLine:
                # Remove Jack comments
                if token == '//' or token == '/**' or token == '':
                    break
                self.appendTokens(token, self.Tokens)

    def hasMoreTokens(self):
        return self.currTokenIndex != len(self.Tokens)

    def advance(self):
        if self.hasMoreTokens():
            self.currToken = self.Tokens[self.currTokenIndex]
            self.currTokenIndex += 1

    def TokenType(self):
        TokenTypes = {'class': TokenType.Keyword.value, 'constructor': TokenType.Keyword.value, 'function': TokenType.Keyword.value,
                      'method': TokenType.Keyword.value, 'field': TokenType.Keyword.value, 'static': TokenType.Keyword.value, 'var': TokenType.Keyword.value, 'int': TokenType.Keyword.value,
                      'char': TokenType.Keyword.value, 'boolean': TokenType.Keyword.value, 'void': TokenType.Keyword.value, 'true': TokenType.Keyword.value,
                      'false': TokenType.Keyword.value, 'null': TokenType.Keyword.value, 'this': TokenType.Keyword.value, 'let': TokenType.Keyword.value, 'do': TokenType.Keyword.value,
                      'if': TokenType.Keyword.value, 'else': TokenType.Keyword.value, 'while': TokenType.Keyword.value, 'return': TokenType.Keyword.value,
                      '{': TokenType.Symbol.value, '}': TokenType.Symbol.value, '(': TokenType.Symbol.value,
                      ')': TokenType.Symbol.value, '[': TokenType.Symbol.value, ']': TokenType.Symbol.value, '.': TokenType.Symbol.value,
                      ',': TokenType.Symbol.value, ';': TokenType.Symbol.value, '+': TokenType.Symbol.value, '-': TokenType.Symbol.value,
                      '*': TokenType.Symbol.value, '/': TokenType.Symbol.value, '&': TokenType.Symbol.value,
                      '|': TokenType.Symbol.value, '<': TokenType.Symbol.value, '>': TokenType.Symbol.value, '=': TokenType.Symbol.value, '~': TokenType.Symbol.value}
        
        # Check if the token is either a keyword or a symbol
        if self.currToken in TokenTypes:
            self.TokensWTypes.append(
                (self.currToken, TokenTypes[self.currToken]))
            return TokenTypes[self.currToken]
        # Check if token is a digit
        elif self.currToken.isdigit():
            self.TokensWTypes.append(
                (self.currToken, TokenType.Int_Const.value))
            return TokenType.Int_Const.value
        # Check if token is a string
        elif self.currToken[0] == '"' and self.currToken[-1] == '"':
            self.TokensWTypes.append(
                (self.currToken, TokenType.String_Const.value))
            return TokenType.String_Const.value
        elif self.currToken[0] != '"' and not self.currToken.isdigit():
            self.TokensWTypes.append(
                (self.currToken, TokenType.Identifier.value))
            return TokenType.Identifier.value

    def Keyword(self):
        if TokenType() == TokenType.Keyword.value:
            return self.currToken

    def Identifier(self):
        if TokenType() == TokenType.Identifier.value:
            return self.currToken

    def IntVal(self):
        if TokenType() == TokenType.Int_Const.value:
            return self.currToken

    def StringVal(self):
        if TokenType() == TokenType.String_Const.value:
            return self.currToken[1:-2]
    
    def Tokenize(self):
        symbolValues = {'<': '&lt;',
                        '>': '&gt;',
                        '&': '&amp;'}
        self.TokenizedFile.write('<tokens> \n')
        while self.hasMoreTokens():
            self.advance()
            tokenType = self.TokenType()
            if self.currToken in symbolValues:
                self.currToken = symbolValues[self.currToken]
            self.TokenizedFile.write(
             f'<{tokenType}> {self.currToken} </{tokenType}> \n')
        # self.TokenizedFile.write(self.TokensWTypes)
        self.TokenizedFile.write('</tokens> \n')

    # def changeSymbolValue(self):
        
    #     if self.currToken in symbolValues:
    #         return symbolValues[self.currToken]

    def appendTokens(self, token, list):
        # splits every keryword and symbol
        token = re.split(r'(\W)', token)
        # Removes unnecessary whitespace
        token = filter(None, token)
        for splittedToken in token:
            list.append(splittedToken)


test = JackTokenizer(
    '/home/Nand2TetrisCourse/nand2tetris/projects/10/Square/Square.jack')
test.Tokenize()
