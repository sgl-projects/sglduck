#include"case.h"
#include<ctype.h>

void str_tolower(char *s) {
	if (s) {
		for (; *s; ++s) {
			*s = tolower((unsigned char)*s);
		}
	}
}

