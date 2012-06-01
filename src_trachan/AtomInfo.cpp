#include "AtomInfo.h"
using namespace std;

AtomInfo::AtomInfo(int in_atom_id, string in_atom_name, string in_res_name,
		   char in_chain_id, int in_res_id){
  atom_id = in_atom_id;
  atom_name = in_atom_name;
  res_name = in_res_name;
  chain_id = in_chain_id;
  res_id = in_res_id;
}
