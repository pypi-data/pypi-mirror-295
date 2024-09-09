from setuptools import setup, find_packages
classifiers = [
"Development Status :: 5 - Production/Stable",
"Intended Audience :: Science/Research",
"Operating System :: MacOS",
"License :: OSI Approved :: MIT License",
"Programming Language :: Python :: 3",
]

setup(
name="COMSTABPY",
version="0.0.3",
description="ComStabPY is an python package that contains basic functions to apply the unified framework for partitioning the drivers of stability of ecological communities",
long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
long_description_content_type='text/markdown',
url="https://github.com/gocchipintive/COMSTABPY",
author="Guido Occhipinti",
author_email="occhipinti.guido@gmail.com",
license="MIT",
classifiers=classifiers,
keywords="stability, ecology, biodiversity",
packages=find_packages(),
)
