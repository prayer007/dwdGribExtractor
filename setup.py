from setuptools import setup, find_packages
import dwdGribExtractor

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='dwdGribExtractor',
    version=dwdGribExtractor.__version__,
    author='Manuel Strohmaier',
    author_email='manuel.strohmaier@joanneum.at',
    description="API for DWD's open weather grib data.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://www.joanneum.at/",
    project_urls={
        'Documentation': 'https://www.joanneum.at/',
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.25.1',
        'multiprocess>=0.70.11.1',
        'xarray>=0.16.2',
        'pandas>=1.2.0',
        'cfgrib>=0.9.9.0',
        'eccodes>=1.2.0',
        'netCDF4>=1.5.6' 
    ]
)