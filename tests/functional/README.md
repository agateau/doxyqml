# Doxyqml functional tests

## Running tests

To run functional tests, run `tests.py` or `tests.py test_id`, where `test_id` is the name of a
directory in `tests/functional`.

## Adding tests

Functional tests are defined by creating a new test directory in
`tests/functional`.

Assuming you want to create a new test called "foo", you would have to create
the following:

```
foo/
  input/
    MyFile.qml
  expected/
    MyFile.qml.cpp
  args.json
```

`input/MyFile.qml` contains the QML code to feed to Doxyqml.

`expected/MyFile.qml.cpp` contains the expected generated C++ code.

`args.json` is an optional file. If it exists it must contain an array of
command line arguments to pass to Doxyqml.

### Generating the expected code

`tests.py` can generate `expected/MyFile.qml.cpp` for you by running it
with the `-u` option:

```
./tests.py -u foo
```
