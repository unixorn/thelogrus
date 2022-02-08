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
Time utility functions
"""
import sys

from dateutil.relativedelta import relativedelta


def human_time(seconds):
    """
    Convert seconds to something more human-friendly
    """
    intervals = ["days", "hours", "minutes", "seconds"]
    chunked_time = relativedelta(seconds=seconds)
    return " ".join(
        "{} {}".format(getattr(chunked_time, k), k)
        for k in intervals
        if getattr(chunked_time, k)
    )


def human_time_converter():
    """
    Cope whether we're passed a time in seconds on the command line or via stdin
    """
    if len(sys.argv) == 2:
        print(human_time(seconds=int(sys.argv[1])))
    else:
        for line in sys.stdin:
            print(human_time(int(line)))
            sys.exit(0)
