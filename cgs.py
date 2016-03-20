# -*- coding: utf-8 -*-

class ClassPropertyDescriptor(object):
    '''
    See `this StackOverflow post <http://stackoverflow.com/a/5191224/1552418>`_.
    This snippet is the intellectual property of its original author.
    '''

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError('can\'t set attribute')
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self



def classproperty(func):
    '''
    See `this StackOverflow post <http://stackoverflow.com/a/5191224/1552418>`_.
    This snippet is the intellectual property of its original author.
    '''

    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)



class cgs(object):
    '''
    Accessors for values of common astronomical quantities in CGS
    (centimeters-grams-seconds) units.
    '''

    @classproperty
    def au(self):
        '''Astronomical unit, cm'''
        return 1.49597870700e13

    @classproperty
    def c(self):
        '''Speed of light in vacuum, cm/s'''
        return 2.99792458e10

    @classproperty
    def G(self):
        '''
        Newtonian gravitational constant,
        :math:`\\textrm{cm}^3 / \\textrm{g} / \\textrm{s}^2`
        '''
        return 6.67384e-8

    @classproperty
    def LSun(self):
        '''Solar luminosity, erg/s'''
        return 3.828e33

    @classproperty
    def MEarth(self):
        '''Earth mass, g'''
        return 5.9726e27

    @classproperty
    def MSun(self):
        '''Solar mass, g'''
        return 1.9885e33

    @classproperty
    def REarth(self):
        '''Earth radius, cm'''
        return 6.378137e8

    @classproperty
    def RSun(self):
        '''Solar radius, cm'''
        return 6.9551e10

# vim: set ft=python:
