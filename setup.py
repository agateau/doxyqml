#!/usr/bin/env python3
import os

from setuptools import setup

from doxyqml import __version__, DESCRIPTION


def read_readme():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root_dir, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(name="doxyqml",
      version=__version__,
      description=DESCRIPTION,
      long_description=read_readme(),
      long_description_content_type="text/markdown",
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
      ])
