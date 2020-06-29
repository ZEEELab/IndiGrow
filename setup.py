from setuptools import setup, find_packages

REQUIRED = ['python-igraph', 'numpy', 'scipy', 'six']

setup(
    name='IndiGrow',
    version='0.0.1',
    packages=find_packages(),
    install_requires=REQUIRED
)