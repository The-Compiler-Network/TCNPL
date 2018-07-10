LETTER [a-zA-Z]
DIGIT [0-9]
SYMBOL [^0-9a-zA-Z]
ASCII \\.|[^"\\]
id {LETTER}[{LETTER}|{DIGIT}]*

bool true|false
int {DIGIT}+
real {DIGIT}+"."{DIGIT}*
char "'"{ASCII}?"'"
string \"{ASCII}*\"
literal {bool}|{int}|{real}|{char}|{string}
array "{"{literal}(,{literal})*"}"

body "{""}"

%%

{id}      { printf("<id: %s>", yytext); }

  /* Literals: */
{bool}    { printf("<bool: %s>", yytext); }
{int}     { printf("<int: %s>", yytext); }
{real}    { printf("<real: %s>", yytext); }
{char}    { printf("<char: %s>", yytext); }
{string}  { printf("<string: %s>", yytext); }
{array}   { printf("<array: %s>", yytext); }

    /* Reserved words: */
  /* Selection and iteration */
repeat({id}=[{id}|{int}]to[{id}|{int}][at[{id}|{int}]]?){body}    { printf("<repeat>"); }
to        { printf("to"); }
at        { printf("at"); }
while     { printf("while"); }
if        { printf("if"); }
elif      { printf("elif"); }
else      { printf("else"); }


as
is
bool

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