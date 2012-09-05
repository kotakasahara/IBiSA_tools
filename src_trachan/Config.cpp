#include "Config.h"
using namespace std;

Config::Config(){
  mode=M_SITE_OCCUPANCY;
  fn_cfg = "";
  fn_cfg_sample = "trachan_sample.cfg";
  min_x = 0.0;
  max_x = 0.0;
  min_y = 0.0;
  max_y = 0.0;
  min_z = 0.0;
  max_z = 0.0;
  append_time = 0.0;
  dt = 1.0;
}

Config::~Config(){
}

void Config::set_all(int argn, char* argv[]){
  vector<string> arg;
  int i;
  for(i=1;i<argn;i++)
    arg.push_back(string(argv[i]));
  set_all(arg);
}

void Config::set_all(const vector<string>& arg){
  vector<string>::const_iterator itr;
  string type,val;
  for(itr = arg.begin(); itr != arg.end(); itr++){
    if((*itr)[0] == '#' || (*itr)[0] == ':' || (*itr)[0] == ';'){
      continue;
    }else if(*itr == "--mode"){
      itr++;
      if (*itr == "test")           { mode=M_TEST; }
      if (*itr == "site-occupancy") { mode=M_SITE_OCCUPANCY; }
      else{
	mode=M_SITE_OCCUPANCY;
        //cerr << "invalid mode [" << *itr << "]\n";
	cerr << "mode: SITE_OCCUPANCY" << endl;
      }
    }else if(*itr == "--fn-cfg"){
      fn_cfg = *++itr;
    }else if(*itr == "--fn-trr"){
      fn_trr.push_back(*++itr);
    }else if(*itr == "--fn-pdb"){
      fn_pdb = *++itr;
    }else if(*itr == "--fn-site-occupancy"){
      fn_site_occupancy = *++itr;
    }else if(*itr == "--fn-pore-axis-density"){
      fn_pore_axis_density = *++itr;
    }else if(*itr == "--fn-pore-axis-coordinates"){
      fn_pore_axis_coordinates = *++itr;
    }else if(*itr == "--fn-pore-axis-coordinates-r"){
      fn_pore_axis_coordinates_r = *++itr;
    }else if(*itr == "--pore-axis-basis-atom-from"){
      pore_axis_basis_atom_a.push_back(atoi((*++itr).c_str()));
    }else if(*itr == "--pore-axis-basis-atom-to"){
      pore_axis_basis_atom_b.push_back(atoi((*++itr).c_str()));
    }else if(*itr == "--pore-axis-basis-from"){
      pore_axis_basis_chain_a.push_back((*++itr).c_str()[0]);
      pore_axis_basis_res_a.push_back(atoi((*++itr).c_str()));
      pore_axis_basis_atomname_a.push_back((*++itr).c_str());
    }else if(*itr == "--pore-axis-basis-to"){
      pore_axis_basis_chain_b.push_back((*++itr).c_str()[0]);
      pore_axis_basis_res_b.push_back(atoi((*++itr).c_str()));
      pore_axis_basis_atomname_b.push_back((*++itr).c_str());
    }else if(*itr == "--site-max-radius"){
      site_max_radius = atof((*++itr).c_str()) * 0.1; // angestrome to nm
    }else if(*itr == "--site-hight-margin"){
      site_hight_margin = atof((*++itr).c_str()) * 0.1; // angestrome to nm
    }else if(*itr == "--site-boundary"){
      site_boundaries.push_back(atof((*++itr).c_str()) * 0.1); // angestrome to nm
    }else if(*itr == "--channel-chain-id"){
      string chains = *++itr;
      for(int i = 0; i < chains.size(); i++)
	channel_chain_id.push_back(chains[i]);
    }else if(*itr == "--trace-atom-name"){
      trace_atom_names.push_back(*++itr);
    }else if(*itr == "--min-x"){
      min_x = atof((*++itr).c_str());
    }else if(*itr == "--max-x"){
      max_x = atof((*++itr).c_str());
    }else if(*itr == "--min-y"){
      min_y = atof((*++itr).c_str());
    }else if(*itr == "--max-y"){
      max_y = atof((*++itr).c_str());
    }else if(*itr == "--min-z"){
      min_z = atof((*++itr).c_str());
    }else if(*itr == "--max-z"){
      max_z = atof((*++itr).c_str());
    }else if(*itr == "--append"){
      append_time = atof((*++itr).c_str());
    }else if(*itr == "--dt"){
      dt = atof((*++itr).c_str());
    }else if(*itr == "--frame-interval"){
      frame_interval = atoi((*++itr).c_str());
    }else{
      cerr << "undefined keyword :" << *itr << endl;
    }
  }
}
