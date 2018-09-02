#!/usr/bin/env python3

from setuptools import setup

from doxyqml import __version__, DESCRIPTION

setup(name="doxyqml",
    version=__version__,
    description=DESCRIPTION,
    author="Aurélien Gâteau",
    author_email="mail@agateau.com",
    license="BSD",
    platforms=["any"],
    url="http://agateau.com/projects/doxyqml",
    packages=["doxyqml"],
    entry_points={
        "console_scripts": [
            "doxyqml = doxyqml.main:main",
        ],
    },
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
