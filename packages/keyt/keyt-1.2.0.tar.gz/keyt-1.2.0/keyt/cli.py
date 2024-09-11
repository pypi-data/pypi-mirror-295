#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2021 deoktr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Keyt CLI, a stateless password manager and generator."""

import argparse
import sys
import time
from base64 import b85encode
from enum import Enum, auto
from getpass import getpass
from hashlib import blake2b, scrypt

try:
    from base58 import b58encode

    BASE58_INSTALLED = True
except ImportError:
    BASE58_INSTALLED = False

try:
    import pyperclip

    PYPERCLIP_INSTALLED = True
except ImportError:
    PYPERCLIP_INSTALLED = False


__version__ = "1.2.0"


class F(Enum):
    """Formats available."""

    MAX = auto()
    HIGH = auto()
    MID = auto()
    PIN = auto()
    PIN6 = auto()


def gen_password(d, u, m, c=0, f="max"):
    """Keyt password generation algorithm."""
    f = f.upper()

    if f not in list(F.__members__):
        msg = f"Invalid format '{f}'."
        raise ValueError(msg)

    f = F[f]

    salt = u.encode()
    key = scrypt(m.encode(), salt=salt, n=16384, r=8, p=2)

    c = str(c) if c > 0 else ""
    data = (d.lower() + c + u).encode()
    seed = blake2b(data, key=key).hexdigest().encode()

    if f == F.MAX:
        password = b85encode(seed).decode()[:40]
    elif f == F.HIGH:
        password = b85encode(seed).decode()[:16]
    elif f == F.MID:
        if not BASE58_INSTALLED:
            raise Exception("Install `base58` or use another format.")
        password = b58encode(seed).decode()[:16]
    elif f == F.PIN:
        password = int(str(int(seed, 16))[:4])
    elif f == F.PIN6:
        password = int(str(int(seed, 16))[:6])

    return password


def parse_args(args=None):
    """CLI arguments parser init."""
    parser = argparse.ArgumentParser(
        prog="keyt",
        usage="keyt [domain] [username] [master_password] [options]",
        description="%(prog)s stateless password manager and generator.",
    )
    parser.add_argument("-V", "--version", action="store_true")
    parser.add_argument(
        "domain",
        help="Domain name/IP/service.",
        nargs="?",
    )
    parser.add_argument(
        "username",
        help="Username/Email/ID.",
        nargs="?",
    )
    parser.add_argument(
        "master_password",
        help="Master password used during the password generation.",
        nargs="?",
    )
    parser.add_argument(
        "-c",
        "--counter",
        help="An integer that can be incremented to get a new password for "
        "the same account. default=0.",
        type=int,
        default=0,
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Password format can be: 'max', 'high', 'mid', 'pin' or 'pin6'. "
        "default=max.",
        default="max",
    )
    parser.add_argument(
        "--confirm",
        help="Ask to confirm master password, useful when generating a new "
        "password.",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output the password, by default copy it to the clipboard.",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--timer",
        help="Time before flushing the clipboard. default=20s.",
        type=int,
        nargs="?",
        default=20,
    )

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def dispatch(args):
    """Dispatch from the CLI parser."""

    if args.version:
        print(f"keyt version {__version__}")
        return

    d = args.domain
    if d is None:
        d = str(input("domain: "))

    u = args.username
    if u is None:
        u = str(input("username: "))

    m = args.master_password
    if m is None:
        m2 = None
        while True:
            m1 = getpass("master password: ")
            if not args.confirm:
                break
            m2 = getpass("master password (confirm): ")
            if m1 == m2:
                break
        m = m1

    password = gen_password(d=d, u=u, m=m, c=args.counter, f=args.format)

    if args.output:
        print(password)
        return

    if not PYPERCLIP_INSTALLED:
        msg = "`pyperclip` is needed.\nYou can also use the `-o` flag."
        raise Exception(msg)

    pyperclip.copy(password)
    timer = args.timer
    if timer and timer > 0:
        print(f"Password copied to the clipboard for {timer}s.")
        time.sleep(timer)
        pyperclip.copy("")  # remove the content of the clipboard
    else:
        print("Password copied to the clipboard.")


def cli():
    """Main function for the cli."""
    parsed_args = parse_args()

    try:
        dispatch(parsed_args)
        sys.exit(0)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    cli()
