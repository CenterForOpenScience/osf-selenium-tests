#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Invoke tasks. To run a task, run ``$ invoke <COMMAND>``. To see a list of
commands, run ``$ invoke --list``.
"""

import os
import sys
import logging
from invoke import task


logging.getLogger('invoke').setLevel(logging.CRITICAL)

HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BIN_PATH = os.path.dirname(sys.executable)

bin_prefix = lambda cmd: os.path.join(BIN_PATH, cmd)

@task(aliases=['flake8'])
def flake(ctx):
    ctx.run('flake8 .', echo=True)

@task(aliases=['autopep8'])
def autopep(ctx):
    ctx.run('autopep8 .', echo=True)

@task
def clean(ctx, verbose=False):
    ctx.run('find . -name "*.pyc" -delete', echo=True)

@task(aliases=['req'])
def requirements(ctx, dev=False):
    """Install python dependencies.

    Examples:
        invoke requirements
    """

    req_file = os.path.join(HERE, 'requirements.txt')
    cmd = bin_prefix('pip install --exists-action w --upgrade -r {} '.format(req_file))
    ctx.run(cmd, echo=True)

@task
def test_module(ctx, module=None, numprocesses=1, params=['--reruns', '3']):
    """Helper for running tests.
    """
    import pytest
    if not numprocesses:
        from multiprocessing import cpu_count
        numprocesses = cpu_count()
    # NOTE: Subprocess to compensate for lack of thread safety in the httpretty module.
    # https://github.com/gabrielfalcao/HTTPretty/issues/209#issue-54090252
    args = ['-s', '-v']
    if numprocesses > 1:
        args += ['-n {}'.format(numprocesses), '--max-slave-restart=0']

    for e in [module, params]:
        if e:
            args.extend([e] if isinstance(e, str) else e)

    retcode = pytest.main(args)
    sys.exit(retcode)

@task
def test_travis_safari(ctx, numprocesses=None):
    """
    Run tests on the latest Safari
    """
    flake(ctx)
    print('Testing modules in "{}" in Safari'.format('tests'))
    test_module(ctx)

@task
def test_travis_chrome(ctx, numprocesses=None):
    """
    Run tests on the latest Chrome
    """
    flake(ctx)
    print('Testing modules in "{}" in Chrome'.format('tests'))
    test_module(ctx)

@task
def test_travis_edge(ctx, numprocesses=None):
    """
    Run tests on the latest Edge
    """
    flake(ctx)
    print('Testing modules in "{}" in Edge'.format('tests'))
    test_module(ctx)

@task
def test_travis_firefox(ctx, numprocesses=None):
    """
    Run tests on the latest Firefox
    """
    flake(ctx)
    print('Testing modules in "{}" in Firefox'.format('tests'))
    test_module(ctx)

@task
def test_travis_msie(ctx, numprocesses=None):
    """
    Run tests on the latest Microsoft Internet Explorer
    """
    flake(ctx)
    print('Testing modules in "{}" in MSIE'.format('tests'))
    test_module(ctx)

@task
def test_travis_android(ctx, numprocesses=None):
    """
    Run tests on Android 7.0, Samsung Galaxy S8
    """
    flake(ctx)
    print('Testing modules in "{}" in android'.format('tests'))
    test_module(ctx)

@task
def test_travis_ios(ctx, numprocesses=None):
    """
    Run tests on ios 10.0, iPhone 7
    """
    flake(ctx)
    print('Testing modules in "{}" on ios'.format('tests'))
    test_module(ctx)

@task
def test_travis_on_prod(ctx, numprocesses=None):
    """
    Runs targeted prod smoke tests on the latest Chrome
    """
    flake(ctx)
    print('Testing modules in "{}" in Chrome'.format('tests'))
    test_module(ctx, module=['-m','smoke_test'])
