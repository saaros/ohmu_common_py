"""
ohmu_common_py - json file handling utility functions

Copyright (c) 2015 Ohmu Ltd
See LICENSE for details
"""
import datetime
import json
import os
import tempfile


def default_json_serialization(obj):
    if isinstance(obj, datetime.datetime):
        if obj.tzinfo:
            return obj.isoformat().replace("+00:00", "Z")
        # assume UTC for datetime objects without a timezone
        return obj.isoformat() + "Z"


def json_encode(obj, compact=True, binary=False):
    res = json.dumps(obj,
                     sort_keys=not compact,
                     indent=None if compact else 4,
                     separators=(",", ":") if compact else None,
                     default=default_json_serialization)
    return res.encode("utf-8") if binary else res


def write_json_file(filename, obj, *, compact=False):
    json_data = json_encode(obj, compact=compact)
    dirname, basename = os.path.dirname(filename), os.path.basename(filename)
    fd, tempname = tempfile.mkstemp(dir=dirname or ".", prefix=basename, suffix=".tmp")
    with os.fdopen(fd, "w") as fp:
        fp.write(json_data)
        if not compact:
            fp.write("\n")
    os.rename(tempname, filename)
