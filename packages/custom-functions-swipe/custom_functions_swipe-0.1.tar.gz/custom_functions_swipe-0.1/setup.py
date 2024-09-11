from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
import pybind11
import os
import sys
import subprocess

class build_ext(_build_ext):
    def build_extensions(self):
        # Ensure CMake is in the PATH
        subprocess.check_call(['cmake', '--version'])
        super().build_extensions()

ext_modules = [
    Extension(
        'custom_functions',
        ['source/module/module.cpp'],
        include_dirs=[pybind11.get_include(),  "C:\\Eigen\\"],
        language='c++'
    )
]

setup(
    name='custom_functions_swipe',
    version='0.1',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    setup_requires=['pybind11'],
    install_requires=['pybind11'],
    description='A custom functions module built with pybind11',
    author='Himanshu'
)
