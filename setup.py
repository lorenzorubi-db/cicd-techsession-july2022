from setuptools import find_packages, setup
from app import __version__

with open('requirements-unit.txt') as f:
    required = f.read().splitlines()

setup(
    name='cicd_project',
    version=__version__,
    description='Project using Notebooks and IDEA',
    author='Yassine Essawabi',
    packages=find_packages(),
    install_requires=required,
    setup_requires=['wheel'],
)
