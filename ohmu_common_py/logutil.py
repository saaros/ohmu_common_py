"""
ohmu_common_py - logging formats and utility functions

Copyright (c) 2015 Ohmu Ltd
See LICENSE for details
"""

import logging
import logging.handlers
import os

try:
    from systemd import daemon  # pylint: disable=no-name-in-module
except ImportError:
    daemon = None


LOG_FORMAT_BASIC = "%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s"
LOG_FORMAT_BASIC_MT = "%(asctime)s\t%(name)s\t%(threadName)s\t%(levelname)s\t%(message)s"
LOG_FORMAT_SHORT = "%(levelname)s\t%(message)s"
LOG_FORMAT_SYSLOG = "%(name)s %(levelname)s: %(message)s"
LOG_FORMAT_SYSLOG_MT = "%(name)s %(threadName)s %(levelname)s: %(message)s"

_multi_threaded = False


def set_syslog_handler(address, facility, logger, multi_threaded=None):
    if multi_threaded is None:
        multi_threaded = _multi_threaded
    syslog_handler = logging.handlers.SysLogHandler(address=address, facility=facility)
    logger.addHandler(syslog_handler)
    formatter = logging.Formatter(LOG_FORMAT_SYSLOG_MT if multi_threaded else LOG_FORMAT_SYSLOG)
    syslog_handler.setFormatter(formatter)
    return syslog_handler


def configure_logging(level=logging.DEBUG, short_log=False, multi_threaded=False):
    global _multi_threaded  # pylint: disable=global-statement
    _multi_threaded = multi_threaded

    # Are we running under systemd?
    if os.getenv("NOTIFY_SOCKET"):
        format_string = LOG_FORMAT_SYSLOG_MT if multi_threaded else LOG_FORMAT_SYSLOG
        if not daemon:
            print(
                "WARNING: Running under systemd but python-systemd not available, "
                "systemd won't see our notifications"
            )
    elif short_log:
        format_string = LOG_FORMAT_SHORT
    else:
        format_string = LOG_FORMAT_BASIC_MT if multi_threaded else LOG_FORMAT_BASIC

    logging.basicConfig(level=level, format=format_string)


def notify_systemd(status):
    if daemon:
        daemon.notify(status)
