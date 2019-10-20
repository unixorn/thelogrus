# The Logrus
#
# Copyright 2015-2019 Joe Block <jpb@unixorn.net>
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
logrus is a collection of utility functions.
'''

import os
import shutil
import subprocess
from setuptools import setup, find_packages, Command


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


PACKAGE_NAME = 'thelogrus'
PACKAGE_VERSION = "0.2.%s" % (run('git rev-list HEAD --count').strip())


class CleanCommand(Command):
  '''
  Add a clean option to setup.py's commands
  '''
  description = 'Clean up'
  user_options = []


  def initialize_options(self):
    '''Initialize clean options'''
    self.cwd = None


  def finalize_options(self):
    '''Finalize clean options'''
    self.cwd = os.getcwd()


  def run(self):
    '''Clean up working directory'''
    assert os.getcwd() == self.cwd, "Must be in package root: %s" % self.cwd
    if os.path.isdir('build'):
      shutil.rmtree('build')
    if os.path.isdir('dist'):
      shutil.rmtree('dist')


setup(
  name=PACKAGE_NAME,
  version=PACKAGE_VERSION,
  author="Joe Block",
  author_email="jpb@unixorn.net",
  description="The Logrus is a collection of random utility functions",
  url="https://github.com/unixorn/thelogrus",
  packages=find_packages(),
  download_url="https://github.com/unixorn/thelogrus/tarball/%s" % PACKAGE_VERSION,
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Operating System :: POSIX",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],
  cmdclass={
    "clean": CleanCommand,
  },
  entry_points={
    "console_scripts": [
      "human-time = %s.time:human_time_converter" % PACKAGE_NAME,
    ]
  },
  install_requires=[
    'dateutils'
  ],
  keywords=["devops", "utility"],
)
