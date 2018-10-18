from LexicalAnalyzer.model.Token import Token


class SyntacticAnalyzer:
    tokens = []
    grammar = {}
    non_terminals = set()
    tree = []

    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        try:
            grammar_file = open(grammar_path, 'r', encoding='utf-8')
            self.read_grammar(grammar_file)
        except:
            pass

    def read_grammar(self, grammar_file):
        self.grammar['S'] = grammar_file.readline().strip('\n')
        line = grammar_file.readline()
        while line:
            left, right = line.split('=')
            left = left.strip(' ')
            self.grammar[left] = []
            self.non_terminals.add(left)
            for production in right.split('|'):
                self.grammar[left] += [production.split()]
            line = grammar_file.readline()

    def __str__(self):
        string = "Tokens:\n"
        for token in self.tokens:
            string += str(token) + "\n"
        string += "Grammar:\n"
        for rule in self.grammar:
            string += "%10s" % rule + " = "
            if rule != 'S':
                for i, production in enumerate(self.grammar[rule]):
                    if i: string += " | "
                    string += ' '.join(production)
            else:
                string += self.grammar[rule]
            string += '\n'
        if self.tree:
            string += "Tree:\n"
            string += self.tree_to_string()
        return string

    def tree_to_string(self):
        string, now, first = "", 0, 0
        for node in sorted(self.tree, key=lambda x:x[0]):
            if node[0] > now:
                now = node[0]
                first = 0
                string += '\n'
            string += (" " if first else "")
            for i, each in enumerate(node[1]):
                string += (" " if i else "") + str(each.get_value() if isinstance(each, Token) else each)
            first = 1
        return string

    def analyse(self):
        self.analyse_code(self.grammar['S'], 0, 0)
        print(self.tree)

    def analyse_code(self, u, pointer, depth):
        prev = pointer
        for production in self.grammar[u]:
            pointer = prev
            final_production = []
            for element in production:
                if element == 'e': break
                if element in self.grammar:
                    found = self.analyse_code(element, pointer, depth + 1)
                    if found == -1: break
                    else:
                        final_production += [element]
                        pointer = found
                elif pointer < len(self.tokens) and element == '\'' + self.tokens[pointer].category.name + '\'':
                    final_production += [self.tokens[pointer]]
                    pointer += 1
                else: break
            else:
                self.tree += [[depth, final_production]]
                return pointer
        else:
            if ['e'] in self.grammar[u]:
                self.tree += [[depth, ['e']]]
                return prev
        return -1
