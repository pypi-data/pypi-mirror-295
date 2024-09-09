import os

import rtoml
from setuptools.glob import glob
from mypyc.build import mypycify


files = glob('src/**/*.py', recursive=True)
all_mypyc_extension_data = mypycify(files)
curdir = os.getcwd()
def get_v(k, v):

    if k in ('sources', 'include-dirs', 'depends'):
        return [f'{curdir}/{src}' for src in v]
    else:
        return v
mypyc_extension_data = [
    {k.replace('_','-'): get_v(k, v) for k, v in ext.__dict__.items() if v is not None and v != []}
    for ext in all_mypyc_extension_data
]

ext_data = {
    'tool': {
        'setuptools': {
            'ext-modules': mypyc_extension_data
        }
    }
}

with open('pyproject.base.toml', 'r') as f:
    base_data = f.read()
toml_data = rtoml.dumps(ext_data)
with open('pyproject.toml', 'w') as f:
    f.write(base_data)
    f.write(toml_data)
