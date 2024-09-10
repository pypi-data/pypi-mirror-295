v0.9.0 (2024-09-09)
===================




- Polcal fits are now done on a per-beam basis. Previously, a single fit to the Calibration Unit (CU) optics was performed
  for the entire DLNIRSP array. This essentially caused the two orthogonally polarized beams to cancel each other out for
  the CU fits. We now fit the CU optics separately for each beam and then use those results to also fit the demodulation
  matrices on a per-beam basis. (`#30 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/30>`__)


v0.8.0 (2024-09-04)
===================




- Linearization task now correctly handles multiple coadds. Previously we only processed the last coadd, but now all
  coadds are processed separately and then averaged together, which improves signal-to-noise. (`#28 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/28>`__)


v0.7.0 (2024-08-19)
===================




- Update linearity correction to average initial bias frames if more than one is found. Uses the last read NDR as opposed to the last NDR, which may be a bias NDR. (`#22 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/22>`__)


v0.6.0 (2024-07-30)
===================




- Two relatively minor changes to the solar gain algorithm have resulted in much improved science output. The biggest
  improvement is that the relative throughput differences between the slits are now correctly accounted for, which results
  in the same scaling across slit borders. The second change improves the separation of solar absorption lines from real gain
  differences and results in better gain correction overall. (`#25 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/25>`__)


v0.5.0 (2024-07-15)
===================




- L1 output files are now remapped, 3D IFU cubes with coordinates (LAT, LON, WAVE). The WCS information for the two spatial axes
  comes directly from the raw L0 frames and pre-computed IFU remapping files. (`#8 <https://bitbucket.org/dkistdc/dkist-processing-dlnirsp/pull-requests/8>`__)


v0.1.0 (2024-06-06)
===================

- Initial release. Pipeline supports both BIFOS and MISI data and produces valid L1 frames. IFU-remapping is not yet implemented
  so the L1 files are presented as a single slit. WCS header values not guaranteed.
