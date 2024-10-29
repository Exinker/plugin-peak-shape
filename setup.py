from setuptools import find_packages, setup

from src import AUTHOR_EMAIL, AUTHOR_NAME, APPLICATION_DESCRIPTION, APPLICATION_NAME, APPLICATION_VERSION


setup(
    # info
    name=APPLICATION_NAME,
    description=APPLICATION_DESCRIPTION,
    license='MIT',
    keywords=['spectroscopy', 'atomic emission spectroscopy', 'atomic absorption spectroscopy', 'emulation'],

    # version
    version=APPLICATION_VERSION,

    # author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

    # setup directories
    packages=find_packages(),

    # setup data
    package_data={
        '': ['*.txt', '*.xml', '*.csv', '*.md'],
    },

    # requires
    install_requires=[
        item.strip() for item in open('requirements.txt', 'r').readlines()
        if item.strip()
    ],
    python_requires='>=3.12',
)
