from enum import Enum

class TokenCategory(Enum):
  ASCII, id, typeBool, typeInt, typeReal, typeChar, typeString, typeArray, asCast, isType, of, bool, int, real, char, string, literal, array, repeat, whileLoop, to, at, ifSel, elifSel, elseSel, opParen, clParen, function, returnFun, entryPoint, opBraces, clBraces, opBrackets, clBrackets, lineIn, textOut, format, unary, exp, mult, aditive, bitShift, relational, logical, bitwiseAnd, bitwiseOr, logicAnd, logicOr, atribution, comma = list(range(50))