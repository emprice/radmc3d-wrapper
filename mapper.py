# -*- coding: utf-8 -*-

import numpy as np


class Mapper(object):
    '''
    '''

    def map_variables(self, io, grid):
        ''' '''
        d = dict()
        d['dust_density'] = self.read_dust_scalar('density', io, grid, True)
        d['dust_temperature'] = \
            self.read_dust_scalar('temperature', io, grid, False)
        d['gas_number_density'] = self.read_gas_numberdens(io, grid)
        d['gas_temperature'] = \
            self.read_gas_global('temperature', io, grid, False)
        d['gas_velocity'] = self.read_gas_global('velocity', io, grid, True)
        return d


    def read_dust_scalar(self, slug, io, grid, inp=True):

        names = list()
        ret = dict()

        try:
            with io.file_open_read('dustopac.inp') as f:
                hdr = np.fromfile(f, sep=' ', count=2, dtype=np.int64)
                nrspec = hdr[1]

                for i in xrange(nrspec):
                    f.readline(); f.readline(); f.readline()
                    names.append(f.readline().strip())
        except IOError:
            return ret

        ext = 'inp' if inp else 'dat'
        bext = 'b' + ext

        if io.file_check_exists('dust_%s.%s' % (slug, ext)):
            ext, sep, count, binary = ext, ' ', 3, False

        elif io.file_check_exists('dust_%s.%s' % (slug, bext)):
            ext, sep, count, binary = bext, '', 4, True

        else:
            return ret

        with io.file_open_read('.'.join(['dust_%s' % slug, ext])) as f:

            hdr = np.fromfile(f, sep=sep, count=count, dtype=np.int64)
            dtype = (np.float64 if hdr[1] == 8 else np.float32) if binary \
                else np.float64
            nrcells = hdr[2] if binary else hdr[1]
            nrspec = hdr[3] if binary else hdr[2]
            shape = grid.shape

            if binary:
                for i in xrange(nrspec):
                    offset = count * np.dtype(np.int64).itemsize + \
                        np.dtype(dtype).itemsize * nrcells * i
                    ret[names[i]] = io.memmap(f, offset=offset, dtype=dtype,
                        shape=shape, mode='r')

            else:
                for i in xrange(nrspec):
                    ret[names[i]] = np.fromfile(f, dtype=dtype,
                        count=nrcells, sep=sep).reshape(shape, order='F')

        return ret


    def read_gas_numberdens(self, io, grid):

        names = list()
        ret = dict()

        try:
            with io.file_open_read('line.inp') as f:
                hdr = np.fromfile(f, sep=' ', count=2, dtype=np.int64)
                nrspec = hdr[1]

                for i in xrange(nrspec):
                    line = f.readline().split()
                    names.append(line[0].strip())
                    for i in xrange(int(line[3])): f.readline()
        except IOError:
            return ret

        for name in names:
            if io.file_check_exists('numberdens_%s.inp' % name):
                ext, sep, count, binary = 'inp', ' ', 2, False

            elif io.file_check_exists('numberdens_%s.binp' % name):
                ext, sep, count, binary = 'binp', '', 3, True

            else:
                return ret

            with io.file_open_read('.'.join(['numberdens_%s' % name, ext])) as f:

                hdr = np.fromfile(f, sep=sep, count=count, dtype=np.int64)
                dtype = (np.float64 if hdr[1] == 8 else np.float32) if binary \
                    else np.float64
                nrcells = hdr[2] if binary else hdr[1]
                shape = grid.shape

                if binary:
                    offset = hdr.nbytes
                    ret[name] = io.memmap(f, offset=offset, dtype=dtype,
                        shape=shape, mode='r')

                else:
                    ret[name] = np.fromfile(f, dtype=dtype,
                        count=nrcells, sep=sep).reshape(shape, order='F')

        return ret


    def read_gas_global(self, slug, io, grid, vector=False):

        ret = None

        if io.file_check_exists('gas_%s.inp' % slug):
            ext, sep, count, binary = 'inp', ' ', 2, False

        elif io.file_check_exists('gas_%s.binp' % slug):
            ext, sep, count, binary = 'binp', '', 3, True

        else:
            return ret

        with io.file_open_read('.'.join(['gas_%s' % slug, ext])) as f:

            hdr = np.fromfile(f, sep=sep, count=count, dtype=np.int64)
            dtype = (np.float64 if hdr[1] == 8 else np.float32) if binary \
                else np.float64
            nrcells = hdr[2] if binary else hdr[1]
            shape = (3,) + grid.shape if vector else grid.shape

            if binary:
                offset = hdr.nbytes
                ret = io.memmap(f, offset=offset, dtype=dtype,
                    shape=shape, mode='r')

            else:
                ret = np.fromfile(f, dtype=dtype,
                    count=3*nrcells if vector else nrcells, sep=sep).\
                        reshape(shape, order='F')

        return ret

# vim: set ft=python:
