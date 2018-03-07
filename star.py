# -*- coding: utf-8 -*-

from coordsys import CartesianCoordinates


class Star(object):
    '''
    Base class for a star definition.

    :param Coordinates center: The coordinates of the center (can use any
        coordinate system; defaults to (0,0,0)
    :param float mass: The mass of the star
    :param float radius: The radius of the star
    '''

    def __init__(self, center=CartesianCoordinates(0.,0.,0.),
    mass=0., radius=0.):

        self._radius = radius
        self._mass = mass
        self._center = center


    def write(self, f, lmbda):
        '''
        Subclasses must define this method, which writes either the effective
        temperature or the flux to the given file handle in the format expected
        by RADMC3D.

        :param file f: Open file handle
        :param np.ndarray lmbda: Array of wavelengths
        '''
        raise NotImplementedError


    @property
    def radius(self):
        '''The radius of this star'''
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def mass(self):
        '''The mass of this star'''
        return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def center(self):
        '''
        The coordinates of the center of this star; expects a subclass of
        :class:`Coordinates`.
        '''
        return self._center

    @center.setter
    def center(self, coord):
        self._center = coord



class BlackbodyStar(Star):
    '''
    Defines an ideal blackbody star, which is parametrized by only its
    effective temperature.

    :param float Teff: Effective temperature in Kelvin
    '''

    def __init__(self, Teff=0., **kwargs):

        super(BlackbodyStar, self).__init__(**kwargs)
        self._Teff = Teff


    def write(self, f, lmbda):
        '''Writes the effective temperature to the open file handle.'''
        f.write('%e\n' % -(self._Teff))


    @property
    def Teff(self):
        '''Effective temperature of this star'''
        return self._Teff

    @Teff.setter
    def Teff(self, val):
        self._Teff = val



class StarContainer(dict):
    '''
    Container for a variable number of stars. To support friendly naming
    of stars, this class inherits from :code:`dict` so that new stars can be
    added like so:

    >>> c = StarContainer()
    >>> c[0] = BlackbodyStar()
    >>> c[0].Teff = 5700.

    String names can also be used instead of numeric indices. If a duplicate
    name is used, the previous star will be overwritten.
    '''

    def write(self, io, lmbda, grid):
        '''
        Writes the current content of this container to input files for
        RADMC3D. This function uses the I/O context to determine the output
        format (binary or ASCII) and formats all files appropriately.

        :param fileio.Io io: Current I/O context
        :param np.ndarray lmbda: Wavelength array
        :param grid.Grid grid: Current grid definition
        '''

        with io.file_open_write('stars.inp') as f:
            f.write('2\n')
            f.write('%d\t%d\n' % (len(self), lmbda.shape[0]))

            for s in self.values():
                u, v, w = s.center.transformTo(grid.coordsys)
                f.write('%e\t%e\t%e\t%e\t%e\n' % (s.radius, s.mass, u, v, w))

            lmbda.tofile(f, sep='\n', format='%e')
            f.write('\n')

            for s in self.values():
                s.write(f, lmbda)

# vim: set ft=python:
