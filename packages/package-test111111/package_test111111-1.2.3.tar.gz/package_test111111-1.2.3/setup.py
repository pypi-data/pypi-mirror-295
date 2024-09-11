import json
from codecs import open
from os import path

from setuptools import setup

SCRIPT_DIR = path.abspath(path.dirname(__file__))

with open(path.join(SCRIPT_DIR, 'package.json'), encoding='utf-8') as f:
    package_json = json.load(f)

package_name = package_json['name']
package_version = package_json['version']
package_description = package_json['description']
package_url = package_json['url']
package_author_name = package_json['author_name']
package_author_email = package_json['author_email']

with open(path.join(SCRIPT_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    python_requires='>=2',
    version=package_version,
    description=package_description,
    long_description_content_type='text/markdown',
    long_description=long_description,
    url=package_url,
    author=package_author_name,
    author_email=package_author_email,
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
    packages=[package_name],
    setup_requires=['requests'],
    install_requires=['requests']
)
