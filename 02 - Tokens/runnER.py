import os

os.system("flex TCNPL.lex")
os.system("gcc lex.yy.c -o ER")
if os.name == 'nt':
    os.system("ER < testCases")
else:
    os.system("./ER < testCases")