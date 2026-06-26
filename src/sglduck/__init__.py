"""sglduck — a Python implementation of the SGL graphics language."""

from . import data
from .db_get_plot import db_get_plot
from .errors import SglError
from .sgl_plot import SglPlot
from .types import type_classifications

__all__ = ["SglError", "SglPlot", "data", "db_get_plot", "type_classifications"]

__version__ = "0.1.0"
