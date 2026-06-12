"""Semantic validation of the pgs object graph.

``validate_semantics`` runs every check over a pgs and its per-layer
DataFrames, raising ``SglError`` on the first violation. Each per-concern
``valid_*`` module mirrors the corresponding rsgl validation file.
"""

from .valid_aesthetics import valid_aesthetics
from .valid_collections import valid_collections
from .valid_column_classes import valid_column_class, valid_column_classes
from .valid_column_refs import valid_column_refs
from .valid_ctas import valid_ctas
from .valid_facet import valid_facet
from .valid_groupings import valid_groupings
from .valid_layering import valid_layering
from .valid_qualifier import valid_box_direction, valid_qualifier
from .valid_scales import valid_scales
from .valid_titles import valid_titles
from .validate_semantics import validate_semantics

__all__ = [
    "validate_semantics",
    "valid_aesthetics",
    "valid_box_direction",
    "valid_collections",
    "valid_column_class",
    "valid_column_classes",
    "valid_column_refs",
    "valid_ctas",
    "valid_facet",
    "valid_groupings",
    "valid_layering",
    "valid_qualifier",
    "valid_scales",
    "valid_titles",
]
