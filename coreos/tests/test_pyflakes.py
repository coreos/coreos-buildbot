# Copyright (C) 2013 The CoreOS Authors.
#
# This program is free software; you can redistribute it and/or modify it under
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import ast
import os

from pyflakes import checker
from twisted.python import log
from twisted.trial import unittest

import coreos

class PyFlakesTestCase(unittest.TestCase):

    def test_coreos(self):
        warnings = 0
        pkg_path = os.path.dirname(coreos.__file__)

        for dir_path, dir_names, file_names in os.walk(pkg_path):
            for file_name in file_names:
                if not file_name.endswith('.py'):
                    continue
                file_path = os.path.join(dir_path, file_name)
                warnings += self._checkPySource(file_path)

        self.failIf(warnings, "pyflakes found %d problems" % warnings)

    def _checkPySource(self, file_path):
        with open(file_path) as file_obj:
            tree = ast.parse(file_obj.read(), file_path)

        warnings = checker.Checker(tree, file_path)
        warnings.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        # Log individual errors so we see them all instead of just the first
        for msg in warnings.messages:
            log.err(self.failureException("pyflakes: %s" % (msg,)))

        return len(warnings.messages)
