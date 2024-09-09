from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.0'
DESCRIPTION = 'Library for finding png images within another png image file'

# Setting up
setup(
    name="png_search_multiple",
    version=VERSION,
    author="Scott Blackburn",
    author_email="<sblack777@hotmail.com>",
    description='Library for finding a list of multiple png file images within another a png image file',
    long_description='Library for finding a list of multiple png file images within another a png image file',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['Pillow>=9.1.0'],
    keywords=['python', 'image', 'search', 'png', 'image processing', 'test automation', 'image search'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)