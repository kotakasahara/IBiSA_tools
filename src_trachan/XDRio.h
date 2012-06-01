#ifndef __XDR_IO_H__
#define __XDR_IO_H__

#include <vector>
#include "define.h"
#include "FileIo.h"
#include "TrnHeader.h"
#include "Coord.h"

//
//typedef Coord<double> Crd;
//typedef Coord Crd;

class XDRio : public FileIo
{
 private:

 public:
  XDRio(std::string in_filename);
  int open();
  template <typename T> T swapbytes(T x);
  template <typename T> T htonl(T x);
  template <typename T> T ntohl(T x);
  template <typename T> bool read_value(T& x);
  bool read_string(std::string& x, int size);
  template <typename T> bool read_crd_vec(std::vector< Coord<T> >& crds, int nitems);
  template <typename T> bool read_crd(Coord<T>& x);

  bool read_trn_header(TrnHeader& trnh);
  bool read_trn_frame(const TrnHeader& trnh,
		      std::vector<Crd>& box,  std::vector<Crd>& x,
		      std::vector<Crd>& v, std::vector<Crd>& f);

  int read_rvec(std::vector<float>& x, int nitems);
  
};

#endif
