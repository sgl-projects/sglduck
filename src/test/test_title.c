#include<stddef.h>
#include<criterion/criterion.h>
#include<aes.h>
#include<cgs.h>
#include<title.h>

Test(title_exists, returns_0_for_null_ptr) {
	cr_expect(!title_exists(X, NULL));
}

Test(title_exists, returns_0_if_title_for_aes_doesnt_exist) {
	struct title_expr title_1 = {
		.aes=Y,
		.title="y title"
	};
	struct title_expr title_2 = {
		.aes=COLOR,
		.title="color title"
	};
	title_1.next=&title_2;

	cr_expect(!title_exists(X, &title_1));
}

Test(title_exists, returns_1_if_title_for_aes_exists) {
	struct title_expr title_1 = {
		.aes=Y,
		.title="y title"
	};
	struct title_expr title_2 = {
		.aes=X,
		.title="x title"
	};
	title_1.next=&title_2;

	cr_expect(title_exists(X, &title_1));
}
