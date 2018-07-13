id [[:alpha:]](_|[[:alnum:]])*

/* Type */
typeBool "bool"
typeInt "int"
typeReal "real"
typeChar "char"
typeString "string"
typeArray "array"

/* Type Especifiers */
asCast "as"
isType "is"
of "of"

/* Literals */
bool "true"|"false"
int [[:digit:]]+
real [[:digit:]]+"."[[:digit:]]*
scynot {real}e{int}
char "'"(\\.|[^"\\])?"'"
string \"(\\.|[^"\\])*\"

/* Iteration */
repeat "repeat"
whileLoop "while"
to "to"
at "at"

/* Selection */
ifSel "if"
elifSel "elif"
elseSel "else"

/* Function parameters / Expressions */
opParen "("
clParen ")"

/* Function */
function "function"
returnFun "return"
entryPoint "@isEntryPoint"

/* Code block */
opBraces "{"
clBraces "}"

/* Array access */
opBrackets "["
clBrackets "]"

/* Operators */
unary "-"|"!"|"~"
exp "**"|"*/"
mult "*"|"/"|"%"
additive "+"|"-"
bitShift "<<"|">>"
relational "<"|"<="|">="|">"
eqOrDiff "=="|"!="
bitAnd "&"
bitOr "|"
logicAnd "&&"
logicOr "||"
attrib "="

/* Separators */
comma ","

%%

{typeBool} { printf(" <typeBool: %s> ", yytext); }
{typeInt} { printf(" <typeInt: %s> ", yytext); }
{typeReal} { printf(" <typeReal: %s> ", yytext); }
{typeChar} { printf(" <typeChar: %s> ", yytext); }
{typeString} { printf(" <typeString: %s> ", yytext); }
{typeArray} { printf(" <typeArray: %s> ", yytext); }
{asCast} { printf(" <asCast: %s> ", yytext); }
{isType} { printf(" <isType: %s> ", yytext); }
{of} { printf(" <of: %s> ", yytext); }
{bool} { printf(" <bool: %s> ", yytext); }
{int} { printf(" <int: %s> ", yytext); }
{real} { printf(" <real: %s> ", yytext); }
{scynot} { printf(" <scynot: %s> ", yytext); }
{char} { printf(" <char: %s> ", yytext); }
{string} { printf(" <string: %s> ", yytext); }
{repeat} { printf(" <repeat: %s> ", yytext); }
{whileLoop} { printf(" <whileLoop: %s> ", yytext); }
{to} { printf(" <to: %s> ", yytext); }
{at} { printf(" <at: %s> ", yytext); }
{ifSel} { printf(" <ifSel: %s> ", yytext); }
{elifSel} { printf(" <elifSel: %s> ", yytext); }
{elseSel} { printf(" <elseSel: %s> ", yytext); }
{opParen} { printf(" <opParen: %s> ", yytext); }
{clParen} { printf(" <clParen: %s> ", yytext); }
{function} { printf(" <function: %s> ", yytext); }
{returnFun} { printf(" <returnFun: %s> ", yytext); }
{entryPoint} { printf(" <entryPoint: %s> ", yytext); }
{opBraces} { printf(" <opBraces: %s> ", yytext); }
{clBraces} { printf(" <clBraces: %s> ", yytext); }
{opBrackets} { printf(" <opBrackets: %s> ", yytext); }
{clBrackets} { printf(" <clBrackets: %s> ", yytext); }
{unary} { printf(" <unary: %s> ", yytext); }
{exp} { printf(" <exp: %s> ", yytext); }
{mult} { printf(" <mult: %s> ", yytext); }
{additive} { printf(" <additive: %s> ", yytext); }
{bitShift} { printf(" <bitShift: %s> ", yytext); }
{relational} { printf(" <relational: %s> ", yytext); }
{eqOrDiff} { printf(" <eqOrDiff: %s> ", yytext); }
{bitAnd} { printf(" <bitAnd: %s> ", yytext); }
{bitOr} { printf(" <bitOr: %s> ", yytext); }
{logicAnd} { printf(" <logicAnd: %s> ", yytext); }
{logicOr} { printf(" <logicOr: %s> ", yytext); }
{attrib} { printf(" <attrib: %s> ", yytext); }
{comma} { printf(" <comma: %s> ", yytext); }
{id} { printf(" <id: %s> ", yytext); }

%%

int yywrap(void)
{
  return(0);
}

int main(void)
{
  yylex();
  return(0);
}
