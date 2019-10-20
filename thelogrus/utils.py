#!/usr/bin/env python3
#
# Copyright 2017-2019 Joe Block <jpb@unixorn.net>
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

'''
Random utility functions
'''

import errno
import logging
import os
import subprocess


def mkdir_p(path):
  '''
  Mimic `mkdir -p`

  :param str path: directory to create
  '''
  assert isinstance(path, basestring), ("path must be a string but is %r" % path)
  try:
    os.makedirs(path, exist_ok=True)
  except OSError as exception:
    if exception.errno != errno.EEXIST:
      raise


def squashDicts(*dict_args):
  '''
  Given any number of dicts, shallow copy and merge into a new dict,
  precedence goes to key value pairs in later dicts.
  '''
  result = {}
  for dictionary in dict_args:
    result.update(dictionary)
  return result


def run(command):
  '''
  Run a command and return stdout.
  '''
  if not isinstance(command, (list, str)):
    raise TypeError('%r is not a str or list' % command)
  if isinstance(command, str):
    cmd = command.split()
  else:
    cmd = command
  return subprocess.check_output(cmd, universal_newlines=True)