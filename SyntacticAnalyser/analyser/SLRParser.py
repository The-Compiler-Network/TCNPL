class SLRParser:

    def closure(self, productions, grammar, nonTerminals, visited):
        closureSet = set()
        if tuple(productions) in visited: return(closureSet)
        visited.add(tuple(productions))
        for p in productions:
            closureSet.add(p)
        for pointer, production in productions:
            production = production[2]
            if pointer < len(production) and production[pointer] in nonTerminals:
                for internProduction in grammar[production[pointer]]:
                    internProductionBlock = (0, (productions[pointer], "=", tuple(internProduction)))
                    if internProductionBlock not in closureSet:
                        closureSet.update(self.closure([internProductionBlock], grammar, nonTerminals, visited))
        return sorted(closureSet)

    def goto(self, state, symbol, grammar, nonTerminals):
        newState = []
        for pointer, production in state:
            if pointer >= len(production[2]) or production[2][pointer] != symbol or production[2][0] == 'e': continue
            newProduction = ((pointer + 1), (production))
            closureSet = self.closure([newProduction], grammar, nonTerminals, set())
            for production in closureSet:
                if (production not in newState): newState += [production]
        return newState

    def getSymbols(self, closureSet):
        symbols = set()
        for pointer, production in closureSet:
            if pointer < len(production[2]): symbols.add(production[2][pointer])
        return symbols

    def buildC(self, S, grammar, terminals, nonTerminals):
        states, C = {}, []
        C += [self.closure([(0, ("S'", "=", tuple([S])))], grammar, nonTerminals, set())]
        i = 0
        while i < len(C):
            symbols = self.getSymbols(C[i])
            for symbol in symbols:
                newState = self.goto(C[i], symbol, grammar, nonTerminals)
                if not newState: continue
                if newState not in C:
                    C += [newState]
                states[(i, symbol)] = C.index(newState)
            i += 1
        return states, C