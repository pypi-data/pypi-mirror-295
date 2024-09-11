from setuptools import setup, find_packages
from pathlib import Path
import codecs
import os

VERSION = '0.1.6'
DESCRIPTION = 'E-Commerce platform API'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name="whalegistic",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="<Whalegistic>",
    author_email="<info@whalegistic.com>",
    license='ISC',
    packages=find_packages(),
    install_requires=["pyjwt", "asyncio", "httpx"],
    keywords="e-commerce, products, webstores, orders, pim, warehouse",
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)