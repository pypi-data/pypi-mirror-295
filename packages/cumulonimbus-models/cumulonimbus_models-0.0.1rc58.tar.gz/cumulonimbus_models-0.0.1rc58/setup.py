import sys

from setuptools import Extension, setup

from setuptools.glob import glob
from mypyc.build import mypycify

files = glob('src/**/*.py', recursive=True)
mypycify_extensions = mypycify(files)
setup(ext_modules=mypycify(files))
