class TokenPosition:
    line = 0
    column = 0

    def __init__(self, line, column):
        self.line = line
        self.column = column