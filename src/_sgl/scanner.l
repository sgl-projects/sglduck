%option noyywrap
%option nodefault
%option noinput
%option nounput
%option case-insensitive

%x FROM_CONTENT
%x SUBQUERY_CONTENT

%{
#include "cgs.h"
#include "parser.tab.h"
#include "flex_overrides.h"

#define MAX_SUBQUERY_LEN 10000

int unclosed_paren_count;
%}

%%

"visualize"	{ return VISUALIZE; }
"as" { return AS; }
"from" { BEGIN(FROM_CONTENT); return FROM; }
"using" { return USING; }
"group" { return GROUP; }
"collect" { return COLLECT; }
"layer" { return LAYER; }
"scale" { return SCALE; }
"by" { return BY; }
"facet" { return FACET; }
"horizontally" { return HORIZONTALLY; }
"vertically" { return VERTICALLY; }
"title" { return TITLE; }
"," { return COMMA; }
-?(0|[1-9][0-9]*) {
	yylval.int_val = atoi(yytext);
	return INTEGER;
}
[^ '\t\n,()]+ { 
	yylval.str = strdup(yytext);
	return UNQUOTED_STRING;
}
'([^'\\]|\\.)*' {
	int match_len = strlen(yytext);
	char *unquoted_str = malloc(match_len - 1);
	strncpy(unquoted_str, yytext + 1, match_len - 2);
	unquoted_str[match_len - 2] = '\0';
	char *src = unquoted_str;
	char *dst = unquoted_str;
	while (*src) {
		if(*src == '\\' && *(src + 1) == '\'') {
			*dst++ = '\'';
			src += 2;
		} else {
			*dst++ = *src++;
		}
	}
	*dst = '\0';
	yylval.str = unquoted_str;
	
	return SINGLE_QUOTED_STRING;
}
"(" |
")" |
"="	{ return yytext[0]; }
[ \t\n]+ { }

<FROM_CONTENT>{
	[^ \t\n(]+ {
		yylval.str = strdup(yytext);
		BEGIN(INITIAL);
		return TABLE_NAME;
	}
	"(" {
		yylval.str = malloc(MAX_SUBQUERY_LEN);
		yylval.str[0] = '\0';
		unclosed_paren_count = 1;
		BEGIN(SUBQUERY_CONTENT);
	}
	[ \t\n]+ { }
}

<SUBQUERY_CONTENT>{
	"(" {
		strcat(yylval.str, yytext);
		unclosed_paren_count++;
	}
	")" {
		unclosed_paren_count--;
		if(unclosed_paren_count == 0) {
			BEGIN(INITIAL);
			return SQL_SUBQUERY;
		} else {
			strcat(yylval.str, yytext);
		}
	}
	.|\n {
		strcat(yylval.str, yytext);
	}
}

%%

void set_scanner_input(const char *input_string) {
	yy_scan_string(input_string);
}

void delete_scanner_buffer(void) {
	yy_delete_buffer(YY_CURRENT_BUFFER);
}

void reset_scanner_state(void) {
	BEGIN(INITIAL);
}
