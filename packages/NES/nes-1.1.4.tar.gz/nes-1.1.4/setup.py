#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup
from nes import __version__


# Get the version number from the relevant file
version = __version__

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='NES',
    # license='',
    # platforms=['GNU/Linux Debian'],
    version=version,
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carles Tena Medina, Alba Vilanova Cortezon",
    author_email='carles.tena@bsc.es, alba.vilanova@bsc.es',
    url='https://earth.bsc.es/gitlab/es/NES',

    keywords=['Python', 'NetCDF4', 'Grib2', 'Earth'],
    install_requires=[
        'configargparse',
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ],
    package_data={'': [
        'README.rst',
        'CHANGELOG.rst',
        'LICENSE',
    ]
    },

    # entry_points={
    #     'console_scripts': [
    #         'NetCDF_mask = snes.netCDF_mask:run',
    #     ],
    # },
)
