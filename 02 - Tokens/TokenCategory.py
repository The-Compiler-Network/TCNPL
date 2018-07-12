from enum import Enum


class TokenCategory(Enum):
  ASCII, id, typeBool, typeInt, typeReal, typeChar, typeString, \
  typeArray, asCast, isType, of, bool, int, real, char, string, \
  literal, array, repeat, whileLoop, to, at, ifSel, elifSel, \
  elseSel, opParen, clParen, function, returnFun, entryPoint, \
  opBraces, clBraces, opBrackets, clBrackets, lineIn, textOut, \
  format, unary, exp, mult, additive, bitShift, relational, \
  eqOrDiff, bitwiseAnd, bitwiseOr, logicAnd, logicOr, \
  attrib, comma = list(range(50))
  # id = [[:alpha:]](_|[[:alnum:]])*
  # typeBool = "bool"
  # typeInt = "int"
  # typeReal = "real"
  # typeChar = "char"
  # typeString = "string"
  # typeArray = "array"
  # as = "as"
  # is = "is"
  # of = "of"
  # bool = "true"|"false"
  # int = [[:digit:]]+
  # real = [[:digit:]]+"."[[:digit:]]*
  # char = "'"{ASCII}?"'"
  # string = \"{ASCII}*\"
  # literal = {bool}|{int}|{real}|{char}|{string}
  # array = "{"{literal}(","{literal})*"}"
  # repeat = "repeat"
  # while = "while"
  # to = "to"
  # at = "at"
  # if = "if"
  # elif = "elif"
  # else = "else"
  # opParen = "("
  # clParen = ")"
  # function = "function"
  # return = "return"
  # entryPoint = "@isEntryPoint"
  # opBraces = "{"
  # clBraces = "}"
  # opBrackets = "["
  # clBrackets = "]"
  # lineIn = "lineIn"
  # textOut = "textOut"
  # format = "format"
  # unary = "-"|"!"|"~"
  # exp = "**"|"*/"
  # mult = "*"|"/"|"%"
  # aditive = "+"|"-"
  # bitShift = "<<"|">>"
  # relational = "<"|"<="|">="|">"
  # eqOrDiff = "=="|"!="
  # bitwiseAnd = "&"
  # bitwiseOr = "|"
  # logicAnd = "&&"
  # logicOr = "||"
  # attrib = "="
  # comma = ","
