# -*- coding: utf-8 -*-
import sys
from packaging.version import Version


def verify_version_increased(last_version, current_version):
    if current_version <= last_version:
        print('New version needs to be higher than old version')
        sys.exit(1)
    print('yes')
    sys.exit(0)


def verify_version_equals(last_version, current_version):
    if last_version != current_version:
        sys.exit(1)
    sys.exit(0)


def verify_version_nequals(last_version, current_version):
    if last_version != current_version:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    if sys.argv[1] == '--equals':
        verify_version_equals(Version(sys.argv[2]), Version(sys.argv[3]))
    if sys.argv[1] == '--nequals':
        verify_version_equals(Version(sys.argv[2]), Version(sys.argv[3]))
    verify_version_increased(Version(sys.argv[1]), Version(sys.argv[2]))
