"""
ohmu_common_py - fileutil tests

Copyright (c) 2016 Ohmu Ltd
See LICENSE for details
"""
from ohmu_common_py import fileutil
import datetime
import json


def test_json_serialization(tmpdir):
    ob = {
        "foo": [
            "bar",
            "baz",
            42,
        ],
        "t": datetime.datetime(2015, 9, 1, 4, 0, 0),
        "f": 0.42,
    }
    res = json.dumps(ob, default=fileutil.default_json_serialization, separators=(",", ":"), sort_keys=True)
    assert res == '{"f":0.42,"foo":["bar","baz",42],"t":"2015-09-01T04:00:00Z"}'

    assert isinstance(fileutil.json_encode(ob), str)
    assert isinstance(fileutil.json_encode(ob, binary=True), bytes)
    assert "\n" not in fileutil.json_encode(ob)
    assert "\n" in fileutil.json_encode(ob, compact=False)

    output_file = tmpdir.join("test.json").strpath
    fileutil.write_json_file(output_file, ob)
    with open(output_file, "r") as fp:
        ob2 = json.load(fp)
    ob_ = dict(ob, t=ob["t"].isoformat() + "Z")
    assert ob2 == ob_

    fileutil.write_json_file(output_file, ob, compact=True)
    with open(output_file, "r") as fp:
        output_data = fp.read()
    assert "\n" not in output_data
    ob2_ = json.loads(output_data)

    assert ob2 == ob2_
