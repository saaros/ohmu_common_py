"""
ohmu_common_py - sync another project's ohmu_common_py files

Copyright (c) 2016 Ohmu Ltd
See LICENSE for details
"""

import os
import version
import sys


FILES = [
    "ohmu_common_py/logutil.py",
    "ohmu_common_py/pgutil.py",
    "test/test_pgutil.py",
    "version.py",
]


def main(target):
    ver = version.get_project_version("ohmu_common_py/version.py")
    curdir = os.path.dirname(__file__)
    for src_f in FILES:
        with open(os.path.join(curdir, src_f), "r") as fp:
            source = fp.read()
        dst_f = src_f.replace("ohmu_common_py", target)
        dst = os.path.join(curdir, "..", target, dst_f)
        with open(dst, "w") as fp:
            fp.write("# Copied from https://github.com/ohmu/ohmu_common_py {} version {}\n".format(src_f, ver))
            fp.write(source.replace("ohmu_common_py", target))


if __name__ == "__main__":
    main(sys.argv[1])
