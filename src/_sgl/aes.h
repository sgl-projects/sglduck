#ifndef AES_H
#define AES_H

enum aes {
	X,
	Y,
	RADIUS,
	THETA,
	COLOR,
	SIZE
};

int valid_aes_str(const char *aes_str);

enum aes aes_enum(const char *aes_str);

#endif
