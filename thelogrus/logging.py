#!/usr/bin/env python3
#
# Copyright 2015-2022 Joe Block <jpb@unixorn.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Logging utility functions
"""

import logging


def get_custom_logger(
    name,
    log_level,
    log_format="%(asctime)s %(levelname)-9s:%(name)s:%(module)s:%(funcName)s: %(message)s",
):
    """
    Set up logging

    :param str name: What log level to set
    :param str log_level: What log level to use
    :param str log_format: Format string for logging
    :rtype: logger
    """
    assert isinstance(log_format, str), (
        "log_format must be a string but is %r" % log_format
    )
    assert isinstance(log_level, str), (
        "log_level must be a string but is %r" % log_level
    )
    assert isinstance(name, str), "name must be a string but is %r" % name

    valid_log_levels = ["CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING"]

    if not log_level:
        log_level = "DEBUG"

    # If they don't specify a valid log level, err on the side of verbosity
    if log_level.upper() not in valid_log_levels:
        log_level = "DEBUG"

    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError("Invalid log level: %s" % log_level)

    logging.basicConfig(level=numeric_log_level, format=log_format)
    logger = logging.getLogger(name)
    return logger
