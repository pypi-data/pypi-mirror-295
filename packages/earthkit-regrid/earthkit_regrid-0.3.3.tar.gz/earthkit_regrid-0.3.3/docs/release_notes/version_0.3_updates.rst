Version 0.3 Updates
/////////////////////////


Version 0.3.2
===============

Fixes
++++++++++++++++
- fixed issue when  reading an interpolation matrix from the cache unnecessarily invoked checking of remote matrix files on download server


Version 0.3.1
===============

Fixes
++++++++++++++++
- fixed issue when failed to interpolate from certain reduced Gaussian grids (e.g. O2560, O1280) to regular latitude-longitude grids when the input was an earthkit-data GRIB :xref:`fieldlist`


Version 0.3.0
===============

New features
++++++++++++++++
- restructured and regenerated matrix inventory
- allow using the ``method`` keyword in :func:`interpolate` to specify the interpolation method
- allow using earthkit-data GRIB :xref:`fieldlist` in :func:`interpolate` as input data. This only works when  the output grid is regular a latitude-longitude grid. This feature requires :xref:`earthkit-data` >= 0.6.0
- added notebook examples:

   - :ref:`/examples/healpix_fieldlist.ipynb`
   - :ref:`/examples/octahedral_fieldlist.ipynb`
