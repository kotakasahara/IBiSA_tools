#include "Read.h"

Read::Read(string inFn){
  op=false;
  filename = inFn;
}

int Read::open(){
  ifs.open(filename.c_str());
  if(!ifs){
    cerr <<"Cannot open "<< filename << "." <<endl;
    return 1;
  }
  op=true;
  return 0;
}
int Read::close(){
  ifs.close();
  op=false;
  return 0;
}

vector<string> Read::load_config(){
  vector<string> vconf;
  open();
  string buf;
  while(ifs>>buf){
    if(buf[0] != '#' and buf[0] != ';')
      vconf.push_back(buf);
  }
  close();
  return vconf;
}
