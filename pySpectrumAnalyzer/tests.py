#!/usr/bin/env python
"""Regression testing for the project."""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2183 $"
__svnDate__ = "$Date: 2011-01-31 16:11:43 -0500 (Mon, 31 Jan 2011) $"
__svnId__ = "$Id: tests.py 2183 2011-01-31 21:11:43Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import DrixUtilities.Testings as Testings

# Globals and constants variables.

if __name__ == "__main__":
    # todo: Correct import errors to be able to use --cover-inclusive option.
    Testings.runTestSuiteWithoutCoverage()
