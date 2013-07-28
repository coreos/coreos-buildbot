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

from buildbot.status.web import baseweb

from coreos.buildbot.web.change_hooks import github_resource

class CoreosStatus(baseweb.WebStatus):
    """BuildBot WebStatus w/ CoreOS addons/resources:
        
     /coreos/change_hook/github : Like the normal hook but with features.
    """

    def __init__(self, *args, **kwargs):
        change_hook_dialects = kwargs.get('change_hook_dialects', None)
        self.coreos_github = None
        if change_hook_dialects:
            coreos_github = change_hook_dialects.pop('coreos_github', None)
        super(CoreosStatus, self).__init__(*args, **kwargs)

        if coreos_github:
            resource_obj = github_resource.GithubResource(
                    dialects={'coreos_github': coreos_github})
            self.putChild("coreos/change_hook/github", resource_obj)
