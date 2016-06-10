#! /usr/bin/env python3
#
# Copyright (c) 2016, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import logging
import sys
import os


if 'DEBUG' in os.environ:
    verbosity = logging.DEBUG
else:
    verbosity = logging.INFO


def format_color(color_code):
    if os.name == 'posix' and sys.stderr.isatty():
        return '\033[1;{}m{}\033[1;0m'.format(color_code, '{}')
    else:
        return '{}'


logging.basicConfig(level=verbosity,
                    format='%(asctime)s %(levelname)s\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


logging.addLevelName(logging.DEBUG,
                     format_color(36).format(
                         logging.getLevelName(logging.DEBUG)))

logging.addLevelName(logging.INFO,
                     format_color(32).format(
                         logging.getLevelName(logging.INFO)))

logging.addLevelName(logging.WARNING,
                     format_color(33).format(
                         logging.getLevelName(logging.WARNING)))

logging.addLevelName(logging.ERROR,
                     format_color(31).format(
                         logging.getLevelName(logging.ERROR)))

logging.addLevelName(logging.CRITICAL,
                     format_color(35).format(
                         logging.getLevelName(logging.CRITICAL)))


if __name__ == '__main__':
    logging.debug('Debug message')
    logging.info('Informational message')
    logging.warning('Warning message')
    logging.error('Error message')
    logging.critical('Critical error message')
