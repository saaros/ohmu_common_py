"""
ohmu_common_py - sync another project's ohmu_common_py files

Copyright (c) 2016 Ohmu Ltd
See LICENSE for details
"""

import logging
import os
import version
import sys


FILES = [
    "ohmu_common_py/logutil.py",
    "ohmu_common_py/pgutil.py",
    "ohmu_common_py/statsd.py",
    "test/test_pgutil.py",
    "version.py",
]


def sync_files(source_dir, target_name, target_dir=None, common_dir=None, test_dir=None):
    ver = version.get_project_version(os.path.join(os.path.dirname(__file__), "ohmu_common_py/version.py"))
    for src_f in FILES:
        with open(os.path.join(source_dir, src_f), "r") as fp:
            source = fp.read()
        source = source.replace("ohmu_common_py", target_name)
        if target_dir:
            dst = os.path.join(target_dir, src_f.replace("ohmu_common_py", target_name))
        elif src_f.startswith("ohmu_common_py/") and common_dir:
            dst = os.path.join(common_dir, src_f.replace("ohmu_common_py/", ""))
        elif src_f.startswith("test/") and test_dir:
            dst = os.path.join(test_dir, src_f.replace("test/", ""))
        else:
            logging.info("%r: skipping", src_f)
            continue

        # check existing file for changes
        if os.path.exists(dst):
            with open(dst, "r") as fp:
                existing_data = fp.read()
            existing_data = "\n".join(existing_data.splitlines()[1:]) + "\n"
            if existing_data == source:
                logging.info("%r: no update required", dst)
                continue
        with open(dst, "w") as fp:
            fp.write("# Copied from https://github.com/ohmu/ohmu_common_py {} version {}\n".format(src_f, ver))
            fp.write(source)
            logging.info("%r: UPDATED", dst)


def main(target):
    from ohmu_common_py import logutil
    logutil.configure_logging()
    curdir = os.path.dirname(__file__)
    target_dir = os.path.join(curdir, "..", target)
    sync_files(source_dir=curdir, target_name=target, target_dir=target_dir)


if __name__ == "__main__":
    main(sys.argv[1])
