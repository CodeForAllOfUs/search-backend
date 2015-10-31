#!/usr/bin/env python3

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

import tests.global_vars as global_vars
from tools.net_tools import get_network_ip


SERVER_PORT = int(os.environ.get('PORT', 9000))

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '{ip}:{port}'.format(ip=get_network_ip(), port=SERVER_PORT)

if __name__ == '__main__':
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])

    if not global_vars.remote_selenium:
        global_vars.display.stop()

    sys.exit(bool(failures))
