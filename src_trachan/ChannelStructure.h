#ifndef __CHANNEL_STRUCTURE_H__
#define __CHANNEL_STRUCTURE_H__


#include "System.h"


class ChannelStructure : public System{
 private:
  std::list<char> channel_chain_id;
  
  // channel features 
  std::list<int> selectivity_filter_res;

  // pore axis
  
  
  std::list<int> pore_axis_basis_atom_a;
  std::list<int> pore_axis_basis_atom_b;
  Crd pore_axis_basis_vec_a; 
  Crd pore_axis_basis_vec_b;
  Crd pore_axis_basis_vec_ab;  // a -> b
  Crd pore_axis_basis_vec_ab2;  // squared
  real pore_axis_basis_vec_ab_ip; // inner product of itself
  real pore_axis_basis_vec_ab_sc; // scolar
 
  // site information
  std::vector<real> site_boundaries;
  real site_max_r;
  real site_hight_margin;
  // trace atom setting
  
  // information in each frame
  // map < atom_id, pair< h, r > >
  std::map< int, std::pair<real, real> > pore_axis_crd;
  // map < site_id, set<atom_id> >
  std::map< int, std::set<int> > site_occupancy;
  
 public:
  ChannelStructure();

  void set_channel_chain_id(std::list<char>& in_id) {channel_chain_id = in_id;};
  void set_selectivity_filter_res(std::list<int>& in_id) {selectivity_filter_res = in_id;};
  int set_pore_axis_basis_atoms(const std::vector<char>    chain_a,
				const std::vector<int>     res_a,
				const std::vector<std::string>  atomname_a,
				const std::vector<int>     atom_a,
				const std::vector<char>    chain_b,
				const std::vector<int>     res_b,
				const std::vector<std::string>  atomname_b,
				const std::vector<int>     atom_b);
  int set_pore_axis_basis_coordinates(const std::vector<Crd>& x);
  int convert_pore_axis_coordinate(const Crd& vec_x, real& h, real& r);


  //site information
  void set_site_max_radius(const real& in_r){ site_max_r = in_r; };
  void set_site_hight_margin(const real& in_h){ site_hight_margin = in_h; };
  void set_site_boundaries(std::vector<real>& in_b){site_boundaries = in_b;};
  int get_site_from_pore_axis(const real& h, const real& r);
  
  // analysis in each frame
  int cal_pore_axis_coordinates(std::vector<Crd>& x);
  int cal_site_occupancy();
  std::string get_text_site_occupancy();
  std::string get_pore_axis_coords_for_density_analysis();
  std::string get_pore_axis_coordinates_h_string();
  std::string get_pore_axis_coordinates_r_string();
  std::string get_pore_axis_coordinates_header_string();


};

#endif
