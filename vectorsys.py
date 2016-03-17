# -*- coding: utf-8 -*-

import abc
import numpy as np
from coordsys import CartesianCoordinates, SphericalCoordinates, \
    CylindricalCoordinates


class VectorField(object):

    @abc.abstractmethod
    def __init__(self):
        pass


    def transformTo(self, sys):

        if sys == CartesianVectorField:

            return self.v_x, self.v_y, self.v_z

        elif sys == SphericalVectorField:

            _, theta, phi = self.coords.transform(SphericalCoordinates)

            v_r     = self.v_x * np.sin(theta) * np.cos(phi) + \
                      self.v_y * np.sin(theta) * np.sin(phi) + \
                      self.v_z * np.cos(theta)
            v_theta = self.v_x * np.cos(theta) * np.cos(phi) + \
                      self.v_y * np.cos(theta) * np.sin(phi) + \
                      self.v_z * -np.sin(theta)
            v_phi   = self.v_x * -np.sin(phi) + self.v_y * np.cos(phi)

            return v_r, v_theta, v_phi

        elif sys == CylindricalVectorField:

            _, phi, _ = self.coords.transform(CylindricalCoordinates)

            v_s   = self.v_x * np.cos(phi) + self.v_y * np.sin(phi)
            v_phi = self.v_x * -np.sin(phi) + self.v_y * np.cos(phi)

            return v_s, v_phi, self.v_z

        raise NotImplementedError(sys)



class CartesianVectorField(VectorField):

    def __init__(self, x, y, z, v_x, v_y, v_z):

        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

        self.coords = CartesianCoordinates(x, y, z)


class CylindricalVectorField(VectorField):

    def __init__(self, s, phi, z, v_s, v_phi, v_z):

        self.coords = CylindricalCoordinates(s, phi, z)

        self.v_x = v_s * np.cos(phi) + v_phi * -np.sin(phi)
        self.v_y = v_s * np.sin(phi) + v_phi * np.cos(phi)
        self.v_z = v_z


class SphericalVectorField(VectorField):

    def __init__(self, r, theta, phi, v_r, v_theta, v_phi):

        self.coords = SphericalCoordinates(r, theta, phi)

        self.v_x = v_r * np.sin(theta) * np.cos(phi) + \
                   v_theta * np.cos(theta) * np.cos(phi) + \
                   v_phi * -np.sin(phi)
        self.v_y = v_r * np.sin(theta) * np.sin(phi) + \
                   v_theta * np.cos(theta) * np.sin(phi) + \
                   v_phi * np.cos(phi)
        self.v_z = v_r * np.cos(theta) + v_theta * -np.sin(theta)
