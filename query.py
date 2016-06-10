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

import argparse
import psycopg2

from logger import logging


parser = argparse.ArgumentParser()

parser.add_argument('-t',
                    '--type',
                    help='Type of hash (auto, md5, sha1, ...)',
                    type=str,
                    dest='hash_type',
                    default='auto')

parser.add_argument('-v',
                    '--value',
                    '--hash',
                    help='Hash for which we must search passwords',
                    type=str,
                    dest='hash_value',
                    required=True)

args = parser.parse_args()

if args.hash_type == 'auto':
    args.hash_type = {
        32: 'md5',
        40: 'sha1',
        56: 'sha224',
        64: 'sha256',
        96: 'sha384',
        128: 'sha512',
    }[len(args.hash_value)]
    logging.debug('Assuming {} hash'.format(args.hash_type))


conn = psycopg2.connect('dbname=rainbows user=rainbows')
cur = conn.cursor()


cur.execute('select clear_text_password'
            ' from rainbows'
            ' where digest(clear_text_password, %(h_type)s) = %(h_value)s',
            {
                'h_type': args.hash_type,
                'h_value': '\\x{}'.format(args.hash_value),
            })

if cur.rowcount == 0:
    print('no match')
else:
    print('Matches:')
    for row in cur.fetchall():
        print('\t{}'.format(row[0]))


cur.close()
conn.close()
