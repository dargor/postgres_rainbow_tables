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

import os
import csv
import argparse
import psycopg2

from glob import glob
from io import StringIO
from logger import logging


# Path to a directory containing passwords, in .txt files
# We set it to our local path, to import test.txt
PWD_LISTS = '.'
# You may want to set it to a clone of github.com/danielmiessler/SecLists
# There are some funny data in these files, you may have to delete/edit lines
#PWD_LISTS = os.path.expanduser('~/contrib/SecLists/Passwords')


parser = argparse.ArgumentParser()

parser.add_argument('-k',
                    '--keep',
                    help='Keep CSV used to feed postgres',
                    action='store_true')

args = parser.parse_args()


conn = psycopg2.connect('dbname=rainbows user=rainbows')
cur = conn.cursor()

cur.execute('prepare p_select as'
            ' select clear_text_password'
            ' from rainbows'
            ' where clear_text_password = $1')


def read_file(fname):

    def read_it(encoding):
        with open(fname, 'r', encoding=encoding) as f:
            return f.read().splitlines()

    try:
        logging.info('Reading {}'.format(fname))
        return read_it('utf-8')
    except UnicodeDecodeError:
        logging.debug('(error while reading file, trying latin-1)')
        return read_it('latin-1')


for fname in sorted(glob('{}/*.txt'.format(PWD_LISTS))):
    n = 0
    # we use a dict to get O(1) performance, instead of O(n) with a list
    l = {}

    for line in read_file(fname):
        clear_text_password = line.strip()
        if len(clear_text_password) > 0 and clear_text_password not in l:
            # yes, files have duplicates and we don't want them
            cur.execute('execute p_select(%(clear_text_password)s)',
                        {'clear_text_password': clear_text_password})
            if cur.rowcount == 0:
                l[clear_text_password] = True
                n += 1
                if n % 10000 == 0:
                    logging.debug('Queued {} passwords'.format(n))
    logging.debug('Queued {} passwords'.format(n))

    stream = StringIO()
    writer = csv.writer(stream,
                        delimiter='\t',
                        escapechar='\\',
                        quotechar=None,
                        doublequote=False)
    for clear_text_password in l:
        t = (clear_text_password,)
        writer.writerow(t)
    stream.seek(0)

    if args.keep:
        dname = 'DEBUG_{}.csv'.format(os.path.basename(fname))
        logging.debug('Dumping values to {}'.format(dname))
        with open(dname, 'w', encoding='utf-8') as f:
            f.write(stream.getvalue())

    logging.debug('Importing queued passwords')
    cur.copy_from(file=stream,
                  table='rainbows',
                  sep='\t',
                  columns=('clear_text_password',))
    conn.commit()
    logging.info('Added {} passwords'.format(len(l)))


cur.execute('deallocate all')

cur.close()
conn.close()
