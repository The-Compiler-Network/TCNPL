from exception.CodeNotFoundError import CodeNotFoundError
from model import TokenCategory
from model.Position import TokenPosition
from model.Token import Token
from model.TokenCategory import TokenCategory


class LexicalAnalyzer:
    TAB_SIZE = 8
    separators = {'(': TokenCategory.opParen, ')': TokenCategory.clParen, '{': TokenCategory.opBraces,
                  '}': TokenCategory.clBraces, '[': TokenCategory.opBrackets, ']': TokenCategory.clBrackets,
                  '!': TokenCategory.unary, '~': TokenCategory.unary, '-': TokenCategory.minus, "**": TokenCategory.exp,
                  "*/": TokenCategory.exp, '*': TokenCategory.mult, '/': TokenCategory.mult, '%': TokenCategory.mult,
                  '+': TokenCategory.plus, "<<": TokenCategory.bitShift, ">>": TokenCategory.bitShift,
                  "<>": TokenCategory.unknown,
                  "><": TokenCategory.unknown,
                  '<': TokenCategory.relational, '>': TokenCategory.relational, "<=": TokenCategory.relational,
                  ">=": TokenCategory.relational, "==": TokenCategory.eqOrDiff, "!=": TokenCategory.eqOrDiff,
                  '&': TokenCategory.bitAnd, '|': TokenCategory.bitOr, "&&": TokenCategory.logicAnd,
                  "||": TokenCategory.logicOr, "&|": TokenCategory.unknown, "|&": TokenCategory.unknown,
                  '=': TokenCategory.attrib, ',': TokenCategory.comma, '"': None, ' ': None, '\t': None}
    escape_char = {"\"": '\"', "\\": '\\', "\'": '\'', "n": '\n', "r": '\r', "t": '\t', "b": '\b', "f":
        '\f', "v": '\v', "0": '\0'}
    keyword_token_map = {"bool": TokenCategory.typeBool, "int": TokenCategory.typeInt, "real": TokenCategory.typeReal,
                         "char": TokenCategory.typeChar, "string": TokenCategory.typeString,
                         "array": TokenCategory.typeArray, "to": TokenCategory.to, "as": TokenCategory.asCast,
                         "is": TokenCategory.isType, "while": TokenCategory.whileLoop, "if": TokenCategory.ifSel,
                         "elif": TokenCategory.elifSel, "else": TokenCategory.elseSel,
                         "function": TokenCategory.function,
                         "return": TokenCategory.returnFun, "@isEntryPoint": TokenCategory.entryPoint}
    file = None
    line = None
    line_size = 0
    token_buffer = []
    current_line = 0
    previous_column = 0
    current_column = 0
    line_tabs = 0
    previous_line_pointer = 0
    line_pointer = 0

    def __init__(self, filepath):
        try:
            self.file = open(filepath, 'r', encoding='utf-8')
        except IOError:
            raise CodeNotFoundError("The specified file from " + filepath +
                                    " could not be found. Please check the path.")

    def next_token(self):
        if self.line is None or self.line_pointer >= self.line_size:
            try:
                self.line = self.read_next_line()
            except EOFError:
                return None
            self.current_line += 1

            self.current_column, self.line_pointer, self.line_size, self.line_tabs = 1, 0, len(self.line), 0
            while self.line_pointer < self.line_size and (
                    self.line[self.line_pointer] == ' ' or self.line[self.line_pointer] == '\t'):
                self.current_column += 1 if self.line[self.line_pointer] == ' ' else self.TAB_SIZE
                self.line_tabs += 1 if self.line[self.line_pointer] == '\t' else 0
                self.line_pointer += 1
            if self.line_pointer == self.line_size:  # empty line
                return self.next_token()
        else:
            self.current_column = self.line_pointer + ((self.TAB_SIZE - 1) * self.line_tabs) + 1

        self.previous_column, string = self.current_column, ""
        while self.line_pointer < self.line_size:
            char = self.line[self.line_pointer]
            if char == '\'' or char == '"':  # string and character literals
                string = char
                self.line_pointer += 1
                while self.line_pointer < self.line_size:
                    c = self.line[self.line_pointer]
                    if c == '\\':
                        self.line_pointer += 1
                        if self.line_pointer < self.line_size and self.line[self.line_pointer] in self.escape_char:
                            string += self.escape_char[self.line[self.line_pointer]]
                        else:
                            string += '\\'
                    else:
                        string += c
                    if c == string[0]:
                        break
                    self.line_pointer += 1
                category = self.get_category(string)
                if category != TokenCategory.unknown:
                    string = string[1:len(string) - 1]
                self.line_pointer += 1
                return Token(TokenPosition(self.current_line, self.previous_column), category, string)
            elif self.is_separator(char):
                if string:
                    return Token(TokenPosition(self.current_line, self.previous_column), self.get_category(string),
                                 string)
                if char != ' ' and char != '\t':
                    if char == '*':
                        self.line_pointer += 1
                        if self.line_pointer < self.line_size and (
                                self.line[self.line_pointer] == '/' or self.line[self.line_pointer] == '*'):
                            char += self.line[self.line_pointer]
                        else:
                            self.line_pointer -= 1
                    if char == '<' or char == '>':
                        self.line_pointer += 1
                        if self.line_pointer < self.line_size and (
                                self.line[self.line_pointer] == '<' or self.line[self.line_pointer] == '>' or self.line[
                            self.line_pointer] == '='):
                            char += self.line[self.line_pointer]
                        else:
                            self.line_pointer -= 1
                    if char == '/':
                        self.line_pointer += 1
                        if self.line_pointer < self.line_size and self.line[self.line_pointer] == '/':
                            self.line = None
                            return self.next_token()
                        self.line_pointer -= 1
                    if char == '&' or char == '|':
                        self.line_pointer += 1
                        if self.line_pointer < self.line_size and (
                                self.line[self.line_pointer] == '&' or self.line[self.line_pointer] == '|'):
                            char += self.line[self.line_pointer]
                        else:
                            self.line_pointer -= 1
                    self.line_pointer += 1
                    return Token(TokenPosition(self.current_line, self.previous_column), self.separators[char], char)
                else:
                    while self.line[self.line_pointer] == ' ' or self.line[self.line_pointer] == '\t':
                        self.line_pointer += 1
                        self.line_tabs += 1 if self.line[self.line_pointer] == '\t' else 0
                    return self.next_token()
            else:
                string += char
            self.line_pointer += 1
        if string:
            return Token(TokenPosition(self.current_line, self.previous_column), self.get_category(string), string)

        return None

    def get_category(self, string):
        if string in self.keyword_token_map:
            return self.keyword_token_map[string]
        return TokenCategory.classify(string)

    def read_next_line(self):
        line = self.file.readline().strip('\n')
        if line:
            print(line)
            return line
        self.file.close()
        raise EOFError

    def parse_next_line(self):

        return True

    def is_separator(self, c):
        return c in self.separators
