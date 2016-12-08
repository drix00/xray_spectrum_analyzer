#!/usr/bin/env python
""" """

###############################################################################
# Copyright 2016 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

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
        import pyHendrixDemersTools.Runner as Runner
        Runner.Runner().run(runFunction=None)
