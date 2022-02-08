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
Random utility functions
"""

import errno
import os


def mkdir_p(path):
    """
    Mimic `mkdir -p`

    :param str path: directory to create
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def squashDicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in later dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def obfuscateString(snippet, showLength=5, smear="*"):
    """Obfuscate a string so we can show parts of it in debug log

    :param str snippet: String to obfuscate
    :param int showLength: How many characters _not_ to obscure and beginning and end of string
    :param char smear: character to replace obscured characters with
    """
    start = snippet[: int(showLength)]

    trailing = snippet[(int(showLength) * -1) :]

    obscured = (len(snippet) - (2 * showLength)) * smear
    return "%s%s%s" % (start, obscured, trailing)
