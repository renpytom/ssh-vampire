#!/usr/bin/env python3

# Copyright 2014 Tom Rothamel <tom@rothamel.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import pwd
import os
import re
import sys

VARS = [
    b"SSH_AUTH_SOCK",
    b"SSH_AGENT_PID",
    ]

def process(pid, uid):
    """
    Looks for an ssh key in /proc/`pid`/environ.

    `pid`
        The process number, which can be a string.

    `uid`
        The userid that must own the process for it to be considered.
    """

    environ_fn = os.path.join("/proc", str(pid), "environ")

    st = os.stat(environ_fn)
    if st.st_uid != uid:
        return

    with open(environ_fn, "rb") as f:
        environ = f.read().split(b"\0")

    # A map from environment variable to its value.
    envvars = { }

    for l in environ:
        try:
            var, value = l.split(b"=", 1)
            envvars[var] = value
        except:
            pass

    for v in VARS:
        if v not in envvars:
            return

    for v in VARS:
        sys.stdout.buffer.write(b'export ' + v + b'=' + envvars[v] + b'\n')

    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description="Scans processes owned by a user to find ssh-agent environment variables. If found, prints those environment variables.")
    ap.add_argument('user', nargs='?', help='The user to take ssh-agent credentials from. If not given, defaults to the current user.')
    args = ap.parse_args()

    if args.user:
        try:
            uid = pwd.getpwnam(args.user).pw_uid
        except:
            args.error("User {} not found.".format(args.user))
    else:
        uid = os.getuid()


    for i in os.listdir("/proc"):
        if re.match(r'\d+$', i):
            process(i, uid)

    sys.stderr.write("Could not find a process with ssh-agent environment variables.")
    sys.exit(1)

if __name__ == "__main__":
    main()

