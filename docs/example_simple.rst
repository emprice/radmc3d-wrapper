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


   io = r3d.Radmc3dIo('simfiles', binary=False)

   config = r3d.Radmc3dConfiguration(io)
   config.istar_sphere = False
   config.incl_dust = True
   config.nphot = 100000
   config.write()

   grid = r3d.Radmc3dGrid(io, r3d.coordsys.CartesianCoordinates)
   grid.u = np.linspace(-10., 10., 32) * r3d.cgs.au
   grid.v = np.linspace(-10., 10., 32) * r3d.cgs.au
   grid.w = np.linspace(-10., 10., 32) * r3d.cgs.au
   grid.write(binary=False)

   dust = MyDust(rho0=1.e-16, sigma=5.*r3d.cgs.au)
   density = r3d.Radmc3dDustDensity(io, dust)
   density.write(grid, binary=False)
