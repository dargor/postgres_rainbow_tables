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

# make configuration

.SILENT:
.PHONY: help xxx todo fixme stuff cksum shellcheck flake compile optimize clean

# default command

all: help

# main commands

help:
	echo ''
	echo '[1;32mxxx[0;0m          ... find XXX notes'
	echo '[1;32mtodo[0;0m         ... find TODO notes'
	echo '[1;32mfixme[0;0m        ... find FIXME notes'
	echo ''
	echo '[1;32mstuff[0;0m        ... find all the above notes'
	echo ''
	echo '[1;32m(s)hellcheck[0;0m ... validate scripts using shellcheck'
	echo '[1;32m(f)lake[0;0m      ... validate sources using flake8'
	echo ''
	echo '[1;32m(l)int[0;0m       ... run shellcheck and flake8'
	echo ''
	echo '[1;33mcompile[0;0m      ... compile sources to standard bytecode'
	echo '[1;33moptimize[0;0m     ... compile sources to optimized bytecode'
	echo ''
	echo '[1;31m(c)lean[0;0m      ... remove pycache stashes and bytecode files'

xxx:
	grep --color XXX $$(find . -iname '*.py')

todo:
	grep --color TODO $$(find . -iname '*.py')

fixme:
	grep --color FIXME $$(find . -iname '*.py')

stuff:
	grep --color -E 'XXX|TODO|FIXME' $$(find . -iname '*.py')

cksum:
	find * -name Makefile -exec md5sum {} \;

shellcheck:
	shellcheck -f gcc $$(find * -name '*.sh')

flake:
	-python3 -m flake8 $$(find * -name '*.py')

lint: shellcheck flake

compile:
	python3 -m compileall -qf .

optimize:
	python3 -OO -m compileall -qf .

clean:
	find . -name '__pycache__' -print0 -o -name '*.py[co]' -print0 | xargs -r0 rm -rf

# shorter aliases

s: shellcheck

f: flake

l: lint

c: clean
