# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np


class Radmc3dIo(object):

    def __init__(self):

        self._outdir = os.getcwd()
        self._clobber = False
        self._binary = False
        self._precis = 8
        self._dtype = np.float64


    def memmap(self, f, offset, dtype, shape, mode):
        ''' '''
        if type(f) is str: f = self.fullpath(f)
        return np.memmap(f, dtype=dtype, mode=mode, offset=offset,
            shape=shape, order='F')


    def safe_check_clobber(self, target):

        if not self.clobber and os.path.isfile(target):
            while True:
                r = raw_input('the file %s already exists! overwrite? [y/n] '
                    % target)
                r = r.lower()

                if r in ['y', 'n']:
                    break

            if r == 'n':
                raise RuntimeError('file overwrite aborted by user!')


    def fullpath(self, fname):

        return os.path.join(self.outdir, fname)


    def file_check_exists(self, target):

        return os.path.isfile(self.fullpath(target))


    def file_open_write(self, target):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        return open(fp, 'w')


    def file_open_read(self, target):

        fp = self.fullpath(target)
        return open(fp, 'r')


    def file_copy(self, src, dest):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        shutil.copy(src, fp)


    def file_delete(self, target):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        os.remove(fp)


    @property
    def outdir(self):
        return self._outdir

    @outdir.setter
    def outdir(self, val):
        self._outdir = val

    @property
    def clobber(self):
        return self._clobber

    @clobber.setter
    def clobber(self, val):
        self._clobber = val

    @property
    def binary(self):
        return self._binary

    @binary.setter
    def binary(self, val):
        self._binary = val

    @property
    def precision(self):
        return 'double' if self._precis == 8 else 'single'

    @precision.setter
    def precision(self, val):
        self._precis = 8 if val == 'double' else 4
        self._dtype = np.float64 if val == 'double' else np.float32

    @property
    def precis(self):
        return self._precis

    @property
    def dtype(self):
        return self._dtype

# vim: set ft=python:
