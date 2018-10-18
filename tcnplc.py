import sys
from LexicalAnalyzer.analyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntacticAnalyzer.analyzer.SyntacticAnalyzer import SyntacticAnalyzer
from SyntacticAnalyzer.analyzer.SLRParser import SLRParser

lexicalAnalyzer = LexicalAnalyzer(sys.argv[1])
# tokens = []
#
# while True:
#     token = lexicalAnalyzer.next_token()
#     if not token:
#         break
#     tokens += [token]
#     # print(token)

syntacticAnalyzer = SLRParser(lexicalAnalyzer, sys.argv[2])
syntacticAnalyzer.analyse()
print(syntacticAnalyzer)
