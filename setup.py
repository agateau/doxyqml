#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup

from doxyqml import doxyqml

setup(name="doxyqml",
    version=doxyqml.VERSION,
    description=doxyqml.DESCRIPTION,
    author="Aurélien Gâteau",
    author_email="mail@agateau.com",
    license="BSD",
    platforms=["any"],
    url="http://agateau.com/projects/doxyqml",
    packages=["doxyqml"],
    scripts=["bin/doxyqml"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
    ]
)
