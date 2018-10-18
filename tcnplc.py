import sys
from LexicalAnalyser.analyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntacticAnalyser.analyser.SyntacticAnalyser import SyntacticAnalyser
from SyntacticAnalyser.analyser.SLRParser import SLRParser

lexicalAnalyser = LexicalAnalyzer(sys.argv[1])
tokens = []

while True:
    token = lexicalAnalyser.next_token()
    if not token:
        break
    tokens += [token]
    # print(token)

syntacticAnalyser = SLRParser(tokens, sys.argv[2])
syntacticAnalyser.analyse()
print(syntacticAnalyser)
