#include<stdlib.h>
#include<criterion/criterion.h>
#include<cgs.h>
#include<aes.h>
#include<geom.h>
#include<cta.h>
#include<qual.h>
#include<direction.h>
#include<sgl_to_cgs.h>

static struct cgs *cgs;
static char *errmsg;

static void setup_test_sgl_to_cgs(void) {
	cgs = malloc(sizeof(struct cgs));
	cgs->layers=NULL;
	cgs->scales=NULL;
	cgs->facets=NULL;
	cgs->titles=NULL;
	errmsg = NULL;
}

static void teardown_test_sgl_to_cgs(void) {
	struct layer *current_layer = cgs->layers;
	struct layer *next_layer;
	struct aes_mapping *current_mapping;
	struct aes_mapping *next_mapping;
	struct geom_expr *current_geom;
	struct geom_expr *next_geom;
	struct grouping_expr *current_grouping;
	struct grouping_expr *next_grouping;
	struct collection_expr *current_collection;
	struct collection_expr *next_collection;

	while(current_layer != NULL) {
		next_layer = current_layer->next;
		free(current_layer->source_sql_query);
		current_mapping = current_layer->aes_mappings;
		while(current_mapping != NULL) {
			next_mapping = current_mapping->next;
			free(current_mapping->col_expr.column);
			free(current_mapping->col_expr.arg);
			free(current_mapping);
			current_mapping = next_mapping;
		}
		current_geom = current_layer->geoms;
		while(current_geom != NULL) {
			next_geom = current_geom->next;
			free(current_geom);
			current_geom = next_geom;
		}
		current_grouping = current_layer->groupings;
		while(current_grouping != NULL) {
			next_grouping = current_grouping->next;
			free(current_grouping->col_expr.column);
			free(current_grouping->col_expr.arg);
			free(current_grouping);
			current_grouping = next_grouping;
		}
		current_collection = current_layer->collections;
		while(current_collection != NULL) {
			next_collection = current_collection->next;
			free(current_collection->col_expr.column);
			free(current_collection->col_expr.arg);
			free(current_collection);
			current_collection = next_collection;
		}

		free(current_layer);
		current_layer = next_layer;
	}

	struct scale_expr *current_scale_expr = cgs->scales;
	struct scale_expr *next_scale_expr;
	while(current_scale_expr != NULL) {
		next_scale_expr = current_scale_expr->next;
		free(current_scale_expr);
		current_scale_expr = next_scale_expr;
	}

	struct facet_expr *current_facet_expr = cgs->facets;
	struct facet_expr *next_facet_expr;
	while(current_facet_expr != NULL) {
		next_facet_expr = current_facet_expr->next;
		free(current_facet_expr->column);
		free(current_facet_expr);
		current_facet_expr = next_facet_expr;
	}

	struct title_expr *current_title_expr = cgs->titles;
	struct title_expr *next_title_expr;
	while(current_title_expr != NULL) {
		next_title_expr = current_title_expr->next;
		free(current_title_expr->title);
		free(current_title_expr);
		current_title_expr = next_title_expr;
	}

	free(cgs);
	free(errmsg);
}

TestSuite(test_sgl_to_cgs, .init = setup_test_sgl_to_cgs, .fini = teardown_test_sgl_to_cgs);

Test(test_sgl_to_cgs, adds_single_aes_mapping) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->aes_mappings->aes == X);
	cr_expect(!strcmp(cgs->layers->aes_mappings->col_expr.column, "col_1"));
	cr_expect(cgs->layers->aes_mappings->col_expr.cta == IDENTITY);
	cr_expect(cgs->layers->aes_mappings->col_expr.arg == NULL);
	cr_expect(cgs->layers->aes_mappings->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_aes_mappings) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y,\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct aes_mapping *first_mapping = cgs->layers->aes_mappings;
	struct aes_mapping *second_mapping = first_mapping->next;

	cr_expect(first_mapping->aes == Y);
	cr_expect(!strcmp(first_mapping->col_expr.column, "col_2"));
	cr_expect(first_mapping->col_expr.cta == IDENTITY);
	cr_expect(first_mapping->col_expr.arg == NULL);
	cr_expect(first_mapping->next == second_mapping);

	cr_expect(second_mapping->aes == X);
	cr_expect(!strcmp(second_mapping->col_expr.column, "col_1"));
	cr_expect(second_mapping->col_expr.cta == IDENTITY);
	cr_expect(second_mapping->col_expr.arg == NULL);
	cr_expect(second_mapping->next == NULL);
}

Test(test_sgl_to_cgs, adds_column_transformation) {
	char *test_stmt = "visualize\n"
										"	bin(col_1) as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->aes_mappings->aes == X);
	cr_expect(!strcmp(cgs->layers->aes_mappings->col_expr.column, "col_1"));
	cr_expect(cgs->layers->aes_mappings->col_expr.cta == BIN);
	cr_expect(cgs->layers->aes_mappings->col_expr.arg == NULL);
	cr_expect(cgs->layers->aes_mappings->next == NULL);
}

Test(test_sgl_to_cgs, adds_aes_mapping_with_function_arg) {
	char *test_stmt = "visualize\n"
										"	bin(col_1, 5) as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->aes_mappings->aes == X);
	cr_expect(!strcmp(cgs->layers->aes_mappings->col_expr.column, "col_1"));
	cr_expect(cgs->layers->aes_mappings->col_expr.cta == BIN);
	cr_expect(cgs->layers->aes_mappings->col_expr.arg->value == 5);
	cr_expect(cgs->layers->aes_mappings->next == NULL);
}

Test(test_sgl_to_cgs, adds_source_sql_query_for_table_name) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_query = "select * from table_1";
	cr_expect(!strcmp(cgs->layers->source_sql_query, expected_query));
}

Test(test_sgl_to_cgs, adds_source_sql_query_for_subquery) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from (\n"
										"	select *\n"
										"	from table_1\n"
										"	where col_2='a'\n"
										")\n"
										"using points\n";

	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_query =	"\n"
													"	select *\n"
													"	from table_1\n"
													"	where col_2='a'\n";
	cr_expect(!strcmp(cgs->layers->source_sql_query, expected_query));
}

Test(test_sgl_to_cgs, adds_geom) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->geoms->geom == POINT);
	cr_expect(cgs->layers->geoms->qual == DEFAULT);
	cr_expect(cgs->layers->geoms->next == NULL);
}

Test(test_sgl_to_cgs, adds_geom_with_qualifier) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using regression line\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->geoms->geom == LINE);
	cr_expect(cgs->layers->geoms->qual == REGRESSION);
	cr_expect(cgs->layers->geoms->next == NULL);
}


Test(test_sgl_to_cgs, doesnt_add_grouping_if_group_by_clause_omitted) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->groupings == NULL);
}

Test(test_sgl_to_cgs, adds_grouping_for_single_column) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										" count(*) as y\n"
										"from table_1\n"
										"group by\n"
										"	col_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct grouping_expr grouping_expr = *(cgs->layers->groupings);
	cr_expect(!strcmp(grouping_expr.col_expr.column, "col_1"));
	cr_expect(grouping_expr.col_expr.cta == IDENTITY);
	cr_expect(grouping_expr.col_expr.arg == NULL);
	cr_expect(grouping_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_grouping_for_single_transformed_column) {
	char *test_stmt = "visualize\n"
										"	bin(col_1) as x,\n"
										" count(*) as y\n"
										"from table_1\n"
										"group by\n"
										"	bin(col_1)\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct grouping_expr grouping_expr = *(cgs->layers->groupings);
	cr_expect(!strcmp(grouping_expr.col_expr.column, "col_1"));
	cr_expect(grouping_expr.col_expr.cta == BIN);
	cr_expect(grouping_expr.col_expr.arg == NULL);
	cr_expect(grouping_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_grouping_with_function_arg) {
	char *test_stmt = "visualize\n"
										"	bin(col_1, 5) as x,\n"
										" count(*) as y\n"
										"from table_1\n"
										"group by\n"
										"	bin(col_1, 5)\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct grouping_expr grouping_expr = *(cgs->layers->groupings);
	cr_expect(!strcmp(grouping_expr.col_expr.column, "col_1"));
	cr_expect(grouping_expr.col_expr.cta == BIN);
	cr_expect(grouping_expr.col_expr.arg->value == 5);
	cr_expect(grouping_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_groupings_for_multiple_grouping_expressions) {
	char *test_stmt = "visualize\n"
										"	bin(col_1) as x,\n"
										" count(*) as y,\n"
										"	col_2 as color\n"
										"from table_1\n"
										"group by\n"
										"	bin(col_1),\n"
										"	col_2\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct grouping_expr second_grouping_expr = *(cgs->layers->groupings);
	struct grouping_expr first_grouping_expr = *(second_grouping_expr.next);
	cr_expect(!strcmp(first_grouping_expr.col_expr.column, "col_1"));
	cr_expect(first_grouping_expr.col_expr.cta == BIN);
	cr_expect(first_grouping_expr.col_expr.arg == NULL);
	cr_expect(first_grouping_expr.next == NULL);
	cr_expect(!strcmp(second_grouping_expr.col_expr.column, "col_2"));
	cr_expect(second_grouping_expr.col_expr.cta == IDENTITY);
	cr_expect(second_grouping_expr.col_expr.arg == NULL);
}

Test(test_sgl_to_cgs, doesnt_add_collection_if_collect_by_clause_omitted) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->collections == NULL);
}

Test(test_sgl_to_cgs, adds_collection_for_single_column) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"collect by\n"
										"	col_3\n"
										"using lines\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct collection_expr collection_expr = *(cgs->layers->collections);
	cr_expect(!strcmp(collection_expr.col_expr.column, "col_3"));
	cr_expect(collection_expr.col_expr.cta == IDENTITY);
	cr_expect(collection_expr.col_expr.arg == NULL);
	cr_expect(collection_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_collection_for_single_transformed_column) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										" col_2 as y\n"
										"from table_1\n"
										"collect by\n"
										"	bin(col_3)\n"
										"using lines\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct collection_expr collection_expr = *(cgs->layers->collections);
	cr_expect(!strcmp(collection_expr.col_expr.column, "col_3"));
	cr_expect(collection_expr.col_expr.cta == BIN);
	cr_expect(collection_expr.col_expr.arg == NULL);
	cr_expect(collection_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_collection_with_function_arg) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										" col_2 as y\n"
										"from table_1\n"
										"collect by\n"
										"	bin(col_3, 5)\n"
										"using lines\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct collection_expr collection_expr = *(cgs->layers->collections);
	cr_expect(!strcmp(collection_expr.col_expr.column, "col_3"));
	cr_expect(collection_expr.col_expr.cta == BIN);
	cr_expect(collection_expr.col_expr.arg->value == 5);
	cr_expect(collection_expr.next == NULL);
}

Test(test_sgl_to_cgs, adds_collections_for_multiple_collection_expressions) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										" col_2 as y\n"
										"from table_1\n"
										"collect by\n"
										"	bin(col_3),\n"
										"	col_4\n"
										"using lines\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct collection_expr second_collection_expr = *(cgs->layers->collections);
	struct collection_expr first_collection_expr = *(second_collection_expr.next);
	cr_expect(!strcmp(first_collection_expr.col_expr.column, "col_3"));
	cr_expect(first_collection_expr.col_expr.cta == BIN);
	cr_expect(first_collection_expr.col_expr.arg == NULL);
	cr_expect(first_collection_expr.next == NULL);
	cr_expect(!strcmp(second_collection_expr.col_expr.column, "col_4"));
	cr_expect(second_collection_expr.col_expr.cta == IDENTITY);
	cr_expect(second_collection_expr.col_expr.arg == NULL);
}

Test(test_sgl_to_cgs, adds_one_layer_for_single_layer) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->layers->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_layers) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"group by\n"
										"	col_1\n"
										"using points\n"
										"\n"
										"layer"
										"\n"
										"visualize\n"
										"	col_2 as y\n"
										"from table_2\n"
										"collect by\n"
										"	col_2\n"
										"using line\n";
						
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct layer *first_layer = cgs->layers;
	struct layer *second_layer = first_layer->next;
	cr_expect(first_layer->aes_mappings->aes == X);
	cr_expect(!strcmp(first_layer->aes_mappings->col_expr.column, "col_1"));
	cr_expect(!strcmp(first_layer->source_sql_query, "select * from table_1"));
	cr_expect(first_layer->geoms->geom == POINT);
	cr_expect(!strcmp(first_layer->groupings->col_expr.column, "col_1"));
	cr_expect(first_layer->collections == NULL);
	cr_expect(second_layer->aes_mappings->aes == Y);
	cr_expect(!strcmp(second_layer->aes_mappings->col_expr.column, "col_2"));
	cr_expect(!strcmp(second_layer->source_sql_query, "select * from table_2"));
	cr_expect(second_layer->geoms->geom == LINE);
	cr_expect(second_layer->groupings == NULL);
	cr_expect(!strcmp(second_layer->collections->col_expr.column, "col_2"));
	cr_expect(second_layer->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_geoms_for_layered_geom_exprs) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using (\n"
											"points\n"
											"layer\n"
											"regression line\n"
										")\n";
						
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct geom_expr first_geom = *(cgs->layers->geoms);
	struct geom_expr second_geom = *(first_geom.next);
	cr_expect(first_geom.geom == POINT);
	cr_expect(first_geom.qual == DEFAULT);
	cr_expect(second_geom.geom == LINE);
	cr_expect(second_geom.qual == REGRESSION);
	cr_expect(second_geom.next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_layers_and_geoms_for_layered_geom_exprs_and_top_level_layer) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using (\n"
											"points\n"
											"layer\n"
											"regression line\n"
										")\n"
										"\n"
										"layer\n"
										"\n"
										"visualize\n"
										"	col_2 as x\n"
										"from table_2\n"
										"using bars\n";
						
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct layer first_layer = *(cgs->layers);
	struct layer second_layer = *(first_layer.next);
	struct geom_expr first_layers_first_geom = *(first_layer.geoms);
	struct geom_expr first_layers_second_geom = *(first_layers_first_geom.next);
	struct geom_expr second_layers_geom = *(second_layer.geoms);

	cr_expect(first_layers_first_geom.geom == POINT);
	cr_expect(first_layers_first_geom.qual == DEFAULT);
	cr_expect(first_layers_second_geom.geom == LINE);
	cr_expect(first_layers_second_geom.qual == REGRESSION);
	cr_expect(first_layers_second_geom.next == NULL);
	cr_expect(second_layers_geom.geom == BAR);
	cr_expect(second_layers_geom.qual == DEFAULT);
	cr_expect(second_layers_geom.next == NULL);
}

Test(test_sgl_to_cgs, doesnt_add_scale_if_none_provided) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->scales== NULL);
}

Test(test_sgl_to_cgs, adds_single_scale) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"scale by\n"
										"	log(x)\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->scales->aes == X);
	cr_expect(cgs->scales->scale == LOG);
	cr_expect(cgs->scales->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_scales) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"scale by\n"
										"	linear(x),\n"
										"	log(y)\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct scale_expr *second_scale = cgs->scales;
	struct scale_expr *first_scale = second_scale->next;
	cr_expect(first_scale->aes == X);
	cr_expect(first_scale->scale == LINEAR);
	cr_expect(first_scale->next == NULL);
	cr_expect(second_scale->aes == Y);
	cr_expect(second_scale->scale == LOG);
}

Test(test_sgl_to_cgs, adds_scale_for_multiple_layers) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"\n"
										"layer\n"
										"\n"
										"visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using regression line\n"
										"\n"
										"scale by\n"
										"	log(x)\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->scales->aes == X);
	cr_expect(cgs->scales->scale == LOG);
	cr_expect(cgs->scales->next == NULL);
}

Test(test_sgl_to_cgs, doesnt_add_facet_if_none_provided) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->facets == NULL);
}

Test(test_sgl_to_cgs, adds_facet_with_default_direction) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"facet by\n"
										"	col_3\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *facet = cgs->facets;
	cr_expect(!strcmp(facet->column, "col_3"));
	cr_expect(facet->direction == DEFAULT_DIRECTION);
	cr_expect(facet->next == NULL);
}

Test(test_sgl_to_cgs, adds_facet_with_horizontal_direction) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"facet by\n"
										"	col_3 horizontally\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *facet = cgs->facets;
	cr_expect(!strcmp(facet->column, "col_3"));
	cr_expect(facet->direction == HORIZONTAL_DIRECTION);
	cr_expect(facet->next == NULL);
}

Test(test_sgl_to_cgs, adds_facet_with_vertical_direction) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"facet by\n"
										"	col_3 vertically\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *facet = cgs->facets;
	cr_expect(!strcmp(facet->column, "col_3"));
	cr_expect(facet->direction == VERTICAL_DIRECTION);
	cr_expect(facet->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_facets_correctly) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"facet by\n"
										"	col_3,\n"
										"	col_4 horizontally,\n"
										"	col_5 vertically\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *third_facet = cgs->facets;
	struct facet_expr *second_facet = third_facet->next;
	struct facet_expr *first_facet = second_facet->next;

	cr_expect(!strcmp(first_facet->column, "col_3"));
	cr_expect(first_facet->direction == DEFAULT_DIRECTION);
	cr_expect(first_facet->next == NULL);
	cr_expect(!strcmp(second_facet->column, "col_4"));
	cr_expect(second_facet->direction == HORIZONTAL_DIRECTION);
	cr_expect(!strcmp(third_facet->column, "col_5"));
	cr_expect(third_facet->direction == VERTICAL_DIRECTION);
}

Test(test_sgl_to_cgs, adds_facet_with_multiple_layers) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"\n"
										"layer\n"
										"\n"
										"visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using regression line\n"
										"\n"	
										"facet by\n"
										"	col_3 horizontally\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *facet = cgs->facets;
	cr_expect(!strcmp(facet->column, "col_3"));
	cr_expect(facet->direction == HORIZONTAL_DIRECTION);
	cr_expect(facet->next == NULL);
}

Test(test_sgl_to_cgs, doesnt_add_title_if_none_provided) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(cgs->titles == NULL);
}

Test(test_sgl_to_cgs, adds_title) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	x as 'Column 1'\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct title_expr *title = cgs->titles;
	cr_expect(!strcmp(title->title, "Column 1"));
	cr_expect(title->aes == X);
	cr_expect(title->next == NULL);
}

Test(test_sgl_to_cgs, adds_empty_string_as_title) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	x as ''\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct title_expr *title = cgs->titles;
	cr_expect(!strcmp(title->title, ""));
	cr_expect(title->aes == X);
	cr_expect(title->next == NULL);
}

Test(test_sgl_to_cgs, allows_escaped_single_quote_in_title) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	x as 'X\\'s Title'\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct title_expr *title = cgs->titles;
	cr_expect(!strcmp(title->title, "X's Title"));
	cr_expect(title->aes == X);
	cr_expect(title->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_titles) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	x as 'Column 1',\n"
										"	y as 'Column 2'\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct title_expr *second_title = cgs->titles;
	struct title_expr *first_title = second_title->next;
	cr_expect(!strcmp(first_title->title, "Column 1"));
	cr_expect(first_title->aes == X);
	cr_expect(first_title->next == NULL);
	cr_expect(!strcmp(second_title->title, "Column 2"));
	cr_expect(second_title->aes == Y);
}

Test(test_sgl_to_cgs, adds_title_with_multiple_layers) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"\n"
										"layer\n"
										"\n"
										"visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using regression line\n"
										"\n"
										"title\n"
										"	x as 'Column 1'\n";
											
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct title_expr *title = cgs->titles;
	cr_expect(!strcmp(title->title, "Column 1"));
	cr_expect(title->aes == X);
	cr_expect(title->next == NULL);
}

Test(test_sgl_to_cgs, adds_multiple_graphics_clauses) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"using points\n"
										"facet by\n"
										"	col_3\n"
										"scale by\n"
										"	log(x)\n"
										"title\n"
										"	x as 'Column 1'\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	struct facet_expr *facet = cgs->facets;
	cr_expect(!strcmp(facet->column, "col_3"));
	cr_expect(facet->direction == DEFAULT_DIRECTION);
	cr_expect(facet->next == NULL);
	struct scale_expr *scale = cgs->scales;
	cr_expect(scale->aes == X);
	cr_expect(scale->scale == LOG);
	cr_expect(scale->next == NULL);
	struct title_expr *title = cgs->titles;
	cr_expect(!strcmp(title->title, "Column 1"));
	cr_expect(title->aes == X);
	cr_expect(title->next == NULL);
}

Test(test_sgl_to_cgs, doesnt_set_errmsg_for_valid_stmt) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(errmsg == NULL);
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_aes) {
	char *test_stmt = "visualize\n"
										"	col_1 as notanaes\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid aesthetic name: notanaes\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_geom) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using notageom\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid geom name: notageom\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_qual) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using notaqual points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid geom qualifier: notaqual\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_geom_in_layered_geom_exprs) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using (\n"
										"	notageom\n"
										"	layer\n"
										"	points\n"
										")\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid geom name: notageom\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_qual_in_layered_geom_exprs) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using (\n"
										"	notaqual points\n"
										"	layer\n"
										"	line\n"
										")\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid geom qualifier: notaqual\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_cta) {
	char *test_stmt = "visualize\n"
										"	not_a_cta(col_1) as x\n"
										"from table_1\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid CTA: not_a_cta\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_cta_in_grouping_expression) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"group by\n"
										"	not_a_cta(col_1)\n"
										"using points\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid CTA: not_a_cta\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_cta_in_collection_expression) {
	char *test_stmt = "visualize\n"
										"	col_1 as x,\n"
										"	col_2 as y\n"
										"from table_1\n"
										"collect by\n"
										"	not_a_cta(col_3)\n"
										"using lines\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid CTA: not_a_cta\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_scale_type) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n"
										"scale by\n"
										"	not_a_scale(x)\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid scale type: not_a_scale\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_scale_aes) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n"
										"scale by\n"
										"	log(notanaes)\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid aesthetic name: notanaes\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_invalid_title_aes) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	notanaes as 'Column 1'\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "Invalid aesthetic name: notanaes\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_unquoted_title) {
	char *test_stmt = "visualize\n"
										"	col_1 as x\n"
										"from table_1\n"
										"using points\n"
										"title\n"
										"	x as Column1\n";

	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "syntax error\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, sets_errmsg_for_general_syntax_error) {
	char *test_stmt = "visualize\n"
										"from geom\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	char *expected_msg = "syntax error\n";
	cr_expect(!strcmp(errmsg, expected_msg));
}

Test(test_sgl_to_cgs, non_identifiers_are_case_insensitive) {
	char *test_stmt = "visUaLize\n"
										"	bIn(mpg) aS X,\n"
										"	COunT(*) As y\n"
										"FroM table_1\n"
										"gROuP bY\n"
										"	BIn(mpg)\n"
										"coLLect By\n"
										"	cyl\n"
										"usinG (\n"
										"	PoiNtS\n"
										"	laYEr\n"
										"	rEgrESsiON lINe\n"
										")\n"
										"fACeT By\n"
										"	cyl veRTICALlY\n"
										"ScaLe bY\n"
										"	LoG(x)\n"
										"TitlE\n"
										"	X As 'Binned mpg'\n";
	
	sgl_to_cgs(test_stmt, cgs, &errmsg);

	cr_expect(errmsg == NULL);
}

