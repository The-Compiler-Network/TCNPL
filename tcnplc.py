import sys
from LexicalAnalyzer.analyzer.LexicalAnalyzer import LexicalAnalyzer
from SyntacticAnalyzer.analyzer.SyntacticAnalyzer import SyntacticAnalyzer
from SyntacticAnalyzer.analyzer.SLRParser import SLRParser
folder_name = sys.argv[1].split('/')
folder_name = folder_name[len(folder_name) - 1].split('.')[0]

lexicalAnalyzer = LexicalAnalyzer(sys.argv[1])
# tokens = []
#
# while True:
#     token = lexicalAnalyzer.next_token()
#     if not token:
#         break
#     tokens += [token]
#     # print(token)

syntacticAnalyzer = SLRParser(lexicalAnalyzer, "Grammar/SLRGrammar")
verdict = syntacticAnalyzer.analyse()
syntacticAnalyzer.save("Results/" + folder_name + "/")
print("\nVerdict:", "Accepted" if verdict else "Rejected")
# print(syntacticAnalyzer)
