from setuptools import find_packages, setup
import os.path
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()
    

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
    

setup(
    name='netbox-data',
    version=get_version('netbox_data/version.py'),
    description='A NetBox plugin that gets Netbox data.',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
