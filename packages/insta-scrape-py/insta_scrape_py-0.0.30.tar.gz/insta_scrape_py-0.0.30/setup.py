from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.30'
DESCRIPTION = 'A Python package to scrape and download Instagram Reels from any Instagram page.'
LONG_DESCRIPTION = 'insta-scrape-py is a Python package designed to help you easily scrape and download Instagram Reels from any public Instagram page. With simple and efficient functionality, insta-scrape-py allows you to extract Reels links from a page, Downlaod reels and downlaod full page reels by providing the username only.'

setup(
    name="insta-scrape-py",
    version=VERSION,
    author="djalti",
    author_email="abdeldjalilselamnia@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tqdm', 'requests'],
    keywords=['python', 'instagram', 'scrape', 'download', 'reels', 'pages'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)