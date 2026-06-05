%parse-param {struct cgs *cgs}
%parse-param {char **errmsg}

%{
#define _GNU_SOURCE
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include"sgl_error.h"
#include "cgs.h"
#include "aes.h"
#include "geom.h"
#include "cta.h"
#include "qual.h"
#include "scale.h"
#include "direction.h"
#include "case.h"

void set_scanner_input(const char *input_string);
void delete_scanner_buffer(void);
void reset_scanner_state(void);

int yylex(void);
void yyerror(struct cgs *cgs, char **errmsg, char const *s);
extern void yyrestart(FILE *input_file);

%}

%union {
	char *str;
	int int_val;
	struct col_expr ce;
	struct fn_arg *fa;
	enum direction direction_enum;
}

%token VISUALIZE AS FROM GROUP COLLECT USING LAYER COMMA SCALE BY TITLE
%token FACET HORIZONTALLY VERTICALLY
%token <str> TABLE_NAME SQL_SUBQUERY
%token <str> UNQUOTED_STRING SINGLE_QUOTED_STRING
%token <int_val> INTEGER

%type <ce> col_expr
%type <fa> fn_arg
%type <direction_enum> direction

%%

statement: layer_list graphic_clauses

graphic_clauses:
	| graphic_clauses graphic_clause

graphic_clause: scale_clause |
	facet_clause |
	title_clause

layer_list: layer_expression |
	layer_list LAYER layer_expression

layer_expression: VISUALIZE {
	struct layer *new_layer = malloc(sizeof(struct layer));
	new_layer->aes_mappings=NULL;
	new_layer->geoms=NULL;
	new_layer->groupings=NULL;
	new_layer->collections=NULL;
	new_layer->next=cgs->layers;
	cgs->layers=new_layer;
} aes_mappings from_clause grouping_clause collection_clause using_clause {}

geom_expr: UNQUOTED_STRING UNQUOTED_STRING {
	char *qual_str=$1;
	str_tolower(qual_str);	
	int print_result;
	if (!valid_qual_str(qual_str)) {
		print_result = asprintf(errmsg, "Invalid geom qualifier: %s\n", qual_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}
	enum qual qual = qual_enum(qual_str);	
	free(qual_str);

	char *geom_str = $2;
	str_tolower(geom_str);
	if (!valid_geom_str(geom_str)) {
		print_result = asprintf(errmsg, "Invalid geom name: %s\n", geom_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}	
	enum geom geom = geom_enum(geom_str);	
	free(geom_str);

	struct geom_expr *new_geom = malloc(sizeof(struct geom_expr));
	new_geom->qual = qual;
	new_geom->geom = geom;
	new_geom->next = cgs->layers->geoms;
	cgs->layers->geoms = new_geom;
} | UNQUOTED_STRING {
	enum qual qual=DEFAULT;
	int print_result;

	char *geom_str=$1;
	str_tolower(geom_str);
	if (!valid_geom_str(geom_str)) {
		print_result = asprintf(errmsg, "Invalid geom name: %s\n", geom_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}	
	enum geom geom = geom_enum(geom_str);	
	free(geom_str);

	struct geom_expr *new_geom = malloc(sizeof(struct geom_expr));
	new_geom->qual = qual;
	new_geom->geom = geom;
	new_geom->next = cgs->layers->geoms;
	cgs->layers->geoms = new_geom;
}

layered_geom_list: geom_expr |
	layered_geom_list LAYER geom_expr

using_clause: USING geom_expr |
	USING '(' layered_geom_list ')'

from_clause: FROM TABLE_NAME {
	char *table_name = $2;
	int print_result;
	print_result = asprintf(&(cgs->layers->source_sql_query), "select * from %s", table_name);
	if(print_result == -1) {
		sgl_error("Memory allocation failed.");
	}
	free(table_name);
} | FROM SQL_SUBQUERY {
	char *sql_subquery=$2;
	cgs->layers->source_sql_query=strdup(sql_subquery);
	free(sql_subquery);
}	

aes_mappings: aes_mapping |
	aes_mappings COMMA aes_mapping

aes_mapping: col_expr AS UNQUOTED_STRING {
	char *aes_str=$3;
	str_tolower(aes_str);
	int print_result;
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}	

	struct aes_mapping *new_mapping = malloc(sizeof(struct aes_mapping));
	new_mapping->aes=aes_enum(aes_str);
	free(aes_str);

	new_mapping->col_expr=$1;
	new_mapping->next=cgs->layers->aes_mappings;	

	cgs->layers->aes_mappings=new_mapping;
}

col_expr: UNQUOTED_STRING '(' UNQUOTED_STRING ')' {
	char *cta_str=$1;
	str_tolower(cta_str);	
	int print_result;
	if (!valid_cta_str(cta_str)) {
		print_result = asprintf(errmsg, "Invalid CTA: %s\n", cta_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}
	enum cta cta = cta_enum(cta_str);	
	free(cta_str);
	char *column_name=$3;
	
	$$.column=strdup(column_name);
	$$.cta=cta;	
	$$.arg=NULL;

	free(column_name);

} | UNQUOTED_STRING '(' UNQUOTED_STRING COMMA fn_arg ')' {
	char *cta_str=$1;
	str_tolower(cta_str);	
	int print_result;
	if (!valid_cta_str(cta_str)) {
		print_result = asprintf(errmsg, "Invalid CTA: %s\n", cta_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}
	enum cta cta = cta_enum(cta_str);	
	free(cta_str);
	char *column_name=$3;

	$$.column=strdup(column_name);
	$$.cta=cta;	
	$$.arg=$5;

	free(column_name);

}	| UNQUOTED_STRING {
	enum cta cta=IDENTITY;
	char *column_name=$1;

	$$.column=strdup(column_name);
	$$.cta=cta;	
	$$.arg=NULL;

	free(column_name);

}

fn_arg: INTEGER {
	int value=$1;

	struct fn_arg *new_arg = malloc(sizeof(struct fn_arg));

	new_arg->value=value;

	$$=new_arg;
}

grouping_clause: |
	GROUP BY grouping_list

grouping_list: grouping_expr |
	grouping_list COMMA grouping_expr

grouping_expr: col_expr {
	struct grouping_expr *new_grouping_expr = malloc(sizeof(struct grouping_expr));

	new_grouping_expr->col_expr=$1;
	new_grouping_expr->next=cgs->layers->groupings;	

	cgs->layers->groupings=new_grouping_expr;
}

collection_clause: |
	COLLECT BY collection_list

collection_list: collection_expr |
	collection_list COMMA collection_expr

collection_expr: col_expr {
	struct collection_expr *new_collection_expr = malloc(sizeof(struct collection_expr));

	new_collection_expr->col_expr=$1;
	new_collection_expr->next=cgs->layers->collections;	

	cgs->layers->collections=new_collection_expr;
}

scale_clause: SCALE BY scale_list {}
	
scale_list: scale_expr |
	scale_list COMMA scale_expr 

scale_expr: UNQUOTED_STRING '(' UNQUOTED_STRING ')' {
	char *scale_str=$1;
	str_tolower(scale_str);
	char *aes_str=$3;
	str_tolower(aes_str);
	int print_result;
	if (!valid_scale_str(scale_str)) {
		print_result = asprintf(errmsg, "Invalid scale type: %s\n", scale_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}	

	enum scale scale = scale_enum(scale_str);
	free(scale_str);
	enum aes aes = aes_enum(aes_str);
	free(aes_str);

	struct scale_expr *new_scale = malloc(sizeof(struct scale_expr));
	new_scale->aes=aes;
	new_scale->scale=scale;

	new_scale->next=cgs->scales;	
	cgs->scales=new_scale;
}

facet_clause: FACET BY facet_list {}

facet_list: facet_expr |
	facet_list COMMA facet_expr

facet_expr: UNQUOTED_STRING direction {
	char *column = $1;
	enum direction facet_direction = $2;

	struct facet_expr *new_facet = malloc(sizeof(struct facet_expr));

	new_facet->column=strdup(column);
	free(column);
	new_facet->direction=facet_direction;	

	new_facet->next=cgs->facets;
	cgs->facets=new_facet;	
}

direction: { $$ = DEFAULT_DIRECTION; } 
| HORIZONTALLY { $$ = HORIZONTAL_DIRECTION; }
| VERTICALLY { $$ = VERTICAL_DIRECTION; }

title_clause: TITLE title_list {}

title_list: title_expr |
	title_list COMMA title_expr

title_expr: UNQUOTED_STRING AS SINGLE_QUOTED_STRING {
	char *aes_str=$1;
	str_tolower(aes_str);	
	char *title_str=$3;
	int print_result;
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_error("Memory allocation failed.");
		}
		YYERROR;
	}	

	enum aes aes = aes_enum(aes_str);
	free(aes_str);

	struct title_expr *new_title = malloc(sizeof(struct title_expr));
	new_title->aes=aes;
	new_title->title=strdup(title_str);
	free(title_str);

	new_title->next=cgs->titles;	
	cgs->titles=new_title;
}

%%

void reverse_layers(struct cgs *cgs) {
	struct layer *previous_layer = NULL;
	struct layer *current_layer = cgs->layers;
	struct layer *next_layer;

	struct geom_expr *previous_geom;
	struct geom_expr *current_geom;
	struct geom_expr *next_geom;

	while(current_layer != NULL) {
		previous_geom = NULL;
		current_geom = current_layer->geoms;
		while(current_geom != NULL) {
			next_geom = current_geom->next;	
			current_geom->next = previous_geom;
			previous_geom = current_geom;
			current_geom = next_geom;	
		}	
		current_layer->geoms = previous_geom;

		next_layer = current_layer->next;	
		current_layer->next = previous_layer;
		previous_layer = current_layer;
		current_layer = next_layer;	
	}
	cgs->layers = previous_layer;
}

void sgl_to_cgs(const char *sgl_stmt, struct cgs *cgs, char **errmsg) {
	set_scanner_input(sgl_stmt);
	int parse_result = yyparse(cgs, errmsg);
	reverse_layers(cgs);
	delete_scanner_buffer();

	if (parse_result != 0) {
		reset_scanner_state();
		yyrestart(NULL);
	}
}

void yyerror(struct cgs *cgs, char **errmsg, char const *s) {
	(void)cgs;

	int print_result;
	print_result = asprintf(errmsg, "%s\n", s);
	if(print_result == -1) {
		sgl_error("Memory allocation failed.");
	}
}
