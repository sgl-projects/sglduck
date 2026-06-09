#include<criterion/criterion.h>
#include<keyword.h>

static struct keyword_enum_row keyword_enum_table[] = {
	{"a", 1},
	{"b", 99}
};
static int keyword_count = KEYWORD_COUNT(keyword_enum_table);

Test(valid_keyword_str, considers_null_ptr_invalid) {
	char *null_ptr = NULL;

	cr_expect(!valid_keyword_str(null_ptr, keyword_enum_table, keyword_count));
}

Test(valid_keyword_str, considers_keywords_valid) {
	cr_expect(valid_keyword_str("a", keyword_enum_table, keyword_count));
	cr_expect(valid_keyword_str("b", keyword_enum_table, keyword_count));
}

Test(valid_keyword_str, considers_non_keyword_str_invalid) {
	char *keyword_str = "notavalidkeyword";

	cr_expect(!valid_keyword_str(keyword_str, keyword_enum_table, keyword_count));
}

Test(enum_int, return_correct_ints_for_keywords) {
	cr_expect(enum_int("a", keyword_enum_table, keyword_count) == 1);
	cr_expect(enum_int("b", keyword_enum_table, keyword_count) == 99);
}

