# -*- coding: utf-8 -*-

import numpy as np
from mapper import *


class GasModel(object):
    '''
    '''

    def density(self, coords, simvars):
        raise NotImplementedError

    def temperature(self, coords, simvars):
        raise NotImplementedError



class MoleculeSpecies(object):
    '''
    '''

    def __init__(self, X=1., inpstyle='leiden', iduma=0, idumb=0,
    partners=list(), mass=4.65119e-23):
        self._inpstyle = inpstyle
        self._iduma = iduma
        self._idumb = idumb
        self._partners = partners
        self._X = X
        self._mass = mass

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, x):
        self._X = x

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, m):
        self._mass = m

    @property
    def inpstyle(self):
        return self._inpstyle

    @inpstyle.setter
    def inpstyle(self, inp):
        self._inpstyle = inp

    @property
    def iduma(self):
        return self._iduma

    @iduma.setter
    def iduma(self, i):
        self._iduma = i

    @property
    def idumb(self):
        return self._idumb

    @idumb.setter
    def idumb(self, i):
        self._idumb = i

    @property
    def partners(self):
        return self._partners

    @partners.setter
    def partners(self, ps):
        self._partners = list(ps)



class MoleculeContainer(dict):
    '''
    Container for a variable number of molecular species. To support friendly
    naming of molecular species, this class inherits from :code:`dict` so that
    new species can be added like so:

    >>> c = MoleculeContainer()
    >>> c.model = SomeGasModel()
    >>> c['some_name'] = MoleculeSpecies()

    If a duplicate name is used, the previous species will be overwritten.
    '''

    def write(self, io, grid):
        '''
        Writes the current content of this container to input files for
        RADMC3D. This function uses the I/O context to determine the output
        format (binary or ASCII) and formats all files appropriately.

        :param fileio.Io io: Current I/O context
        :param grid.Grid grid: Current grid definition
        '''

        with io.file_open_write('line.inp') as f:
            f.write('2\n')
            f.write('%d\n' % len(self))

            for k, g in zip(self.keys(), self.values()):
                f.write('%s\t%s\t%d\t%d\t%d\n' % (k, g.inpstyle,
                    g.iduma, g.idumb, len(g.partners)))

                for p in g.partners:
                    f.write('%s\n' % p)

        hdr = np.empty((2,), dtype=np.int64)
        hdr[0] = 1
        hdr[1] = grid.nrcells

        if io.binary:
            hdr = np.insert(hdr, 1, [np.dtype(io.dtype).itemsize])

        mapper = Mapper()
        simvars = mapper.map_variables(io, grid)

        ext = 'binp' if io.binary else 'inp'
        fname = '.'.join(['gas_temperature', ext])
        sep = '' if io.binary else '\n'

        with io.file_open_write(fname) as f:
            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')

            if io.binary:
                shape = grid.shape
                offset = hdr.nbytes

                gastemp = io.memmap(fname, offset=offset, shape=shape,
                    dtype=io.dtype, mode='w+')
                gastemp[:] = self.model.temperature(grid.cellcoords, simvars)[:]

            else:
                gastemp = self.model.temperature(grid.cellcoords, simvars).\
                    ravel(order='F')
                gastemp.tofile(f, sep=sep, format='%e')

        density = self.model.density(grid.cellcoords, simvars)

        for k, g in zip(self.keys(), self.values()):
            fname = '.'.join(['numberdens_%s' % k, ext])
            number_density = density * g.X / g.mass

            with io.file_open_write(fname) as f:
                hdr.tofile(f, sep=sep, format='%d')
                if not io.binary: f.write('\n')

                if io.binary:
                    shape = grid.shape
                    offset = hdr.nbytes

                    numdens = io.memmap(fname, offset=offset, shape=shape,
                        dtype=io.dtype, mode='w+')
                    numdens[:] = number_density

                else:
                    numdens = number_density.ravel(order='F')
                    numdens.tofile(f, sep=sep, format='%e')

        fname = '.'.join(['gas_velocity', ext])

        with io.file_open_write(fname) as f:
            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')

            shape = (3,) + grid.shape

            if io.binary:
                offset = hdr.nbytes
                gasvel = io.memmap(fname, offset=offset, shape=shape,
                    dtype=io.dtype, mode='w+')
            else:
                gasvel = np.empty(shape, dtype=io.dtype)

            gasvel[0,:,:,:], gasvel[1,:,:,:], gasvel[2,:,:,:] = \
                self.model.velocity(grid.cellcoords).transformTo(grid.vectorsys)

            if not io.binary:
                gasvel = np.column_stack((gasvel[0,:,:,:].ravel(order='F'),
                    gasvel[1,:,:,:].ravel(order='F'),
                    gasvel[2,:,:,:].ravel(order='F')))
                gasvel.tofile(f, sep='\n', format='%e')


    @property
    def model(self):
        ''' '''
        return self._model

    @model.setter
    def model(self, m):
        ''' '''
        self._model = m

# vim: set ft=python:
