#include "FileIo.h"
using namespace std;

//FileIo::FileIo(){
//}
FileIo::FileIo(string in_filename){
  filename = in_filename;
  op = false;
}

int FileIo::open(){
  fs.open(filename.c_str());
  if(!fs){
    cerr <<"Cannot open "<< filename << "." <<endl;
    return 1;
  }
  op=true;
  return 0;
}
int FileIo::open_write(){
  cerr << "open " << filename << endl;
  fs.open(filename.c_str(), ios::out);
  if(!fs){
    cerr <<"Cannot open "<< filename << ". (out)" <<endl;
    return 1;
  }
  op=true;
  return 0;
}
int FileIo::open_append(){
  fs.open(filename.c_str(), ios::app);
  if(!fs){
    cerr <<"Cannot open "<< filename << ". (app)" <<endl;
    return 1;
  }
  op=true;
  return 0;
}

int FileIo::close(){
  fs.close();
  op=false;
  return 0;
}

vector<string> FileIo::read_ascii_strings(){
  vector<string> vconf;
  open();
  string buf;
  while(fs && getline(fs,buf)){
    if(buf[0] != '#'){
      stringstream ss(buf);
      string buf2;
      while(ss >> buf2){
	if(buf2[0] == '#') break;
	vconf.push_back(buf);
      }
    }
  }
  close();
  return vconf;
}

int FileIo::write_string(std::string line){
  fs << line;
  return 0;
}
