from LexicalAnalyzer.model.Token import Token
from LexicalAnalyzer.analyzer.LexicalAnalyzer import LexicalAnalyzer
from math import log10, floor
import os
TABLE = True
LIVE = False
ALCINO = True

class SLRParser:
    token = None
    tokens = []
    grammar = {}
    grammar_follow = {}
    terminals = set()
    non_terminals = set()
    tree = []
    gotos = {}
    canonical = []
    table = {}
    tree_pointer = 0
    stack_history = []
    lexicalAnalyzer = None
    verdict = False
    ambiguity = []

    def __init__(self, lexicalAnalyzer, grammar_path):
        self.lexicalAnalyzer = lexicalAnalyzer
        self.tokens = []
        self.next_token()
        try:
            self.read_grammar(open(grammar_path, 'r', encoding="utf-8"))
        except Exception as e:
            print(e, self.grammar)
        for n in self.non_terminals:
            self.grammar_follow[n] = sorted(self.follow(n, set()))

    def __str__(self):
        string = ""

        string += "Tokens:\n"
        for token in self.tokens:
            string += str(token) + "\n"
        string += '\n'

        if self.ambiguity:
            string += "Ambiguity:\n"
            for ambiguity in self.ambiguity:
                string += str(ambiguity) + '\n'
            string += '\n'

        string += "Grammar:\n"
        for rule in self.grammar:
            string += "%11s" % rule + " = "
            if rule != 'S':
                for i, production in enumerate(self.grammar[rule]):
                    if i: string += " | "
                    string += ' '.join(production)
            else:
                string += self.grammar[rule]
            string += '\n'
        string += '\n'

        string += "Follow:\n"
        for n in self.non_terminals:
            string += "follow(%s) = " % n + str(self.grammar_follow[n]) + '\n'
        string += '\n'

        # string += "Canonical:\n"
        # for i, state in enumerate(self.canonical):
        #     string += "I_%d = " % i + str(state) + '\n'
        # string += '\n'

        if TABLE:
            string += "SLR Table:\n"
            columns = sorted(self.terminals) + ["EOF"] + sorted(self.non_terminals)
            biggest_cell = max(len(i) for i in columns)
            for row in self.table:
                for column in self.table[row]:
                    cell = self.table[row][column]
                    biggest_cell = max(biggest_cell, len(" ".join(cell)))
            string += " "*(3+floor(log10(len(self.table)))) + "|" + "|".join([c.center(biggest_cell, ' ') for c in columns]) + '\n'
            for i in range(len(self.table)):
                index = "I_%d" % i
                string += str(index).center(2+floor(log10(len(self.table))), ' ') + "|" + "|".join([(" ".join(self.table[index][c])).center(biggest_cell, ' ') for c in columns]) + '\n'
            string += '\n'

        string += "Stack:\n"
        for step in self.stack_history:
            string += str(step) + '\n'
        string += '\n'

        if self.verdict:
            string += "Tree:\n"
            string += self.tree_to_string()

        string += "Verdict: " + "Accepted" if self.verdict else "Rejected" + '\n'

        return string

    def tree_to_string(self):
        self.tree = [[self.grammar['S']]] + self.tree
        self.tree_pointer, level_tree, level_pointer = 0, {}, {}
        self.tree_to_level_tree(0, level_tree)
        for l in sorted(level_tree):
            level_tree[l].reverse()
            level_pointer[l] = 0
        new_tree = []
        self.level_tree_to_tree(0, level_pointer, level_tree, new_tree)
        self.tree, self.tree_pointer = new_tree, 0
        return self.tree_to_string_util(0)
    def tree_to_level_tree(self, depth, level_tree):
        if depth not in level_tree: level_tree[depth] = []
        level_tree[depth] += [self.tree[self.tree_pointer]]
        for element in self.tree[self.tree_pointer]:
            if (element in self.non_terminals):
                self.tree_pointer += 1
                self.tree_to_level_tree(depth + 1, level_tree)
    def level_tree_to_tree(self, depth, level_pointer, level_tree, new_tree):
        if depth not in level_tree or level_pointer[depth] >= len(level_tree[depth]): return
        new_tree += [level_tree[depth][level_pointer[depth]]]
        for element in level_tree[depth][level_pointer[depth]]:
            if (element in self.non_terminals):
                self.level_tree_to_tree(depth + 1, level_pointer, level_tree, new_tree)
        level_pointer[depth] += 1
    def tree_to_string_util(self, depth):
        tree_string = ""
        for element in self.tree[self.tree_pointer]:
            tree_string += '\t'*depth + str(element) + '\n'
            if (element in self.non_terminals):
                self.tree_pointer += 1
                tree_string += self.tree_to_string_util(depth + 1)
        return tree_string

    def save(self, folder):
        try: os.mkdir(folder)
        except: pass

        tokens = open(folder + "tokens", "w")
        for token in self.tokens:
            print(token, file=tokens)
        tokens.close()

        stack = open(folder + "stack", "w")
        for step in self.stack_history:
            print(step, file=stack)
        stack.close()

        follow = open(folder + "follow", "w")
        for n in self.non_terminals:
            print("follow(%s) =" % n, self.grammar_follow[n], file=follow)
        follow.close()

        canonical = open(folder + "canonical", "w")
        for i, state in enumerate(self.canonical):
            print("I_%d =" % i, state, file=canonical)
        canonical.close()

        table = open(folder + "table", "w")
        columns = sorted(self.terminals) + ["EOF"] + sorted(self.non_terminals)
        biggest_cell = max(len(i) for i in columns)
        for row in self.table:
            for column in self.table[row]:
                cell = self.table[row][column]
                biggest_cell = max(biggest_cell, len(" ".join(cell)))
        print(" "*(3+floor(log10(len(self.table)))) + "|" + "|".join([c.center(biggest_cell, ' ') for c in columns]), file=table)
        for i in range(len(self.table)):
            index = "I_%d" % i
            print(str(index).center(3+floor(log10(len(self.table))), ' ') + "|" + "|".join([(" ".join(self.table[index][c])).center(biggest_cell, ' ') for c in columns]), file=table)
        table.close()

        tree = open(folder + "tree", "w")
        print(self.tree_to_string(), file=tree)
        print("\nVerdict: " + "Accepted" if self.verdict else "Rejected", file=tree)
        tree.close()

    def read_grammar(self, grammar_file):
        self.grammar['S'] = grammar_file.readline().strip('\n')
        line = grammar_file.readline()
        while line:
            left, right = line.split('=')
            left = left.strip(' ')
            if left not in self.grammar: self.grammar[left] = []
            self.non_terminals.add(left)
            for production in right.split('|'):
                elements = production.split()
                for element in elements:
                    if (element[0] == '\'' and element != '\'e\''): self.terminals.add(element)
                self.grammar[left] += [elements]
            line = grammar_file.readline()
            while line == '\n': line = grammar_file.readline()

    def first(self, production, visited):
        if production == ['e']: return ['e']
        if tuple(production) in visited: return []
        visited.add(tuple(production))
        first_set, epis = set(), 0
        for element in production:
            doneAll = True
            if element not in self.non_terminals:
                first_set.add(element)
                break
            elif ['e'] in self.grammar[element]: epis, doneAll = epis + 1, False
            if element in self.non_terminals:
                inside_epi = False
                for productions in self.grammar[element]:
                    first_minus_epi = self.first(productions, visited)
                    first_set.update(first_minus_epi)
                    if 'e' in first_minus_epi:
                        inside_epi = True
                        first_set.remove('e')
                if not inside_epi: break
                else: epis += done
        else:
            if epis >= len(production): first_set.add('e')
        return first_set

    def follow(self, X, visited):
        follow_set = set()
        if (X == self.grammar['S']): follow_set.add("EOF")
        for A in self.non_terminals:
            for production in self.grammar[A]:
                if (X not in production): continue
                is_last = False
                for i, element in enumerate(production):
                    if (element != X): continue
                    is_last = i == len(production) - 1
                    if (i < len(production) - 1):
                        first_minus_epi = self.first(production[i + 1:], set())
                        follow_set.update(first_minus_epi)
                        if ('e' in first_minus_epi): is_last = True
                if (is_last):
                    if (A == X): continue
                    if (A not in visited):
                        visited.add(A)
                        follow_set.update(self.grammar_follow[A] if A in self.grammar_follow else self.follow(A, visited))
        if ('e' in follow_set): follow_set.remove('e')
        return follow_set

    def closure(self, production_block, visited):
        closure_set = set()
        if tuple(production_block) in visited: return closure_set
        visited.add(tuple(production_block))

        closure_set.add(production_block)
        dot, production = production_block[0], production_block[1][2]
        if dot < len(production) and production[dot] in self.non_terminals:
            for inter_production in self.grammar[production[dot]]:
                inter_production_block = (0, (production[dot], "=", tuple(inter_production)))
                closure_set.update(self.closure(inter_production_block, visited))
        return sorted(closure_set)

    def goto(self, state, symbol):
        new_state = []
        for dot, production in state:
            if dot >= len(production[2]) or production[2][dot] != symbol or production[2][0] == 'e': continue
            new_production_block = ((dot + 1), (production))
            closure_set = self.closure(new_production_block, set())
            for production_block in closure_set:
                if production_block not in new_state: new_state += [production_block]
        return new_state

    def get_symbols(self, closure_set):
        symbols = set()
        for dot, production in closure_set:
            if dot < len(production[2]): symbols.add(production[2][dot])
        return symbols

    def build_canonical(self):
        self.canonical += [self.closure((0, ("S'", "=", tuple([self.grammar['S']]) )), set())]
        i = 0
        while i < len(self.canonical):
            symbols = self.get_symbols(self.canonical[i])
            for symbol in symbols:
                new_state = self.goto(self.canonical[i], symbol)
                if not new_state: continue
                if new_state not in self.canonical: self.canonical += [new_state]
                self.gotos[(i, symbol)] = self.canonical.index(new_state)
            i += 1

    def init_table(self):
        for i in range(len(self.canonical)):
            index = "I_%d" % i
            self.table[index] = {}
            for t in self.terminals: self.table[index][t] = ["Error"]
            for n in self.non_terminals: self.table[index][n] = ["Error"]
            self.table[index]["EOF"] = ["Error"]

    def build_SLR_table(self):
        self.init_table()

        # RULE: S' = S .
        closure_set = self.canonical[self.gotos[(0, self.grammar['S'])]] # goto(I_0, S)
        self.table["I_%d" % self.canonical.index(closure_set)]["EOF"] = ["Accepted"]
        if ['e'] in self.grammar[self.grammar['S']]: self.table["I_0"]["EOF"] = ["Accepted"]

        # RULE: goto(state, symbol) [symbol = terminals U nonTerminals]
        for state, symbol in sorted(self.gotos):
            index = "I_%d" % state
            if self.table[index][symbol] != ["Error"]: self.ambiguity += ["Duplication on %s %s" % (str(index), str(symbol))]
            self.table[index][symbol] = [("s" if symbol in self.terminals else "") + str(self.gotos[(state, symbol)])]

        # RULE: A = alpha .
        for i in range(len(self.canonical)):
            index = "I_%d" % i
            for dot, production in self.canonical[i]:
                n, production = production[0], production[2]
                if n == "S'": continue
                if dot >= len(production):
                    for f in self.grammar_follow[n]:
                        if self.table[index][f] != ["Error"]: self.ambiguity += ["Duplication on %s %s from %s to r%d %s %s" % (str(index), str(f), str(self.table[index][f]), self.grammar[n].index([*production]), str(production), str(n))]
                        self.table[index][f] = ["r%d" % self.grammar[n].index([*production]), n]

    def actual_token(self):
        return '\'' + self.token.category.name + '\'' if self.token else "EOF"

    def next_token(self):
        if ALCINO and self.token is not None: print(self.token)
        prev = (self.token.category.name, self.token.value) if self.token else None
        self.token = self.lexicalAnalyzer.next_token()
        if self.token is not None: self.tokens += [self.token]
        return prev

    def parse(self):
        stack = [[0, ""]]
        while (stack):
            if LIVE: print(stack)
            self.stack_history += [stack.copy()]

            state, symbol = stack[len(stack) - 1]
            action = self.table["I_%d" % state][self.actual_token()]

            if action[0] == "Error": return(False)
            if action[0] == "Accepted": return(True)

            if action[0][0] == 's': # stacks
                stack += [[int(action[0][1:]), self.next_token()]]
            elif action[0][0] == 'r': # redecuts
                n = action[1] # gets non_terminal
                production = self.grammar[n][int(action[0][1:])]
                now = []
                for i in range(len(production)):
                    state, symbol = stack.pop(len(stack) - 1)
                    now = [symbol] + now
                if ALCINO: print(" "*13, n, "=", now)
                self.tree = [now] + self.tree
                state, symbol = stack[len(stack) - 1]
                trasition = int(self.table["I_%d" % state][n][0])
                stack += [[trasition, n]]

    def analyse(self):
        self.build_canonical()
        self.build_SLR_table()
        try:
            self.verdict = self.parse()
        except KeyError as e:
            print("Syntatic Analysis failed because of unknown token:", e)
        return self.verdict
