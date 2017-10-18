#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Invoke tasks. To run a task, run ``$ invoke <COMMAND>``. To see a list of
commands, run ``$ invoke --list``.
"""

import os
import sys
import json
import platform
import subprocess
import logging
from time import sleep
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
        inv requirements
    """

    req_file = os.path.join(HERE, 'requirements.txt')
    cmd = bin_prefix('pip install --exists-action w --upgrade -r {} '.format(req_file))
    ctx.run(cmd, echo=True)

@task
def test_module(ctx, module=None, numprocesses=None, params=None):
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
    modules = [module] if isinstance(module, str) else module
    args.extend(modules)
    if params:
        params = [params] if isinstance(params, str) else params
        args.extend(params)
    retcode = pytest.main(args)
    sys.exit(retcode)

@task
def test_travis(ctx, verbose=False):
    print('Testing modules in "{}"'.format('tests'))
    test_module(ctx, module=['tests'], numprocesses=1)
