r"""
# OGRePy: An Object-Oriented General Relativity Package for Python
v1.1.0 (2024-09-08)

By **Barak Shoshany**\
Email: <baraksh@gmail.com>\
Website: <https://baraksh.com/>\
GitHub: <https://github.com/bshoshany>

GitHub repository: <https://github.com/bshoshany/OGRePy>\
PyPi project: <https://pypi.org/project/OGRePy/>

Based on the Mathematica package [OGRe](https://github.com/bshoshany/OGRe) by Barak Shoshany.

Copyright (c) 2024 [Barak Shoshany](https://baraksh.com/). Licensed under the [MIT license](https://github.com/bshoshany/OGRePy/blob/master/LICENSE.txt).

If you use this package in published software or research, please provide a link to [the GitHub repository](https://github.com/bshoshany/OGRePy) in the source code and documentation.
"""

# Import SymPy (for convenience, so we don't have to import it to the notebook separately).
import sympy as s

# Import all public OGRePy objects.
from ._core import Coordinates, CovariantD, Metric, OGRePyError, PartialD, Tensor, __version__, calc, diag, doc, func, info, options, release_date, sym, syms, update_check, welcome

# The names that will be exported if using `from OGRePy import *`. Contains exactly all the names imported above.
__all__: list[str] = ["s", "Coordinates", "CovariantD", "Metric", "OGRePyError", "PartialD", "Tensor", "__version__", "calc", "diag", "doc", "func", "info", "options", "release_date", "sym", "syms", "update_check", "welcome"]
