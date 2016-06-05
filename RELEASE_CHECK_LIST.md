Update NEWS:

    r!git log --pretty=format:'- \%s (\%an)' x.y.z-1..HEAD

Bump version number in doxyqml/doxyqml.py

Commit

Create tarball:

    ./setup.py sdist --formats=bztar

Install tarball in virtual env:

    virtualenv --python python3 /tmp/doxyqml
    . /tmp/doxyqml/bin/activate
    cd /tmp/doxyqml
    tar xf doxyqml-$version.tar.bz2
    cd doxyqml-$version
    ./setup.py install

Run unit tests:

    ./tests/unit/tests.py

Run functional tests:

    ./tests/functional/tests.py

If ok, create "x.y.z" tag:

    git tag -a x.y.z

Push:

    git push
    git push --tags

Publish on PyPI:

    ./setup.py sdist --formats=bztar upload

Update project page

Blog
