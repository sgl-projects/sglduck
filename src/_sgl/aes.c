#include"aes.h"
#include"keyword.h"

static struct keyword_enum_row aes_keyword_enum_table[] = {
	{"x", X},
	{"y", Y},
	{"theta", THETA},
	{"r", RADIUS},
	{"color", COLOR},
	{"size", SIZE}
};

static int aes_count = KEYWORD_COUNT(aes_keyword_enum_table);

int valid_aes_str(const char *aes_str) {
	return valid_keyword_str(aes_str, aes_keyword_enum_table, aes_count);
}

enum aes aes_enum(const char *aes_str) {
	return (enum aes)enum_int(aes_str, aes_keyword_enum_table, aes_count);	
}
