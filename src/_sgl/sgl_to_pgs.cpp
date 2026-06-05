#include <pybind11/pybind11.h>
#include <stdexcept>
#include <string>

extern "C" {
#include "sgl_to_cgs.h"
#include "cgs.h"
#include "aes.h"
#include "geom.h"
#include "cta.h"
#include "qual.h"
#include "scale.h"
#include "direction.h"
}

namespace py = pybind11;

/*
 * pybind11 bridge — the Python analog of rsgl's Rcpp bridge (sgl_to_rgs.cpp).
 *
 * It calls the reused C parser (sgl_to_cgs) and walks the resulting cgs linked
 * lists in the same order as the Rcpp bridge, emitting plain Python containers
 * (the "pgs" structure) instead of an Rcpp::List. Class variants are carried as
 * string tags under a "class" key (e.g. {"class": "sgl_geom_point"}), exactly
 * where the Rcpp bridge set the S3 class attribute; pgs.py reconstructs typed
 * objects from those tags. Like the Rcpp bridge, it emits one pgs layer per
 * geom_expr (a layer with N geoms expands to N pgs layers sharing source/aes),
 * and it frees the C structs in the same order.
 */

static std::string aes_name(enum aes a) {
	switch (a) {
		case X: return "x";
		case Y: return "y";
		case RADIUS: return "r";
		case THETA: return "theta";
		case COLOR: return "color";
		case SIZE: return "size";
		default: return "unknown";
	}
}

static std::string cta_class(enum cta c) {
	switch (c) {
		case IDENTITY: return "sgl_cta_identity";
		case AVG: return "sgl_cta_avg";
		case BIN: return "sgl_cta_bin";
		case COUNT: return "sgl_cta_count";
		default: return "sgl_cta";
	}
}

static std::string geom_class(enum geom g) {
	switch (g) {
		case POINT: return "sgl_geom_point";
		case BAR: return "sgl_geom_bar";
		case LINE: return "sgl_geom_line";
		case BOX: return "sgl_geom_box";
		default: return "sgl_geom";
	}
}

static std::string scale_class(enum scale s) {
	switch (s) {
		case LINEAR: return "sgl_scale_linear";
		case LN: return "sgl_scale_ln";
		case LOG: return "sgl_scale_log";
		default: return "sgl_scale";
	}
}

static std::string qual_str(enum qual q) {
	switch (q) {
		case HORIZONTAL: return "horizontal";
		case JITTERED: return "jittered";
		case REGRESSION: return "regression";
		case UNSTACKED: return "unstacked";
		case VERTICAL: return "vertical";
		case DEFAULT: return "default";
		default: return "unknown";
	}
}

static std::string direction_str(enum direction d) {
	switch (d) {
		case DEFAULT_DIRECTION: return "default";
		case HORIZONTAL_DIRECTION: return "horizontal";
		case VERTICAL_DIRECTION: return "vertical";
		default: return "unknown";
	}
}

// Build a col_expr dict: {"column": str, "cta": {"class": str}, ["arg": int]}.
static py::dict build_col_expr(const struct col_expr &ce) {
	py::dict d;
	d["column"] = std::string(ce.column);
	py::dict cta_obj;
	cta_obj["class"] = cta_class(ce.cta);
	d["cta"] = cta_obj;
	if (ce.arg != NULL) {
		d["arg"] = ce.arg->value;
	}
	return d;
}

static py::dict sgl_to_pgs(const std::string &sgl_stmt) {
	struct cgs cgs;
	cgs.layers = NULL;
	cgs.scales = NULL;
	cgs.facets = NULL;
	cgs.titles = NULL;
	char *errmsg = NULL;

	// Call the reused C parser.
	sgl_to_cgs(sgl_stmt.c_str(), &cgs, &errmsg);

	// Check for errors (parser/scanner messages, matching rsgl's Rcpp::stop).
	if (errmsg != NULL) {
		std::string error_message(errmsg);
		free(errmsg);
		throw std::runtime_error(error_message);
	}

	py::dict result;
	py::list layers;

	struct layer *current_layer = cgs.layers;
	while (current_layer != NULL) {
		struct layer *next_layer = current_layer->next;
		py::dict layer;

		// Source SQL query.
		if (current_layer->source_sql_query != NULL) {
			layer["source_sql_query"] = std::string(current_layer->source_sql_query);
		} else {
			layer["source_sql_query"] = py::none();
		}

		// Aesthetic mappings, keyed by aes name.
		py::dict aes_list;
		struct aes_mapping *current = current_layer->aes_mappings;
		while (current != NULL) {
			aes_list[py::str(aes_name(current->aes))] = build_col_expr(current->col_expr);
			current = current->next;
		}
		layer["aes_mappings"] = aes_list;

		// Groupings (only when present).
		if (current_layer->groupings != NULL) {
			py::list grouping_list;
			struct grouping_expr *current_grouping = current_layer->groupings;
			while (current_grouping != NULL) {
				grouping_list.append(build_col_expr(current_grouping->col_expr));
				current_grouping = current_grouping->next;
			}
			layer["groupings"] = grouping_list;
		}

		// Collections (only when present).
		if (current_layer->collections != NULL) {
			py::list collection_list;
			struct collection_expr *current_collection = current_layer->collections;
			while (current_collection != NULL) {
				collection_list.append(build_col_expr(current_collection->col_expr));
				current_collection = current_collection->next;
			}
			layer["collections"] = collection_list;
		}

		// Geom exprs: build the list, then emit one layer per geom_expr.
		py::list geom_list;
		struct geom_expr *current_geom_expr = current_layer->geoms;
		while (current_geom_expr != NULL) {
			py::dict geom_obj;
			geom_obj["class"] = geom_class(current_geom_expr->geom);

			py::dict geom_expr;
			geom_expr["qual"] = qual_str(current_geom_expr->qual);
			geom_expr["geom"] = geom_obj;
			geom_list.append(geom_expr);
			current_geom_expr = current_geom_expr->next;
		}

		for (auto geom_expr : geom_list) {
			py::dict layer_copy = py::reinterpret_steal<py::dict>(PyDict_Copy(layer.ptr()));
			layer_copy["geom_expr"] = geom_expr;
			layers.append(layer_copy);
		}

		// Free this layer's allocations, matching the Rcpp bridge.
		if (current_layer->source_sql_query != NULL) {
			free(current_layer->source_sql_query);
		}

		current = current_layer->aes_mappings;
		while (current != NULL) {
			struct aes_mapping *next = current->next;
			free(current->col_expr.column);
			free(current->col_expr.arg);
			free(current);
			current = next;
		}

		struct geom_expr *current_geom = current_layer->geoms;
		while (current_geom != NULL) {
			struct geom_expr *next_geom = current_geom->next;
			free(current_geom);
			current_geom = next_geom;
		}

		struct grouping_expr *current_grouping = current_layer->groupings;
		while (current_grouping != NULL) {
			struct grouping_expr *next_grouping = current_grouping->next;
			free(current_grouping->col_expr.column);
			free(current_grouping->col_expr.arg);
			free(current_grouping);
			current_grouping = next_grouping;
		}

		struct collection_expr *current_collection = current_layer->collections;
		while (current_collection != NULL) {
			struct collection_expr *next_collection = current_collection->next;
			free(current_collection->col_expr.column);
			free(current_collection->col_expr.arg);
			free(current_collection);
			current_collection = next_collection;
		}

		free(current_layer);
		current_layer = next_layer;
	}

	result["layers"] = layers;

	// Scales (only when present), keyed by aes name.
	if (cgs.scales != NULL) {
		py::dict scale_list;
		struct scale_expr *current_scale_expr = cgs.scales;
		while (current_scale_expr != NULL) {
			struct scale_expr *next_scale_expr = current_scale_expr->next;

			py::dict scale_obj;
			scale_obj["class"] = scale_class(current_scale_expr->scale);
			scale_list[py::str(aes_name(current_scale_expr->aes))] = scale_obj;

			free(current_scale_expr);
			current_scale_expr = next_scale_expr;
		}
		result["scales"] = scale_list;
	}

	// Facets (only when present).
	if (cgs.facets != NULL) {
		py::list facet_list;
		struct facet_expr *current_facet_expr = cgs.facets;
		while (current_facet_expr != NULL) {
			struct facet_expr *next_facet_expr = current_facet_expr->next;

			py::dict facet_entry;
			facet_entry["column"] = std::string(current_facet_expr->column);
			facet_entry["direction"] = direction_str(current_facet_expr->direction);
			facet_list.append(facet_entry);

			free(current_facet_expr->column);
			free(current_facet_expr);
			current_facet_expr = next_facet_expr;
		}
		result["facets"] = facet_list;
	}

	// Titles (only when present), keyed by aes name.
	if (cgs.titles != NULL) {
		py::dict title_list;
		struct title_expr *current_title_expr = cgs.titles;
		while (current_title_expr != NULL) {
			struct title_expr *next_title_expr = current_title_expr->next;

			title_list[py::str(aes_name(current_title_expr->aes))] =
				std::string(current_title_expr->title);

			free(current_title_expr->title);
			free(current_title_expr);
			current_title_expr = next_title_expr;
		}
		result["titles"] = title_list;
	}

	return result;
}

PYBIND11_MODULE(_sgl, m) {
	m.doc() = "Compiled SGL parser bridge: SGL statement -> pgs structure.";
	m.def("sgl_to_pgs", &sgl_to_pgs, py::arg("sgl_stmt"),
	      "Parse a SGL statement and return its pgs (Python grammar structure).");
}
