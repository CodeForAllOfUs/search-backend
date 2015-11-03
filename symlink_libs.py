#!/usr/bin/env python3

import os
import sys

base_dir = os.path.abspath(os.path.dirname(__file__))

src_backend_libs_base = os.path.abspath(os.path.expanduser('~/codeforallofus-libs/backend'))
src_frontend_libs_base = os.path.abspath(os.path.expanduser('~/codeforallofus-libs/frontend'))

dest_backend_libs_base = os.path.join(base_dir, 'codeforallofus_search')
dest_frontend_libs_base = os.path.join(base_dir, 'codeforallofus_search/search-frontend')

for filename in os.listdir(src_backend_libs_base):
    dest_file = os.path.join(dest_backend_libs_base, filename)
    if not os.path.exists(dest_file):
        os.symlink(os.path.join(src_backend_libs_base, filename), dest_file)
    print('Backend libs copied:')
    print(dest_file)

for filename in os.listdir(src_frontend_libs_base):
    dest_file = os.path.join(dest_frontend_libs_base, filename)
    if not os.path.exists(dest_file):
        os.symlink(os.path.join(src_frontend_libs_base, filename), dest_file)
    print('Frontend libs copied:')
    print(dest_file)

sys.exit(0)
