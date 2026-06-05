#include"scale.h"
#include"keyword.h"

static struct keyword_enum_row scale_keyword_enum_table[] = {
	{"linear", LINEAR},
	{"ln", LN},
  {"log", LOG}
};

static int scale_count = KEYWORD_COUNT(scale_keyword_enum_table);

int valid_scale_str(const char *scale_str) {
  return valid_keyword_str(scale_str, scale_keyword_enum_table, scale_count);
}

enum scale scale_enum(const char *scale_str) {
  return (enum scale)enum_int(scale_str, scale_keyword_enum_table, scale_count);
}

