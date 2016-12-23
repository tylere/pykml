import sys, os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.1.2'

setup(
    name='pykml',
    version=version,
    packages=['pykml',],
    package_dir={'': 'src'},
    package_data={
        'pykml': [
            'schemas/*.xsd',
            'test/*.py',
            'test/testfiles/*.kml',
            'test/testfiles/google_kml_developers_guide/*.kml',
            'test/testfiles/google_kml_tutorial/*.kml',
        ],
    },
    install_requires=[
        'lxml>=2.2.6',
    ],
    tests_require=['nose'],
    description="Python KML library",
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='kml',
    author='Tyler Erickson',
    author_email='tylerickson@gmail.com',
    url='http://pypi.python.org/pypi/pykml',
    license='BSD',
    long_description="""\
=========
pyKML
=========
pyKML is a Python package for parsing and authoring KML documents. It is based
on the lxml.objectify API (http://codespeak.net/lxml/objectify.html) which
provides Pythonic access to XML documents.

.. figure:: http://pykml.googlecode.com/hg/docs/source/logo/pyKML_logo_200x200.png
   :scale: 100 %
   :alt: pyKML logo

See the Package Documentation for information on installation and usage.
""",
    entry_points = {
        'console_scripts': [
            'kml2pykml = pykml.factory:kml2pykml',
            'csv2kml = pykml.util:csv2kml',
            'validate_kml = pykml.parser:validate_kml',
        ],
    }
)
