# -*- coding: utf-8 -*-

import numpy as np


class Radmc3dDustSpecies(object):
    '''
    Base class from which all dust species definitions should inherit. For
    example, to define a new (and fairly contrived) species with density
    everywhere equal to the square of the distance from the center:

    .. code-block:: python

       import radmc3d as r3d

       class SomeDustSpecies(r3d.Radmc3dDustSpecies):
           def density(self, coords):
               rr, _, _ = coords.transformTo(r3d.SphericalCoordinates)
               return rr**2
    '''

    def density(self, coords):
        '''
        Evaluates the dust density (in :math:`\\textrm{g} / \\textrm{cm}^3`) at
        each of the input coordinates. Vector operations are highly advised.

        :param Coordinates coords: The points at which to return the
            density

        :returns: An array of densities
        :rtype: np.ndarray

        :raises NotImplementedError: if the user does not define a density
            function
        '''
        raise NotImplementedError



class Radmc3dDustContainer(dict):
    '''
    Container for a variable number of dust species. To support friendly naming
    of dust species, this class inherits from :code:`dict` so that new
    species can be added like so:

    >>> c = Radmc3dDustContainer()
    >>> c['some_name'] = SomeDustSpecies()

    If a duplicate name is used, the previous species will be overwritten.
    '''

    def write(self, io, grid):
        '''
        Writes the current content of this container to input files for
        RADMC3D. This function uses the I/O context to determine the output
        format (binary or ASCII) and formats all files appropriately.

        :param fileio.Radmc3dIo io: Current I/O context
        :param grid.Radmc3dGrid grid: Current grid definition
        '''

        with io.file_open_write('dustopac.inp') as f:
            f.write('2\n')
            f.write('%d\n' % len(self))
            f.write('%s\n' % ('=' * 80))

            for k in self.keys():
                f.write('1\n0\n')
                f.write('%s\n' % k)
                f.write('%s\n' % ('=' * 80))

        ext = 'binp' if io.binary else 'inp'
        fname = '.'.join(['dust_density', ext])
        sep = '' if io.binary else '\n'

        with io.file_open_write(fname) as f:
            hdr = np.empty((3,), dtype=np.int64)
            hdr[0] = 1
            hdr[1] = grid.nrcells
            hdr[2] = len(self)

            if io.binary:
                hdr = np.insert(hdr, 1, [np.dtype(io.dtype).itemsize])

            hdr.tofile(f, sep=sep, format='%d')
            if not io.binary: f.write('\n')

            if io.binary:
                for i, d in enumerate(self.values()):
                    shape = (grid.nu, grid.nv, grid.nw)
                    offset = 4 * np.dtype(np.int64).itemsize + \
                        i * grid.nrcells * np.dtype(io.dtype).itemsize

                    density = io.memmap(fname, offset=offset, shape=shape,
                        dtype=io.dtype, mode='w+')
                    density[:] = d.density(grid.cellcoords)[:]

            else:
                for d in self.values():
                    density = d.density(grid.cellcoords)
                    density.tofile(f, sep=sep, format='%e')

# vim: set ft=python:
