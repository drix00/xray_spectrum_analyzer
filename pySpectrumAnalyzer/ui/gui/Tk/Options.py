#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2937 $"
__svnDate__ = "$Date: 2014-09-01 10:20:37 -0400 (Mon, 01 Sep 2014) $"
__svnId__ = "$Id: Options.py 2937 2014-09-01 14:20:37Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
UI_TK = "Tk"

class Options(object):
        def __init__(self, args=None, configurationFile=None):
                # TODO: Allow configurationFile to be either a filename string or a list of filename string.

                # Set default options.
                self._ui = UI_TK

        def getUI(self):
                return self._ui

if __name__ == '__main__': #pragma: no cover
        import DrixUtilities.Runner as Runner
        Runner.Runner().run(runFunction=None)
