import os

os.system("flex TCNPL.lex")
os.system("gcc lex.yy.c -o ER")
os.system("./ER < testCases")