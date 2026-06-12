# DEV-ONLY makefile.
#
# Regenerates the committed bison/flex output, (re)builds the extension, and
# builds/runs the Criterion C unit tests in tests/_sgl (requires the criterion
# library, e.g. `brew install criterion`).
# This file is NOT part of the sdist/wheel (see MANIFEST.in): end users compile
# the already-generated src/_sgl/parser.tab.c, parser.tab.h and scanner.c with a
# C/C++ compiler only — bison/flex are a developer-only tool. Run `make parser`
# / `make scanner` after editing parser.y / scanner.l, and commit the output.

CC = gcc
CFLAGS = -g
CRITERION_CFLAGS := $(shell pkg-config --cflags criterion)
TEST_LDFLAGS := $(shell pkg-config --libs criterion)

SRC = src/_sgl
TEST = tests/_sgl

SRC_OBJS = $(SRC)/parser.tab.o $(SRC)/scanner.o $(SRC)/aes.o $(SRC)/geom.o $(SRC)/cta.o $(SRC)/qual.o $(SRC)/scale.o $(SRC)/keyword.o $(SRC)/title.o $(SRC)/case.o $(SRC)/cgs_order.o
TEST_OBJS = $(TEST)/test_sgl_to_cgs.o $(TEST)/test_aes.o $(TEST)/test_geom.o $(TEST)/test_cta.o $(TEST)/test_qual.o $(TEST)/test_scale.o $(TEST)/test_keyword.o $(TEST)/test_title.o $(TEST)/test_case.o $(TEST)/test_cgs_order.o $(TEST)/stubs.o

# Regenerate parser + scanner, then build the package in editable mode.
build: parser scanner
	pip install -e .

test: $(TEST)/test
	$(TEST)/test -j1

$(TEST)/test: $(SRC_OBJS) $(TEST_OBJS)
	$(CC) $(CFLAGS) -o $(TEST)/test $(TEST_OBJS) $(SRC_OBJS) $(TEST_LDFLAGS)

parser:
	bison -d -o $(SRC)/parser.tab.c $(SRC)/parser.y

scanner:
	flex -o $(SRC)/scanner.c $(SRC)/scanner.l

$(SRC)/%.o: $(SRC)/%.c
	$(CC) $(CFLAGS) -o $@ -c $< -I./$(SRC)

$(TEST)/test_sgl_to_cgs.o: $(TEST)/test_sgl_to_cgs.c $(SRC)/aes.h $(SRC)/direction.h $(SRC)/qual.h $(SRC)/sgl_to_cgs.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_sgl_to_cgs.o -c $(TEST)/test_sgl_to_cgs.c -I./$(SRC)

$(TEST)/test_aes.o: $(TEST)/test_aes.c $(SRC)/aes.h $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_aes.o -c $(TEST)/test_aes.c -I./$(SRC)

$(TEST)/test_geom.o: $(TEST)/test_geom.c $(SRC)/geom.h $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_geom.o -c $(TEST)/test_geom.c -I./$(SRC)

$(TEST)/test_cta.o: $(TEST)/test_cta.c $(SRC)/cta.h $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_cta.o -c $(TEST)/test_cta.c -I./$(SRC)

$(TEST)/test_qual.o: $(TEST)/test_qual.c $(SRC)/qual.h $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_qual.o -c $(TEST)/test_qual.c -I./$(SRC)

$(TEST)/test_scale.o: $(TEST)/test_scale.c $(SRC)/scale.h $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_scale.o -c $(TEST)/test_scale.c -I./$(SRC)

$(TEST)/test_keyword.o: $(TEST)/test_keyword.c $(SRC)/keyword.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_keyword.o -c $(TEST)/test_keyword.c -I./$(SRC)

$(TEST)/test_title.o: $(TEST)/test_title.c $(SRC)/title.h $(SRC)/aes.h $(SRC)/cgs.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_title.o -c $(TEST)/test_title.c -I./$(SRC)

$(TEST)/test_case.o: $(TEST)/test_case.c $(SRC)/case.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_case.o -c $(TEST)/test_case.c -I./$(SRC)

$(TEST)/test_cgs_order.o: $(TEST)/test_cgs_order.c $(SRC)/cgs_order.h $(SRC)/cgs.h
	$(CC) $(CFLAGS) $(CRITERION_CFLAGS) -o $(TEST)/test_cgs_order.o -c $(TEST)/test_cgs_order.c -I./$(SRC)

$(TEST)/stubs.o: $(TEST)/stubs.c $(SRC)/sgl_error.h
	$(CC) $(CFLAGS) -o $(TEST)/stubs.o -c $(TEST)/stubs.c -I./$(SRC)

clean:
	rm -f $(SRC)/*.o
	rm -rf build/ src/pysgl/_sgl*.so src/_sgl/*.so
	rm -f $(TEST)/*.o
	rm -f $(TEST)/test

.PHONY: build parser scanner test clean
