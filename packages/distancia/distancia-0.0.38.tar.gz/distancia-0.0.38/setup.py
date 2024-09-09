import setuptools
#from setuptools import setup, Extension,find_packages

from distutils.core import setup, Extension

from Cython.Build import cythonize

#ext_modules = cythonize([Extension("distancia.distance", ["distancia/distance.py"])])
    
with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
#setup(
    
    #ext_modules=ext_modules,

    name="distancia", # Replace with your username

    version="0.0.38",

    author="Yves Mercadier",

    author_email="",

    description="distance metrics",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://pypi.org/project/distancia/",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.0',

)
