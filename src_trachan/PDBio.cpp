#include "PDBio.h"
using namespace std;

PDBio::PDBio(string in_filename)
  : FileIo(in_filename){
}

vector<AtomInfo> PDBio::read_pdb(){
  vector<AtomInfo> ai;
  open();
  string buf;
  
  while(fs && getline(fs, buf)){
    if(buf.substr(0,6) == "ATOM  "){
      ai.push_back(parse_atom_info(buf, ai.size()));
    }
  }
  close();
  return ai;
}

AtomInfo PDBio::parse_atom_info(string line, int last_id){
  //itn atom_id = atoi(line.substr(6,5).c_str());
  char atom_name[5];
  sscanf(line.substr(12,4).c_str(),"%s", atom_name);
  char res_name[4];
  sscanf(line.substr(17,3).c_str(),"%s", res_name);
  char chain_id = line[21];
  int res_id = atoi(line.substr(22,4).c_str());
  return AtomInfo(last_id, atom_name, res_name, chain_id, res_id);
}
