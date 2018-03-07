# -*- coding: utf-8 -*-

import numpy as np
from mapper import *
from coordsys import CartesianCoordinates


class VtkRender(object):
    '''
    Renders the current input and output files as VTK output that can be
    visualized with VisIt and other VTK visualization software.
    '''

    def render(self, io, grid):
        '''
        Writes the VTK file for all variables that can be found in the output
        directory.

        :param Io io: Current I/O context
        :param Grid grid: Current grid definition
        '''

        mapper = Mapper()
        mapped = mapper.map_variables(io, grid)

        vtk_grid = grid.vtk

        for scalar in ['dust_density', 'dust_temperature', 'gas_number_density']:
            for k, v in mapped[scalar].items():
                if v is None: continue
                vtk_grid.add_scalar_cell_data('%s_%s' % (scalar, k), v.ravel())

        for scalar in ['gas_temperature']:
            s = mapped[scalar]
            if s is None: continue
            vtk_grid.add_scalar_cell_data(scalar, s.ravel())

        for vector in ['gas_velocity']:
            v = mapped[vector]
            if v is None: continue
            vtk_grid.add_vector_cell_data(vector, v[:,0], v[:,1], v[:,2])

        vtk_grid.write_to_file('model')

# vim: set ft=python:
