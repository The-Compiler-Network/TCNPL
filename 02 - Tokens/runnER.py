import os, sys

os.system("flex TCNPL.lex")
os.system("gcc lex.yy.c -o ER")
if os.name == 'nt':
  os.system("ER < %s" % sys.argv[1])
else:
  os.system("./ER < %s" % sys.argv[1])