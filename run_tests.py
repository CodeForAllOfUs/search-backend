#!/usr/bin/env python3

import os
import sys
import argparse

import django
from django.conf import settings
from django.test.utils import get_runner

from tests.global_vars import drivers, display, remote_selenium
from tools.net_tools import get_network_ip


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '{ip}:{port}'.format(ip=get_network_ip(), port='9000-9100')

def parse_args():
    bool_choices = ['yes', 'no']
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter): pass

    parser = argparse.ArgumentParser(
            description='Run server-side and/or selenium tests.',
            formatter_class=CustomFormatter,
    )
    parser.add_argument('--unit',
            choices=bool_choices,
            nargs='?', const='yes', default='yes',
            help='Add unit tests to the run queue.'
    )
    parser.add_argument('--functional',
            choices=bool_choices,
            nargs='?', const='yes', default='yes',
            help='Add functional tests to the run queue.'
    )
    parser.add_argument('--acceptance',
            dest='acceptance',
            choices=bool_choices,
            nargs='?', const='yes', default='no',
            help='Add Selenium tests to the run queue.'
    )
    return parser.parse_args()

def add_selenium_drivers():
    drivers.add_firefox('ff', remote=remote_selenium, platform='LINUX')
    drivers.add_chrome('ch',  remote=remote_selenium, platform='LINUX')

def main():
    args = parse_args()
    test_labels = []

    for test_type in ['unit', 'functional', 'acceptance']:
        if getattr(args, test_type) == 'yes':
            if test_type == 'acceptance':
                add_selenium_drivers()
            test_labels.append('tests.tests_{}'.format(test_type))

    if not test_labels:
        print('No tests were configured to run. Exiting...')
        sys.exit(1)

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(test_labels)

    if display:
        display.stop()
    drivers.quit()
    sys.exit(bool(failures))

if __name__ == '__main__':
    main()
