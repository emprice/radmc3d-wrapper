# -*- coding: utf-8 -*-

import os
import shlex
import subprocess


def execute(cmd, working_dir):

    olddir = os.getcwd()

    try:
        os.chdir(working_dir)

        args = shlex.split(cmd)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        for line in iter(proc.stdout.readline, b''):
            sys.stdout.write(line)
            sys.stdout.flush()
        for line in iter(proc.stderr.readline, b''):
            sys.stderr.write(line)
            sys.stderr.flush()
    finally:
        os.chdir(olddir)


from fileio import *
from configuration import *
from grid import *
from simulation import *
from render import *

# vim: set ft=python:
