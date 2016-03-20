# -*- coding: utf-8 -*-

import numpy as np
from coordsys import CartesianCoordinates, SphericalCoordinates, \
    CylindricalCoordinates


class Radmc3dGrid(object):

    def __init__(self):

        self.coordmap = { 0 : CartesianCoordinates,
                          100 : SphericalCoordinates,
                          200 : CylindricalCoordinates }
        self.coordmap.update({ v : k for k, v in self.coordmap.items() })

        self.nu = self.nv = self.nw = 0
        self._ptcoords = None
        self._cellcoords = None

        self._coordsys = CartesianCoordinates
        self._u = np.empty((0,))
        self._v = np.empty((0,))
        self._w = np.empty((0,))


    def write(self, io):
        '''
        Writes a grid definition to a file.
        '''

        sep = '' if io.binary else '\n'
        ext = 'binp' if io.binary else 'inp'

        with io.file_open_write('.'.join(['amr_grid', ext])) as f:

            hdr = np.empty((10,), dtype=np.int64)
            hdr[0] = 1
            hdr[1] = 0
            hdr[2] = self.coordmap[self.coordsys]
            hdr[3] = 0
            hdr[4] = hdr[5] = hdr[6] = 1
            hdr[7] = self.nu
            hdr[8] = self.nv
            hdr[9] = self.nw

            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')
            self._u.astype(io.dtype).tofile(f, sep=sep, format='%e')
            if not io.binary: f.write('\n')
            self._v.astype(io.dtype).tofile(f, sep=sep, format='%e')
            if not io.binary: f.write('\n')
            self._w.astype(io.dtype).tofile(f, sep=sep, format='%e')


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
    def coordsys(self):
        return self._coordsys

    @coordsys.setter
    def coordsys(self, val):
        self._coordsys = val
        self.update_coords()

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
