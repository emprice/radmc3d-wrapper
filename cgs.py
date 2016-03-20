# -*- coding: utf-8 -*-

class cgs(object):

    @property
    def au(self):
        '''Astronomical unit, cm'''
        return 1.49597870700e13

    @property
    def c(self):
        '''Speed of light in vacuum, cm/s'''
        return 2.99792458e10

    @property
    def G(self):
        '''Newtonian gravitational constant, cm^3/g/s^2'''
        return 6.67384e-8

    @property
    def LSun(self):
        '''Solar luminosity, erg/s'''
        return 3.828e33

    @property
    def MEarth(self):
        '''Earth mass, g'''
        return 5.9726e27

    @property
    def MSun(self):
        '''Solar mass, g'''
        return 1.9885e33

    @property
    def REarth(self):
        '''Earth radius, cm'''
        return 6.378137e8

    @property
    def RSun(self):
        '''Solar radius, cm'''
        return 6.9551e10
