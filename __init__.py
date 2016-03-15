# -*- coding: utf-8 -*-

import os
from configuration import *


class Radmc3dIo(object):

    def __init__(self, outdir, clobber=False):

        self.outdir = outdir
        self.clobber = clobber


    def safe_check_clobber(self, target):

        if not self.clobber and os.path.isfile(target):
            while True:
                r = raw_input('the file %s already exists! overwrite? [y/n] ')
                r = r.lower()

                if r in ['y', 'n']:
                    break

            if r == 'n':
                raise RuntimeError('file overwrite aborted by user!')


    def file_open_write(self, target, clobber=False):

        self.safe_check_clobber(target)
        return open(target, 'w')


    def fullpath(self, fname):

        return os.path.join(self.outdir, fname)

# vim: set ft=python:
