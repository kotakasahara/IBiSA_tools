#include "System.h"
using namespace std;

System::System(){
}


/////////////////// trace atom setting //////////////////////////

int System::set_trace_atom_id_from_atom_names(list<string> atom_names){
  trace_atom_id = list<int>();
  vector<AtomInfo>::iterator i_a;
  for(i_a = atom_info.begin();
      i_a != atom_info.end(); i_a++){
    //cout << (*i_a).get_atom_name() << " " << (*i_a).get_atom_id() << endl;
    if(find(atom_names.begin(), atom_names.end(),
	    (*i_a).get_atom_name()) != atom_names.end()){
      trace_atom_id.push_back((*i_a).get_atom_id());
    }
  }
  //cout << "trace_atom_id.size() : " << trace_atom_id.size() << endl;
  return 0;
}


////////////////// displacement //////////////////////////
double System::cal_displacement(Crd atom, Crd prev, Crd box){
  double dx = fabs(atom[0] - prev[0]);
  double dy = fabs(atom[1] - prev[1]);
  double dz = fabs(atom[2] - prev[2]);
  if(dx > box[0]*0.5){
    dx = box[0] - dx;
  }
  if(dy > box[1]*0.5){
    dy = box[1] - dy;
  }
  if(dz > box[2]*0.5){
    dz = box[2] - dz;
  }
  return sqrt(dx*dx+dy*dy+dz*dz);
}

/*
double System::cal_displacement_trace_atoms(vector<Crd> x,
					    vector<Crd> prev,
					    const Crd& box){
  stringstream ss;
  list<int>::iterator i_atom;
  for(i_atom = trace_atom_id.begin();
      i_atom != trace_atom_id.end(); i_atom++){
    cal_displacement(x[i_atom], prev[i_atom], box);
  }
}
*/
