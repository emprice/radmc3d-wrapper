# -*- coding: utf-8 -*-

from configuration import *
from fileio import *
from grid import *
from star import *
from dust import *
from render import *
from __init__ import execute


class Radmc3dSimulation(object):

    def __init__(self):

        self._lmbda = np.empty((0,))
        self.nlmbda = 0

        self._dust = dict()

        self._config = Radmc3dConfiguration()
        self._io = Radmc3dIo()
        self._grid = Radmc3dGrid()
        self._star = Radmc3dStarContainer()
        self._dust = Radmc3dDustContainer()

        self._render = Radmc3dVtkRender()


    def commit(self):

        self.write_wavelengths()

        self._config.write(self._io)
        self._grid.write(self._io)
        self._star.write(self._io, self._lmbda, self._grid)
        self._dust.write(self._io, self._grid)


    def write_wavelengths(self):

        with self._io.file_open_write('wavelength_micron.inp') as f:
            f.write('%d\n' % self.nlmbda)
            self._lmbda.tofile(f, sep='\n', format='%e')


    def mctherm(self):

        execute('radmc3d mctherm', self.io.outdir)


    def render(self):

        self._render.render(self._io, self._grid)


    @property
    def lmbda(self):
        return self._lmbda

    @lmbda.setter
    def lmbda(self, arr):
        self._lmbda = arr.copy()
        self.nlmbda = arr.shape[0]

    @property
    def config(self):
        return self._config

    @property
    def io(self):
        return self._io

    @property
    def grid(self):
        return self._grid

    @property
    def dust(self):
        return self._dust

    @property
    def star(self):
        return self._star

# vim: set ft=python:
