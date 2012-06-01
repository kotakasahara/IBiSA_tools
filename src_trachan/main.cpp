#include <iostream>
#include "TraChan.h"
using namespace std;

int main(int argn, char* argv[]){
  TraChan tc;
  tc.setup(argn, argv);
  tc.main_routine();
  return 0;
}
