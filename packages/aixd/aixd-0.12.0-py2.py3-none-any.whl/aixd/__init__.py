"""
********************************************************************************
AI-eXtended Design
********************************************************************************

.. currentmodule:: aixd


.. toctree::
    :maxdepth: 2

    aixd.data
    aixd.mlmodel
    aixd.sampler
    aixd.visualisation

"""

from __future__ import print_function

import os
from aixd.__version__ import __author__, __copyright__, __license__, __author_email__ as __email__, __version__


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))


__all__ = ["HOME", "DOCS", "__author__", "__copyright__", "__license__", "__email__", "__version__"]
