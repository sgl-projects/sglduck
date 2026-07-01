#include<stddef.h>
#include<stdlib.h>
#include"cgs.h"

void free_aes_mappings(struct aes_mapping *aes_mappings) {
        struct aes_mapping *current = aes_mappings;
        struct aes_mapping *next;
        while (current != NULL) {
                        next = current->next;
                        free(current->col_expr.column);
                        free(current->col_expr.arg);
                        free(current);
                        current = next;
        }
}

void free_geoms(struct geom_expr *geoms) {
        struct geom_expr *current_geom = geoms;
        struct geom_expr *next_geom;
        while (current_geom != NULL) {
                        next_geom = current_geom->next;
                        free(current_geom);
                        current_geom = next_geom;
        }
}

void free_groupings(struct grouping_expr *groupings) {
        struct grouping_expr *current_grouping = groupings;
        struct grouping_expr *next_grouping;
        while (current_grouping != NULL) {
                        next_grouping = current_grouping->next;
                        free(current_grouping->col_expr.column);
                        free(current_grouping->col_expr.arg);
                        free(current_grouping);
                        current_grouping = next_grouping;
        }
}

void free_collections(struct collection_expr *collections) {
        struct collection_expr *current_collection = collections;
        struct collection_expr *next_collection;
        while (current_collection != NULL) {
                        next_collection = current_collection->next;
                        free(current_collection->col_expr.column);
                        free(current_collection->col_expr.arg);
                        free(current_collection);
                        current_collection = next_collection;
        }
}

void free_layer(struct layer *layer) {
        free_aes_mappings(layer->aes_mappings);
        free(layer->source_sql_query);
        free_geoms(layer->geoms);
        free_groupings(layer->groupings);
        free_collections(layer->collections);
        free(layer);
}

void free_scales(struct scale_expr *scales) {
        struct scale_expr *current_scale_expr = scales;
        struct scale_expr *next_scale_expr;
        while (current_scale_expr != NULL) {
                next_scale_expr = current_scale_expr->next;
                free(current_scale_expr);
                current_scale_expr = next_scale_expr;
        }
}

void free_facets(struct facet_expr *facets) {
        struct facet_expr *current_facet_expr = facets;
        struct facet_expr *next_facet_expr;
        while (current_facet_expr != NULL) {
                next_facet_expr = current_facet_expr->next;
                free(current_facet_expr->column);
                free(current_facet_expr);
                current_facet_expr = next_facet_expr;
        }
}

void free_titles(struct title_expr *titles) {
        struct title_expr *current_title_expr = titles;
        struct title_expr *next_title_expr;
        while (current_title_expr != NULL) {
                next_title_expr = current_title_expr->next;
                free(current_title_expr->title);
                free(current_title_expr);
                current_title_expr = next_title_expr;
        }
}

void free_cgs(struct cgs *cgs) {
	struct layer *current_layer = cgs->layers;
	struct layer *next_layer;
	while (current_layer != NULL) {
		next_layer = current_layer->next;
		free_layer(current_layer);
		current_layer = next_layer;
	}
	if (cgs->scales != NULL) {
		free_scales(cgs->scales);
	}

	if (cgs->facets != NULL) {
		free_facets(cgs->facets);
	}

	if (cgs->titles != NULL) {
		free_titles(cgs->titles);
	}
	free(cgs);
}
