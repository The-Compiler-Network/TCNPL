ASCII \\.|[^"\\]

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

/* Function parameters */
openParenthesis "("
closeParenthesis ")"

/* Function */
function "function"
return "return"
isEntryPoint "@isEntryPoint"

/* Code block */
openBraces "{"
closeBraces "}"

/* Array access */
openBrackets "["
closeBrackets "]"

/* Input and Output */
lineIn "lineIn"
textOut "textOut"
format "format"

/* Operators */
unary "-"
exponential "**"|"*/"
multiplicative "*"|"/"|"%"
aditive "+"|"-"
bitwiseShift "<<"|">>"
relational "<"|" <="|">="|">"
logical "=="|"!="
bitwiseAnd "&"
bitwiseOr "|"
logicalAnd "&&"
logicalOr "||"
atribution "="
comma ","

id [[:alpha:]](_|[[:alnum:]])*

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
{openParenthesis} { printf(" <openParenthesis: %s> ", yytext); }
{closeParenthesis} { printf(" <closeParenthesis: %s> ", yytext); }
{function} { printf(" <function: %s> ", yytext); }
{return} { printf(" <return: %s> ", yytext); }
{isEntryPoint} { printf(" <isEntryPoint: %s> ", yytext); }
{openBraces} { printf(" <openBraces: %s> ", yytext); }
{closeBraces} { printf(" <closeBraces: %s> ", yytext); }
{openBrackets} { printf(" <openBrackets: %s> ", yytext); }
{closeBrackets} { printf(" <closeBrackets: %s> ", yytext); }
{lineIn} { printf(" <lineIn: %s> ", yytext); }
{textOut} { printf(" <textOut: %s> ", yytext); }
{format} { printf(" <format: %s> ", yytext); }
{unary} { printf(" <unary: %s> ", yytext); }
{exponential} { printf(" <exponential: %s> ", yytext); }
{multiplicative} { printf(" <multiplicative: %s> ", yytext); }
{aditive} { printf(" <aditive: %s> ", yytext); }
{bitwiseShift} { printf(" <bitwiseShift: %s> ", yytext); }
{relational} { printf(" <relational: %s> ", yytext); }
{logical} { printf(" <logical: %s> ", yytext); }
{bitwiseAnd} { printf(" <bitwiseAnd: %s> ", yytext); }
{bitwiseOr} { printf(" <bitwiseOr: %s> ", yytext); }
{logicalAnd} { printf(" <logicalAnd: %s> ", yytext); }
{logicalOr} { printf(" <logicalOr: %s> ", yytext); }
{atribution} { printf(" <atribution: %s> ", yytext); }
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
