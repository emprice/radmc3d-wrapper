# -*- coding: utf-8 -*-

import numpy as np


class Configuration(object):
    '''
    Simple container class for the RADMC3D configuration. Both member assignment
    and retrieval are supported, but no validation is done on the set values.
    '''

    def __init__(self):

        self._incl_dust = None
        self._incl_lines = None
        self._incl_freefree = None
        self._nphot = None
        self._nphot_scat = None
        self._nphot_spec = None
        self._iseed = None
        self._ifast = None
        self._enthres = None
        self._itempdecoup = None
        self._istar_sphere = None
        self._ntemp = None
        self._temp0 = None
        self._temp1 = None
        self._scattering_mode_max = None
        self._rto_style = None
        self._camera_tracemode = None
        self._camera_nrrefine = None
        self._camera_refine_criterion = None
        self._camera_incl_stars = None
        self._camera_starsphere_nrpix = None
        self._camera_spher_cavity_relres = None
        self._camera_localobs_projection = None
        self._camera_min_dangle = None
        self._camera_max_dangle = None
        self._camera_min_dr = None
        self._camera_diagnostics_subpix = None
        self._camera_secondorder = None
        self._camera_interpol_jnu = None
        self._mc_weighted_photons = None
        self._optimized_motion = None
        self._lines_mode = None
        self._lines_maxdoppler = None
        self._lines_partition_ntempint = None
        self._lines_partition_temp0 = None
        self._lines_partition_temp1 = None
        self._lines_show_pictograms = None
        self._tgas_eq_tdust = None
        self._modified_random_walk = None


    def write(self, io):
        '''
        Writes the encapsulated configuration to the file :code:`radmc3d.inp`.

        :param Io io: Global I/O instance
        '''

        with io.file_open_write('radmc3d.inp') as f:
            props = self.__dict__
            props = { k[1:] : v for k, v in props.items()
                      if k[0] == '_' and v is not None }
            temp = ['%s = %s' % (k, (v if not isinstance(v, bool) else
                int(v))) for k, v in props.items()]
            f.write('\n'.join(temp))


    @property
    def incl_dust(self):
        return self._incl_dust

    @incl_dust.setter
    def incl_dust(self, val):
        self._incl_dust = val

    @property
    def incl_lines(self):
        return self._incl_lines

    @incl_lines.setter
    def incl_lines(self, val):
        self._incl_lines = val

    @property
    def incl_freefree(self):
        return self._incl_freefree

    @incl_freefree.setter
    def incl_freefree(self, val):
        self._incl_freefree = val

    @property
    def nphot(self):
        return self._nphot

    @nphot.setter
    def nphot(self, val):
        self._nphot = val

    @property
    def nphot_scat(self):
        return self._nphot_scat

    @nphot_scat.setter
    def nphot_scat(self, val):
        self._nphot_scat = val

    @property
    def nphot_spec(self):
        return self._nphot_spec

    @nphot_spec.setter
    def nphot_spec(self, val):
        self._nphot_spec = val

    @property
    def iseed(self):
        return self._iseed

    @iseed.setter
    def iseed(self, val):
        self._iseed = val

    @property
    def ifast(self):
        return self._ifast

    @ifast.setter
    def ifast(self, val):
        self._ifast = val

    @property
    def enthres(self):
        return self._enthres

    @enthres.setter
    def enthres(self, val):
        self._enthres = val

    @property
    def itempdecoup(self):
        return self._itempdecoup

    @itempdecoup.setter
    def itempdecoup(self, val):
        self._itempdecoup = val

    @property
    def istar_sphere(self):
        return self._istar_sphere

    @istar_sphere.setter
    def istar_sphere(self, val):
        self._istar_sphere = val

    @property
    def ntemp(self):
        return self._ntemp

    @ntemp.setter
    def ntemp(self, val):
        self._ntemp = val

    @property
    def temp0(self):
        return self._temp0

    @temp0.setter
    def temp0(self, val):
        self._temp0 = val

    @property
    def temp1(self):
        return self._temp1

    @temp1.setter
    def temp1(self, val):
        self._temp1 = val

    @property
    def scattering_mode_max(self):
        return self._scattering_mode_max

    @scattering_mode_max.setter
    def scattering_mode_max(self, val):
        self._scattering_mode_max = val

    @property
    def rto_style(self):
        return self._rto_style

    @rto_style.setter
    def rto_style(self, val):
        self._rto_style = val

    @property
    def camera_tracemode(self):
        return self._camera_tracemode

    @camera_tracemode.setter
    def camera_tracemode(self, val):
        self._camera_tracemode = val

    @property
    def camera_nrrefine(self):
        return self._camera_nrrefine

    @camera_nrrefine.setter
    def camera_nrrefine(self, val):
        self._camera_nrrefine = val

    @property
    def camera_refine_criterion(self):
        return self._camera_refine_criterion

    @camera_refine_criterion.setter
    def camera_refine_criterion(self, val):
        self._camera_refine_criterion = val

    @property
    def camera_incl_stars(self):
        return self._camera_incl_stars

    @camera_incl_stars.setter
    def camera_incl_stars(self, val):
        self._camera_incl_stars = val

    @property
    def camera_starsphere_nrpix(self):
        return self._camera_starsphere_nrpix

    @camera_starsphere_nrpix.setter
    def camera_starsphere_nrpix(self, val):
        self._camera_starsphere_nrpix = val

    @property
    def camera_spher_cavity_relres(self):
        return self._camera_spher_cavity_relres

    @camera_spher_cavity_relres.setter
    def camera_spher_cavity_relres(self, val):
        self._camera_spher_cavity_relres = val

    @property
    def camera_localobs_projection(self):
        return self._camera_localobs_projection

    @camera_localobs_projection.setter
    def camera_localobs_projection(self, val):
        self._camera_localobs_projection = val

    @property
    def camera_min_dangle(self):
        return self._camera_min_dangle

    @camera_min_dangle.setter
    def camera_min_dangle(self, val):
        self._camera_min_dangle = val

    @property
    def camera_max_dangle(self):
        return self._camera_max_dangle

    @camera_max_dangle.setter
    def camera_max_dangle(self, val):
        self._camera_max_dangle = val

    @property
    def camera_min_dr(self):
        return self._camera_min_dr

    @camera_min_dr.setter
    def camera_min_dr(self, val):
        self._camera_min_dr = val

    @property
    def camera_diagnostics_subpix(self):
        return self._camera_diagnostics_subpix

    @camera_diagnostics_subpix.setter
    def camera_diagnostics_subpix(self, val):
        self._camera_diagnostics_subpix = val

    @property
    def camera_secondorder(self):
        return self._camera_secondorder

    @camera_secondorder.setter
    def camera_secondorder(self, val):
        self._camera_secondorder = val

    @property
    def camera_interpol_jnu(self):
        return self._camera_interpol_jnu

    @camera_interpol_jnu.setter
    def camera_interpol_jnu(self, val):
        self._camera_interpol_jnu = val

    @property
    def mc_weighted_photons(self):
        return self._mc_weighted_photons

    @mc_weighted_photons.setter
    def mc_weighted_photons(self, val):
        self._mc_weighted_photons = val

    @property
    def optimized_motion(self):
        return self._optimized_motion

    @optimized_motion.setter
    def optimized_motion(self, val):
        self._optimized_motion = val

    @property
    def lines_mode(self):
        return self._lines_mode

    @lines_mode.setter
    def lines_mode(self, val):
        self._lines_mode = val

    @property
    def lines_maxdoppler(self):
        return self._lines_maxdoppler

    @lines_maxdoppler.setter
    def lines_maxdoppler(self, val):
        self._lines_maxdoppler = val

    @property
    def lines_partition_ntempint(self):
        return self._lines_partition_ntempint

    @lines_partition_ntempint.setter
    def lines_partition_ntempint(self, val):
        self._lines_partition_ntempint = val

    @property
    def lines_partition_temp0(self):
        return self._lines_partition_temp0

    @lines_partition_temp0.setter
    def lines_partition_temp0(self, val):
        self._lines_partition_temp0 = val

    @property
    def lines_partition_temp1(self):
        return self._lines_partition_temp1

    @lines_partition_temp1.setter
    def lines_partition_temp1(self, val):
        self._lines_partition_temp1 = val

    @property
    def lines_show_pictograms(self):
        return self._lines_show_pictograms

    @lines_show_pictograms.setter
    def lines_show_pictograms(self, val):
        self._lines_show_pictograms = val

    @property
    def tgas_eq_tdust(self):
        return self._tgas_eq_tdust

    @tgas_eq_tdust.setter
    def tgas_eq_tdust(self, val):
        self._tgas_eq_tdust = val

    @property
    def modified_random_walk(self):
        return self._modified_random_walk

    @modified_random_walk.setter
    def modified_random_walk(self, val):
        self._modified_random_walk = val

# vim: set ft=python:
