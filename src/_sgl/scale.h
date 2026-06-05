#ifndef SCALE_H
#define SCALE_H

enum scale {
	LINEAR,
	LN,
	LOG
};

int valid_scale_str(const char *scale_str);

enum scale scale_enum(const char *scale_str);

#endif
