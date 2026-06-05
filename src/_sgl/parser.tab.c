/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 4 "parser.y"

#define _GNU_SOURCE
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include"panic.h"
#include "cgs.h"
#include "aes.h"
#include "geom.h"
#include "cta.h"
#include "qual.h"
#include "scale.h"
#include "direction.h"
#include "case.h"

void set_scanner_input(const char *input_string);
void delete_scanner_buffer(void);
void reset_scanner_state(void);

int yylex(void);
void yyerror(struct cgs *cgs, char **errmsg, char const *s);
extern void yyrestart(FILE *input_file);


#line 96 "parser.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "parser.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_VISUALIZE = 3,                  /* VISUALIZE  */
  YYSYMBOL_AS = 4,                         /* AS  */
  YYSYMBOL_FROM = 5,                       /* FROM  */
  YYSYMBOL_GROUP = 6,                      /* GROUP  */
  YYSYMBOL_COLLECT = 7,                    /* COLLECT  */
  YYSYMBOL_USING = 8,                      /* USING  */
  YYSYMBOL_LAYER = 9,                      /* LAYER  */
  YYSYMBOL_COMMA = 10,                     /* COMMA  */
  YYSYMBOL_SCALE = 11,                     /* SCALE  */
  YYSYMBOL_BY = 12,                        /* BY  */
  YYSYMBOL_TITLE = 13,                     /* TITLE  */
  YYSYMBOL_FACET = 14,                     /* FACET  */
  YYSYMBOL_HORIZONTALLY = 15,              /* HORIZONTALLY  */
  YYSYMBOL_VERTICALLY = 16,                /* VERTICALLY  */
  YYSYMBOL_TABLE_NAME = 17,                /* TABLE_NAME  */
  YYSYMBOL_SQL_SUBQUERY = 18,              /* SQL_SUBQUERY  */
  YYSYMBOL_UNQUOTED_STRING = 19,           /* UNQUOTED_STRING  */
  YYSYMBOL_SINGLE_QUOTED_STRING = 20,      /* SINGLE_QUOTED_STRING  */
  YYSYMBOL_INTEGER = 21,                   /* INTEGER  */
  YYSYMBOL_22_ = 22,                       /* '('  */
  YYSYMBOL_23_ = 23,                       /* ')'  */
  YYSYMBOL_YYACCEPT = 24,                  /* $accept  */
  YYSYMBOL_statement = 25,                 /* statement  */
  YYSYMBOL_graphic_clauses = 26,           /* graphic_clauses  */
  YYSYMBOL_graphic_clause = 27,            /* graphic_clause  */
  YYSYMBOL_layer_list = 28,                /* layer_list  */
  YYSYMBOL_layer_expression = 29,          /* layer_expression  */
  YYSYMBOL_30_1 = 30,                      /* $@1  */
  YYSYMBOL_geom_expr = 31,                 /* geom_expr  */
  YYSYMBOL_layered_geom_list = 32,         /* layered_geom_list  */
  YYSYMBOL_using_clause = 33,              /* using_clause  */
  YYSYMBOL_from_clause = 34,               /* from_clause  */
  YYSYMBOL_aes_mappings = 35,              /* aes_mappings  */
  YYSYMBOL_aes_mapping = 36,               /* aes_mapping  */
  YYSYMBOL_col_expr = 37,                  /* col_expr  */
  YYSYMBOL_fn_arg = 38,                    /* fn_arg  */
  YYSYMBOL_grouping_clause = 39,           /* grouping_clause  */
  YYSYMBOL_grouping_list = 40,             /* grouping_list  */
  YYSYMBOL_grouping_expr = 41,             /* grouping_expr  */
  YYSYMBOL_collection_clause = 42,         /* collection_clause  */
  YYSYMBOL_collection_list = 43,           /* collection_list  */
  YYSYMBOL_collection_expr = 44,           /* collection_expr  */
  YYSYMBOL_scale_clause = 45,              /* scale_clause  */
  YYSYMBOL_scale_list = 46,                /* scale_list  */
  YYSYMBOL_scale_expr = 47,                /* scale_expr  */
  YYSYMBOL_facet_clause = 48,              /* facet_clause  */
  YYSYMBOL_facet_list = 49,                /* facet_list  */
  YYSYMBOL_facet_expr = 50,                /* facet_expr  */
  YYSYMBOL_direction = 51,                 /* direction  */
  YYSYMBOL_title_clause = 52,              /* title_clause  */
  YYSYMBOL_title_list = 53,                /* title_list  */
  YYSYMBOL_title_expr = 54                 /* title_expr  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_int8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  6
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   63

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  24
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  31
/* YYNRULES -- Number of rules.  */
#define YYNRULES  51
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  88

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   276


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      22,    23,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_int16 yyrline[] =
{
       0,    49,    49,    51,    52,    54,    55,    56,    58,    59,
      61,    61,    71,   102,   125,   126,   128,   129,   131,   139,
     145,   146,   148,   170,   191,   212,   224,   234,   235,   237,
     238,   240,   249,   250,   252,   253,   255,   264,   266,   267,
     269,   303,   305,   306,   308,   322,   323,   324,   326,   328,
     329,   331
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "VISUALIZE", "AS",
  "FROM", "GROUP", "COLLECT", "USING", "LAYER", "COMMA", "SCALE", "BY",
  "TITLE", "FACET", "HORIZONTALLY", "VERTICALLY", "TABLE_NAME",
  "SQL_SUBQUERY", "UNQUOTED_STRING", "SINGLE_QUOTED_STRING", "INTEGER",
  "'('", "')'", "$accept", "statement", "graphic_clauses",
  "graphic_clause", "layer_list", "layer_expression", "$@1", "geom_expr",
  "layered_geom_list", "using_clause", "from_clause", "aes_mappings",
  "aes_mapping", "col_expr", "fn_arg", "grouping_clause", "grouping_list",
  "grouping_expr", "collection_clause", "collection_list",
  "collection_expr", "scale_clause", "scale_list", "scale_expr",
  "facet_clause", "facet_list", "facet_expr", "direction", "title_clause",
  "title_list", "title_expr", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-75)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  0

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int8 yypact[] =
{
      11,   -75,    19,    13,   -75,     1,   -75,    11,    -4,     2,
      -2,   -75,    21,   -75,    14,     8,    16,   -75,   -75,   -75,
     -75,    10,   -12,     1,    24,    12,    15,    29,    25,   -75,
      17,    -6,   -75,   -75,   -75,    26,    30,   -75,    18,    31,
     -75,    22,     8,    -3,    33,   -75,    23,   -75,     1,    27,
      37,    28,    15,   -75,   -75,   -75,   -75,   -75,    17,   -75,
      32,   -75,    36,   -75,     1,    -1,   -75,    34,   -75,   -75,
     -75,     1,   -75,    38,   -75,    35,    39,   -75,   -75,   -75,
       1,   -75,   -75,    -8,   -75,    39,   -75,   -75
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       0,    10,     0,     3,     8,     0,     1,     0,     2,    25,
       0,    20,     0,     9,     0,     0,     0,     4,     5,     6,
       7,     0,     0,     0,    27,     0,     0,     0,    48,    49,
       0,     0,    18,    19,    21,     0,    32,    22,     0,    37,
      38,     0,     0,    45,    41,    42,     0,    23,     0,     0,
       0,     0,     0,    51,    50,    46,    47,    44,     0,    26,
       0,    31,    28,    29,     0,     0,    11,     0,    39,    43,
      24,     0,    36,    33,    34,    13,     0,    16,    40,    30,
       0,    12,    14,     0,    35,     0,    17,    15
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -75,   -75,   -75,   -75,   -75,    42,   -75,   -74,   -75,   -75,
     -75,   -75,    40,   -48,   -75,   -75,   -75,   -21,   -75,   -75,
     -29,   -75,   -75,     0,   -75,   -75,    -5,   -75,   -75,   -75,
      20
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
       0,     2,     8,    17,     3,     4,     5,    77,    83,    66,
      24,    10,    11,    12,    60,    36,    62,    63,    50,    73,
      74,    18,    39,    40,    19,    44,    45,    57,    20,    28,
      29
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int8 yytable[] =
{
      61,    85,    82,    22,    46,    32,    33,    14,    23,    15,
      16,    87,    55,    56,     1,    86,    72,    47,    75,     6,
       9,    76,     7,    61,    21,    25,    26,    27,    30,    31,
      35,    37,    72,    41,    38,    42,    43,    49,    48,    64,
      51,    52,    53,    58,    59,    65,    71,    67,    80,    13,
      79,    84,    68,    69,    81,    70,     0,    78,    75,     0,
       0,     0,    54,    34
};

static const yytype_int8 yycheck[] =
{
      48,     9,    76,     5,    10,    17,    18,    11,    10,    13,
      14,    85,    15,    16,     3,    23,    64,    23,    19,     0,
      19,    22,     9,    71,    22,     4,    12,    19,    12,    19,
       6,    19,    80,     4,    19,    10,    19,     7,    12,    12,
      22,    10,    20,    10,    21,     8,    10,    19,    10,     7,
      71,    80,    52,    58,    19,    23,    -1,    23,    19,    -1,
      -1,    -1,    42,    23
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,     3,    25,    28,    29,    30,     0,     9,    26,    19,
      35,    36,    37,    29,    11,    13,    14,    27,    45,    48,
      52,    22,     5,    10,    34,     4,    12,    19,    53,    54,
      12,    19,    17,    18,    36,     6,    39,    19,    19,    46,
      47,     4,    10,    19,    49,    50,    10,    23,    12,     7,
      42,    22,    10,    20,    54,    15,    16,    51,    10,    21,
      38,    37,    40,    41,    12,     8,    33,    19,    47,    50,
      23,    10,    37,    43,    44,    19,    22,    31,    23,    41,
      10,    19,    31,    32,    44,     9,    23,    31
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    24,    25,    26,    26,    27,    27,    27,    28,    28,
      30,    29,    31,    31,    32,    32,    33,    33,    34,    34,
      35,    35,    36,    37,    37,    37,    38,    39,    39,    40,
      40,    41,    42,    42,    43,    43,    44,    45,    46,    46,
      47,    48,    49,    49,    50,    51,    51,    51,    52,    53,
      53,    54
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     2,     0,     2,     1,     1,     1,     1,     3,
       0,     7,     2,     1,     1,     3,     2,     4,     2,     2,
       1,     3,     3,     4,     6,     1,     1,     0,     3,     1,
       3,     1,     0,     3,     1,     3,     1,     3,     1,     3,
       4,     3,     1,     3,     2,     0,     1,     1,     2,     1,
       3,     3
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (cgs, errmsg, YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value, cgs, errmsg); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, struct cgs *cgs, char **errmsg)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  YY_USE (cgs);
  YY_USE (errmsg);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, struct cgs *cgs, char **errmsg)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep, cgs, errmsg);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule, struct cgs *cgs, char **errmsg)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)], cgs, errmsg);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule, cgs, errmsg); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep, struct cgs *cgs, char **errmsg)
{
  YY_USE (yyvaluep);
  YY_USE (cgs);
  YY_USE (errmsg);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (struct cgs *cgs, char **errmsg)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 10: /* $@1: %empty  */
#line 61 "parser.y"
                            {
	struct layer *new_layer = malloc(sizeof(struct layer));
	new_layer->aes_mappings=NULL;
	new_layer->geoms=NULL;
	new_layer->groupings=NULL;
	new_layer->collections=NULL;
	new_layer->next=cgs->layers;
	cgs->layers=new_layer;
}
#line 1204 "parser.tab.c"
    break;

  case 11: /* layer_expression: VISUALIZE $@1 aes_mappings from_clause grouping_clause collection_clause using_clause  */
#line 69 "parser.y"
                                                                          {}
#line 1210 "parser.tab.c"
    break;

  case 12: /* geom_expr: UNQUOTED_STRING UNQUOTED_STRING  */
#line 71 "parser.y"
                                           {
	char *qual_str=(yyvsp[-1].str);
	str_tolower(qual_str);	
	int print_result;
	if (!valid_qual_str(qual_str)) {
		print_result = asprintf(errmsg, "Invalid geom qualifier: %s\n", qual_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}
	enum qual qual = qual_enum(qual_str);	
	free(qual_str);

	char *geom_str = (yyvsp[0].str);
	str_tolower(geom_str);
	if (!valid_geom_str(geom_str)) {
		print_result = asprintf(errmsg, "Invalid geom name: %s\n", geom_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}	
	enum geom geom = geom_enum(geom_str);	
	free(geom_str);

	struct geom_expr *new_geom = malloc(sizeof(struct geom_expr));
	new_geom->qual = qual;
	new_geom->geom = geom;
	new_geom->next = cgs->layers->geoms;
	cgs->layers->geoms = new_geom;
}
#line 1247 "parser.tab.c"
    break;

  case 13: /* geom_expr: UNQUOTED_STRING  */
#line 102 "parser.y"
                    {
	enum qual qual=DEFAULT;
	int print_result;

	char *geom_str=(yyvsp[0].str);
	str_tolower(geom_str);
	if (!valid_geom_str(geom_str)) {
		print_result = asprintf(errmsg, "Invalid geom name: %s\n", geom_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}	
	enum geom geom = geom_enum(geom_str);	
	free(geom_str);

	struct geom_expr *new_geom = malloc(sizeof(struct geom_expr));
	new_geom->qual = qual;
	new_geom->geom = geom;
	new_geom->next = cgs->layers->geoms;
	cgs->layers->geoms = new_geom;
}
#line 1274 "parser.tab.c"
    break;

  case 18: /* from_clause: FROM TABLE_NAME  */
#line 131 "parser.y"
                             {
	char *table_name = (yyvsp[0].str);
	int print_result;
	print_result = asprintf(&(cgs->layers->source_sql_query), "select * from %s", table_name);
	if(print_result == -1) {
		sgl_panic("Memory allocation failed.");
	}
	free(table_name);
}
#line 1288 "parser.tab.c"
    break;

  case 19: /* from_clause: FROM SQL_SUBQUERY  */
#line 139 "parser.y"
                      {
	char *sql_subquery=(yyvsp[0].str);
	cgs->layers->source_sql_query=strdup(sql_subquery);
	free(sql_subquery);
}
#line 1298 "parser.tab.c"
    break;

  case 22: /* aes_mapping: col_expr AS UNQUOTED_STRING  */
#line 148 "parser.y"
                                         {
	char *aes_str=(yyvsp[0].str);
	str_tolower(aes_str);
	int print_result;
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}	

	struct aes_mapping *new_mapping = malloc(sizeof(struct aes_mapping));
	new_mapping->aes=aes_enum(aes_str);
	free(aes_str);

	new_mapping->col_expr=(yyvsp[-2].ce);
	new_mapping->next=cgs->layers->aes_mappings;	

	cgs->layers->aes_mappings=new_mapping;
}
#line 1324 "parser.tab.c"
    break;

  case 23: /* col_expr: UNQUOTED_STRING '(' UNQUOTED_STRING ')'  */
#line 170 "parser.y"
                                                  {
	char *cta_str=(yyvsp[-3].str);
	str_tolower(cta_str);	
	int print_result;
	if (!valid_cta_str(cta_str)) {
		print_result = asprintf(errmsg, "Invalid CTA: %s\n", cta_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}
	enum cta cta = cta_enum(cta_str);	
	free(cta_str);
	char *column_name=(yyvsp[-1].str);
	
	(yyval.ce).column=strdup(column_name);
	(yyval.ce).cta=cta;	
	(yyval.ce).arg=NULL;

	free(column_name);

}
#line 1351 "parser.tab.c"
    break;

  case 24: /* col_expr: UNQUOTED_STRING '(' UNQUOTED_STRING COMMA fn_arg ')'  */
#line 191 "parser.y"
                                                         {
	char *cta_str=(yyvsp[-5].str);
	str_tolower(cta_str);	
	int print_result;
	if (!valid_cta_str(cta_str)) {
		print_result = asprintf(errmsg, "Invalid CTA: %s\n", cta_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}
	enum cta cta = cta_enum(cta_str);	
	free(cta_str);
	char *column_name=(yyvsp[-3].str);

	(yyval.ce).column=strdup(column_name);
	(yyval.ce).cta=cta;	
	(yyval.ce).arg=(yyvsp[-1].fa);

	free(column_name);

}
#line 1378 "parser.tab.c"
    break;

  case 25: /* col_expr: UNQUOTED_STRING  */
#line 212 "parser.y"
                          {
	enum cta cta=IDENTITY;
	char *column_name=(yyvsp[0].str);

	(yyval.ce).column=strdup(column_name);
	(yyval.ce).cta=cta;	
	(yyval.ce).arg=NULL;

	free(column_name);

}
#line 1394 "parser.tab.c"
    break;

  case 26: /* fn_arg: INTEGER  */
#line 224 "parser.y"
                {
	int value=(yyvsp[0].int_val);

	struct fn_arg *new_arg = malloc(sizeof(struct fn_arg));

	new_arg->value=value;

	(yyval.fa)=new_arg;
}
#line 1408 "parser.tab.c"
    break;

  case 31: /* grouping_expr: col_expr  */
#line 240 "parser.y"
                        {
	struct grouping_expr *new_grouping_expr = malloc(sizeof(struct grouping_expr));

	new_grouping_expr->col_expr=(yyvsp[0].ce);
	new_grouping_expr->next=cgs->layers->groupings;	

	cgs->layers->groupings=new_grouping_expr;
}
#line 1421 "parser.tab.c"
    break;

  case 36: /* collection_expr: col_expr  */
#line 255 "parser.y"
                          {
	struct collection_expr *new_collection_expr = malloc(sizeof(struct collection_expr));

	new_collection_expr->col_expr=(yyvsp[0].ce);
	new_collection_expr->next=cgs->layers->collections;	

	cgs->layers->collections=new_collection_expr;
}
#line 1434 "parser.tab.c"
    break;

  case 37: /* scale_clause: SCALE BY scale_list  */
#line 264 "parser.y"
                                  {}
#line 1440 "parser.tab.c"
    break;

  case 40: /* scale_expr: UNQUOTED_STRING '(' UNQUOTED_STRING ')'  */
#line 269 "parser.y"
                                                    {
	char *scale_str=(yyvsp[-3].str);
	str_tolower(scale_str);
	char *aes_str=(yyvsp[-1].str);
	str_tolower(aes_str);
	int print_result;
	if (!valid_scale_str(scale_str)) {
		print_result = asprintf(errmsg, "Invalid scale type: %s\n", scale_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}	

	enum scale scale = scale_enum(scale_str);
	free(scale_str);
	enum aes aes = aes_enum(aes_str);
	free(aes_str);

	struct scale_expr *new_scale = malloc(sizeof(struct scale_expr));
	new_scale->aes=aes;
	new_scale->scale=scale;

	new_scale->next=cgs->scales;	
	cgs->scales=new_scale;
}
#line 1478 "parser.tab.c"
    break;

  case 41: /* facet_clause: FACET BY facet_list  */
#line 303 "parser.y"
                                  {}
#line 1484 "parser.tab.c"
    break;

  case 44: /* facet_expr: UNQUOTED_STRING direction  */
#line 308 "parser.y"
                                      {
	char *column = (yyvsp[-1].str);
	enum direction facet_direction = (yyvsp[0].direction_enum);

	struct facet_expr *new_facet = malloc(sizeof(struct facet_expr));

	new_facet->column=strdup(column);
	free(column);
	new_facet->direction=facet_direction;	

	new_facet->next=cgs->facets;
	cgs->facets=new_facet;	
}
#line 1502 "parser.tab.c"
    break;

  case 45: /* direction: %empty  */
#line 322 "parser.y"
           { (yyval.direction_enum) = DEFAULT_DIRECTION; }
#line 1508 "parser.tab.c"
    break;

  case 46: /* direction: HORIZONTALLY  */
#line 323 "parser.y"
               { (yyval.direction_enum) = HORIZONTAL_DIRECTION; }
#line 1514 "parser.tab.c"
    break;

  case 47: /* direction: VERTICALLY  */
#line 324 "parser.y"
             { (yyval.direction_enum) = VERTICAL_DIRECTION; }
#line 1520 "parser.tab.c"
    break;

  case 48: /* title_clause: TITLE title_list  */
#line 326 "parser.y"
                               {}
#line 1526 "parser.tab.c"
    break;

  case 51: /* title_expr: UNQUOTED_STRING AS SINGLE_QUOTED_STRING  */
#line 331 "parser.y"
                                                    {
	char *aes_str=(yyvsp[-2].str);
	str_tolower(aes_str);	
	char *title_str=(yyvsp[0].str);
	int print_result;
	if (!valid_aes_str(aes_str)) {
		print_result = asprintf(errmsg, "Invalid aesthetic name: %s\n", aes_str);
		if(print_result == -1) {
			sgl_panic("Memory allocation failed.");
		}
		YYERROR;
	}	

	enum aes aes = aes_enum(aes_str);
	free(aes_str);

	struct title_expr *new_title = malloc(sizeof(struct title_expr));
	new_title->aes=aes;
	new_title->title=strdup(title_str);
	free(title_str);

	new_title->next=cgs->titles;	
	cgs->titles=new_title;
}
#line 1555 "parser.tab.c"
    break;


#line 1559 "parser.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (cgs, errmsg, YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, cgs, errmsg);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp, cgs, errmsg);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (cgs, errmsg, YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, cgs, errmsg);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp, cgs, errmsg);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 356 "parser.y"


void reverse_layers(struct cgs *cgs) {
	struct layer *previous_layer = NULL;
	struct layer *current_layer = cgs->layers;
	struct layer *next_layer;

	struct geom_expr *previous_geom;
	struct geom_expr *current_geom;
	struct geom_expr *next_geom;

	while(current_layer != NULL) {
		previous_geom = NULL;
		current_geom = current_layer->geoms;
		while(current_geom != NULL) {
			next_geom = current_geom->next;	
			current_geom->next = previous_geom;
			previous_geom = current_geom;
			current_geom = next_geom;	
		}	
		current_layer->geoms = previous_geom;

		next_layer = current_layer->next;	
		current_layer->next = previous_layer;
		previous_layer = current_layer;
		current_layer = next_layer;	
	}
	cgs->layers = previous_layer;
}

void sgl_to_cgs(const char *sgl_stmt, struct cgs *cgs, char **errmsg) {
	set_scanner_input(sgl_stmt);
	int parse_result = yyparse(cgs, errmsg);
	reverse_layers(cgs);
	delete_scanner_buffer();

	if (parse_result != 0) {
		reset_scanner_state();
		yyrestart(NULL);
	}
}

void yyerror(struct cgs *cgs, char **errmsg, char const *s) {
	(void)cgs;

	int print_result;
	print_result = asprintf(errmsg, "%s\n", s);
	if(print_result == -1) {
		sgl_panic("Memory allocation failed.");
	}
}
