"""
ohmu_common_py - logutil tests

Copyright (c) 2016 Ohmu Ltd
See LICENSE for details
"""
# pylint: disable=protected-access
from ohmu_common_py import logutil
import logging
import logging.handlers
import os
import pytest


@pytest.yield_fixture
def reset_logging():
    """reset root log handler to the default value after running the test"""
    notify_socket = os.environ.pop("NOTIFY_SOCKET", None)
    roothandlers = logging.getLogger().handlers
    oldhandlers = roothandlers.copy()
    roothandlers.clear()
    try:
        yield
    finally:
        roothandlers.clear()
        roothandlers.extend(oldhandlers)
        if notify_socket is not None:
            os.environ["NOTIFY_SOCKET"] = notify_socket


def test_configure_logging(reset_logging):  # pylint: disable=redefined-outer-name,unused-argument
    roothandlers = logging.getLogger().handlers
    roothandlers.clear()
    logutil.configure_logging(short_log=True)
    assert "(name)" not in roothandlers[0].formatter._fmt

    roothandlers.clear()
    logutil.configure_logging(short_log=False)
    assert "(name)" in roothandlers[0].formatter._fmt
    assert "(threadName)" not in roothandlers[0].formatter._fmt

    roothandlers.clear()
    logutil.configure_logging(multi_threaded=True)
    assert "(threadName)" in roothandlers[0].formatter._fmt
    assert "(asctime)" in roothandlers[0].formatter._fmt

    os.environ["NOTIFY_SOCKET"] = "/dev/null"
    roothandlers.clear()
    logutil.configure_logging(multi_threaded=True)
    assert "(threadName)" in roothandlers[0].formatter._fmt
    assert "(asctime)" not in roothandlers[0].formatter._fmt


def test_syslog_handler(reset_logging):  # pylint: disable=redefined-outer-name,unused-argument
    rootlogger = logging.getLogger()
    roothandlers = rootlogger.handlers
    roothandlers.clear()
    logutil.configure_logging()
    logutil.set_syslog_handler("/dev/log", "local2", rootlogger)
    assert len(roothandlers) == 2

    assert isinstance(roothandlers[0], logging.StreamHandler)
    assert "(asctime)" in roothandlers[0].formatter._fmt
    assert "(threadName)" not in roothandlers[0].formatter._fmt

    assert isinstance(roothandlers[1], logging.handlers.SysLogHandler)
    assert "(asctime)" not in roothandlers[1].formatter._fmt
    assert "(threadName)" not in roothandlers[1].formatter._fmt

    roothandlers.clear()
    logutil.configure_logging(multi_threaded=True)
    logutil.set_syslog_handler("/dev/log", "local2", rootlogger)
    assert len(roothandlers) == 2

    assert isinstance(roothandlers[0], logging.StreamHandler)
    assert "(threadName)" in roothandlers[0].formatter._fmt
    assert isinstance(roothandlers[1], logging.handlers.SysLogHandler)
    assert "(threadName)" in roothandlers[1].formatter._fmt
