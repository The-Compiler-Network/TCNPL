class SyntacticAnalyser:
    tokens = []

    def __init__(self, tokens):
        self.tokens = tokens

    def __str__(self):
        for token in self.tokens:
            print(token)