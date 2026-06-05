#include"cta.h"
#include"keyword.h"

static struct keyword_enum_row cta_keyword_enum_table[] = {
  {"avg", AVG},
  {"bin", BIN},
  {"count", COUNT}
};

static int cta_count = KEYWORD_COUNT(cta_keyword_enum_table);

int valid_cta_str(const char *cta_str) {
  return valid_keyword_str(cta_str, cta_keyword_enum_table, cta_count);
}

enum cta cta_enum(const char *cta_str) {
  return (enum cta)enum_int(cta_str, cta_keyword_enum_table, cta_count);
}
