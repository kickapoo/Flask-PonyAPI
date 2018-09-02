"""
Flask-PonyAPI
-------------

API creation for Pony ORM Entities with no effort.
"""
import re
from setuptools import setup

with open('flask_ponyapi/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name='Flask-PonyAPI',
    version=version,
    url='https://github.com/fuzzyelements/Flask-PonyAPI',
    license='BSD',
    author='Stavros Anastasiadis',
    author_email='anastasiadis.st00@gmail.com',
    description='API creation for Pony ORM Entities with no effort.',
    long_description=__doc__,
    packages=['flask_ponyapi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'Pony'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
