#include<criterion/criterion.h>
#include<cgs.h>
#include<cgs_order.h>

Test(reverse_layers, leaves_single_layer_as_is) {
	struct layer test_layer = {0};
	struct cgs test_cgs = {
		.layers = &test_layer
	}; 

	reverse_layers(&test_cgs);

	cr_expect(test_cgs.layers == &test_layer);
	cr_expect(test_layer.next == NULL);
}

Test(reverse_layers, reverses_layers) {
	struct layer test_layer_1 = {0};
	struct layer test_layer_2 = {0};
	test_layer_1.next = &test_layer_2;
	struct cgs test_cgs = {
		.layers = &test_layer_1
	}; 

	reverse_layers(&test_cgs);

	cr_expect(test_cgs.layers == &test_layer_2);
	cr_expect(test_layer_2.next == &test_layer_1);
	cr_expect(test_layer_1.next == NULL);
}

Test(reverse_geoms, leaves_single_geom_as_is) {
	struct geom_expr test_geom = {0};
	struct layer test_layer = {
		.geoms = &test_geom
	};

	reverse_geoms(&test_layer);

	cr_expect(test_layer.geoms == &test_geom);
	cr_expect(test_geom.next == NULL);
}

Test(reverse_geoms, reverses_geoms) {
	struct geom_expr test_geom_1 = {0};
	struct geom_expr test_geom_2 = {0};
	test_geom_1.next = &test_geom_2;
	struct layer test_layer = {
		.geoms = &test_geom_1
	};

	reverse_geoms(&test_layer);

	cr_expect(test_layer.geoms == &test_geom_2);
	cr_expect(test_geom_2.next == &test_geom_1);
	cr_expect(test_geom_1.next == NULL);
}

Test(reorder_cmpnts, reverses_layers) {
	struct layer test_layer_1 = {0};
	struct layer test_layer_2 = {0};
	test_layer_1.next = &test_layer_2;
	struct cgs test_cgs = {
		.layers = &test_layer_1
	}; 

	reorder_cmpnts(&test_cgs);

	cr_expect(test_cgs.layers == &test_layer_2);
	cr_expect(test_layer_2.next == &test_layer_1);
	cr_expect(test_layer_1.next == NULL);
}

Test(reorder_cmpnts, reverses_geoms_in_each_layer) {
	struct geom_expr test_geom_1 = {0};
	struct geom_expr test_geom_2 = {0};
	test_geom_1.next = &test_geom_2;
	struct layer test_layer_1 = {
		.geoms = &test_geom_1
	};
	struct geom_expr test_geom_3 = {0};
	struct geom_expr test_geom_4 = {0};
	test_geom_3.next = &test_geom_4;
	struct layer test_layer_2 = {
		.geoms = &test_geom_3
	};
	test_layer_1.next = &test_layer_2;
	struct cgs test_cgs = {
		.layers = &test_layer_1
	};

	reorder_cmpnts(&test_cgs);

	cr_expect(test_layer_1.geoms == &test_geom_2);
	cr_expect(test_geom_2.next == &test_geom_1);
	cr_expect(test_geom_1.next == NULL);
	cr_expect(test_layer_2.geoms == &test_geom_4);
	cr_expect(test_geom_4.next == &test_geom_3);
	cr_expect(test_geom_3.next == NULL);
}

