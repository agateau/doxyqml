#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

from doxyqml import doxyqml

setup(name="doxyqml",
    version=doxyqml.VERSION,
    description=doxyqml.DESCRIPTION,
    author="Aurélien Gâteau",
    author_email="agateau@kde.org",
    license="BSD",
    platforms=["any"],
    url="http://agateau.com/projects/doxyqml",
    packages=["doxyqml"],
    scripts=["bin/doxyqml"],
    )
