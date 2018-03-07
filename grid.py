# -*- coding: utf-8 -*-

import numpy as np
from coordsys import CartesianCoordinates, SphericalCoordinates, \
    CylindricalCoordinates
from vectorsys import CartesianVectorField, SphericalVectorField, \
    CylindricalVectorField
import cyvtk as vtk


class Grid(object):

    def __init__(self):

        self.coordmap = { 0 : CartesianCoordinates,
                          100 : SphericalCoordinates,
                          200 : CylindricalCoordinates }
        self.coordmap.update({ v : k for k, v in self.coordmap.items() })
        self.vectormap = { CartesianCoordinates : CartesianVectorField,
                           SphericalCoordinates : SphericalVectorField,
                           CylindricalCoordinates : CylindricalVectorField }

        self._nu = self._nv = self._nw = 0
        self._ptcoords = None
        self._cellcoords = None

        self._coordsys = CartesianCoordinates
        self._u = np.empty((0,))
        self._v = np.empty((0,))
        self._w = np.empty((0,))


    def write(self, io):
        '''
        Writes a grid definition to a file.

        :param Io io: Current I/O context
        '''
        raise NotImplementedError


    def update_coords(self):
        '''
        Private function. Updates the definitions of the point and cell
        coordinates after a change to one of the coordinate arrays.
        '''
        raise NotImplementedError


    @property
    def ptcoords(self):
        '''Read-only; gives the point coordinates of this grid.'''
        return self._ptcoords

    @property
    def cellcoords(self):
        '''
        Read-only; gives the cell coordinates of this grid. Currently, these
        are defined simply to be the midpoints of each dimension of the
        point coordinates.
        '''
        return self._cellcoords

    @property
    def coordsys(self):
        '''
        Set to one of CartesianCoordinates, SphericalCoordinates, or
        CylindricalCoordinates. Note that cylindrical coordinates, though
        documented in the RADMC3D manual, do not seem to be supported yet.
        '''
        return self._coordsys

    @coordsys.setter
    def coordsys(self, val):
        self._coordsys = val
        self.update_coords()

    @property
    def u(self):
        '''
        The first coordinate of the grid. This is called :code:`x` in the
        RADMC3D manual; we use :code:`u` here to avoid confusion with
        true Cartesian coordinates. Expects a NumPy array.
        '''
        return self._u

    @u.setter
    def u(self, arr):
        self._u = arr.copy()
        self._nu = self._u.shape[0] - 1
        self.update_coords()

    @property
    def v(self):
        '''
        The first coordinate of the grid. This is called :code:`y` in the
        RADMC3D manual; we use :code:`v` here to avoid confusion with
        true Cartesian coordinates. Expects a NumPy array.
        '''
        return self._v

    @v.setter
    def v(self, arr):
        self._v = arr.copy()
        self._nv = self._v.shape[0] - 1
        self.update_coords()

    @property
    def w(self):
        '''
        The first coordinate of the grid. This is called :code:`z` in the
        RADMC3D manual; we use :code:`w` here to avoid confusion with
        true Cartesian coordinates. Expects a NumPy array.
        '''
        return self._w

    @w.setter
    def w(self, arr):
        self._w = arr.copy()
        self._nw = self._w.shape[0] - 1
        self.update_coords()

    @property
    def nu(self):
        '''Read-only; gives the number of cells in the `u` dimension.'''
        return self._nu

    @property
    def nv(self):
        '''Read-only; gives the number of cells in the `v` dimension.'''
        return self._nv

    @property
    def nw(self):
        '''Read-only; gives the number of cells in the `w` dimension.'''
        return self._nw

    @property
    def vectorsys(self):
        ''' '''
        return self.vectormap[self.coordsys]

    @property
    def shape(self):
        raise NotImplementedError

    @property
    def vtk(self):
        raise NotImplementedError



class RegularGrid(Grid):
    '''
    Represents a RADMC3D grid. Currently, only regular grids are supported,
    but AMR and oct-tree grids may be added later.
    '''

    def __init__(self):
        super(RegularGrid, self).__init__()


    def write(self, io):
        '''
        Writes a grid definition to a file.

        :param Io io: Current I/O context
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
            hdr[7] = self._nu
            hdr[8] = self._nv
            hdr[9] = self._nw

            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')
            self._u.astype(io.dtype).tofile(f, sep=sep, format='%e')
            if not io.binary: f.write('\n')
            self._v.astype(io.dtype).tofile(f, sep=sep, format='%e')
            if not io.binary: f.write('\n')
            self._w.astype(io.dtype).tofile(f, sep=sep, format='%e')


    def update_coords(self):
        '''
        Private function. Updates the definitions of the point and cell
        coordinates after a change to one of the coordinate arrays.
        '''
        uu, vv, ww = np.meshgrid(self._u, self._v, self._w, indexing='ij')
        self._ptcoords = self.coordsys(uu, vv, ww)

        umid = (self._u[1:] + self._u[:-1]) / 2.
        vmid = (self._v[1:] + self._v[:-1]) / 2.
        wmid = (self._w[1:] + self._w[:-1]) / 2.

        uu, vv, ww = np.meshgrid(umid, vmid, wmid, indexing='ij')
        self._cellcoords = self.coordsys(uu, vv, ww)


    @property
    def shape(self):
        return (self._nu, self._nv, self._nw)

    @property
    def nrcells(self):
        '''Read-only; gives the total number of cells in this grid.'''
        return self._nu * self._nv * self._nw

    @property
    def vtk(self):

        xx, yy, zz = self._ptcoords.transformTo(CartesianCoordinates)
        return vtk.PyUnstructuredGrid(xx.ravel(), yy.ravel(), zz.ravel())

# vim: set ft=python:
