# Licensed under a 3-clause BSD style license - see LICENSE.rst
import Ska.tdb
for tablename in sorted(Ska.tdb.tables.keys()):
    table = tables[tablename]
    print tablename
    print '^^^^^^^^^^^^^^^^^^^^^^^^^'
    print
    descrs = table.data.dtype.descr
    width = max([len(x[0]) for x in descrs])
    fmt = '{:' + str(width) + 's} {:5s}'
    header = fmt.format('=' * width, '=' * 10)
    print header
    print fmt.format('  Column  ', 'Type')
    print header
    for name, dtype in descrs:
        dtype = dtype[1:]
        out = {'i8': 'int', 'f8': 'float'}.get(dtype, dtype)
        if out.startswith('S'):
            out = 'string({})'.format(out[1:])
        print fmt.format(name, out)
    print header
    print
