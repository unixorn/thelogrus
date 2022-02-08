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
#
"""
Utility functions for dealing with programs.
"""

import distutils.spawn
import os
import subprocess
import sys


def _usage(message):
    """
    Default usage/error print function for exec_subcommand.

    :param str message: What to interpolate into our output.
    """
    print("%s" % sys.argv[0])
    print("Called as %s" % (" ".join(sys.argv)))
    print(
        "Attempted to find an executable using all the permutations of %s with no luck."
        % "-".join(sys.argv)
    )
    print("%s" % message)


def exec_subcommand(unfound=_usage):
    """
    Process the command line arguments and run the appropriate subcommand.

    The goal is to be able to do git-style handoffs to subcommands where
    if we do `foo blah foo bar` and the executable foo-blah-foo exists,
    we'll call it with the argument bar.

    We deliberately don't do anything with the arguments other than hand
    them off to the subcommand. Subcommands are responsible for their
    own argument parsing and validity checks.

    Use os.execvp so that subcommands inherit our stdin, and we don't
    have to handle returning their error codes.

    :param function unfound: Function to call if we can't find a suitable subcommand
    """
    try:
        (command, args) = find_subcommand(sys.argv)

        # If we can't construct a subcommand from sys.argv, it'll still be able
        # to find this driver script, and re-running ourself isn't useful.
        if os.path.basename(command) == sys.argv[0]:
            unfound("Could not find a subcommand for %s" % " ".join(sys.argv))
            sys.exit(1)
    except Exception as e:
        unfound(str(e))
        sys.exit(1)
    args.insert(0, command)
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvp(os.path.basename(command), args)


def find_subcommand(args):
    """
    Given a list ['foo','bar', 'baz'], attempts to create a command name
    in the format 'foo-bar-baz'. If that command exists, we run it. If it
    doesn't, we check to see if foo-bar exists, in which case we run
    `foo-bar baz`.

    We keep peeling chunks off the end of the command name and adding them
    to the argument list until we find a valid command name we can run.

    This allows us to easily make git-style command drivers where, for
    example we have a driver script, foo, and subcommand scripts foo-bar
    and foo-baz, and when the user types `foo bar foobar` we find the foo-bar
    script and run it as

      `foo-bar foobar`

    :param list|tuple args: list to try and convert to a command args pair
    :returns: command and arguments list
    :rtype: tuple
    :raises StandardError: if the args can't be matched to an executable subcommand
    """
    command = None
    # If the only command we find is the first element of args, we've found the
    # driver script itself and re-executing it will cause an infinite loop, so
    # don't even look at the first element on its own.
    for i in range(len(args) - 1):
        command = "-".join(args[: (len(args) - i)])
        command_arguments = args[len(args) - i :]
        if is_program(os.path.basename(command)):
            return (command, command_arguments)
    raise RuntimeError("Could not find a subcommand executable for %s" % " ".join(args))


def is_program(name):
    """
    Search for a given program in $PATH, and return True if it exists and
    is executable.

    :param str name: Name of program to search for
    :returns: whether or not the program can be found in $PATH
    :rtype: bool
    """
    return distutils.spawn.find_executable(name) is not None


def run(command):
    """
    Run a command and return stdout.
    """
    if not isinstance(command, (list, str)):
        raise TypeError("%r is not a str or list" % command)
    if isinstance(command, str):
        cmd = command.split()
    else:
        cmd = command
    return subprocess.check_output(cmd, universal_newlines=True)


def subcommander_driver():
    """
    Process the command line arguments and run the appropriate subcommand.

    We want to be able to do git-style handoffs to subcommands where if we
    do `foo blah foo bar` and the executable foo-blah-foo exists, we'll call
    it with the argument bar.

    We deliberately don't do anything with the arguments other than hand
    them off to the foo subcommand. Subcommands are responsible for their
    own argument parsing.
    """
    try:
        (command, args) = find_subcommand(sys.argv)

        # If we can't construct a subcommand from sys.argv, it'll still be able
        # to find this driver script, and re-running ourself isn't useful.
        if os.path.basename(command) == sys.argv[0]:
            print("Could not find a subcommand for %s" % " ".join(sys.argv))
            sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    subprocess.check_call([command] + args)
