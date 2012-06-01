#ifndef __CONFIG_H__
#define __CONFIG_H__

#include "define.h"
#include "Coord.h"
#include <string>
#include <vector>
#include <list>
#include <set>
#include <cstdlib>
#include <iostream>

class Config{
 private:
 public:
  int mode;
  
  // input filenames
  std::string fn_cfg;
  std::string fn_cfg_sample;
  std::list<std::string> fn_trr; // --fn-trr
  std::string fn_pdb; // --fn-pdb

  // output filenames
  std::string fn_site_occupancy; // --fn-site-occupancy
  std::string fn_pore_axis_density; // --fn-pore-axis-density
  std::string fn_pore_axis_coordinates; // --fn-pore-axis-coordinates
  std::string fn_pore_axis_coordinates_r; // --fn-pore-axis-coordinates-r

  // pore axis settings
  std::vector<char> pore_axis_basis_chain_a; // --pore-axis-basis-from
  std::vector<int>  pore_axis_basis_res_a; // --pore-axis-basis-from
  std::vector<std::string>  pore_axis_basis_atomname_a; // --pore-axis-basis-from
  std::vector<int>  pore_axis_basis_atom_a; // --pore-axis-basis-from

  std::vector<char> pore_axis_basis_chain_b; // --pore-axis-basis-from
  std::vector<int>  pore_axis_basis_res_b; // --pore-axis-basis-from
  std::vector<std::string>  pore_axis_basis_atomname_b; // --pore-axis-basis-from
  std::vector<int>  pore_axis_basis_atom_b; // --pore-axis-basis-from

  // site settings
  real site_max_radius; // --site-max-radius
  real site_hight_margin; // --site-hight-margin
  std::vector<real> site_boundaries; // --site-boundary

  std::list<char> channel_chain_id; // --channel-chain-id

  // atom names to be analyzed
  std::list<std::string> trace_atom_names; // --trace-atom-name

  // area to be considered
  double min_x; // --min-x
  double max_x; // --max-x
  double min_y; // --min-y
  double max_y; // --max-y
  double min_z; // --min-z
  double max_z; // --max-z

  double append_time; //time for begining of trajectory
  double dt;     //the time interval between trajectory frames

  Config();
  ~Config();

  void set_all(int argn,char* argv[]);
  void set_all(const std::vector<std::string>& arg);
  void operator=(Config op);
};

#endif
