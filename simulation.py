# -*- coding: utf-8 -*-

from configuration import *
from fileio import *
from grid import *
from star import *
from dust import *
from render import *
from __init__ import execute


class Radmc3dSimulation(object):
    '''
    Primary class for carrying out simulations with RADMC3D.
    '''

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
        '''
        Writes the encapsulated data to files in the output directory, to be
        read by RADMC3D.
        '''

        self.write_wavelengths()

        self._config.write(self._io)
        self._grid.write(self._io)
        self._star.write(self._io, self._lmbda, self._grid)
        self._dust.write(self._io, self._grid)


    def write_wavelengths(self):
        '''Private function; writes the list of wavelengths to a file.'''

        with self._io.file_open_write('wavelength_micron.inp') as f:
            f.write('%d\n' % self.nlmbda)
            self._lmbda.tofile(f, sep='\n', format='%e')


    def mctherm(self):
        '''Runs the :code:`mctherm` command of RADMC3D.'''
        execute('radmc3d mctherm', self.io.outdir)


    def render(self):
        '''Outputs a VTK file with all defined variables.'''
        self._render.render(self._io, self._grid)


    @property
    def lmbda(self):
        '''Array of wavelengths at which to perform the simulation.'''
        return self._lmbda

    @lmbda.setter
    def lmbda(self, arr):
        self._lmbda = arr.copy()
        self.nlmbda = arr.shape[0]

    @property
    def config(self):
        '''Accessor to the underlying configuration object.'''
        return self._config

    @property
    def io(self):
        '''Accessor to the underlying I/O context object.'''
        return self._io

    @property
    def grid(self):
        '''Accessor to the underlying grid object.'''
        return self._grid

    @property
    def dust(self):
        '''Accessor to the underlying dust container object.'''
        return self._dust

    @property
    def star(self):
        '''Accessor to the underlying star container object.'''
        return self._star

# vim: set ft=python:
