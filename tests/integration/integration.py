#!/usr/bin/env python

import difflib
import os
import shutil
import sys
import subprocess


def build(doxyfile_path, input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.copytree(input_dir, output_dir)
    shutil.copy2(doxyfile_path, output_dir)
    subprocess.check_call(["doxygen"], cwd=output_dir)


def compare(output_dir, expected_dir):
    ok = True
    lst = os.listdir(expected_dir)
    assert(lst)
    for name in lst:
        out_path = os.path.join(output_dir, name)
        if not os.path.exists(out_path):
            print("ERROR: File {} does not exist".format(out_path))
            ok = False
            continue

        out_lines = open(out_path).readlines()

        expected_path = os.path.join(expected_dir, name)
        expected_lines = open(expected_path).readlines()

        delta = difflib.unified_diff(expected_lines, out_lines, fromfile="expected", tofile="output")
        delta_lines = list(delta)
        if delta_lines:
            ok = False
            print("ERROR: Failure on {}".format(name))
            for line in delta_lines:
                sys.stderr.write(line)
    return ok


def main():
    os.chdir(os.path.dirname(__file__))
    doxyfile_path = "Doxyfile"

    errors = 0
    for test_dir in os.listdir("."):
        if not os.path.isdir(test_dir):
            continue

        print("Testing {}...".format(test_dir))
        input_dir = os.path.join(test_dir, "input")
        output_dir = os.path.join(test_dir, "output")
        expected_dir = os.path.join(test_dir, "expected")

        build(doxyfile_path, input_dir, output_dir)
        ok = compare(os.path.join(output_dir, "xml"), expected_dir)
        if not ok:
            errors += 1

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
