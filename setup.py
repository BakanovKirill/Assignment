__author__ = 'feanor'
from setuptools import setup, find_packages

setup(
    name = "watermarking",
    version = "1.0",
    url = 'https://github.com/BakanovKirill/Watermarking',
    license = 'BSD',
    description = "A test project for PayLogic.",
    author = 'Kirill Bakanov',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)