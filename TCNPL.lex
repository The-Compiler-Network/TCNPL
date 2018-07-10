LETTER [a-zA-Z]
DIGIT [0-9]
SYMBOL [^0-9a-zA-Z]
ASCII \\.|[^\\"]

%%

  /* Constantes Literais: */
{DIGIT}+ { printf("<int: %s>", yytext); }
{DIGIT}+.{DIGIT}* { printf("<real: %s>", yytext); }
'{ASCII}?' { printf("<char: %s>", yytext); }
  /* \"(\\.|[^\\"])*\" { printf("<string: %s>", yytext); } */
\"{ASCII}*\" { printf("<string: %s>", yytext); }

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