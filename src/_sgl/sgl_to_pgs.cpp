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
}

namespace py = pybind11;

// Mirrors rsgl's sgl_to_rgs.cpp. Where rsgl sets R class attributes
// (e.g. c("sgl_geom_point", "sgl_geom")), we carry the variant as a string
// tag under a "class" key; pgs.py reconstructs typed objects from those tags.
py::dict sgl_to_pgs(std::string sgl_stmt) {
    struct cgs cgs;
		cgs.layers = NULL;
		cgs.scales = NULL;
		cgs.facets= NULL;
		cgs.titles= NULL;
    char *errmsg = NULL;
		struct layer *current_layer;
		struct layer *next_layer;
		struct scale_expr *current_scale_expr;
		struct scale_expr *next_scale_expr;
		struct facet_expr *current_facet_expr;
		struct facet_expr *next_facet_expr;
		struct title_expr *current_title_expr;
		struct title_expr *next_title_expr;

    // Call the C parser function
    sgl_to_cgs(sgl_stmt.c_str(), &cgs, &errmsg);

    // Check for errors
    if (errmsg != NULL) {
        std::string error_message(errmsg);
        free(errmsg);
        throw std::runtime_error(error_message);
    }

    // Convert C struct to Python dict
 		py::dict result;
		py::list layers;

		current_layer = cgs.layers;

		while(current_layer != NULL) {
			next_layer = current_layer->next;
			py::dict layer;

			// Add SQL query
			if (current_layer->source_sql_query != NULL) {
					layer["source_sql_query"] = std::string(current_layer->source_sql_query);
			} else {
					layer["source_sql_query"] = py::none();
			}

			// Convert aesthetic mappings to Python dict
			py::dict aes_list;
			struct aes_mapping *current = current_layer->aes_mappings;
			while (current != NULL) {
					std::string aes_name;
					switch(current->aes) {
							case X:
									aes_name = "x";
									break;
							case Y:
									aes_name = "y";
									break;
							case RADIUS:
									aes_name = "r";
									break;
							case THETA:
									aes_name = "theta";
									break;
							case COLOR:
									aes_name = "color";
									break;
							case SIZE:
									aes_name = "size";
									break;
							default:
									aes_name = "unknown";
					}

					py::dict cta_obj;
					switch(current->col_expr.cta) {
							case IDENTITY:
								cta_obj["class"] = "sgl_cta_identity";
								break;
							case AVG:
								cta_obj["class"] = "sgl_cta_avg";
								break;
							case BIN:
								cta_obj["class"] = "sgl_cta_bin";
								break;
							case COUNT:
								cta_obj["class"] = "sgl_cta_count";
								break;
							default:
								cta_obj["class"] = "sgl_cta";
					}

					std::string column = std::string(current->col_expr.column);
					py::dict col_expr;
					col_expr["column"] = column;
					col_expr["cta"] = cta_obj;
					if (current->col_expr.arg != NULL) {
						col_expr["arg"] = current->col_expr.arg->value;
					}
					aes_list[py::str(aes_name)] = col_expr;

					current = current->next;
			}
			layer["aes_mappings"] = aes_list;

			// Convert groupings to Python list
			if(current_layer->groupings != NULL) {
				py::list grouping_list;
				struct grouping_expr *current_grouping = current_layer->groupings;
				while (current_grouping != NULL) {
						std::string column = std::string(current_grouping->col_expr.column);

						py::dict cta_obj;
						switch(current_grouping->col_expr.cta) {
								case IDENTITY:
									cta_obj["class"] = "sgl_cta_identity";
									break;
								case AVG:
									cta_obj["class"] = "sgl_cta_avg";
									break;
								case BIN:
									cta_obj["class"] = "sgl_cta_bin";
									break;
								case COUNT:
									cta_obj["class"] = "sgl_cta_count";
									break;
								default:
									cta_obj["class"] = "sgl_cta";
						}

						py::dict col_expr;
						col_expr["column"] = column;
						col_expr["cta"] = cta_obj;
						if (current_grouping->col_expr.arg != NULL) {
							col_expr["arg"] = current_grouping->col_expr.arg->value;
						}

						grouping_list.append(col_expr);

						current_grouping = current_grouping->next;
				}
				layer["groupings"] = grouping_list;
			}

			// Convert collections to Python list
			if(current_layer->collections != NULL) {
				py::list collection_list;
				struct collection_expr *current_collection = current_layer->collections;
				while (current_collection != NULL) {
						std::string column = std::string(current_collection->col_expr.column);

						py::dict cta_obj;
						switch(current_collection->col_expr.cta) {
							case IDENTITY:
								cta_obj["class"] = "sgl_cta_identity";
								break;
							case AVG:
								cta_obj["class"] = "sgl_cta_avg";
								break;
							case BIN:
								cta_obj["class"] = "sgl_cta_bin";
								break;
							case COUNT:
								cta_obj["class"] = "sgl_cta_count";
								break;
							default:
								cta_obj["class"] = "sgl_cta";
						}

						py::dict col_expr;
						col_expr["column"] = column;
						col_expr["cta"] = cta_obj;
						if (current_collection->col_expr.arg != NULL) {
							col_expr["arg"] = current_collection->col_expr.arg->value;
						}

						collection_list.append(col_expr);

						current_collection = current_collection->next;
				}
				layer["collections"] = collection_list;
			}

			// Convert geoms to geom list
			py::list geom_list;
			struct geom_expr *current_geom_expr = current_layer->geoms;
			while(current_geom_expr != NULL) {
				py::dict geom_obj;
				enum geom geom_enum = current_geom_expr->geom;
				switch(geom_enum) {
						case POINT:
								geom_obj["class"] = "sgl_geom_point";
								break;
						case BAR:
								geom_obj["class"] = "sgl_geom_bar";
								break;
						case LINE:
								geom_obj["class"] = "sgl_geom_line";
								break;
						case BOX:
								geom_obj["class"] = "sgl_geom_box";
								break;
						default:
								geom_obj["class"] = "sgl_geom";
				}

				// Convert qual enum
				enum qual qual_enum = current_geom_expr->qual;
				std::string qual_str;
				switch(qual_enum) {
						case HORIZONTAL:
							qual_str = "horizontal";
							break;
						case JITTERED:
							qual_str = "jittered";
							break;
						case REGRESSION:
							qual_str = "regression";
							break;
						case UNSTACKED:
							qual_str = "unstacked";
							break;
						case VERTICAL:
							qual_str = "vertical";
							break;
						case DEFAULT:
							qual_str = "default";
							break;
						default:
							qual_str = "unknown";
				}

				py::dict geom_expr;
				// Add geom_expr
				geom_expr["qual"] = qual_str;
				geom_expr["geom"] = geom_obj;
				geom_list.append(geom_expr);
				current_geom_expr = current_geom_expr->next;
			}

			// Add layer for each geom expr
			for (size_t i = 0; i < geom_list.size(); i++) {
				layer["geom_expr"] = geom_list[i];
				layers.append(py::reinterpret_steal<py::dict>(PyDict_Copy(layer.ptr())));
			}

			// Clean up allocated memory
			if (current_layer->source_sql_query != NULL) {
					free(current_layer->source_sql_query);
			}

			// Free the linked list of aes_mappings
			current = current_layer->aes_mappings;
			while (current != NULL) {
					struct aes_mapping *next = current->next;
					free(current->col_expr.column);
					free(current->col_expr.arg);
					free(current);
					current = next;
			}

			// Free the linked list of geoms
			struct geom_expr *current_geom = current_layer->geoms;
			struct geom_expr *next_geom;
			while (current_geom != NULL) {
					next_geom = current_geom->next;
					free(current_geom);
					current_geom = next_geom;
			}

			// Free the linked list of groupings
			struct grouping_expr *current_grouping = current_layer->groupings;
			struct grouping_expr *next_grouping;
			while (current_grouping != NULL) {
					next_grouping = current_grouping->next;
					free(current_grouping->col_expr.column);
					free(current_grouping->col_expr.arg);
					free(current_grouping);
					current_grouping = next_grouping;
			}

			// Free the linked list of collections
			struct collection_expr *current_collection = current_layer->collections;
			struct collection_expr *next_collection;
			while (current_collection != NULL) {
					next_collection = current_collection->next;
					free(current_collection->col_expr.column);
					free(current_collection->col_expr.arg);
					free(current_collection);
					current_collection = next_collection;
			}

			free(current_layer);
			current_layer = next_layer;
		}

		result["layers"] = layers;

		if (cgs.scales != NULL) {
			py::dict scale_list;
			current_scale_expr = cgs.scales;
			while (current_scale_expr != NULL) {
				next_scale_expr = current_scale_expr->next;

				py::dict scale_obj;
				switch(current_scale_expr->scale) {
						case LINEAR:
								scale_obj["class"] = "sgl_scale_linear";
								break;
						case LN:
								scale_obj["class"] = "sgl_scale_ln";
								break;
						case LOG:
								scale_obj["class"] = "sgl_scale_log";
								break;
						default:
								scale_obj["class"] = "sgl_scale";
				}

				std::string scale_aes;
				switch(current_scale_expr->aes) {
						case X:
								scale_aes = "x";
								break;
						case Y:
								scale_aes = "y";
								break;
						case RADIUS:
								scale_aes = "r";
								break;
						case THETA:
								scale_aes = "theta";
								break;
						case COLOR:
								scale_aes = "color";
								break;
						case SIZE:
								scale_aes = "size";
								break;
						default:
								scale_aes = "unknown";
				}

				scale_list[py::str(scale_aes)] = scale_obj;

				free(current_scale_expr);
				current_scale_expr = next_scale_expr;
			}
			result["scales"] = scale_list;
		}

		if (cgs.facets != NULL) {
			py::list facet_list;
			current_facet_expr = cgs.facets;
			while (current_facet_expr != NULL) {
				next_facet_expr = current_facet_expr->next;

				py::dict facet_entry;
				std::string column_name = current_facet_expr->column;
				std::string facet_direction;
				switch(current_facet_expr->direction) {
						case DEFAULT_DIRECTION:
								facet_direction = "default";
								break;
						case HORIZONTAL_DIRECTION:
								facet_direction = "horizontal";
								break;
						case VERTICAL_DIRECTION:
								facet_direction = "vertical";
								break;
						default:
								facet_direction = "unknown";
				}

				facet_entry["column"] = column_name;
				facet_entry["direction"] = facet_direction;

				facet_list.append(facet_entry);

				free(current_facet_expr->column);
				free(current_facet_expr);
				current_facet_expr = next_facet_expr;
			}
			result["facets"] = facet_list;
		}

		if (cgs.titles != NULL) {
			py::dict title_list;
			current_title_expr = cgs.titles;
			while (current_title_expr != NULL) {
				next_title_expr = current_title_expr->next;

				std::string title_aes;
				switch(current_title_expr->aes) {
						case X:
								title_aes = "x";
								break;
						case Y:
								title_aes = "y";
								break;
						case RADIUS:
								title_aes = "r";
								break;
						case THETA:
								title_aes = "theta";
								break;
						case COLOR:
								title_aes = "color";
								break;
						case SIZE:
								title_aes = "size";
								break;
						default:
								title_aes = "unknown";
				}

				std::string title = current_title_expr->title;
				title_list[py::str(title_aes)] = title;

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
