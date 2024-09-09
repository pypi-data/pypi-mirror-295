from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = ''

# Setting up
setup(
    name="vis-calendar009",
    version=VERSION,
    author="Omer Cakir",
    author_email="<omercakir2323@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['calendar',],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)