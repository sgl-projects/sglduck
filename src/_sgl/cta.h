#ifndef CTA_H
#define CTA_H

enum cta {
	IDENTITY,
	AVG,
	BIN,
	COUNT
};

int valid_cta_str(const char *cta_str);

enum cta cta_enum(const char *cta_str);

#endif
