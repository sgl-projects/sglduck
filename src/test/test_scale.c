#include<criterion/criterion.h>
#include<scale.h>

Test(valid_scale_str, treats_null_ptr_as_invalid) {
	char *scale_str = NULL;

	cr_expect(!valid_scale_str(scale_str));
}

Test(valid_scale_str, treats_scale_keywords_as_valid) {
  char *keywords[] = {
    "linear",
		"ln",
    "log"
  };
  size_t keyword_count = sizeof(keywords)/sizeof(keywords[0]);

  for(int i=0; i < keyword_count; i++) {
    cr_expect(
      valid_scale_str(keywords[i]),
      "failed for input \"%s\"", keywords[i]
    );
  }
}

Test(valid_scale_str, treats_made_up_scale_as_invalid) {
	char *scale_str = "notavalidscale";

	cr_expect(!valid_scale_str(scale_str));
}

Test(scale_enum, return_correct_enums_for_keywords) {
  struct keyword_and_expected_enum {
    char *keyword;
    enum scale expected_enum;
  };

  struct keyword_and_expected_enum keywords_and_expected_enums[] = {
    {"linear", LINEAR},
		{"ln", LN},
    {"log", LOG}
  };

  size_t keyword_count = sizeof(keywords_and_expected_enums)/sizeof(struct keyword_and_expected_enum);

  char *keyword;
  enum scale expected_enum;

  for(int i=0; i < keyword_count; i++) {
    keyword = keywords_and_expected_enums[i].keyword;
    expected_enum = keywords_and_expected_enums[i].expected_enum;
    cr_expect(
      scale_enum(keyword) == expected_enum,
      "failed for input \"%s\"", keyword
    );
  }
}
