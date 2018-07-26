from exception.CodeNotFoundError import CodeNotFoundError
from model import TokenCategory
from model.Position import TokenPosition
from model.Token import Token


class LexicalAnalyzer:

    SEPARATORS = {'{', '}', '(', ')', ',', '"', ' '}
    ESCAPE_CHAR = {"\\\"": '\"', "\\\\": '\\', "\\\'": '\'', "\\n": '\n', "\\r": '\r', "\\t": '\t', "\\b": '\b', "\\f":
                   '\f', "\\v": '\v', "\\0": '\0'}
    file = None
    token_buffer = []
    code_lines = []
    lines_qt = 0
    current_line = 0

    def __init__(self, filepath):
        try:
            self.file = open(filepath, 'r', encoding='utf-8')
        except IOError:
            raise CodeNotFoundError("The specified file from " + filepath +
                                    " could not be found. Please check the path.")
        self.code_lines = self.file.readlines()
        self.file.close()
        self.lines_qt = len(self.code_lines)

    # TODO: ARRUMAR. APENAS POG TEMPORÁRIA
    def next_token(self):
        if not self.token_buffer:
            if not self.parse_next_line():
                return None
        return self.token_buffer.pop(0)

    def parse_next_line(self):
        if self.current_line >= self.lines_qt:
            return False
        line = self.code_lines[self.current_line].strip('\n')
        self.current_line += 1
        new_col = 0
        string = ""
        col, line_size = 0, len(line)
        while col < line_size:
            c = line[col]
            if c == '"':
                string += c
                col += 1
                while col < line_size:
                    c = line[col]
                    if c != '\\':
                        string += c
                    if c == '"':
                        break
                    if c == '\\':
                        col += 1
                        if col < line_size:
                            c = line[col]
                        c = self.ESCAPE_CHAR["\\" + c]
                        string += c
                    col += 1
                self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), None, string))
                string = ""
                new_col = col + 1
            elif self.is_separator(c):
                if string:
                    self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), None, string))
                if c != ' ':
                    ccol = col
                    if new_col:
                        ccol += 1
                    self.token_buffer.append(Token(TokenPosition(self.current_line, ccol), None, c))
                new_col = col + 2
                string = ""
            else:
                string += c
            col += 1
        if string:
            self.token_buffer.append(Token(TokenPosition(self.current_line, new_col), None, string))
        return True

    def is_separator(self, c):
        return c in self.SEPARATORS
