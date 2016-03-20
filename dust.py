# -*- coding: utf-8 -*-

import numpy as np


class Radmc3dDustSpecies(object):

    def density(self, coords):
        '''
        '''
        raise NotImplementedError



class Radmc3dDustContainer(dict):

    def write(self, io, grid):

        with io.file_open_write('dustopac.inp') as f:
            f.write('2\n')
            f.write('%d\n' % len(self))
            f.write('%s\n' % ('=' * 80))

            for k in self.keys():
                f.write('1\n0\n')
                f.write('%s\n' % k)
                f.write('%s\n' % ('=' * 80))

        ext = 'binp' if io.binary else 'inp'
        fname = '.'.join(['dust_density', ext])
        sep = '' if io.binary else '\n'

        with io.file_open_write(fname) as f:
            hdr = np.empty((3,), dtype=np.int64)
            hdr[0] = 1
            hdr[1] = grid.nrcells
            hdr[2] = len(self)

            if io.binary:
                hdr = np.insert(hdr, 1, [np.dtype(io.dtype).itemsize])

            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')

            if io.binary:
                for i, d in enumerate(self.values()):
                    shape = (grid.nu, grid.nv, grid.nw)
                    size = grid.nu * grid.nv * grid.nw
                    offset = 4 * np.dtype(np.int64).itemsize + \
                        i * size * np.dtype(io.dtype).itemsize

                    density = io.memmap(fname, offset=offset, shape=shape,
                        dtype=io.dtype, mode='w+')
                    density[:] = d.density(grid.cellcoords)[:]

            else:
                for d in self.values():
                    density = d.density(grid.cellcoords)
                    density.tofile(f, sep=sep, format='%e')

# vim: set ft=python:
