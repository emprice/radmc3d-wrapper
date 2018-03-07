# -*- coding: utf-8 -*-

from configuration import *
from fileio import *
from grid import *
from star import *
from dust import *
from gas import *
from render import *
from __init__ import execute


class Simulation(object):
    '''
    Primary class for carrying out simulations with RADMC3D.
    '''

    def __init__(self):

        self._lmbda = np.empty((0,))
        self.nlmbda = 0

        self._config = Configuration()
        self._io = Io()
        self._grid = Grid()
        self._star = StarContainer()
        self._dust = DustContainer()
        self._gas = MoleculeContainer()
        self._render = VtkRender()

        self._config_written = False
        self._grid_written = False
        self._cleaned = False


    def commit_mctherm(self):
        '''
        Writes the encapsulated data to files in the output directory, to be
        read by RADMC3D for Monte Carlo thermal simulation.
        '''

        if not self._cleaned:
            self._io.smart_clean_outdir()
            self._cleaned = True

        self.write_wavelengths()

        if not self._config_written:
            self._config.write(self._io)
            self._config_written = True

        if not self._grid_written:
            self._grid.write(self._io)
            self._grid_written = True

        self._star.write(self._io, self._lmbda, self._grid)
        self._dust.write(self._io, self._grid)


    def commit_lines(self):
        '''
        '''
        if not self._cleaned:
            self._io.smart_clean_outdir()
            self._cleaned = True

        if not self._config_written:
            self._config.write(self._io)
            self._config_written = True

        if not self._grid_written:
            self._grid.write(self._io)
            self._grid_written = True

        self._gas.write(self._io, self._grid)


    def write_wavelengths(self):
        '''Private function; writes the list of wavelengths to a file.'''

        with self._io.file_open_write('wavelength_micron.inp') as f:
            f.write('%d\n' % self.nlmbda)
            self._lmbda.tofile(f, sep='\n', format='%e')


    def run_mctherm(self):
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

    @grid.setter
    def grid(self, g):
        self._grid = g

    @property
    def dust(self):
        '''Accessor to the underlying dust container object.'''
        return self._dust

    @property
    def gas(self):
        '''Accessor to the underlying molecule container object.'''
        return self._gas

    @property
    def star(self):
        '''Accessor to the underlying star container object.'''
        return self._star

# vim: set ft=python:
