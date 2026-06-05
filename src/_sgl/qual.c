#include"qual.h"
#include"keyword.h"

static struct keyword_enum_row qual_keyword_enum_table[] = {
	{"horizontal", HORIZONTAL},
  {"jittered", JITTERED},
  {"regression", REGRESSION},
  {"unstacked", UNSTACKED},
	{"vertical", VERTICAL}
};

static int qual_count = KEYWORD_COUNT(qual_keyword_enum_table);

int valid_qual_str(const char *qual_str) {
  return valid_keyword_str(qual_str, qual_keyword_enum_table, qual_count);
}

enum qual qual_enum(const char *qual_str) {
  return (enum qual)enum_int(qual_str, qual_keyword_enum_table, qual_count);
}

