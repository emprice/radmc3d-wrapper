# -*- coding: utf-8 -*-

import os
import shutil


class Radmc3dIo(object):
    '''
    Handles file opening, reading, and clobbering in a safe and consistent way.

    :param outdir: Output directory for all simulation files (including
        intermediates, which are *not* removed)
    :param clobber: If `True`, clobbers existing files without prompting; if
        `False`, prompts the user for each file before clobbering.
    '''

    def __init__(self, outdir, clobber=False, binary_input=True):

        self.outdir = outdir
        self.clobber = clobber

        ext = 'binp' if binary_input else 'inp'
        self.filemap = \
            { 'config' : 'radmc3d.inp',
              'amr_grid' : '.'.join(['amr_grid', ext]),
              'dust_density' : '.'.join(['dust_density', ext]),
              'dust_temperature' : '.'.join(['dust_temperature', ext]),
              'gas_number_density' : '.'.join(['gas_number_density', ext]) }


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

        return os.path.join(self.outdir, self.filemap[fname])


    def file_check_exists(self, target):

        return os.path.isfile(target)


    def file_open_write(self, target):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        return open(fp, 'wb')


    def file_open_read(self, target):

        fp = self.fullpath(target)
        return open(fp, 'rb')


    def file_copy(self, src, dest):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        shutil.copy(src, fp)


    def file_delete(self, target):

        fp = self.fullpath(target)
        self.safe_check_clobber(fp)
        os.remove(fp)

# vim: set ft=python:
