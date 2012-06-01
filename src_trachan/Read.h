#ifndef __READ_H__
#define __READ_H__

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <list>
#include <set>
#include <cstdlib>
using namespace std;

class Read{
 private:
  string filename;
  bool op;
  int cur_line;
 public:
  ifstream ifs;
  Read(string inFn);
  string getFn(){return filename;};
  bool is_open(){return op;};
  int open();
  int close();
  vector<string> load_config();
};

#endif
