#ifndef __ATOM_INFO_H__
#define __ATOM_INFO_H__

#include <string>
#include "Coord.h"

class AtomInfo{
 private:
  int atom_id;
  std::string atom_name;
  std::string res_name;
  char chain_id;
  int res_id;
  
 public:
  AtomInfo(int in_atom_id, std::string in_atom_name, std::string in_res_name,
	   char in_chain_id, int in_res_id);
  int get_atom_id(){return atom_id;};
  std::string get_atom_name(){return atom_name;};
  std::string get_res_name(){return res_name;};
  char get_chain_id(){return chain_id;};
  int get_res_id(){return res_id;};

};

#endif
