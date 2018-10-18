from LexicalAnalyser.model.Token import Token

class SLRParser:
    tokens = []
    grammar = {}
    grammar_follow = {}
    terminals = set()
    non_terminals = set()
    tree = []
    states = {}
    canonical = []
    table = {}

    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        try:
            self.read_grammar(open(grammar_path, 'r', encoding="utf-8"))
            for n in self.non_terminals:
                self.grammar_follow[n] = sorted(self.follow(n, set()))
        except Exception as e:
            print("File couldn't be opened", e)
            pass

    def __str__(self):
        string = "Tokens:\n"
        for token in self.tokens:
            string += str(token) + "\n"

        string += "Follow:\n"
        for n in self.non_terminals:
            print(n, self.grammar_follow)
            string += "follow(%s) = " % n + self.grammar_follow[n] + '\n'

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

        string += "Canonical:\n"
        for i, state in enumerate(self.canonical):
            string += "I_%d = " % i + str(state) + '\n'
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

    def first(self, production, visited):
        if (production == ['e']): return ['e']
        if (tuple(production) in visited): return []
        visited.add(tuple(production))
        firstSet, epis = set(), 0
        for element in production:
            doneAll = True
            if (element not in self.non_terminals):
                firstSet.add(element)
                break
            elif (['e'] in self.grammar[element]): epis, doneAll = epis + 1, False
            if (element in self.non_terminals):
                insideEpi = False
                for productions in self.grammar[element]:
                    firstMinusEpi = first(productions, visited)
                    firstSet.update(firstMinusEpi)
                    if ('e' in firstMinusEpi):
                        insideEpi = True
                        firstSet.remove('e')
                if (not insideEpi): break
                else: epis += done
        else:
            if (epis >= len(production)): firstSet.add('e')
        return firstSet

    def follow(self, X, visited):
        followSet = set()
        if (X == self.grammar['S']): followSet.add("EOF")
        for A in self.non_terminals:
            for production in self.grammar[A]:
                if (X not in production): continue
                isLast = False
                for i, element in enumerate(production):
                    if (element != X): continue
                    isLast = i == len(production) - 1
                    if (i < len(production) - 1):
                        firstMinusEpi = self.first(production[i + 1], set())
                        followSet.update(firstMinusEpi)
                        if ('e' in firstMinusEpi): isLast = True
                if (isLast):
                    if (A == X): continue
                    if (A not in visited):
                        visited.add(A)
                        followSet.update(self.grammar_follow[A] if A in self.grammar_follow else self.follow(A, visited))
        if ('e' in followSet): followSet.remove('e')
        return followSet

    def closure(self, productionBlock, visited):
        closureSet = set()
        if tuple(productionBlock) in visited: return(closureSet)
        visited.add(tuple(productionBlock))

        closureSet.add(productionBlock)
        dot, production = productionBlock[0], productionBlock[1][2]
        if dot < len(production) and production[dot] in self.non_terminals:
            for internProduction in self.grammar[production[dot]]:
                internProductionBlock = (0, (production[dot], "=", tuple(internProduction)))
                closureSet.update(self.closure(internProductionBlock, visited))
        return sorted(closureSet)

    def goto(self, state, symbol):
        newState = []
        for dot, production in state:
            if dot >= len(production[2]) or production[2][dot] != symbol or production[2][0] == 'e': continue
            newProductionBlock = ((dot + 1), (production))
            closureSet = self.closure(newProductionBlock, set())
            for productionBlock in closureSet:
                if (productionBlock not in newState): newState += [productionBlock]
        return newState

    def getSymbols(self, closureSet):
        symbols = set()
        for dot, production in closureSet:
            if dot < len(production[2]): symbols.add(production[2][dot])
        return symbols

    def buildCanonical(self):
        self.canonical += [self.closure((0, ("S'", "=", tuple([self.grammar['S']]) )), set())]
        i = 0
        while i < len(self.canonical):
            symbols = self.getSymbols(self.canonical[i])
            for symbol in symbols:
                newState = self.goto(self.canonical[i], symbol)
                if not newState: continue
                if newState not in self.canonical: self.canonical += [newState]
                self.states[(i, symbol)] = self.canonical.index(newState)
            i += 1

    def initTable(self):
        for i in range(len(self.states)):
            index = "I_%d" % i
            self.table[index] = {}
            for t in self.terminals + ["EOF"]: self.table[index][t] = ["Error"]
            for n in self.non_terminals: self.table[index][n] = ["Error"]

    def buildSLRTable(self):
        eofTerminals = self.terminals + ["EOF"]
        self.table = self.initTable()

        # RULE: S' = S .
        closureSet = self.closure[self.states[(0, grammar['S'])]]
        self.table["I_%d" % self.closure.index(closureSet)]["EOF"] = ["Accepted"]
        if (['e'] in self.grammar[self.grammar['S']]): self.table["I_0"]["EOF"] = ["Accepted"]

        # RULE: goto(state, symbol) [symbol = terminals U nonTerminals]
        for state, symbol in sorted(self.states):
            index = "I_%d" % state
            table[index][symbol] = [("e" if symbol in terminals else "") + str(self.states[(state, symbol)])]

        # RULE: A = alpha .
        for i in range(len(self.closure)):
            index = "I_%d" % i
            for dot in production in closure[i]:
                n, production = production[0], production[2]
                if (n == "S'"): continue
                if (dot >= len(production)):
                    for f in self.grammar_follow[n]:
                        self.table[index][f] = ["r%d" % grammar[n].index([*production]), n]

    def analyse(self):
        self.buildCanonical()
        pass
