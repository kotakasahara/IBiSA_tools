#ifndef __TRN_HEADER_H__
#define __TRN_HEADER_H__

#include <string>

class TrnHeader {
 private:
 public:
  int magic;
  std::string filetype;
  int ir_size;
  int e_size;
  int box_size;
  int vir_size;
  int pres_size;
  int top_size;
  int sym_size;
  int x_size;
  int v_size;
  int f_size;
  int natoms;
  int step;
  int nre;
  float t;
  float lambda;

  TrnHeader();
};



#endif
