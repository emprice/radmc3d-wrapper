# -*- coding: utf-8 -*-

import abc
import numpy as np


class Coordinates(object):
    '''
    Base class for coordinate containers. All coordinates are expected to be
    stored as Cartesian regardless of the coordinate system. This class is
    then responsible for converting to any supported coordinate system.
    '''

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def __init__(self):
        pass


    def transformTo(self, sys):
        '''
        Transforms the coordinates stored in this container to the coordinate
        system specified.

        :param Coordinates sys: The coordinate system to transform to
        '''

        if sys == CartesianCoordinates:

            return self.x, self.y, self.z

        elif sys == SphericalCoordinates:

            r     = np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
            theta = np.mod(np.arctan2(np.sqrt(self.x * self.x +
                self.y * self.y), self.z) + 2. * np.pi, 2. * np.pi)
            phi   = np.mod(np.arctan2(self.y, self.x) + 2. * np.pi, 2. * np.pi)

            return r, theta, phi

        elif sys == CylindricalCoordinates:

            s   = np.sqrt(self.x * self.x + self.y * self.y)
            phi = np.mod(np.arctan2(self.y, self.x) + 2. * np.pi, 2. * np.pi)

            return s, phi, self.z

        raise NotImplementedError(sys)



class CartesianCoordinates(Coordinates):
    '''
    Basic container class for Cartesian coordinates.

    :param x: The *x*-coordinate; may be a float type or NumPy array
    :param y: The *y*-coordinate; may be a float type or NumPy array
    :param z: The *z*-coordinate; may be a float type or NumPy array
    '''

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z



class SphericalCoordinates(Coordinates):
    '''
    Basic container class for spherical polar coordinates.

    :param r: The radial coordinate; may be a float type or NumPy array
    :param theta: The latitudinal coordinate; may be a float type or NumPy array
    :param phi: The azimuthal coordinate; may be a float type or NumPy array
    '''

    def __init__(self, r, theta, phi):

        self.x = r * np.sin(theta) * np.cos(phi)
        self.y = r * np.sin(theta) * np.sin(phi)
        self.z = r * np.cos(theta)



class CylindricalCoordinates(Coordinates):
    '''
    Basic container class for cylindrical coordinates.

    :param s: The radial coordinate; may be a float type or NumPy array
    :param phi: The azimuthal coordinate; may be a float type or NumPy array
    :param z: The vertical coorindate; may be a float type or NumPy array
    '''

    def __init__(self, s, phi, z):

        self.x = s * np.cos(phi)
        self.y = s * np.sin(phi)
        self.z = z
