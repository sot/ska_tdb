#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make the numpy data files that are used by ska_tdb.  From the repo root directory:

$ ./make_tdb.py

This creates files in ./data/p0<VERSION>/.  These dirs get installed to $SKA/data/ska_tdb
via the Makefile with "make install".

This requires that directories be in /proj/sot/ska/ops/TDB which are the '*.txt' files
that have been created by CXCDS from the MSFC-1949 files.  These are normally supplied
by DS (historically Ian Evans) following a TDB update.

There is some normalization vs. the input 1949 files and my memory is that it isn't so
trivial to make the .txt files (but this might be wrong).
"""

from __future__ import print_function

import os
import glob

import numpy as np
from astropy.io import ascii

TDB_ROOT = '/proj/sot/ska/ops/TDB'

names = 'tcntr tes tlmt tloc tmsrment towner tpc tpp tsc tsmpl tstream ttdm_fmt ttdm'.split()

TDB_versions = [os.path.basename(x) for x in glob.glob(os.path.join(TDB_ROOT, 'p0??'))]

for TDB_version in sorted(TDB_versions):
    out_path = os.path.join('data', TDB_version)
    if os.path.exists(out_path):
        print('Skipping TDB version {}: already processed'.format(TDB_version))
        continue

    if any(not os.path.exists(os.path.join(TDB_ROOT, TDB_version, name + '.txt'))
           for name in names):
        print('Skipping TDB version {}: input file(s) missing'.format(TDB_version))
        continue

    os.mkdir(out_path)
    print('Processing TDB version {}'.format(TDB_version))

    for name in names:
        filename = os.path.join(TDB_ROOT, TDB_version, name + '.txt')
        print(name, filename)

        # Get the header column names from existing RDB files
        colname_file = os.path.join(TDB_ROOT, name + '.rdb')
        with open(colname_file, 'r') as fh:
            colnames = fh.readline().split()

        with open(filename, 'r') as fh:
            dat = fh.read().strip()
            lines = dat.splitlines()

        # Get rid of trailing junk.  It looks like two RDB files were massaged to remove
        # some null columns and so the names are not defined.
        if name == 'tmsrment':
            strip_string = ',,;'
        elif name == 'tsmpl':
            strip_string = ',;'
        else:
            strip_string = ';'

        # Remove the junk after making sure it is actually there as expected.
        if not all(x.endswith(strip_string) for x in lines if len(x)):
            raise Exception('Not ending with {}'.format(strip_string))
        n_strip = len(strip_string)
        lines = [x[:-n_strip] for x in lines]

        dat = ascii.read(lines, guess=False, delimiter=',', quotechar='"', names=colnames,
                         format='no_header')
        print('Masked : {}'.format(dat.masked))
        print()

        np.save(os.path.join(out_path, name + '.npy'), dat)
