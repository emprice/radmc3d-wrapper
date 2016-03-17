# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np


class Radmc3dIo(object):
    '''
    Handles file opening, reading, and clobbering in a safe and consistent way.

    :param outdir: Output directory for all simulation files (including
        intermediates, which are *not* removed)
    :param clobber: If :code:`True`, clobbers existing files without prompting;
        if :code:`False`, prompts the user for each file before clobbering.
    '''

    def __init__(self, outdir, clobber=False, binary=True, precision='double'):

        self.outdir = outdir
        self.clobber = clobber
        self._binary = binary
        self._precis = 8 if precision == 'double' else 4
        self._dtype = np.float64 if precision == 'double' else np.float32


    def memmap(self, f, offset, dtype, shape, mode):
        ''' '''
        return np.memmap(f, dtype=dtype, mode=mode, offset=offset,
            shape=shape, order='F')


    def safe_check_clobber(self, target):

        if not self.clobber and self.file_check_exists(target):
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

        return os.path.isfile(target)


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
    def binary(self):
        return self._binary


    @property
    def precision(self):
        return self._precis

# vim: set ft=python:
