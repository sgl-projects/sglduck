#ifndef KEYWORD_H
#define KEYWORD_H

#define KEYWORD_COUNT(table) (sizeof(table)/sizeof(table[0]))

struct keyword_enum_row {
  const char *keyword;
  int enum_int;
};

int valid_keyword_str(
	const char *keyword_str,
	struct keyword_enum_row *keyword_enum_table,
	int keyword_count
);

int enum_int(
	const char *keyword_str,
	struct keyword_enum_row *keyword_enum_table,
	int keyword_count
);

#endif
