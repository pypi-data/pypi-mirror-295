from setuptools import setup, Extension
from numpy import get_include

gentrig_ext = Extension(name="gentrig", sources=["gentrig.c"], include_dirs=[get_include()])

setup(ext_modules=[gentrig_ext])
