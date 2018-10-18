from enum import Enum

class TokenCategory(Enum):
	id, typeBool, typeInt, typeReal, typeChar, typeString, \
	typeArray, asCast, isType, of, bool, int, real, scynot, char, \
	string, repeat, whileLoop, to, at, ifSel, \
	elifSel, elseSel, opParen, clParen, function, returnFun, \
	entryPoint, opBraces, clBraces, opBrackets, clBrackets, \
	unary,  exp, mult, plus, minus, bitShift, relational, eqOrDiff,\
	bitAnd, bitOr, logicAnd, logicOr, attrib, comma, unknown = list(range(47))

	def __str__(self):
		return "%04d, %10s" % (self.value, self.name)

	def classify(string):
		i = 0

		if string[i] == '"' or string[i] == '\'':
			if len(string) > 1 and string[0] == string[len(string) - 1]:
				if string[0] == '"':
					return TokenCategory.string
				else:
					if len(string) > 3:
						return TokenCategory.unknown
					else:
						return TokenCategory.char
			else:
				return TokenCategory.unknown

		if 'A' <= string[i] <= 'Z' or 'a' <= string[i] <= 'z':
			i += 1
			while i < len(string) and ('A' <= string[i] <= 'Z' or 'a' <= string[i] <= 'z' or '0' <= string[i] <= '9' or string[i] == '_'):
				i += 1
			if i == len(string):
				return TokenCategory.id
			else:
				return TokenCategory.unknown

		while i < len(string) and '0' <= string[i] <= '9':
			i += 1
		if i == len(string):
			return TokenCategory.int

		if string[i] == '.':
			i += 1
			while i < len(string) and '0' <= string[i] <= '9':
				i += 1
			if i == len(string):
				return TokenCategory.real

		if string[i] == 'e':
			i += 1
			while i < len(string) and '0' <= string[i] <= '9':
				i += 1
			if i == len(string):
				return TokenCategory.scynot

		return TokenCategory.unknown

# id = [[:alpha:]](_|[[:alnum:]])*
# typeBool = "bool"
# typeInt = "int"
# typeReal = "real"
# typeChar = "char"
# typeString = "string"
# typeArray = "array"
# asCast = "as"
# isType = "is"
# of = "of"
# bool = "true"|"false"
# int = [[:digit:]]+
# real = [[:digit:]]+"."[[:digit:]]*
# scynot = {real}e{int}
# char = "'"(\\.|[^"\\])?"'"
# string = \"(\\.|[^"\\])*\"
# repeat = "repeat"
# whileLoop = "while"
# to = "to"
# at = "at"
# ifSel = "if"
# elifSel = "elif"
# elseSel = "else"
# opParen = "("
# clParen = ")"
# function = "function"
# returnFun = "return"
# entryPoint = "@isEntryPoint"
# opBraces = "{"
# clBraces = "}"
# opBrackets = "["
# clBrackets = "]"
# unary = "!"|"~"
# exp = "**"|"*/"
# mult = "*"|"/"|"%"
# plus = "+" # should have a single category for '+' sign, since it has multiple features
# minus = "-" # should have a single category for '-' sign, since it has multiple features
# bitShift = "<<"|">>"
# relational = "<"|"<="|">="|">"
# eqOrDiff = "=="|"!="
# bitAnd = "&"
# bitOr = "|"
# logicAnd = "&&"
# logicOr = "||"
# attrib = "="
# comma = ","
