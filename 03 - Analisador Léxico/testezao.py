from analyzer.LexicalAnalyzer import LexicalAnalyzer

la = LexicalAnalyzer("../02 - Tokens/testCases/helloWorld.tcn")

while True:
    token = la.next_token()
    if not token:
        break
    token.pretty_print()
