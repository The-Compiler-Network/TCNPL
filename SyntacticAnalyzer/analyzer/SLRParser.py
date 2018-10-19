from LexicalAnalyzer.model.Token import Token
from LexicalAnalyzer.analyzer.LexicalAnalyzer import LexicalAnalyzer

class SLRParser:
    token = None
    tokens = []
    grammar = {}
    grammar_follow = {}
    terminals = set()
    non_terminals = set()
    tree = []
    states = {}
    canonical = []
    table = {}
    codePointer = 0
    treePointer = 0
    stack_history = []
    lexicalAnalyzer = None
    verdict = False

    def __init__(self, lexicalAnalyzer, grammar_path):
        self.lexicalAnalyzer = lexicalAnalyzer
        self.tokens = []
        self.next_token()
        try:
            self.read_grammar(open(grammar_path, 'r', encoding="utf-8"))
            for n in self.non_terminals:
                self.grammar_follow[n] = sorted(self.follow(n, set()))
        except Exception as e:
            print(e)
            pass

    def __str__(self):
        string = "Tokens:\n"
        for token in self.tokens:
            string += str(token) + "\n"
        string += '\n'

        string += "Follow:\n"
        for n in self.non_terminals:
            # print(n, self.grammar_follow)
            string += "follow(%s) = " % n + str(self.grammar_follow[n]) + '\n'
        string += '\n'

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
        string += '\n'

        # string += "Canonical:\n"
        # for i, state in enumerate(self.canonical):
        #     string += "I_%d = " % i + str(state) + '\n'
        # string += '\n'

        string += "SLR Table:\n"
        columns = sorted(self.terminals) + ["EOF"] + sorted(self.non_terminals)
        string += " "*5 + "|" + " | ".join([c.center(14, ' ') for c in columns]) + '\n'
        for i in range(len(self.table)):
            index = "I_%d" % i
            string += str(index).center(5, ' ') + "|" + " | ".join([(" ".join(self.table[index][c])).center(14, ' ') for c in columns]) + '\n'
        string += '\n'

        string += "Stack:\n"
        for node in self.stack_history:
            string += str(node) + '\n'
        string += '\n'

        if self.verdict:
            string += "Tree:\n"
            string += self.tree_to_string()

        string += "Verdict: " + str(self.verdict) + '\n'

        return string

    def tree_to_string(self):
        self.tree += [[self.grammar['S']]]
        self.tree.reverse()
        self.treePointer = 0
        newTree = []
        self.tree_to_string_util(0, newTree)
        tree_string = ""
        for t in newTree:
            tree_string += "\t"*t[0] + str(t[1]) + '\n'
        return(tree_string)

    def tree_to_string_util(self, depth, newTree):
        newTree += [[depth, self.tree[self.treePointer]]]
        for element in self.tree[self.treePointer]:
            if (element in self.non_terminals):
                self.treePointer += 1
                self.tree_to_string_util(depth + 1, newTree)

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
                    firstMinusEpi = self.first(productions, visited)
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
                        firstMinusEpi = self.first(production[i + 1:], set())
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
        for i in range(len(self.canonical)):
            index = "I_%d" % i
            self.table[index] = {}
            for t in self.terminals: self.table[index][t] = ["Error"]
            for n in self.non_terminals: self.table[index][n] = ["Error"]
            self.table[index]["EOF"] = ["Error"]

    def buildSLRTable(self):
        self.initTable()

        # RULE: S' = S .
        closureSet = self.canonical[self.states[(0, self.grammar['S'])]]
        self.table["I_%d" % self.canonical.index(closureSet)]["EOF"] = ["Accepted"]
        if (['e'] in self.grammar[self.grammar['S']]): self.table["I_0"]["EOF"] = ["Accepted"]

        # RULE: goto(state, symbol) [symbol = terminals U nonTerminals]
        for state, symbol in sorted(self.states):
            index = "I_%d" % state
            self.table[index][symbol] = [("e" if symbol in self.terminals else "") + str(self.states[(state, symbol)])]

        # RULE: A = alpha .
        for i in range(len(self.canonical)):
            index = "I_%d" % i
            for dot, production in self.canonical[i]:
                n, production = production[0], production[2]
                if (n == "S'"): continue
                if (dot >= len(production)):
                    for f in self.grammar_follow[n]:
                        self.table[index][f] = ["r%d" % self.grammar[n].index([*production]), n]

    def actual_token(self):
        return('\'' + self.token.category.name + '\'' if self.token else "EOF")

    def next_token(self):
        self.codePointer += 1
        prev = (self.token.category.name, self.token.value) if self.token else None
        self.token = self.lexicalAnalyzer.next_token()
        self.tokens += [self.token]
        return(prev)

    def parse(self):
        self.codePointer = -1
        stack = [[0, ""]]
        while (stack):
            self.stack_history += [stack.copy()]

            state, symbol = stack[len(stack) - 1]
            action = self.table["I_%d" % state][self.actual_token()]

            if (action[0] == "Error"): return(False)
            if (action[0] == "Accepted"): return(True)

            if (action[0][0] == 'e'): # stacks
                stack += [[int(action[0][1:]), self.next_token()]]
            elif (action[0][0] == 'r'): # redecuts
                n = action[1] # gets non_terminal
                production = self.grammar[n][int(action[0][1:])]
                now = []
                for i in range(len(production)):
                    state, symbol = stack.pop(len(stack) - 1)
                    now += [symbol]
                self.tree += [now]
                state, symbol = stack[len(stack) - 1]
                trasition = int(self.table["I_%d" % state][n][0])
                stack += [[trasition, n]]

    def analyse(self):
        self.buildCanonical()
        self.buildSLRTable()
        self.verdict = self.parse()
        pass
