Simple use example
==================

.. code-block:: python
   import radmc3d as r3d
   import numpy as np


   class MyDust(r3d.Radmc3dDustSpecies):
       def __init__(self, rho0, sigma):
           self.rho0 = rho0
           self.sigma = sigma

       def density(self, coords):
           rr, _, _ = coords.transformTo(r3d.SphericalCoordinates)
           return self.rho0 * np.exp(-0.5 * rr**2 / self.sigma**2)


   sim = r3d.Radmc3dSimulation()

   sim.io.outdir = 'simfiles'
   sim.io.clobber = True
   sim.io.binary = True

   sim.config.istar_sphere = False
   sim.config.incl_dust = True
   sim.config.nphot = 100000

   sim.grid.coordsys = r3d.coordsys.CartesianCoordinates
   sim.grid.u = np.linspace(-10., 10., 32) * r3d.cgs.au
   sim.grid.v = np.linspace(-10., 10., 32) * r3d.cgs.au
   sim.grid.w = np.linspace(-10., 10., 32) * r3d.cgs.au

   sim.lmbda = np.logspace(-1., 3., 1000)

   sim.dust['silicate'] = MyDust(rho0=1.e-16, sigma=5.*r3d.cgs.au)

   sim.star[0] = r3d.Radmc3dBlackbodyStar(radius=r3d.cgs.RSun,
       mass=r3d.cgs.MSun, Teff=5700.,
       center=r3d.CartesianCoordinates(0., 0., 0.),

   sim.commit()
   sim.mctherm()
   sim.render()
