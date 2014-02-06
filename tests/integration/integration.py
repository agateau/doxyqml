#!/usr/bin/env python

import difflib
import os
import shutil
import sys
import subprocess


class Test(object):
    def __init__(self, name):
        self.name = name
        self.input_dir = os.path.join(self.name, "input")
        self.output_dir = os.path.join(self.name, "output")
        self.expected_dir = os.path.join(self.name, "expected")


    def build(self):
        ok = True
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.mkdir(self.output_dir)

        for name in os.listdir(self.input_dir):
            if not name.endswith(".qml"):
                continue
            out_path = os.path.join(self.output_dir, name + ".cpp")
            with open(out_path, "w") as out:
                ret = subprocess.call(
                    ["doxyqml", name],
                    stdout=out,
                    cwd=self.input_dir)
                if ret != 0:
                    self.error("doxyqml failed on {}".format(name))
                    ok = False
        return ok


    def compare(self):
        lst = os.listdir(self.expected_dir)
        if not lst:
            self.error("expected_dir '{}' is empty".format(self.expected_dir))
            return False

        ok = True
        for name in lst:
            out_path = os.path.join(self.output_dir, name)
            if not os.path.exists(out_path):
                self.error("File {} does not exist".format(out_path))
                ok = False
                continue

            out_lines = open(out_path).readlines()

            expected_path = os.path.join(self.expected_dir, name)
            expected_lines = open(expected_path).readlines()

            delta = difflib.unified_diff(expected_lines, out_lines, fromfile="expected", tofile="output")
            delta_lines = list(delta)
            if delta_lines:
                ok = False
                self.error("Failure on {}".format(name))
                for line in delta_lines:
                    sys.stderr.write(line)
        return ok

    def error(self, msg):
        print("{}: ERROR: {}".format(self.name, msg))


def main():
    os.chdir(os.path.dirname(__file__))

    errors = 0
    for test_dir in os.listdir("."):
        if not os.path.isdir(test_dir):
            continue

        print("Testing {}...".format(test_dir))
        test = Test(test_dir)
        if not (test.build() and test.compare()):
            errors += 1
            continue

    print("")
    if errors:
        print("Failure: {} errors".format(errors))
        return 1
    else:
        print("Success")
        return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
