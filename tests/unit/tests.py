#!/usr/bin/env python3
import os
import sys
import unittest


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    args = [sys.argv[0]] + ["discover", "--start-directory", current_dir, "--pattern", "*testcase.py"] + sys.argv[1:]
    unittest.main(module=None, argv=args)
# vi: ts=4 sw=4 et
