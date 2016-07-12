=======================
Appendix
=======================

Converting a trajectory file
-------------------------------------------------------------------------

*IBiSA_tools* can read only .trr format. When you analyze trajectories written in other format, the files have to be converted into .trr file.

Some tools for the conversion exist. Here, a sample code powered by the Python library *MDAnalysis* is presented.::

  import MDAnalysis
  
  u = MDAnalysis.Universe("initial.pdb","trajectory.ncdf")
  writer = MDAnalysis.coordinates.TRJ.TRRWriter("trajectory.trr", len(u.atoms))
  for ts in u.trajectory:
      writer.write_next_timestep(ts)

The script converts *trajectory.ncdf* (AMBER, NetCDF file) into *trajectory.trr* file (GROMACS, .trr file). *initial.pdb* is the initial coordinates writtein in the flat .pdb format.

