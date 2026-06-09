#include<criterion/criterion.h>
#include<aes.h>

Test(valid_aes_str, treats_null_ptr_as_invalid) {
	char *aes_str = NULL;

	cr_expect(!valid_aes_str(aes_str));
}

Test(valid_aes_str, treats_aes_keywords_as_valid) {
	char *keywords[] = {
		"x",
		"y",
		"theta",
		"r",
		"color",
		"size"
	};
	size_t keyword_count = sizeof(keywords)/sizeof(keywords[0]);

	for(int i=0; i < keyword_count; i++) {
		cr_expect(
			valid_aes_str(keywords[i]),
			"failed for input \"%s\"", keywords[i]
		);
	}
}

Test(valid_aes_str, treats_made_up_aes_as_invalid) {
	char *aes_str = "notavalidaes";

	cr_expect(!valid_aes_str(aes_str));
}

Test(aes_enum, return_correct_enums_for_keywords) {
	struct keyword_and_expected_enum {
		char *keyword;
		enum aes expected_enum;
	};

	struct keyword_and_expected_enum keywords_and_expected_enums[] = {
		{"x", X},
		{"y", Y},
		{"theta", THETA},
		{"r", RADIUS},
		{"color", COLOR},
		{"size", SIZE}
	};

	size_t keyword_count = sizeof(keywords_and_expected_enums)/sizeof(struct keyword_and_expected_enum);

	char *keyword;
	enum aes expected_enum;

	for(int i=0; i < keyword_count; i++) {
		keyword = keywords_and_expected_enums[i].keyword;
		expected_enum = keywords_and_expected_enums[i].expected_enum;
		cr_expect(
			aes_enum(keyword) == expected_enum,
			"failed for input \"%s\"", keyword
		);
	}
}
