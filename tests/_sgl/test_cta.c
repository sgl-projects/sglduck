#include<criterion/criterion.h>
#include<cta.h>

Test(valid_cta_str, treats_null_ptr_as_invalid) {
	char *cta_str = NULL;

	cr_expect(!valid_cta_str(cta_str));
}

Test(valid_cta_str, treats_cta_keywords_as_valid) {
  char *keywords[] = {
		"avg",
    "bin",
    "count"
  };
  size_t keyword_count = sizeof(keywords)/sizeof(keywords[0]);

  for(int i=0; i < keyword_count; i++) {
    cr_expect(
      valid_cta_str(keywords[i]),
      "failed for input \"%s\"", keywords[i]
    );
  }
}

Test(valid_cta_str, treats_made_up_cta_as_invalid) {
	char *cta_str = "notavalidcta";

	cr_expect(!valid_cta_str(cta_str));
}

Test(cta_enum, return_correct_enums_for_keywords) {
  struct keyword_and_expected_enum {
    char *keyword;
    enum cta expected_enum;
  };

  struct keyword_and_expected_enum keywords_and_expected_enums[] = {
		{"avg", AVG},
		{"bin", BIN},
		{"count", COUNT}
  };

  size_t keyword_count = sizeof(keywords_and_expected_enums)/sizeof(struct keyword_and_expected_enum);

  char *keyword;
  enum cta expected_enum;

  for(int i=0; i < keyword_count; i++) {
    keyword = keywords_and_expected_enums[i].keyword;
    expected_enum = keywords_and_expected_enums[i].expected_enum;
    cr_expect(
      cta_enum(keyword) == expected_enum,
      "failed for input \"%s\"", keyword
    );
  }
}
