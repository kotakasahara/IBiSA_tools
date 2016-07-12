#ifndef __DEFINE_H__
#define __DEFINE_H__

#include <string>

static std::string developer = "Kota Kasahara";
static std::string affiliation = "College of Life Sciences, Ritsumeikan University";
static std::string email = "ktkshr@fc.ritsumei.ac.jp";
static std::string citation = "in preparation";

static std::string cp = 
  "-----------------------------------------------------------------\n"
  "                      TraChan                \n"
  "  TRAjectory analyzer for CHANnel pore axis  \n"
  "-----------------------------------------------------------------\n"
  "Copyright (c) 2016 Kota Kasahara, Ritsumeikan University\n"  
  "This software is distributed under the terms of the GPL license\n";

static std::string cp_gromacs = 
  "-----------------------------------------------------------------\n"
  "This program contains some parts of the source code of GROMACS \n"
  "software. Check out http://www.gromacs.org about GROMACS.\n"
  "Copyright (c) 1991-2000, University of Groningen, The Netherlands.\n"
  "Copyright (c) 2001-2010, The GROMACS development team at\n"
  "Uppsala University & The Royal Institute of Technology, Sweden.\n"
  "-----------------------------------------------------------------\n";

enum {
  M_TEST = 1,
  M_DIFF_COEFF,
  M_SITE_OCCUPANCY,
  M_DUMMY
};


#endif
