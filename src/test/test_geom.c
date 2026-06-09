#include<criterion/criterion.h>
#include<geom.h>

Test(valid_geom_str, treats_null_ptr_as_invalid) {
	char *geom_str = NULL;

	cr_expect(!valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_point_as_valid) {
	char *geom_str = "point";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_points_as_valid) {
	char *geom_str = "points";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_bar_as_valid) {
	char *geom_str = "bar";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_bars_as_valid) {
	char *geom_str = "bars";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_line_as_valid) {
	char *geom_str = "line";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_lines_as_valid) {
	char *geom_str = "lines";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_box_as_valid) {
	char *geom_str = "box";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_boxes_as_valid) {
	char *geom_str = "boxes";

	cr_expect(valid_geom_str(geom_str));
}

Test(valid_geom_str, treats_made_up_geom_as_invalid) {
	char *geom_str = "notavalidgeom";

	cr_expect(!valid_geom_str(geom_str));
}

Test(geom_enum, returns_point_enum_for_point) {
	char *geom_str = "point";

	cr_expect(geom_enum(geom_str) == POINT);
}

Test(geom_enum, returns_point_enum_for_points) {
	char *geom_str = "points";

	cr_expect(geom_enum(geom_str) == POINT);
}

Test(geom_enum, returns_bar_enum_for_bar) {
	char *geom_str = "bar";

	cr_expect(geom_enum(geom_str) == BAR);
}

Test(geom_enum, returns_bar_enum_for_bars) {
	char *geom_str = "bars";

	cr_expect(geom_enum(geom_str) == BAR);
}

Test(geom_enum, returns_line_enum_for_line) {
	char *geom_str = "line";

	cr_expect(geom_enum(geom_str) == LINE);
}

Test(geom_enum, returns_line_enum_for_lines) {
	char *geom_str = "lines";

	cr_expect(geom_enum(geom_str) == LINE);
}

Test(geom_enum, returns_box_enum_for_box) {
	char *geom_str = "box";

	cr_expect(geom_enum(geom_str) == BOX);
}

Test(geom_enum, returns_box_enum_for_boxes) {
	char *geom_str = "boxes";

	cr_expect(geom_enum(geom_str) == BOX);
}
