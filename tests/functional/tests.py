#!/usr/bin/env python3
# encoding: utf-8

import argparse
import difflib
import json
import os
import shutil
import sys
import subprocess

from doxyqml.main import main as doxyqml_main


def list_files(topdir):
    result = []

    for root, dirs, files in os.walk(topdir):
        for name in files:
            subdir = root[len(topdir) + 1:]
            result.append(subdir and os.path.join(subdir, name) or name)

    return result


class SubprocessRunner:
    def __init__(self, executable):
        self.executable = executable

    def run(self, qml_file, args, stdout, cwd):
        return subprocess.call(
            [self.executable, qml_file] + args,
            stdout=stdout, cwd=cwd)


class ImportRunner:
    def run(self, qml_file, args, stdout, cwd):
        pwd = os.getcwd()
        os.chdir(cwd)
        try:
            return doxyqml_main([qml_file] + args, out=stdout)
        finally:
            os.chdir(pwd)


class Test(object):
    def __init__(self, name, runner):
        self.name = name
        self.runner = runner
        self.input_dir = os.path.join(self.name, "input")
        self.output_dir = os.path.join(self.name, "output")
        self.expected_dir = os.path.join(self.name, "expected")
        self._read_args()

    def _read_args(self):
        args_json = os.path.join(self.name, "args.json")
        if not os.path.exists(args_json):
            self.args = []
            return
        with open(args_json) as f:
            self.args = json.load(f)
            assert type(self.args) is list

    def build(self):
        ok = True
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.mkdir(self.output_dir)

        for name in list_files(self.input_dir):
            if not name.endswith(".qml"):
                continue

            out_path = os.path.join(self.output_dir, name + ".cpp")
            out_dir = os.path.dirname(out_path)

            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)

            with open(out_path, "w") as out:
                ret = self.runner.run(name, args=self.args, stdout=out, cwd=self.input_dir)
                if ret != 0:
                    self.error("doxyqml failed on {}".format(name))
                    ok = False
        return ok

    def update(self):
        if os.path.exists(self.expected_dir):
            shutil.rmtree(self.expected_dir)
        shutil.copytree(self.output_dir, self.expected_dir)

    def compare(self):
        lst = list_files(self.expected_dir)
        if not lst:
            self.error("expected_dir '{}' is empty".format(self.expected_dir))
            return False

        ok = True
        for name in lst:
            if name.startswith("."):
                continue
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
    script_dir = os.path.dirname(__file__) or "."

    default_doxyqml = "doxyqml"

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update",
                        help="Update expected output from test ID", metavar="ID")
    parser.add_argument("--doxyqml", default=default_doxyqml,
                        help="Path to the doxyqml executable ({})".format(default_doxyqml))
    parser.add_argument("test_id", nargs="?",
                        help="Run specified test only")
    parser.add_argument("--import", dest="import_", action="store_true",
                        help="Import Doxyqml module instead of using the executable. Useful for code coverage.")
    args = parser.parse_args()

    if args.import_:
        runner = ImportRunner()
    else:
        runner = SubprocessRunner(args.doxyqml)

    os.chdir(script_dir)

    if args.update:
        print("Updating {}...".format(args.update))
        test = Test(args.update, runner)
        if not test.build():
            return 1
        test.update()
        return 0

    if args.test_id:
        if not os.path.isdir(args.test_id):
            parser.error("Invalid test id '{}'".format(args.test_id))
        test_list = [args.test_id]
    else:
        test_list = [x for x in os.listdir(".") if os.path.isdir(x)]

    errors = 0
    for test_dir in test_list:
        print("Testing {}...".format(test_dir))
        test = Test(test_dir, runner)
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
