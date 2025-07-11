# src/path_comment/__about__.py
"""Package metadata such as version information.

This file is generated automatically by *setuptools-scm* during the
build process. Apart from adding this explanatory docstring, **do not**
edit the content manually, as it will be overwritten the next time the
version is bumped.
"""

# file generated by setuptools-scm – don't change, don't track in VCS

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, Union

    VERSION_TUPLE = Tuple[Union[int, str], ...]
else:
    VERSION_TUPLE = object

__version__ = "0.1.dev4+g19f384.d20250612"
__version_tuple__: VERSION_TUPLE = (0, 1, "dev4", "g19f384.d20250612")

# For backward compatibility
version = __version__
version_tuple = __version_tuple__
