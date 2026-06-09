#include<stddef.h>
#include"cgs.h"
#include"cgs_order.h"

void reverse_layers(struct cgs *cgs) {
  struct layer *previous_layer = NULL;
  struct layer *current_layer = cgs->layers;
  struct layer *next_layer;

  while(current_layer != NULL) {
    next_layer = current_layer->next;
    current_layer->next = previous_layer;
    previous_layer = current_layer;
    current_layer = next_layer;
  }
  cgs->layers = previous_layer;
}

void reverse_geoms(struct layer *layer) {
	struct geom_expr *previous_geom = NULL;
	struct geom_expr *current_geom = layer->geoms;
	struct geom_expr *next_geom;

	while(current_geom != NULL) {
		next_geom = current_geom->next;
		current_geom->next = previous_geom;
		previous_geom = current_geom;
		current_geom = next_geom;
	}
	layer->geoms = previous_geom;
}

void reorder_cmpnts(struct cgs *cgs) {
	reverse_layers(cgs);

	struct layer *current_layer = cgs->layers;
	while(current_layer != NULL) {
		reverse_geoms(current_layer);
		current_layer = current_layer->next;
	}
}
