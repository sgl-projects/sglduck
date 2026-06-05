#ifndef CGS_H
#define CGS_H

#include"aes.h"
#include"geom.h"
#include"cta.h"
#include"qual.h"
#include"scale.h"
#include"direction.h"

struct geom_expr {
	enum geom geom;
	enum qual qual;
	struct geom_expr *next;
};

struct fn_arg {
	int value;
};

struct col_expr {
	char *column;
	enum cta cta;
	struct fn_arg *arg;
};

struct aes_mapping {
	enum aes aes;
	struct col_expr col_expr;
	struct aes_mapping *next;
};

struct grouping_expr {
	struct col_expr col_expr;
	struct grouping_expr *next;
};

struct collection_expr {
	struct col_expr col_expr;
	struct collection_expr *next;
};

struct layer {
	struct geom_expr *geoms;
	char *source_sql_query;
	struct aes_mapping *aes_mappings;
	struct grouping_expr *groupings;
	struct collection_expr *collections;
	struct layer *next;
};

struct scale_expr {
	enum aes aes;
	enum scale scale;
	struct scale_expr *next;
};

struct facet_expr {
	char *column;
	enum direction direction;
	struct facet_expr *next;
};

struct title_expr {
	enum aes aes;
	char *title;
	struct title_expr *next;
};

struct cgs {
	struct layer *layers;
	struct scale_expr *scales;
	struct facet_expr *facets;
	struct title_expr *titles;
};

#endif
