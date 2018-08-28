"""
Flask-PonyAPI
-------------

API creation for Pony ORM Entities with no effort.
"""
from setuptools import setup


setup(
    name='Flask-PonyAPI',
    version='0.0.3',
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
    test_suite='test_ponyapi',
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
