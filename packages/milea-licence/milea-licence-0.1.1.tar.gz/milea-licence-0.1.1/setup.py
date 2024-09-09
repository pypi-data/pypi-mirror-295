
from setuptools import find_packages, setup

setup(
    name='milea-licence',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['milea_base>=0.4'],
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    description='Milea Framework - Milea Licence Module',
    license='MIT',
)
