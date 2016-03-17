# -*- coding: utf-8 -*-

import numpy as np
from coordsys import CartesianCoordinates, SphericalCoordinates, \
    CylindricalCoordinates


class Radmc3dGrid(object):

    def __init__(self, io, coordsys):

        self.io = io
        self.coordsys = coordsys

        self.coordmap = { 0 : CartesianCoordinates,
                          100 : SphericalCoordinates,
                          200 : CylindricalCoordinates }
        self.coordmap.update({ v : k for k, v in self.coordmap.items() })

        self.nu = self.nv = self.nw = 0
        self._ptcoords = None
        self._cellcoords = None

        self._u = np.empty((0,))
        self._v = np.empty((0,))
        self._w = np.empty((0,))


    def write(self, binary=True, dtype=np.float64):
        '''
        Writes a grid definition to a file.
        '''

        sep = '' if binary else '\n'
        ext = 'binp' if binary else 'inp'

        with self.io.file_open_write('.'.join(['amr_grid', ext])) as f:

            hdr = np.empty((10,), dtype=np.int64)
            hdr[0] = 1
            hdr[1] = 0
            hdr[2] = self.coordmap[self.coordsys]
            hdr[3] = 0
            hdr[4] = hdr[5] = hdr[6] = 1
            hdr[7] = self.nu
            hdr[8] = self.nv
            hdr[9] = self.nw

            if binary:
                hdr = np.insert(hdr, 1, [8 if dtype == np.float64 else 4])

            hdr.tofile(f, sep, format='%d')
            if not binary: f.write('\n')
            self._u.tofile(f, sep=sep, format='%e')
            if not binary: f.write('\n')
            self._v.tofile(f, sep=sep, format='%e')
            if not binary: f.write('\n')
            self._w.tofile(f, sep=sep, format='%e')


    def read(self, binary=True):
        '''
        Reads a grid definition from an existing file.
        '''

        sep = '' if binary else ' '
        ext = 'binp' if binary else 'inp'

        with self.io.file_open_read('.'.join(['amr_grid', ext])) as f:
            count = 3 if binary else 2
            hdr = np.fromfile(f, dtype=np.int64, count=count, sep=sep)

            self.iformat = hdr[0]
            assert self.iformat == 1

            dtype = np.float64 if not binary else \
                (np.float64 if hdr[1] == 8 else np.float32)
            self.gridstyle = hdr[1] if not binary else hdr[2]

            if self.gridstyle == 0:
                hdr = np.fromfile(f, dtype=np.int64, count=8, sep=sep)
                self.coordsys, _, self.inclx, self.incly, \
                    self.inclz, self.nu, self.nv, self.nw = hdr

                self._u = np.fromfile(f, dtype=dtype, count=self.nu+1, sep=sep)
                self._v = np.fromfile(f, dtype=dtype, count=self.nv+1, sep=sep)
                self._w = np.fromfile(f, dtype=dtype, count=self.nw+1, sep=sep)
                self.update_coords()

            else:
                raise NotImplementedError


    def update_coords(self):
        '''

        '''
        uu, vv, ww = np.meshgrid(self._u, self._v, self._w, indexing='ij')
        self._ptcoords = self.coordsys(uu, vv, ww)

        umid = (self._u[1:] + self._u[:-1]) / 2.
        vmid = (self._v[1:] + self._v[:-1]) / 2.
        wmid = (self._w[1:] + self._w[:-1]) / 2.

        uu, vv, ww = np.meshgrid(umid, vmid, wmid, indexing='ij')
        self._cellcoords = self.coordsys(uu, vv, ww)


    @property
    def nrcells(self):
        return self.nu * self.nv * self.nw

    @property
    def ptcoords(self):
        return self._ptcoords

    @property
    def cellcoords(self):
        return self._cellcoords

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, arr):
        self._u = arr.copy()
        self.nu = self._u.shape[0] - 1
        self.update_coords()

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, arr):
        self._v = arr.copy()
        self.nv = self._v.shape[0] - 1
        self.update_coords()

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, arr):
        self._w = arr.copy()
        self.nw = self._w.shape[0] - 1
        self.update_coords()

# vim: set ft=python:
