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
MAX_TRAVIS_RETRIES = int(os.getenv('MAX_TRAVIS_RETRIES', 3))


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
def test_module_wo_exit(ctx, module=None, numprocesses=1, params=['--reruns', '1']):
    """Helper for running tests.
    """
    import pytest
    if not numprocesses:
        from multiprocessing import cpu_count
        numprocesses = cpu_count()
    # NOTE: Subprocess to compensate for lack of thread safety in the httpretty module.
    # https://github.com/gabrielfalcao/HTTPretty/issues/209#issue-54090252
    args = ['-s', '-v', '--tb=short']
    if numprocesses > 1:
        args += ['-n {}'.format(numprocesses), '--max-slave-restart=0']

    for e in [module, params]:
        if e:
            args.extend([e] if isinstance(e, str) else e)

    print('>>> pytest args: {}'.format(args))
    retcode = pytest.main(args)
    return retcode

@task
def test_module(ctx, module=None, numprocesses=1, params=['--reruns', '1']):
    """Helper for running tests.
    """
    retcode = test_module_wo_exit(ctx, module, numprocesses, params)
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

@task
def test_travis_failures_only_chrome(ctx, numprocesses=None):
    """
    Run tests on the latest Chrome
    """
    print('Testing modules in "{}" in Chrome'.format('tests'))
    test_module(ctx, params=['--last-failed', '--last-failed-no-failures', 'none'])

@task
def test_travis_failures_only_edge(ctx, numprocesses=None):
    """
    Run tests on the latest Edge
    """
    print('Testing modules in "{}" in Edge'.format('tests'))
    test_module(ctx, params=['--last-failed', '--last-failed-no-failures', 'none'])

@task
def test_travis_failures_only_firefox(ctx, numprocesses=None):
    """
    Run tests on the latest Firefox
    """
    print('Testing modules in "{}" in Firefox'.format('tests'))
    test_module(ctx, params=['--last-failed', '--last-failed-no-failures', 'none'])

@task
def test_travis_part_one(ctx, numprocesses=None):
    """Run first group of tests on the browser defined by TEST_BUILD."""
    flake(ctx)

    part_one_files = ['test_dashboard.py', 'test_institutions.py', 'test_landing.py',
                      'test_login.py', 'test_meetings.py', 'test_my_projects.py',
                      'test_navbar.py']
    part_one_file_names = ['tests/{}'.format(x) for x in part_one_files]

    print('Testing part one modules in "/test/" in {}'.format(os.environ['TEST_BUILD']))
    retcode = test_module_wo_exit(ctx, params=part_one_file_names)

    # retcodes: http://doc.pytest.org/en/latest/usage.html#possible-exit-codes
    if retcode != 1:
        sys.exit(retcode)

    part_one_file_names = ['--last-failed', '--last-failed-no-failures', 'none'] + part_one_file_names

    for i in range(1, MAX_TRAVIS_RETRIES+1):
        print('Retesting part one failures, iteration {}, in "/test/" '
              'in {}'.format(i, os.environ['TEST_BUILD']))
        retcode = test_module_wo_exit(ctx, params=part_one_file_names)
        if retcode != 1:
            break

    sys.exit(retcode)

@task
def test_travis_part_two(ctx, numprocesses=None):
    """Run second group of tests on the browser defined by TEST_BUILD."""
    flake(ctx)

    part_two_files = ['test_preprints.py', 'test_project.py', 'test_project_files.py',
                      'test_quickfiles.py', 'test_register.py', 'test_registries.py',
                      'test_search.py', 'test_user.py']
    part_two_file_names = ['tests/{}'.format(x) for x in part_two_files]

    print('Testing part one modules in "/test/" in {}'.format(os.environ['TEST_BUILD']))
    retcode = test_module_wo_exit(ctx, params=part_two_file_names)

    if retcode != 1:
        sys.exit(retcode)

    part_two_file_names = ['--last-failed', '--last-failed-no-failures', 'none'] + part_two_file_names

    for i in range(1, MAX_TRAVIS_RETRIES+1):
        print('Retesting part two failures, iteration {}, in "/test/" '
              'in {}'.format(i, os.environ['TEST_BUILD']))
        retcode = test_module_wo_exit(ctx, params=part_two_file_names)
        if retcode != 1:
            break

    sys.exit(retcode)
