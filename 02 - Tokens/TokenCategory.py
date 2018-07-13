from enum import Enum

class TokenCategory(Enum):
  id, typeBool, typeInt, typeReal, typeChar, typeString, \
  typeArray, asCast, isType, of, bool, int, real, scynot, char, \
  string, literal, array, repeat, whileLoop, to, at, ifSel, \
  elifSel, elseSel, opParen, clParen, function, returnFun, \
  entryPoint, opBraces, clBraces, opBrackets, clBrackets, \
  unary,  exp, mult, additive, bitShift, relational, eqOrDiff,\
  bitAnd, bitOr, logicAnd, logicOr, attrib, comma = list(range(47))
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
# literal = {bool}|{int}|{real}|{char}|{string}
# array = "{"{literal}(","{literal})*"}"
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
