Update NEWS:

    r!git log --pretty=format:'- \%s (\%an)' x.y.z-1..HEAD

Bump version number in doxyqml/doxyqml.py

Commit

Create tarball:

    ./setup.py sdist --formats=bztar

Install tarball in virtual env:

    pew mktmpenv
    cd /tmp
    tar xf path/to/doxyqml/dists/doxyqml-$version.tar.bz2
    cd doxyqml-$version
    ./setup.py install

Run unit tests:

    ./tests/unit/tests.py

Run functional tests:

    ./tests/functional/tests.py
    exit

If OK, create "x.y.z" tag:

    git tag -a x.y.z

Push:

    git push
    git push --tags

Publish on PyPI:

    twine upload dists/doxyqml-$version.tar.bz2

Update project page

Blog
