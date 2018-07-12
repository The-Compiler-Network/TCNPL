ASCII \\.|[^"\\]
id [[:alpha:]](_|[[:alnum:]])*

/* Type */
typeBool "bool"
typeInt "int"
typeReal "real"
typeChar "char"
typeString "string"
typeArray "array"

/* Type Especifiers */
as "as"
is "is"
of "of"

/* Literals */
bool "true"|"false"
int [[:digit:]]+
real [[:digit:]]+"."[[:digit:]]*
char "'"{ASCII}?"'"
string \"{ASCII}*\"
literal {bool}|{int}|{real}|{char}|{string}
array "{"{literal}(","{literal})*"}"

/* Iteration */
repeat "repeat"
while "while"
to "to"
at "at"

/* Selection */
if "if"
elif "elif"
else "else"

/* Function parameters / Expressions */
opParen "("
clParen ")"

/* Function */
function "function"
return "return"
entryPoint "@isEntryPoint"

/* Code block */
opBraces "{"
clBraces "}"

/* Array access */
opBrackets "["
clBrackets "]"

/* Input and Output */
lineIn "lineIn"
textOut "textOut"
format "format"

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
atribution "="

/* Separators */
comma ","

%%

{typeBool} { printf(" <typeBool: %s> ", yytext); }
{typeInt} { printf(" <typeInt: %s> ", yytext); }
{typeReal} { printf(" <typeReal: %s> ", yytext); }
{typeChar} { printf(" <typeChar: %s> ", yytext); }
{typeString} { printf(" <typeString: %s> ", yytext); }
{typeArray} { printf(" <typeArray: %s> ", yytext); }
{as} { printf(" <as: %s> ", yytext); }
{is} { printf(" <is: %s> ", yytext); }
{of} { printf(" <of: %s> ", yytext); }
{bool} { printf(" <bool: %s> ", yytext); }
{int} { printf(" <int: %s> ", yytext); }
{real} { printf(" <real: %s> ", yytext); }
{char} { printf(" <char: %s> ", yytext); }
{string} { printf(" <string: %s> ", yytext); }
{array} { printf(" <array: %s> ", yytext); }
{repeat} { printf(" <repeat: %s> ", yytext); }
{while} { printf(" <while: %s> ", yytext); }
{to} { printf(" <to: %s> ", yytext); }
{at} { printf(" <at: %s> ", yytext); }
{if} { printf(" <if: %s> ", yytext); }
{elif} { printf(" <elif: %s> ", yytext); }
{else} { printf(" <else: %s> ", yytext); }
{opParen} { printf(" <opParen: %s> ", yytext); }
{clParen} { printf(" <clParen: %s> ", yytext); }
{function} { printf(" <function: %s> ", yytext); }
{return} { printf(" <return: %s> ", yytext); }
{entryPoint} { printf(" <isEntryPoint: %s> ", yytext); }
{opBraces} { printf(" <opBraces: %s> ", yytext); }
{clBraces} { printf(" <clBraces: %s> ", yytext); }
{opBrackets} { printf(" <opBrackets: %s> ", yytext); }
{clBrackets} { printf(" <clBrackets: %s> ", yytext); }
{lineIn} { printf(" <lineIn: %s> ", yytext); }
{textOut} { printf(" <textOut: %s> ", yytext); }
{format} { printf(" <format: %s> ", yytext); }
{unary} { printf(" <unary: %s> ", yytext); }
{exp} { printf(" <exponential: %s> ", yytext); }
{mult} { printf(" <multiplicative: %s> ", yytext); }
{additive} { printf(" <additive: %s> ", yytext); }
{bitShift} { printf(" <bitShift: %s> ", yytext); }
{relational} { printf(" <relational: %s> ", yytext); }
{eqOrDiff} { printf(" <eqOrDiff: %s> ", yytext); }
{bitAnd} { printf(" <bitAnd: %s> ", yytext); }
{bitOr} { printf(" <bitOr: %s> ", yytext); }
{logicAnd} { printf(" <logicAnd: %s> ", yytext); }
{logicOr} { printf(" <logicOr: %s> ", yytext); }
{atribution} { printf(" <atribution: %s> ", yytext); }
{comma} { printf(" <comma: %s> ", yytext); }
  /* {end} { printf(" <end: \\n> \n"); } */
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
