#ifndef __TRA_CHAN_H__
#define __TRA_CHAN_H__

#include <fstream>
#include <sstream>
#include "Config.h"
#include "FileIo.h"
#include "XDRio.h"
#include "PDBio.h"
#include "ChannelStructure.h"

class TraChan{
 private:
  Config cfg;
 public:
  TraChan();
  int setup(int argn, char* argv[]);
  int generate_sample_config();
  int main_routine();
  int mode_test();
  int mode_site_occupancy();
};

#endif
