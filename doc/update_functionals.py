#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HORTON: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2017 The HORTON Development Team
#
# This file is part of HORTON.
#
# HORTON is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
"""Generate list of functionals in documentation."""


from cStringIO import StringIO
import json
import os

from horton.meanfield.cext import ULibXCWrapper

from common import write_if_changed


def main():
    """Main program."""
    # Load dependency information -> libxc version
    with open('../dependencies.json') as f:
        dependencies = json.load(f)
    # Order does not matter here. Just make it easy to look things up
    dependencies = dict((d['name'], d) for d in dependencies)
    libxc_version = dependencies['libxc']['version_ci']

    # find the qaworkdir
    qaworkdir = os.getenv('QAWORKDIR')
    if qaworkdir is None:
        qaworkdir = '../qaworkdir'

    # find all the functional keys by processing funcs_key.c
    keys = []
    with open('%s/cached/libxc-%s/funcs_key.c' % (qaworkdir, libxc_version)) as f:
        for line in f:
            if line.startswith('{'):
                words = line.strip()[1:-3].split(',')
                key = words[0][1:-1]
                if len(key) > 0:
                    keys.append(key)

    # sort the functions

    splitkeys = []
    for key in keys:
        words = key.split('_')
        if words[0] == 'hyb':
            prefix = '_'.join(words[:2])
            mid = words[2]
            suffix = '_'.join(words[3:])
        else:
            prefix = words[0]
            mid = words[1]
            suffix = '_'.join(words[2:])
        splitkeys.append((prefix, mid, suffix))

    splitkeys.sort(cmp=cmp_splitkey)
    keys = []
    for splitkey in splitkeys:
        splitkey = [part for part in splitkey if len(part) > 0]
        keys.append('_'.join(splitkey))

    # make a rst table of all functionals

    s = StringIO()

    print >> s, '.. _ref_functionals:'
    print >> s
    print >> s, 'LibXC Functionals'
    print >> s, '#################'
    print >> s
    print >> s, 'The following functionals are available in HORTON through `LibXC'
    print >> s, '<http://www.tddft.org/programs/octopus/wiki/index.php/Libxc>`_ %s.' % \
        libxc_version
    print >> s, '[marques2012]_'
    print >> s
    for key in keys:
        try:
            w = ULibXCWrapper(key)
            print >> s, '**%s**' % key
            print >> s, '   | %s' % w.name
            for line in w.refs.split('\n'):
                line = line.strip()
                if len(line) > 0:
                    print >> s, '   | *%s*' % line
            print >> s
        except ValueError:
            # A bug in libxc ...
            print 'FAILED to load functional', key

    write_if_changed('tech_ref_functionals.rst', s.getvalue())


def cmp_prefix(prefix1, prefix2):
    """Compare order of two LibXC functional prefixes."""
    l = ['lda', 'gga', 'hyb_gga', 'mgga', 'hyb_mgga']
    pos1 = l.index(prefix1)
    pos2 = l.index(prefix2)
    return cmp(pos1, pos2)


def cmp_middle(middle1, middle2):
    """Compare the middle part of a LibXC functional key."""
    l = ['k', 'x', 'c', 'xc']
    pos1 = l.index(middle1)
    pos2 = l.index(middle2)
    return cmp(pos1, pos2)


def cmp_splitkey(sk1, sk2):
    """Compare LibXC functional keys (splitted)."""
    result = cmp_prefix(sk1[0], sk2[0])
    if result == 0:
        result = cmp_middle(sk1[1], sk2[1])
    if result == 0:
        result = cmp(sk1[2], sk2[2])
    return result


if __name__ == '__main__':
    main()
