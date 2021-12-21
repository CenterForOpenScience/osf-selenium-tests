#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Invoke tasks. To run a task, run ``$ invoke <COMMAND>``. To see a list of
commands, run ``$ invoke --list``.
"""

import glob
import logging
import os
import sys

from invoke import task


logging.getLogger('invoke').setLevel(logging.CRITICAL)

HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BIN_PATH = os.path.dirname(sys.executable)
bin_prefix = lambda cmd: os.path.join(BIN_PATH, cmd)
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))


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
def test_module_wo_exit(ctx, module=None, params=None):
    """Helper for running tests."""
    import pytest

    if params is None:
        params = []

    args = ['-s', '-v', '--tb=short']
    for e in [module, params]:
        if e:
            args.extend([e] if isinstance(e, str) else e)

    print('>>> pytest args: {}'.format(args))
    retcode = pytest.main(args)
    return retcode


@task
def test_module(ctx, module=None, params=None):
    """Helper for running tests."""
    retcode = test_module_wo_exit(ctx, module, params)
    sys.exit(retcode)


@task
def test_selenium_on_prod(ctx):
    """
    Runs targeted prod smoke tests on the latest Chrome
    """
    flake(ctx)
    print('>>> Testing modules in "{}" in Chrome'.format('tests'))
    test_selenium_with_retries(
        ctx, 'Master', _get_test_file_list(), module=['-m', 'smoke_test']
    )


def _get_test_file_list():
    all_test_files = glob.glob('tests/test_*.py')
    all_test_files.sort()
    return all_test_files


@task
def test_selenium_with_retries(ctx, file_list, module=None):
    """Run group of tests on the browser defined by TEST_BUILD."""
    flake(ctx)

    print('>>> Testing modules in "/tests/" in {}'.format(os.environ['TEST_BUILD']))
    print('>>> File list is: {}'.format(file_list))
    retcode = test_module_wo_exit(ctx, params=file_list, module=module)

    if retcode != 1:
        sys.exit(retcode)

    file_list = ['--last-failed', '--last-failed-no-failures', 'none'] + file_list

    for i in range(1, MAX_RETRIES + 1):
        print(
            '>>> Retesting failures, iteration {}, in "/test/" '
            'in {}'.format(i, os.environ['TEST_BUILD'])
        )
        retcode = test_module_wo_exit(ctx, params=file_list, module=module)

        if retcode != 1:
            break

    sys.exit(retcode)
