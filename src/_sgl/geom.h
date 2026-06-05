#ifndef GEOM_H
#define GEOM_H

enum geom { 
	BAR,
	BOX,
	LINE,
	POINT
};

int valid_geom_str(const char *geom_str);

enum geom geom_enum(const char *geom_str);

#endif
