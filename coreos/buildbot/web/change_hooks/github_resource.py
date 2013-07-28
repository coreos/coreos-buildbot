# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

# code inspired/copied from contrib/github_buildbot
#  and inspired from code from the Chromium project
# otherwise, Andrew Melo <andrew.melo@gmail.com> wrote the rest
# but "the rest" is pretty minimal

from buildbot.status.web import change_hook
from twisted.python import log

from coreos.buildbot.web.change_hooks import github

class GithubResource(change_hook.ChangeHookResource):
    """Customized ChangeHookResource for our custom github hook.

    ChangeHookResource only loads from buildbot.status.web.hooks but we
    want our own hook module, not the ones shipped with buildbot.
    """

    def getChanges(self, request):
        changes = []
        src = None

        # For consistency with normal change hooks the config dict
        # dialects is the same format but we only use coreos_github.
        dialect = 'coreos_github'
        if dialect in self.dialects:
            changes, src = github.getChanges(request, self.dialects[dialect])
            log.msg("Got the following changes %s" % changes)
        else:
            log.msg("The coreos_github changehook wasn't whitelisted")
            raise ValueError("The dialect specified wasn't whitelisted")

        return (changes, src)
