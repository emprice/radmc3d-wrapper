# -*- coding: utf-8 -*-

import re
import os
import glob
import numpy as np


class Io(object):
    '''
    Class defining common I/O operations needed by the module so that they
    can be carried out in a consistent way.
    '''

    def __init__(self):

        self._outdir = os.getcwd()
        self._clobber = False
        self._binary = False
        self._precis = 8
        self._dtype = np.float64


    def smart_clean_outdir(self):
        '''
        '''

        p = re.compile(r'(.*?\.(binp|bdat))|(radmc3d\..*)|(^(?!(dustkappa|molecule)).*?\.inp)|(.*?\.vt[usk]{1})')

        for dirpath, dirnames, filenames in os.walk(self._outdir):
            for f in filenames:
                if p.match(f): self.file_remove(f)
            break


    def fullpath(self, fname):
        '''
        Returns a "full path" (the concatenation of the output directory and
        given filename) to a file.

        :param str fname: The filename relative to the output directory

        :returns: The filename relative to the initial directory
        :rtype: str
        '''

        return os.path.join(self.outdir, fname)


    def memmap(self, f, offset, dtype, shape, mode):
        '''
        Returns a memory map (in FORTRAN order, since RADMC3D uses this
        format exclusively) that can be used like an array but is written
        to a file in binary format.

        :param f: A filename or file-like object; if a filename is given, it
            should be relative to the global output directory
        :param int offset: Offset in the file (in bytes) at which the map should
            begin
        :param dtype: The data type (:code:`np.float64` or :code:`np.float32`)
            of the mapped array
        :param tuple shape: A tuple representing the shape of the mapped array
        :param str mode: The mode string, generally :code:`w+` for writing or
            :code:`r` for reading only

        :returns: Memory map to the array
        :rtype: numpy.core.memmap.memmap
        '''

        if type(f) is str: f = self.fullpath(f)
        return np.memmap(f, dtype=dtype, mode=mode, offset=offset,
            shape=shape, order='F')


    def safe_check_clobber(self, target):
        '''
        Checks whether it is safe to clobber a file. If the user has specified
        that file clobbering is allowed or if the file does not exist, this
        method has no effect; otherwise, the user is prompted for each
        existing file and must approve clobbering to continue.

        :param str target: A filename relative to the global output directory

        :raises RuntimeError: if the user aborts clobbering
        '''

        fp = self.fullpath(target)
        if not self.clobber and os.path.isfile(fp):
            while True:
                r = raw_input('the file %s already exists! ' % fp +
                              'ok to overwrite? [y/n] ')
                r = r.lower()

                if r in ['y', 'n']:
                    break

            if r == 'n':
                raise RuntimeError('file overwrite aborted by user!')


    def file_check_exists(self, target):
        '''
        Checks whether the given file exists.

        :param str target: A filename relative to the global output directory

        :returns: :code:`True` if the file exists, :code:`False` otherwise
        :rtype: bool
        '''

        return os.path.isfile(self.fullpath(target))


    def file_open_write(self, target):
        '''
        Opens a file for writing, checking whether it is safe to clobber any
        existing file by the same name before doing so.

        :param str target: A filename relative to the global output directory

        :returns: A file pointer to the open file
        :rtype: file
        '''

        self.safe_check_clobber(target)
        return open(self.fullpath(target), 'w')


    def file_open_read(self, target):
        '''
        Opens a file for reading; there is no need to check whether clobbering
        is safe in this case, because this is not a destructive operation.

        :param str target: A filename relative to teh global output directory

        :returns: A file pointer to the open file
        :rtype: file
        '''

        return open(self.fullpath(target), 'r')


    def file_remove(self, target):
        self.safe_check_clobber(target)
        os.remove(self.fullpath(target))


    @property
    def outdir(self):
        '''The output directory, relative to the initial directory'''
        return self._outdir

    @outdir.setter
    def outdir(self, val):
        self._outdir = val

    @property
    def clobber(self):
        '''
        :code:`True` if existing files should be clobbered if they already
        exist, :code:`False` otherwise.
        '''
        return self._clobber

    @clobber.setter
    def clobber(self, val):
        self._clobber = val

    @property
    def binary(self):
        '''
        :code:`True` if input files should be binary; :code:`False` if
        ASCII should be used instead. Note that this has no effect on the
        format of output files; for that setting, see
        :func:`~configuration.Configuration.rto_style`.
        '''
        return self._binary

    @binary.setter
    def binary(self, val):
        self._binary = val

    @property
    def precision(self):
        '''
        Set to :code:`double` if double-precision input is desired; otherwise,
        set to :code:`single`. Note that this has no effect on the format of
        output files; for that setting, see
        :func:`~configuration.Configuration.rto_single`.
        '''
        return 'double' if self._precis == 8 else 'single'

    @precision.setter
    def precision(self, val):
        self._precis = 8 if val == 'double' else 4
        self._dtype = np.float64 if val == 'double' else np.float32

    @property
    def precis(self):
        '''
        Read-only; gives the number of bytes of the current float data type.
        '''
        return self._precis

    @property
    def dtype(self):
        '''Read-only; gives the current float data type as a NumPy dtype.'''
        return self._dtype

# vim: set ft=python:
