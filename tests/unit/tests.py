#!/usr/bin/env python3

import os
import unittest
import sys

doxyqml_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
sys.path.insert(0, doxyqml_path)

from qmlclasstestcase import *
from qmlparsertestcase import *
from lexertestcase import *

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# vi: ts=4 sw=4 et
