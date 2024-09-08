import sys

from setuptools import setup

if sys.version_info[1] > 12:
    setup()
else:
    from setuptools.glob import glob
    from mypyc.build import mypycify
    files = glob('src/**/*.py', recursive=True)
    setup(ext_modules=mypycify(files))
