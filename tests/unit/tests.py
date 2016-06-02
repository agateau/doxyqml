#!/usr/bin/env python

from __future__ import division, absolute_import, print_function, unicode_literals

import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "doxyqml"))

from qmlclasstestcase import *
from qmlparsertestcase import *

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# vi: ts=4 sw=4 et
