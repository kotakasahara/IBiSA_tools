#include "ChannelStructure.h"
using namespace std;

////////////// constructor ///////////////////

ChannelStructure::ChannelStructure() :System(){
}

/////////// pore axis coordinates //////////////

int ChannelStructure::set_pore_axis_basis_atoms
( vector<char> chain_a,  vector<int>  res_a,  vector<string>  atomname_a, vector<int> atom_a,
  vector<char> chain_b,  vector<int>  res_b,  vector<string>  atomname_b, vector<int> atom_b){
  
  // seeking all atoms to find atoms satisfying conditions specified in the config, i.e.,
  // cfg.pore_axis_basis_chain_a, _b
  // cfg.pore_axis_basis_res_a, _b
  // cfg.pore_axis_basis_atomname_a, _b
  // id of picked atoms will be stored to pore_axis_basis_atom_a and _b

  vector<AtomInfo>::iterator i_ai;
  for(i_ai = atom_info.begin();
      i_ai != atom_info.end(); i_ai++){
    vector<char>::iterator iCh = chain_a.begin();
    vector<int>::iterator iRes = res_a.begin();
    vector<string>::iterator iAtN = atomname_a.begin();
    for(;iCh != chain_a.end(); iCh++, iRes++, iAtN++){
      if(((*i_ai).get_atom_name() == "*" ||
	  (*i_ai).get_atom_name() == (*iAtN)) &&
	 ((*i_ai).get_chain_id() == '*' ||
	  (*i_ai).get_chain_id() == (*iCh)) &&
	 ((*i_ai).get_res_id() <= 0 || 
	  (*i_ai).get_res_id() == (*iRes))){
	pore_axis_basis_atom_a.push_back((*i_ai).get_atom_id());
      }
    }


    iCh = chain_b.begin();
    iRes = res_b.begin();
    iAtN = atomname_b.begin();
    for(;iCh != chain_b.end(); iCh++, iRes++, iAtN++){
      if(((*i_ai).get_atom_name() == "*" ||
	  (*i_ai).get_atom_name() == (*iAtN)) &&
	 ((*i_ai).get_chain_id() == '*' ||
	  (*i_ai).get_chain_id() == (*iCh)) &&
	 ((*i_ai).get_res_id() <= 0 || 
	  (*i_ai).get_res_id() == (*iRes))){
	pore_axis_basis_atom_b.push_back((*i_ai).get_atom_id());
      }
    }
  }
  
  // cfg.pore_axis_basis_atom_a, b

  vector<int>::iterator iAt = atom_a.begin();
  for(;iAt != atom_a.end(); iAt++){
    pore_axis_basis_atom_a.push_back(*iAt);
  }
  iAt = atom_b.begin();
  for(;iAt != atom_b.end(); iAt++){
    pore_axis_basis_atom_b.push_back(*iAt);
  }

  cout << "pore axis basis a" << endl;
  list<int>::iterator i_atom;
  for(i_atom = pore_axis_basis_atom_a.begin();
      i_atom != pore_axis_basis_atom_a.end(); i_atom++){
    cout << *i_atom << " " <<atom_info[*i_atom].get_atom_name() << " "
	 <<atom_info[*i_atom].get_res_name() << " "
	 <<atom_info[*i_atom].get_res_id() << endl;
  }
  cout << "pore axis basis b" << endl;
  for(i_atom = pore_axis_basis_atom_b.begin();
      i_atom != pore_axis_basis_atom_b.end(); i_atom++){
    cout << *i_atom << " " <<atom_info[*i_atom].get_atom_name() << " "
	 <<atom_info[*i_atom].get_res_name() << " "
	 <<atom_info[*i_atom].get_res_id() << endl;
  }

  if (pore_axis_basis_atom_a.empty() ||
      pore_axis_basis_atom_b.empty()){
    cerr << "Error: the pore axis cannot be defined." << endl;
    cerr << "The basis atoms have to be specified in the configuration file" << endl;
    cerr << "--pore-axis-basis-from [CHAIN(char)] [RESIDUE(int)] [ATOMNAME(str)]" << endl;
    cerr << "--pore-axis-basis-from A 374 O" << endl;
    cerr << "--pore-axis-basis-from B 374 O" << endl;
    cerr << "--pore-axis-basis-from C 374 O" << endl;
    cerr << "--pore-axis-basis-from D 374 O" << endl;
    cerr << "--pore-axis-basis-to A 377 O" << endl;
    cerr << "--pore-axis-basis-to B 377 O" << endl;
    cerr << "--pore-axis-basis-to C 377 O" << endl;
    cerr << "--pore-axis-basis-to D 377 O" << endl;
    cerr << endl << "EXAMPLE:" << endl;
    
    exit(1);
  }
  return 0;
}

int ChannelStructure::set_pore_axis_basis_coordinates(const vector<Crd>& x){
  list<int>::iterator i_a;
  vector<Crd> crd_basis_a;
  for(i_a = pore_axis_basis_atom_a.begin();
      i_a != pore_axis_basis_atom_a.end(); i_a++){
    //cout << "crd " <<*i_a << " " << x[*i_a].get_string() << endl;
    crd_basis_a.push_back(x[*i_a]);
  }
  pore_axis_basis_vec_a = cal_coord_center(crd_basis_a);
  //cout << "pore_axis_basis_vec_a " << pore_axis_basis_vec_a.get_string() << endl;
  
  vector<Crd> crd_basis_b;
  for(i_a = pore_axis_basis_atom_b.begin();
      i_a != pore_axis_basis_atom_b.end(); i_a++){
    //cout << "crd " <<*i_a << " " << x[*i_a].get_string() << endl;
    crd_basis_b.push_back(x[*i_a]);
  }
  pore_axis_basis_vec_b = cal_coord_center(crd_basis_b);
  //cout << "pore_axis_basis_vec_b " << pore_axis_basis_vec_b.get_string() << endl;
  
  pore_axis_basis_vec_ab
    = pore_axis_basis_vec_b - pore_axis_basis_vec_a;
  //cout << "pore_axis_basis_vec_ab " << pore_axis_basis_vec_ab.get_string() << endl;
  pore_axis_basis_vec_ab2
    = pore_axis_basis_vec_ab * pore_axis_basis_vec_ab;
  //cout << "pore_axis_basis_vec_ab2 " << pore_axis_basis_vec_ab2.get_string() << endl;
  pore_axis_basis_vec_ab_ip
    = pore_axis_basis_vec_ab2.sum();
  //cout << "pore_axis_basis_vec_ab2_ip " << pore_axis_basis_vec_ab_ip << endl;
  pore_axis_basis_vec_ab_sc
    = sqrt(pore_axis_basis_vec_ab_ip);
  //cout << "pore_axis_basis_vec_ab2_sc " << pore_axis_basis_vec_ab_sc << endl;

  return 0;
}

int ChannelStructure::convert_pore_axis_coordinate
(const Crd& vec_x, real& h, real& r){
  //cout << vec_x.get_string() << endl;

  Crd vec_ax; // a -> x
  vec_ax = vec_x - pore_axis_basis_vec_a;
  //cout << vec_ax.get_string() << endl;

  real ip_ab_ax; //innter product of ab and ax
  ip_ab_ax = pore_axis_basis_vec_ab.inner_product(vec_ax);
  //cout << "pore_axis_basis_vec_ab " << pore_axis_basis_vec_ab.get_string() << endl;
  //cout << ip_ab_ax << endl;

  Crd vec_ay; // y means crossing point between a->b and its normal on x
  vec_ay = pore_axis_basis_vec_ab *  (ip_ab_ax / pore_axis_basis_vec_ab_ip);
  //cout << vec_ay.get_string() << endl;
  
  real sc_ay = sqrt(vec_ay.inner_product(vec_ay));
  //cout << sc_ay << endl;
  real sc_ax = sqrt(vec_ax.inner_product(vec_ax));
  //cout << sc_ax << endl;
  real cos_theta = ip_ab_ax / (pore_axis_basis_vec_ab_sc * sc_ay);
  //cout << cos_theta << endl;

  if(cos_theta >= 0) h = sc_ay;
  else h = -sc_ay;

  Crd vec_y = vec_ay + pore_axis_basis_vec_a; 
  Crd vec_yx = vec_y - vec_x;

  r = vec_yx.scalar();

  return 0;
}

//////////////////  site information ////////////////////
int ChannelStructure::get_site_from_pore_axis(const real& h, const real& r){
  if(r > site_max_r)
    return 0;
  for(int i=0; i<(int)site_boundaries.size(); i++){
    if(h > site_boundaries[i]) return i;
  }
  return 0;
}



/////////////////// analysis in each frame /////////////////////////

int ChannelStructure::cal_pore_axis_coordinates(vector<Crd>& x){
  pore_axis_crd.clear();
  list<int>::iterator i_a;
  for(i_a = trace_atom_id.begin();
      i_a != trace_atom_id.end(); i_a++){
    real h;
    real r;
    convert_pore_axis_coordinate(x[*i_a], h, r);
    //cout << "atom:" << *i_a << " " << h << " / " << r <<endl;//debug
    pore_axis_crd.insert
      (make_pair
       (atom_info[*i_a].get_atom_id(), make_pair(h,r)));
  }
  return 0;
}

string ChannelStructure::get_pore_axis_coords_for_density_analysis(){
  stringstream ss;
  list<int>::iterator i_atom;
  for(i_atom = trace_atom_id.begin();
      i_atom != trace_atom_id.end(); i_atom++){
    map<int, pair<real,real> >::iterator i_crd;
    i_crd = pore_axis_crd.find(*i_atom);
    if(i_crd != pore_axis_crd.end() &&
       i_crd->second.second <= site_max_r &&
       i_crd->second.first < (*site_boundaries.begin())+site_hight_margin &&
       i_crd->second.first > (*--site_boundaries.end())-site_hight_margin)
      ss << atom_info[*i_atom].get_atom_name() <<"\t"
	 << i_crd->second.first * 10 << "\t"
	 << i_crd->second.second * 10 << endl;
  }
  return ss.str();
}
string ChannelStructure::get_pore_axis_coordinates_header_string(){
  stringstream ss;
  list<int>::iterator i_atom;
  for(i_atom = trace_atom_id.begin();
      i_atom != trace_atom_id.end(); i_atom++){
    ss << atom_info[*i_atom].get_atom_id()
       << ":" << atom_info[*i_atom].get_atom_name();
    if(i_atom != --trace_atom_id.end())
      ss << "\t";
  }
  ss << endl;
  return ss.str();
}
string ChannelStructure::get_pore_axis_coordinates_h_string(){
  stringstream ss;
  list<int>::iterator i_atom;
  for(i_atom = trace_atom_id.begin();
      i_atom != trace_atom_id.end(); i_atom++){
    map<int, pair<real,real> >::iterator i_crd;
    i_crd = pore_axis_crd.find(*i_atom);
    if(i_crd != pore_axis_crd.end() &&
       i_crd->second.second <= site_max_r &&
       i_crd->second.first < (*site_boundaries.begin())+site_hight_margin &&
       i_crd->second.first > (*--site_boundaries.end())-site_hight_margin)
      ss << "\t" << i_crd->second.first * 10;
    else
      ss << "\t-";
    //      }
  }
  return ss.str();
}
string ChannelStructure::get_pore_axis_coordinates_r_string(){
  stringstream ss;
  list<int>::iterator i_atom;
  for(i_atom = trace_atom_id.begin();
      i_atom != trace_atom_id.end(); i_atom++){
    map<int, pair<real,real> >::iterator i_crd;
    i_crd = pore_axis_crd.find(*i_atom);
    if(i_crd != pore_axis_crd.end() &&
       i_crd->second.second <= site_max_r &&
       i_crd->second.first < (*site_boundaries.begin())+site_hight_margin &&
       i_crd->second.first > (*--site_boundaries.end())-site_hight_margin)
      ss << "\t" << i_crd->second.second * 10; //nm -> angestrome
    else
      ss << "\t-";
    //      }
  }
  return ss.str();
}

int ChannelStructure::cal_site_occupancy(){
  site_occupancy.clear();
  list<int>::iterator i_a;
  for(i_a = trace_atom_id.begin();
      i_a != trace_atom_id.end(); i_a++){
    map<int, pair<real,real> >::iterator i_crd;
    i_crd = pore_axis_crd.find(*i_a);
    int site = get_site_from_pore_axis(i_crd->second.first, i_crd->second.second);
    if(site > 0){
      map<int, set<int> >::iterator i_site;
      i_site = site_occupancy.find(site);
      if(i_site == site_occupancy.end()){
	set<int> tmp_set;
	tmp_set.insert(*i_a);
	site_occupancy.insert(make_pair(site, tmp_set));
      }else{
	i_site->second.insert(*i_a);
      }
    }
  }
  return 0;
}
string ChannelStructure::get_text_site_occupancy(){
  stringstream st;
  map< int, set<int> >::iterator i_site;
  for(i_site = site_occupancy.begin();
      i_site != site_occupancy.end(); i_site++){
    set<int>::iterator i_atom;
    for(i_atom = i_site->second.begin();
	i_atom != i_site->second.end(); i_atom++){
      st << " " << i_site->first << ":" << *i_atom << ":" << atom_info[*i_atom].get_atom_name();
    }
  }
  return st.str();
}

