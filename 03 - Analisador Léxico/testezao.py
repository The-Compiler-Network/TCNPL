from analyzer.LexicalAnalyzer import LexicalAnalyzer

la = LexicalAnalyzer("../02 - Tokens/testCases/fibonacci.tcn")

firstLine = -1
while True:
	token = la.next_token()
	if not token:
		break
	if token.get_line() > firstLine:
		firstLine = token.get_line()
		print()
	print(token)
