from LexicalAnalyser.model.Token import Token

class SLRParser:
    tokens = []
    grammar = {}
    terminals = set()
    non_terminals = set()
    tree = []

    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        try:
            self.read_grammar(open(grammar_path, 'r', encoding="utf-8"))
        except Exception as e:
            print("File couldn't be opened", e)
            pass

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
        return string
        if self.tree:
            string += "Tree:\n"
            string += self.tree_to_string()
        return string

    def read_grammar(self, grammar_file):
        self.grammar['S'] = grammar_file.readline().strip('\n')
        line = grammar_file.readline()
        while line:
            left, right = line.split('=')
            left = left.strip(' ')
            self.grammar[left] = []
            self.non_terminals.add(left)
            for production in right.split('|'):
                elements = production.split()
                for element in elements:
                    if (element[0] == '\'' and element != '\'e\''): self.terminals.add(element)
                self.grammar[left] += [elements]
            line = grammar_file.readline()

    def closure(self, productionBlock, visited):
        closureSet = set()
        if tuple(productionBlock) in visited: return(closureSet)
        visited.add(tuple(productionBlock))

        closureSet.add(productionBlock)
        pointer, production = productionBlock[0], productionBlock[1][2]
        if pointer < len(production) and production[pointer] in self.non_terminals:
            for internProduction in self.grammar[production[pointer]]:
                internProductionBlock = (0, (productions[pointer], "=", tuple(internProduction)))
                closureSet.update(self.closure(internProductionBlock, visited))
        return sorted(closureSet)

    def goto(self, state, symbol):
        newState = []
        for pointer, production in state:
            if pointer >= len(production[2]) or production[2][pointer] != symbol or production[2][0] == 'e': continue
            newProductionBlock = ((pointer + 1), (production))
            closureSet = self.closure(newProductionBlock, set())
            for productionBlock in closureSet:
                if (productionBlock not in newState): newState += [productionBlock]
        return newState

    def getSymbols(self, closureSet):
        symbols = set()
        for pointer, production in closureSet:
            if pointer < len(production[2]): symbols.add(production[2][pointer])
        return symbols

    def buildCanonical(self, S):
        states, canonical = {}, []
        canonical += [self.closure((0, ("S'", "=", ((S)) )), set())]
        i = 0
        while i < len(canonical):
            symbols = self.getSymbols(canonical[i])
            for symbol in symbols:
                newState = self.goto(canonical[i], symbol)
                if not newState: continue
                if newState not in canonical: canonical += [newState]
                states[(i, symbol)] = canonical.index(newState)
            i += 1
        return states, canonical

    def analyse():
        pass
