Update NEWS:

    r!git log --pretty=format:'- \%s (\%an)' x.y.z-1..HEAD

Bump version number in doxyqml/doxyqml.py

Commit

Create tarball:

    python setup.py sdist --formats=bztar

Install tarball in virtual env:

    virtualenv /tmp/doxyqml
    . /tmp/doxyqml/bin/activate
    cd /tmp/doxyqml
    tar xf doxyqml-$version.tar.bz2
    cd doxyqml-$version
    python setup.py install

Run unit tests:

    python tests/unit/tests.py

Run functional tests:

    python tests/functional/tests.py

If ok, create "x.y.z" tag:

    git tag -a x.y.z

Push:

    git push
    git push --tags

Publish on PyPI:

    python setup.py sdist --formats=bztar upload

Update project page

Blog
