#include<criterion/criterion.h>
#include<string.h>
#include<case.h>

Test(str_tolower, leaves_null_ptr_as_is) {
	char *s = NULL;

	str_tolower(s);

	cr_expect(s == NULL);
}

Test(str_tolower, leaves_empty_str_as_is) {
	char s[] = "";

	str_tolower(s);

	cr_expect(!strcmp(s, ""));
}

Test(str_tolower, lower_cases_non_empty_str) {
	char s[] = "A STRinG.";

	str_tolower(s);

	cr_expect(!strcmp(s, "a string."));
}
