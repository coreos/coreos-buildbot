#!/usr/bin/python

from distutils.core import setup

setup(
    name='coreos-buildbot',
    version='0.0.1',
    description='Tools and modules for CoreOS BuildBots',
    author='Michael Marineau',
    author_email='michael.marineau@coreos.com',
    url='https://github.com/coreos/coreos-buildbot',
    packages=[
        'coreos',
        'coreos.buildbot',
        'coreos.buildbot.web',
        'coreos.buildbot.web.change_hooks',
        'coreos.tests',
    ],
)
