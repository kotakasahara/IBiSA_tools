#ifndef __PDB_IO_H__
#define __PDB_IO_H__

#include <string>
#include <sstream>
#include <cstdio>
#include "define.h"
#include "FileIo.h"
#include "AtomInfo.h"

class PDBio : public FileIo
{
 private:
 public:
  PDBio(std::string in_filename);
  std::vector<AtomInfo> read_pdb();
  AtomInfo parse_atom_info(std::string line, int last_id);
};

#endif
