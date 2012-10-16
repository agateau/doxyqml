# Goals

Turns a .qml into something Doxygen can swallow through an input filter.

# Setup

First, make sure doxyqml is in $PATH. For example with:

    ln -s /path/to/doxyqml.py $HOME/bin/doxyqml

Then in your Doxygen file, add .qml files to `FILE_PATTERNS`:

    FILE_PATTERNS = *.qml

And set `FILTER_PATTERNS`:

    FILTER_PATTERNS = *.qml=doxyqml
