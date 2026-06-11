#include<stddef.h>
#include"aes.h"
#include"cgs.h"
#include"title.h"

int title_exists(enum aes aes, struct title_expr *titles) {
	struct title_expr *current_title = titles;
	while (current_title != NULL) {
		if (current_title->aes == aes) {
			return 1;
		}
		current_title = current_title->next;
	}
	return 0;
}
