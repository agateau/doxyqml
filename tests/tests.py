import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "doxyqml"))

from qmlfunctiontestcase import QmlFunctionTestCase

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# vi: ts=4 sw=4 et
