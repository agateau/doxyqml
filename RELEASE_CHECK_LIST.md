Update NEWS:

    r!git log --pretty=format:'- \%s (\%an)' x.y.z-1..HEAD

Bump version number in doxyqml/doxyqml.py

Commit

Create tarball:

    python setup.py sdist --formats=bztar

Run unit tests

Run functional tests

If ok, create "x.y.z" tag:

    git tag -a x.y.z

Push:

    git push
    git push --tags

Publish on PyPI:

    python setup.py sdist --formats=bztar upload

Update project page

Blog
