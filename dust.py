# -*- coding: utf-8 -*-

import numpy as np


class Radmc3dDustSpecies(object):

    def density(self, coords):
        '''
        '''
        raise NotImplementedError


    def kappa(self, lmbda):
        '''
        '''
        raise NotImplementedError


    def kapscatmat(self, lmbda):
        '''
        '''
        raise NotImplementedError



class Radmc3dDustDensity(object):


    def __init__(self, io, specs):

        self.io = io

        if hasattr(specs, '__iter__'):
            specs = list(specs)
        else:
            specs = [specs]

        self.specs = specs
        self.nrspec = len(specs)


    def write(self, grid, binary=True, dtype=np.float64):
        '''
        '''

        ext = 'binp' if binary else 'inp'
        fname = '.'.join(['dust_density', ext])

        with self.io.file_open_write(fname) as f:

            sep = '' if binary else '\n'
            hdr = np.empty((3,), dtype=np.int64)
            hdr[0] = 1
            hdr[1] = grid.nrcells
            hdr[2] = self.nrspec

            if binary:
                hdr = np.insert(hdr, 1, [np.dtype(dtype).itemsize])

            hdr.tofile(f, sep=sep, format='%d')
            if not binary: f.write('\n')

            if binary:
                f.close()

                for i in xrange(self.nrspec):
                    shape = (grid.nu, grid.nv, grid.nw)
                    size = grid.nu * grid.nv * grid.nw
                    offset = 4 * np.dtype(np.int64).itemsize + \
                        i * size * np.dtype(dtype).itemsize

                    density = self.io.memmap(self.io.fullpath(fname),
                        offset=offset, shape=shape, dtype=dtype, mode='w+')
                    density[:] = self.specs[i].density(grid.cellcoords)

            else:
                for i in xrange(self.nrspec):
                    density = self.specs[i].density(grid.cellcoords)
                    density.tofile(f, sep=sep, format='%e')
