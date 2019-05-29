from setuptools import setup, find_packages

from wlkernel import __version__


setup(
    name='wlkernel',
    version=__version__,
    description='Weisfeiler-Lehman kernel for RDF graphs',
    packages=find_packages(exclude=['tests']),
)
