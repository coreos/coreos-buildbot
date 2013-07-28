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

import re
from twisted.python import log
from dateutil.parser import parse as dateparse

try:
    import json
    assert json
except ImportError:
    import simplejson as json


DEFAULT_OPTIONS = {
        'include_tags': False,
        'include_copies': False,
}

def getChanges(request, options=None):
    """
    Responds only to POST events and starts the build process

    :arguments:
        request
            the http request object
    """
    # options may be None or True, both mean to use default values
    if not isinstance(options, dict):
        options = {}

    for name, value in DEFAULT_OPTIONS.iteritems():
        options.setdefault(name, value)

    payload = json.loads(request.args['payload'][0])
    user = payload['repository']['owner']['name']
    repo = payload['repository']['name']
    repo_url = payload['repository']['url']
    raw_project = request.args.get('project', None)
    project = raw_project[0] if raw_project is not None else ''
    # This field is unused:
    #private = payload['repository']['private']
    changes = process_change(payload, user, repo, repo_url, project, options)
    log.msg("Received %s changes from github" % len(changes))
    return (changes, 'git')


def process_change(payload, user, repo, repo_url, project, options):
    """
    Consumes the JSON as a python object and actually starts the build.

    :arguments:
        payload
            Python Object that represents the JSON sent by GitHub Service
            Hook.
    """
    commits = list(payload['commits'])
    head_commit = payload.get('head_commit', None)
    newrev = payload['after']
    refname = payload['ref']

    ref_re = r'^refs\/(heads\/(?P<branch>.+)|(?P<tag>tags\/.+))$'
    match = re.match(ref_re, refname)
    if not match:
        log.msg("Ignoring refname `%s': Unknown ref type" % refname)
        return []

    elif re.match(r"^0*$", newrev):
        log.msg("Ignoring refname `%s': Deleted" % refname)
        return []

    elif options['include_tags'] and match.group('tag'):
        branch = match.group('tag')

        # Tags most likely don't contain new commits
        if not commits and head_commit:
            commits.append(head_commit)

    elif match.group('branch'):
        branch = match.group('branch')

        # Optionally allow copied branches
        if options['include_copies'] and not commits and head_commit:
            commits.append(head_commit)

    else:
        log.msg("Ignoring refname `%s': Not a branch" % refname)
        return []

    return [process_commit(c, branch, repo_url, project) for c in commits]


def process_commit(commit, branch, repo_url, project):
    """
    Translates the JSON python object to a change dict.

    :arguments:
        commit
            Object from the commits list or head_commit in the payload.
        branch
            Branch name previously parsed from the payload.
    """
    files = []
    if 'added' in commit:
        files.extend(commit['added'])
    if 'modified' in commit:
        files.extend(commit['modified'])
    if 'removed' in commit:
        files.extend(commit['removed'])
    when_timestamp = dateparse(commit['timestamp'])

    log.msg("New revision: %s" % commit['id'][:8])
    change = {
        'author': '%s <%s>' % (
            commit['author']['name'], commit['author']['email']
        ),
        'files': files,
        'comments': commit['message'],
        'revision': commit['id'],
        'when_timestamp': when_timestamp,
        'branch': branch,
        'revlink': commit['url'],
        'repository': repo_url,
        'project': project
    }

    return change
