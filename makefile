# DEV-ONLY makefile — mirrors rsgl/makefile.
#
# Regenerates the committed bison/flex output and (re)builds the extension.
# This file is NOT part of the sdist/wheel (see MANIFEST.in): end users compile
# the already-generated src/_sgl/parser.tab.c, parser.tab.h and scanner.c with a
# C/C++ compiler only — bison/flex are a developer-only tool. Run `make parser`
# / `make scanner` after editing parser.y / scanner.l, and commit the output.

SRC = src/_sgl

# Regenerate parser + scanner, then build the package in editable mode.
build: parser scanner
	pip install -e .

parser:
	bison -d -o $(SRC)/parser.tab.c $(SRC)/parser.y

scanner:
	flex -o $(SRC)/scanner.c $(SRC)/scanner.l

clean:
	rm -f $(SRC)/*.o
	rm -rf build/ src/pysgl/_sgl*.so src/_sgl/*.so

.PHONY: build parser scanner clean
