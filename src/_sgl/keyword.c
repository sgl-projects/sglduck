#include<string.h>
#include"sgl_error.h"
#include"keyword.h"

int valid_keyword_str(const char *keyword_str, struct keyword_enum_row *keyword_enum_table, int keyword_count) {
  if (!keyword_str) return 0;

	for(int i=0; i<keyword_count; i++) {
    if(!strcmp(keyword_str, keyword_enum_table[i].keyword)) {
      return 1;
    }
  }

  return 0;
}

int enum_int(const char *keyword_str, struct keyword_enum_row *keyword_enum_table, int keyword_count) {
  struct keyword_enum_row current_row;
  for(int i=0; i<keyword_count; i++) {
    current_row = keyword_enum_table[i];
    if(!strcmp(keyword_str, current_row.keyword)) {
      return current_row.enum_int;
    }
  }
  sgl_error("Error: unexpected token '%s'", keyword_str);
}
