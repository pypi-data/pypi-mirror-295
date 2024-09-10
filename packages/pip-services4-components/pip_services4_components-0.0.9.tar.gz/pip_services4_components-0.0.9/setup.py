"""
Pip.Services Components
--------------------

Pip.Services is an open-source library of basic microservices.
pip_services4_components package provides basic abstractions portable across variety of languages.

Links
`````

* `website <http://github.com/pip-services/pip-services>`
* `development version <https://github.com/pip-services4/pip-services4-python/tree/main/pip-services4-components-python>`

"""

from setuptools import setup
from setuptools import find_packages

try:
    readme = open('README.md').read()
except:
    readme = __doc__

setup(
    name='pip_services4_components',
    version='0.0.9',
    url='https://github.com/pip-services4/pip-services4-python/tree/main/pip-services4-components-python',
    license='MIT',
    description='Component definitions for Pip.Services in Python',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'PyYAML >= 6.0, < 7.0',
        'pip_services4_commons >= 0.0.1, < 1.0', 
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
