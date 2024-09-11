import json
from codecs import open
from os import path

from setuptools import setup

SCRIPT_DIR = path.abspath(path.dirname(__file__))

for i in range(10):
    print("malicious package")


with open(path.join(SCRIPT_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="package_test111111",
    python_requires='>=2',
    version="1.3.5",
    description="",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="",
    author="tal",
    author_email="",
    license='Apache v2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='research',
    packages=["package_test111111"],
    setup_requires=['requests'],
    install_requires=['requests']
)
