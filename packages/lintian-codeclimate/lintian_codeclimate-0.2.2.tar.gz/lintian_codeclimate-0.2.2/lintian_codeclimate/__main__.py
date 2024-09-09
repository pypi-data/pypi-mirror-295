# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Module execution interface for lintian-codeclimate.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import sys

from .parser import main

if __name__ == "__main__":
    sys.exit(main())
