LETTER [a-zA-Z]
DIGIT [0-9]
SYMBOL [^0-9a-zA-Z]
ASCII \\.|[^"\\]
id {LETTER}(_|{LETTER}|{DIGIT})*

bool "true"|"false"
int {DIGIT}+
real {DIGIT}+"."{DIGIT}*
char "'"{ASCII}?"'"
string \"{ASCII}*\"
literal {bool}|{int}|{real}|{char}|{string}
array "{"{literal}(","{literal})*"}"

repeat "repeat"
while "while"
  /*to "to"
  at "at"

  if "if"
  elif "elif"
  else "else"*/

counterLoopControl "("{id}"="({id}|{int})"to"({id}|{int})("at"({id}|{int}))?")"

body "{""}"

%%

    /* Reserved words: */
  /* Selection and iteration {id}=[{id}|{int}]to[{id}|{int}][at[{id}|{int}]]? */


{repeat}{counterLoopControl}{body} { printf("<repeat counter: %s>", yytext); }
{repeat}{while}"("")"{body} { printf("<repeat while: %s>", yytext); }
{repeat}{body}{while}"("")" { printf("<while repeat: %s>", yytext); }
  /*"repeat("{id}"="({id}|{int}){to}({id}|{int})")"{body}    { printf("<repeat: %s>", yytext); }*/

  /* Literals: */
{bool}    { printf("<bool: %s>", yytext); }
{int}     { printf("<int: %s>", yytext); }
{real}    { printf("<real: %s>", yytext); }
{char}    { printf("<char: %s>", yytext); }
{string}  { printf("<string: %s>", yytext); }
{array}   { printf("<array: %s>", yytext); }


{body}    { printf("<body: %s>", yytext); }

{id}      { printf("<id: %s>", yytext); }

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