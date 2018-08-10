import sys
from analyzer.LexicalAnalyzer import LexicalAnalyzer

la = LexicalAnalyzer(sys.argv[1])

while True:
	token = la.next_token()
	if not token:
		break
	print(token)
