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

counterLoopControl "("{id}"="({id}|{int})"to"({id}|{int})("at"({id}|{int}))?")"

body "{""}"

%%

    /* Reserved words: */
  /* Selection and iteration {id}=[{id}|{int}]to[{id}|{int}][at[{id}|{int}]]? */

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