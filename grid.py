# -*- coding: utf-8 -*-

import numpy as np


class Radmc3dGrid(object):

    def __init__(self, io):

        self.io = io


    def load(self, binary=True):
        '''
        Reads a grid definition from an existing file
        '''

        sep = '' if binary else ' '

        with self.io.file_open_read('amr_grid') as f:
            count = 3 if binary else 2
            hdr = np.fromfile(f, dtype=np.int64, count=count, sep=sep)

            self.iformat = hdr[0]
            assert self.iformat == 1

            dtype = np.float64 if not binary else \
                (np.float64 if hdr[1] == 8 else np.float32)
            self.gridstyle = hdr[1] if not binary else hdr[2]

            if self.gridstyle == 0:
                hdr = np.fromfile(f, dtype=np.int64, count=8, sep=sep)
                self.coordsystem, _, self.inclx, self.incly, \
                    self.inclz, self.nx, self.ny, self.nz = hdr

                self.x = np.fromfile(f, dtype=dtype, count=self.nx+1, sep=sep)
                self.y = np.fromfile(f, dtype=dtype, count=self.ny+1, sep=sep)
                self.z = np.fromfile(f, dtype=dtype, count=self.nz+1, sep=sep)

            elif self.gridstyle == 1:
                raise NotImplementedError

            elif self.gridstyle == 2:
                raise NotImplementedError

            else:
                raise NotImplementedError

# vim: set ft=python:
