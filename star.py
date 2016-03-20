# -*- coding: utf-8 -*-

from coordsys import CartesianCoordinates


class Radmc3dStar(object):

    def __init__(self, center=CartesianCoordinates(0.,0.,0.),
    mass=0., radius=0.):

        self._radius = radius
        self._mass = mass
        self._center = center


    def write(self, f, lmbda):

        raise NotImplementedError


    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, coord):
        self._center = coord



class Radmc3dBlackbodyStar(Radmc3dStar):

    def __init__(self, Teff=0., **kwargs):

        super(Radmc3dBlackbodyStar, self).__init__(**kwargs)
        self._Teff = Teff


    def write(self, f, lmbda):

        f.write('%e\n' % -(self._Teff))


    @property
    def Teff(self):
        return self._Teff

    @Teff.setter
    def Teff(self, val):
        self._Teff = val



class Radmc3dStarContainer(dict):

    def write(self, io, lmbda, grid):

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
