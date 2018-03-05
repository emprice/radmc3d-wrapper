# -*- coding: utf-8 -*-

import numpy as np
import cyvtk as vtk
from coordsys import CartesianCoordinates


class Radmc3dVtkRender(object):
    '''
    Renders the current input and output files as VTK output that can be
    visualized with VisIt and other VTK visualization software.
    '''

    def read_dust_density(self, io, grid):
        '''
        Private function. Reads the current dust density input file.

        :param Radmc3dIo io: Current I/O context
        :param Radmc3dGrid grid: Current grid definition

        :returns: A dictionary of name-array pairs for each dust species
        :rtype: dict

        :raises IOError: if a required file is not found
        '''

        names = list()

        with io.file_open_read('dustopac.inp') as f:
            hdr = np.fromfile(f, sep=' ', count=2, dtype=np.int64)
            nrspec = hdr[1]

            for i in xrange(nrspec):
                f.readline(); f.readline(); f.readline()
                names.append('dust_density_' + f.readline().strip())

        if io.file_check_exists('dust_density.inp'):
            ext, sep, count, binary = 'inp', ' ', 3, False

        elif io.file_check_exists('dust_density.binp'):
            ext, sep, count, binary = 'binp', '', 4, True

        else:
            return

        ret = dict()

        with io.file_open_read('.'.join(['dust_density', ext])) as f:

            hdr = np.fromfile(f, sep=sep, count=count, dtype=np.int64)
            dtype = (np.float64 if hdr[1] == 8 else np.float32) if binary \
                else np.float64
            nrcells = hdr[2] if binary else hdr[1]
            nrspec = hdr[3] if binary else hdr[2]
            shape = (grid.nu, grid.nv, grid.nw)

            if binary:
                for i in xrange(nrspec):
                    offset = count * np.dtype(np.int64).itemsize + \
                        np.dtype(dtype).itemsize * nrcells * i
                    ret[names[i]] = io.memmap(f, offset=offset, dtype=dtype,
                        shape=shape, mode='r')

            else:
                for i in xrange(nrspec):
                    ret[names[i]] = np.fromfile(f, dtype=dtype,
                        count=nrcells*nrspec, sep=sep).reshape(shape, order='F')

        return ret


    def read_dust_temperature(self, io, grid):
        '''
        Private function. Reads the current dust temperature output file.

        :param Radmc3dIo io: Current I/O context
        :param Radmc3dGrid grid: Current grid definition

        :returns: A dictionary of name-array pairs for each dust species
        :rtype: dict

        :raises IOError: if a required file is not found
        '''

        names = list()

        with io.file_open_read('dustopac.inp') as f:
            hdr = np.fromfile(f, sep=' ', count=2, dtype=np.int64)
            nrspec = hdr[1]

            for i in xrange(nrspec):
                f.readline(); f.readline(); f.readline()
                names.append('dust_temperature_' + f.readline().strip())

        if io.file_check_exists('dust_temperature.dat'):
            ext, sep, count, binary = 'dat', ' ', 3, False

        elif io.file_check_exists('dust_temperature.bdat'):
            ext, sep, count, binary = 'bdat', '', 4, True

        else:
            return

        ret = dict()

        with io.file_open_read('.'.join(['dust_temperature', ext])) as f:

            hdr = np.fromfile(f, sep=sep, count=count, dtype=np.int64)
            dtype = (np.float64 if hdr[1] == 8 else np.float32) if binary \
                else np.float64
            nrcells = hdr[2] if binary else hdr[1]
            nrspec = hdr[3] if binary else hdr[2]
            shape = (grid.nu, grid.nv, grid.nw)

            if binary:
                for i in xrange(nrspec):
                    offset = count * np.dtype(np.int64).itemsize + \
                        np.dtype(dtype).itemsize * nrcells * i
                    ret[names[i]] = io.memmap(f, offset=offset, dtype=dtype,
                        shape=shape, mode='r')

            else:
                for i in xrange(nrspec):
                    ret[names[i]] = np.fromfile(f, dtype=dtype,
                        count=nrcells*nrspec, sep=sep).reshape(shape, order='F')

        return ret


    def render(self, io, grid):
        '''
        Writes the VTK file for all variables that can be found in the output
        directory.

        :param Radmc3dIo io: Current I/O context
        :param Radmc3dGrid grid: Current grid definition
        '''

        cellData = dict()
        cellData.update(self.read_dust_density(io, grid))
        cellData.update(self.read_dust_temperature(io, grid))

        xx, yy, zz = grid.ptcoords.transformTo(CartesianCoordinates)
        c = vtk.PyStructuredGrid(xx, yy, zz)
        for k, v in cellData:
            c.add_scalar_point_data(k, v)
        c.write_to_file(io.fullpath('model'))

# vim: set ft=python:
