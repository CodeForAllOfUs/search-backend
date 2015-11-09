#!/usr/bin/env python3

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

import tests.global_vars as global_vars
from tools.net_tools import get_network_ip


os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '{ip}:{port}'.format(ip=get_network_ip(), port='9000-9100')

if __name__ == '__main__':
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])

    global_vars.drivers.close()

    if not global_vars.remote_selenium:
        global_vars.display.stop()

    sys.exit(bool(failures))
