#include <pybind11/pybind11.h>
#include <stdexcept>
#include <string>

extern "C" {
#include "sgl_to_cgs.h"
#include "cgs.h"
#include "aes.h"
#include "geom.h"
#include "qual.h"
#include "scale.h"
#include "direction.h"
#include "cgs_free.h"
}

namespace py = pybind11;

// Mirrors rsgl's sgl_to_rgs.cpp. Where rsgl sets R class attributes
// (e.g. c("sgl_geom_point", "sgl_geom")), we carry the variant as a string
// tag under a "class" key; pgs.py reconstructs typed objects from those tags.

std::string pgs_aes_str(enum aes c_aes_enum) {
	switch(c_aes_enum) {
		case X:
				return "x";
		case Y:
				return "y";
		case RADIUS:
				return "r";
		case THETA:
				return "theta";
		case COLOR:
				return "color";
		case SIZE:
				return "size";
	}
	throw std::runtime_error("unexpected aes");
}

py::dict pgs_col_expr(struct col_expr c_col_expr) {
	std::string pgs_cta_class;
	switch(c_col_expr.cta) {
		case IDENTITY:
			pgs_cta_class = "sgl_cta_identity";
			break;
		case AVG:
			pgs_cta_class = "sgl_cta_avg";
			break;
		case BIN:
			pgs_cta_class = "sgl_cta_bin";
			break;
		case COUNT:
			pgs_cta_class = "sgl_cta_count";
			break;
	}
	py::dict pgs_cta_obj;
	pgs_cta_obj["class"] = pgs_cta_class;

	py::dict result;
	result["column"] = std::string(c_col_expr.column);
	result["cta"] = pgs_cta_obj;
	if (c_col_expr.arg != NULL) {
		result["arg"] = c_col_expr.arg->value;
	}
	return result;
}

py::dict pgs_aes_mappings(struct aes_mapping *c_aes_mappings) {
	struct aes_mapping *current = c_aes_mappings;
	py::dict result;
	std::string aes_name;
	while (current != NULL) {
		aes_name = pgs_aes_str(current->aes);
		result[py::str(aes_name)] = pgs_col_expr(current->col_expr);
		current = current->next;
	}
	return result;
}

py::list pgs_groupings(struct grouping_expr *c_groupings) {
	struct grouping_expr *current = c_groupings;
	py::list result;
	while (current != NULL) {
		result.append(
			pgs_col_expr(current->col_expr)
		);
		current = current->next;
	}
	return result;
}

py::list pgs_collections(struct collection_expr *c_collections) {
	struct collection_expr *current = c_collections;
	py::list result;
	while (current != NULL) {
		result.append(
			pgs_col_expr(current->col_expr)
		);
		current = current->next;
	}
	return result;
}

py::dict pgs_geom_expr(struct geom_expr *c_geom_expr) {
	std::string pgs_geom_class;
	switch(c_geom_expr->geom) {
		case POINT:
			pgs_geom_class = "sgl_geom_point";
			break;
		case BAR:
			pgs_geom_class = "sgl_geom_bar";
			break;
		case LINE:
			pgs_geom_class = "sgl_geom_line";
			break;
		case BOX:
			pgs_geom_class = "sgl_geom_box";
			break;
	}
	py::dict pgs_geom_obj;
	pgs_geom_obj["class"] = pgs_geom_class;

	std::string pgs_qual_str;
	switch(c_geom_expr->qual) {
		case HORIZONTAL:
			pgs_qual_str = "horizontal";
			break;
		case JITTERED:
			pgs_qual_str = "jittered";
			break;
		case REGRESSION:
			pgs_qual_str = "regression";
			break;
		case UNSTACKED:
			pgs_qual_str = "unstacked";
			break;
		case VERTICAL:
			pgs_qual_str = "vertical";
			break;
		case DEFAULT:
			pgs_qual_str = "default";
			break;
	}

	py::dict result;
	result["geom"] = pgs_geom_obj;
	result["qual"] = pgs_qual_str;
	return result;
}

py::dict pgs_layer(struct layer *c_layer, struct geom_expr *c_geom_expr) {
	py::dict result;
	result["aes_mappings"] = pgs_aes_mappings(c_layer->aes_mappings);
	result["source_sql_query"] = std::string(c_layer->source_sql_query);
	result["geom_expr"] = pgs_geom_expr(c_geom_expr);
	if (c_layer->groupings != NULL) {
		result["groupings"] = pgs_groupings(c_layer->groupings);
	}
	if(c_layer->collections != NULL) {
		result["collections"] = pgs_collections(c_layer->collections);
	}
	return result;
}

py::dict pgs_scales(struct scale_expr *c_scales) {
	struct scale_expr *current_scale_expr = c_scales;
	std::string pgs_scale_class;
	std::string pgs_aes;
	py::dict result;
	while (current_scale_expr != NULL) {
		py::dict pgs_scale_obj;
		switch(current_scale_expr->scale) {
			case LINEAR:
				pgs_scale_class = "sgl_scale_linear";
				break;
			case LN:
				pgs_scale_class = "sgl_scale_ln";
				break;
			case LOG:
				pgs_scale_class = "sgl_scale_log";
				break;
		}
		pgs_scale_obj["class"] = pgs_scale_class;
		pgs_aes = pgs_aes_str(current_scale_expr->aes);

		result[py::str(pgs_aes)] = pgs_scale_obj;

		current_scale_expr = current_scale_expr->next;
	}
	return result;
}

py::list pgs_facets(struct facet_expr *c_facets) {
	std::string column_name;
	std::string pgs_facet_direction;
	py::list result;
	struct facet_expr *current_facet_expr = c_facets;
	while (current_facet_expr != NULL) {
		py::dict facet_entry;
		switch(current_facet_expr->direction) {
			case DEFAULT_DIRECTION:
				pgs_facet_direction = "default";
				break;
			case HORIZONTAL_DIRECTION:
				pgs_facet_direction = "horizontal";
				break;
			case VERTICAL_DIRECTION:
				pgs_facet_direction = "vertical";
				break;
		}
		facet_entry["direction"] = pgs_facet_direction;
		facet_entry["column"] = std::string(current_facet_expr->column);

		result.append(facet_entry);

		current_facet_expr = current_facet_expr->next;
	}
	return result;
}

py::dict pgs_titles(struct title_expr *c_titles) {
	std::string pgs_aes;
	py::dict result;
	struct title_expr *current_title_expr = c_titles;
	while (current_title_expr != NULL) {
		pgs_aes = pgs_aes_str(current_title_expr->aes);
		result[py::str(pgs_aes)] = std::string(current_title_expr->title);

		current_title_expr = current_title_expr->next;
	}
	return result;
}

py::dict sgl_to_pgs(std::string sgl_stmt) {
	struct cgs *cgs = (struct cgs *)malloc(sizeof(struct cgs));
	char *errmsg = NULL;

	sgl_to_cgs(sgl_stmt.c_str(), cgs, &errmsg);

	if (errmsg != NULL) {
		std::string error_message(errmsg);
		free(errmsg);
		free_cgs(cgs);
		throw std::runtime_error(error_message);
	}

	py::dict result;
	py::list layers;

	struct layer *current_layer = cgs->layers;
	struct geom_expr *current_geom_expr;
	while(current_layer != NULL) {
		current_geom_expr = current_layer->geoms;
		while(current_geom_expr != NULL) {
			layers.append(pgs_layer(current_layer, current_geom_expr));
			current_geom_expr = current_geom_expr->next;
		}
		current_layer = current_layer->next;
	}

	result["layers"] = layers;

	if (cgs->scales != NULL) {
		result["scales"] = pgs_scales(cgs->scales);
	}

	if (cgs->facets != NULL) {
		result["facets"] = pgs_facets(cgs->facets);
	}

	if (cgs->titles != NULL) {
		result["titles"] = pgs_titles(cgs->titles);
	}

	free_cgs(cgs);

	return result;
}

PYBIND11_MODULE(_sgl, m) {
	m.doc() = "Compiled SGL parser bridge: SGL statement -> pgs structure.";
	m.def("sgl_to_pgs", &sgl_to_pgs, py::arg("sgl_stmt"),
	      "Parse a SGL statement and return its pgs (Python grammar structure).");
}
