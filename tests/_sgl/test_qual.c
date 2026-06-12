#include<criterion/criterion.h>
#include<qual.h>

Test(valid_qual_str, treats_horizontal_as_valid) {
	char *qual_str = "horizontal";

	cr_expect(valid_qual_str(qual_str));
}

Test(valid_qual_str, treats_jittered_as_valid) {
	char *qual_str = "jittered";

	cr_expect(valid_qual_str(qual_str));
}

Test(valid_qual_str, treats_regression_as_valid) {
	char *qual_str = "regression";

	cr_expect(valid_qual_str(qual_str));
}

Test(valid_qual_str, treats_unstacked_as_valid) {
	char *qual_str = "unstacked";

	cr_expect(valid_qual_str(qual_str));
}

Test(valid_qual_str, treats_vertical_as_valid) {
	char *qual_str = "vertical";

	cr_expect(valid_qual_str(qual_str));
}

Test(valid_qual_str, treats_made_up_qual_as_invalid) {
	char *qual_str = "notavalidqual";

	cr_expect(!valid_qual_str(qual_str));
}

Test(qual_enum, returns_horizontal_enum_for_horizontal) {
	char *qual_str = "horizontal";

	cr_expect(qual_enum(qual_str) == HORIZONTAL);
}

Test(qual_enum, returns_jittered_enum_for_jittered) {
	char *qual_str = "jittered";

	cr_expect(qual_enum(qual_str) == JITTERED);
}

Test(qual_enum, returns_regression_enum_for_regression) {
	char *qual_str = "regression";

	cr_expect(qual_enum(qual_str) == REGRESSION);
}

Test(qual_enum, returns_unstacked_enum_for_unstacked) {
	char *qual_str = "unstacked";

	cr_expect(qual_enum(qual_str) == UNSTACKED);
}

Test(qual_enum, returns_vertical_enum_for_vertical) {
	char *qual_str = "vertical";

	cr_expect(qual_enum(qual_str) == VERTICAL);
}
