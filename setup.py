#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='fedimint-helper',
      version='1.0',
      # Modules to import from other scripts:
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # Executables
      scripts=["faucet.py"],
     )