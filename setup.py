#!/usr/bin/env python

# Script information for the file.
__author__ = "Hendrix Demers"
__email__ = "hendrix.demers@mail.mcgill.ca"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2015 Hendrix Demeners"
__license__ = ""

# Standard library modules.
import os
import zipfile
from distutils.cmd import Command

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

class TestDataCommand(Command):

    description = "create a zip of all files in the testData folder"
    user_options = [('dist-dir=', 'd',
                     "directory to put final built distributions in "
                     "[default: dist]"), ]

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

    def run(self):
        if not os.path.isdir(self.dist_dir):
            os.makedirs(self.dist_dir)

        basepath = os.path.dirname(__file__)
        testdatapath = os.path.join(basepath, 'testData')

        zipfilename = self.distribution.get_fullname() + '-testData.zip'
        zipfilepath = os.path.join(self.dist_dir, zipfilename)
        with zipfile.ZipFile(zipfilepath, 'w') as z:
            for root, _dirs, files in os.walk(testdatapath):
                for file in files:
                    filename = os.path.join(root, file)
                    arcname = os.path.relpath(filename, basepath)
                    z.write(filename, arcname)

setup(name="pySpectrumAnalyzer",
      version='0.1',
      url='',
      description="",
      author="Hendrix Demers",
      author_email="hendrix.demers@mail.mcgill.ca",
      license="",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],

      packages=find_packages(),

      include_package_data=False, # Do not include test data

      install_requires=['numpy',
                        'scipy',
                        'matplotlib',
                        #'PySide',
                        'Pillow',
                        'six',
                        ],
      setup_requires=['nose', 'coverage'],

      test_suite='nose.collector',

      cmdclass={'zip_testdata': TestDataCommand},
)

