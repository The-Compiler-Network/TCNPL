from enum import Enum

class TokenCategory(Enum):
  id, typeBool, typeInt, typeReal, typeChar, typeString, \
  typeArray, asCast, isType, of, bool, int, real, char, \
  string, repeat, whileLoop, to, at, ifSel, \
  elifSel, elseSel, opParen, clParen, function, returnFun, \
  entryPoint, opBraces, clBraces, opBrackets, clBrackets, \
  unary,  exp, mult, plus, minus, bitShift, relational, eqOrDiff, \
  bitXor, bitAnd, bitOr, logicAnd, logicOr, attrib, comma, unknown = list(range(47))
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
# real = [[:digit:]]+"."[[:digit:]]*(e{int})?
# scinot = {real}e{int} DISABLED
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
# unary = "-"|"!"|"~"
# exp = "**"|"*/"
# mult = "*"|"/"|"%"
# additive = "+"|"-"
# bitShift = "<<"|">>"
# relational = "<"|"<="|">="|">"
# eqOrDiff = "=="|"!="
# bitAnd = "&"
# bitOr = "|"
# logicAnd = "&&"
# logicOr = "||"
# attrib = "="
# comma = ","
