#ifndef __SYSTEM_H__
#define __SYSTEM_H__

#include <cmath>
#include <sstream>
#include <list>
#include <vector>
#include <map>
#include <set>
#include <cmath>
#include "Coord.h"
#include "AtomInfo.h"
#include "Config.h"
#include "TrnHeader.h"

class System{
 private:
 protected:
  // basic structural information
  std::vector<AtomInfo> atom_info;
  std::list<int> trace_atom_id;
  std::vector<Crd> displacement;

 public:
  System();
  void set_atom_info(const std::vector<AtomInfo>& in_ai) {atom_info = in_ai;};
  int get_n_atoms(){return atom_info.size();};
  int set_trace_atom_id_from_atom_names(std::list<std::string> atom_names);  
  
  double cal_displacement(Crd atom, Crd prev, Crd box);
  double cal_displacement_trace_atoms(const std::vector<Crd>& x,
				      const std::vector<Crd>& prev,
				      const Crd& box);
};

#endif
