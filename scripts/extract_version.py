# -*- coding: utf-8 -*-
import re
import sys


version_regex = \
   r'[0-9]+\.[0-9]+(\.[0-9]+)?((a|b|rc)[0-9]+)?(\.post[0-9]+)?(\.dev[0-9]+)?'


def extract_version(changelog):
    version = re.search(version_regex, changelog)
    if version:
        print(version.group(0))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        with open('CHANGELOG.md', 'r') as f:
            data = f.read()
    else:
        data = sys.argv[1]

    extract_version(data)
