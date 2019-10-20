# logrus

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/unixorn/logrus.svg)](https://github.com/unixorn/logrus/stargazers)
[![Code Climate](https://codeclimate.com/github/unixorn/logrus/badges/gpa.svg)](https://codeclimate.com/github/unixorn/logrus)
[![Issue Count](https://codeclimate.com/github/unixorn/logrus/badges/issue_count.svg)](https://codeclimate.com/github/unixorn/logrus)


The logrus is a collection of random utility functions. Nothing in here
is all that special, they're just yet another implementation of functions
I've rewritten at every job to use in various utility scripts. By open
sourcing them now, I'm hoping to not have to write them again.

# Installation

`pip install logrus`

# License

Apache 2.0 license.

# Included Commands

## human-time

Takes a value in seconds either from stdin or as arg 1 and converts it to a more meat-friendly format using the humanTime function.

`human-time 1234` will print "20 minutes, 34 seconds"

# Included functions

## logrus.cli

### exec_subcommand(unfound)

Creates a `git`-style driver command. If your script is named `foo`, and is run as `foo bar baz` and there is an executable in your `$PATH` named `foo-bar`, it will call `foo-bar` with `baz` as the command line argument.

`unfound` is an optional argument that should be a function pointer and will be called if `exec_subcommand` can't find a suitable subcommand. Mainly useful for you to have a custom usage message.

Example usage:

```
#!/usr/bin/env python3
#
# Test script for thelogrus
#
# Confirms that thelogrus.cli.exec_subcommand works as expected
#
# Copyright 2019, Joe Block <jpb@unixorn.net>

from thelogrus.cli import exec_subcommand


def _usage(message):
  '''
  Custom usage printer
  '''
  print("%s" % sys.argv[0])
  print("Called as %s" % (' '.join(sys.argv)))
  print("Oh look, a custom usage message.")
  print("Attempted to find an executable using all the permutations of %s with no luck." % '-'.join(sys.argv))
  print("%s" % message)


if __name__ == '__main__':
  exec_subcommand(unfound=_usage)
```

### find_subcommand(args)

Given a list ['foo','bar', 'baz'], attempts to create a command name in the
format 'foo-bar-baz'. If that command exists, we run it. If it doesn't, we
check to see if foo-bar exists, in which case we run `foo-bar baz`. We keep
taking chunks off the end of the command name and adding them to the argument
list until we find a valid command name we can run.

This allows us to easily make git-style command drivers where for example we
have a driver script, foo, and subcommand scripts foo-bar and foo-baz, and when
the user types `foo bar foobar` we find the foo-bar script and run it as
`foo-bar foobar`

Example usage:

```
#!/usr/bin/env python3

import os
import subprocess
import sys
from thelogrus.cli import find_subcommand


def subcommander_driver():
  '''
  Process the command line arguments and run the appropriate subcommand.

  We want to be able to do git-style handoffs to subcommands where if we
  do `foo blah foo bar` and the executable foo-blah-foo exists, we'll call
  it with the argument bar.

  We deliberately don't do anything with the arguments other than hand
  them off to the foo subcommand. Subcommands are responsible for their
  own argument parsing.
  '''
  try:
    (command, args) = find_subcommand(sys.argv)

    # If we can't construct a subcommand from sys.argv, it'll still be able
    # to find this driver script, and re-running ourself isn't useful.
    if os.path.basename(command) == sys.argv[0]:
      print("Could not find a subcommand for %s" % ' '.join(sys.argv))
      sys.exit(1)
  except Exception as e:
    print(str(e))
    sys.exit(1)
  subprocess.check_call([command] + args)


if __name__ == '__main__':
  subcommander_driver()
```

### is_program(name)

Search for a given program in `$PATH`, and return `True` if it exists and
is executable.

### run(command)

Runs a command (either a str or list) and returns its `stdout`.

## logrus.logging

### getCustomLogger(name, logLevel)

Returns a custom logger with nicely formatted output.

## logrus.time

### humanTime(seconds)

Takes a value in seconds, returns it in meat-friendly format. `humanFriendlyTime(8675309)` would return "100 days 9 hours 48 minutes 29 seconds".

## logrus.utils

### mkdir_p(path)

os module doesn't have a `mkdir -p` equivalent so added one.

### squashDicts(*dict_args)

Return a dict that is all the dict_args squashed together.
