# Packaging and installing the library

from setuptools import setup, find_packages

setup(
  name="biginsight",
  version="0.0.33",
  description="Track all user's action on a mobile app and website",
  author="Geottuse",
  author_email="admin@geottuse.com",
  packages=find_packages(),
  install_requires=[], # dependencies
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  python_requires='>=3.9'
)
