#include "XDRio.h"
using namespace std;

XDRio::XDRio(string in_filename)
  :FileIo(in_filename){
}
int XDRio::open(){
  //  fs = fstream(get_filename().c_str(), ios::in | ios::binary);
  fs.open(get_filename().c_str(), ios::in | ios::binary);
  if(!fs){
    cerr <<"Cannot open "<< get_filename() << "." <<endl;
    return 1;
  }
  return 0;
}
template <typename T> T XDRio::swapbytes(T x){
  //  cout << "swapbytes" <<endl;
  T y;
  char *px = (char*)&x;
  char *py = (char*)&y;
  for(int i=0;i<4;i++)
    py[i] = px[3-i];
  return y;
}
template <typename T> T XDRio::htonl(T x){
  return x;
}
template <typename T> T XDRio::ntohl(T x){
  short s=0x0F00;
  if ( *((char*)&s) == (char)0x0F)
    return x;
  else
    return swapbytes(x);
  //return x;
}
template <typename T> bool XDRio::read_value(T& x){
  T value;
  if(!fs.read((char*) &value, 4))
    return false;
  x = ntohl(value);
  return true;
}


bool XDRio::read_string(string& x, int max_size){
  char buf[max_size];
  unsigned int size;
  read_value(size);
  //cout << size << endl;
  if (max_size < size)
    return false;
  
  int i;
  for (i = 0; i < size; i++){
    char chara;
    if(!fs.read((char*) &chara, 1))
      return false;
    //    cout << (char) chara << ":" << chara << endl;
    buf[i] = (char)chara;
  }
  buf[i] = '\0';
  //  cout << endl;
  //  cout << buf << endl;
  x = string(buf);
  return true;
}

bool XDRio::read_trn_frame(const TrnHeader& trnh,
			  vector<Crd>& box,  vector<Crd>& x,
			  vector<Crd>& v, vector<Crd>& f){
  bool ret=true;
  vector<Crd> pv;
  if(trnh.box_size != 0){
    ret = ret && read_crd_vec(box, Crd::dim);
    //    cout << box[0][0] << ":" << box[0][1] << ":" << box[0][2] << endl;
    //    cout << box[1][0] << ":" << box[1][1] << ":" << box[1][2] << endl;
    //    cout << box[2][0] << ":" << box[2][1] << ":" << box[2][2] << endl;
  }

  if(trnh.vir_size != 0) ret = ret && read_crd_vec(pv, Crd::dim);
  if(trnh.pres_size != 0) ret = ret && read_crd_vec(pv, Crd::dim);
  if(trnh.x_size != 0) ret = ret && read_crd_vec(x, trnh.natoms);
  if(trnh.v_size != 0) ret = ret && read_crd_vec(v, trnh.natoms);
  if(trnh.f_size != 0) ret = ret && read_crd_vec(f, trnh.natoms);
  return ret;
}

template <typename T> bool XDRio::read_crd_vec(vector< Coord<T> >& crds, int nitems){
  int ret = true;
  crds.reserve(nitems);  
  for(int i=0; i<nitems && ret; i++){
    Coord<T> x;
    ret = ret && read_crd(x);
    crds.push_back(x);
  }
  return ret;
}

template <typename T> bool XDRio::read_crd(Coord<T>& x){
  int ret = true;
  vector<T> y;
  y.reserve(Crd::dim);
  for(int i=0; i<Crd::dim && ret; i++){
    T z;
    ret = ret && read_value(z);
    y.push_back(z);
  }
  x = Crd(y[0], y[1], y[2]);
  return ret;
}

bool XDRio::read_trn_header(TrnHeader& trnh){
  int ret = true;

  ret = ret && read_value(trnh.magic);
  //cout << "magic : " << ret << " : " << trnh.magic << endl;

  int tmp_int;
  ret = ret && read_value(tmp_int);
  //cout << "tmp_int : " << ret << " : " << tmp_int << endl;

  string head;
  ret = ret && read_string(trnh.filetype, 1024);
  //cout << ret << " : " << head << endl;
    
  ret = ret && read_value(trnh.ir_size);
  //cout << ret << " : ir_size : " << ir_size << endl;    

  ret = ret && read_value(trnh.e_size);
  //cout << ret << " : e_size : " << e_size << endl;    

  ret = ret && read_value(trnh.box_size);
  //cout << ret << " : box_size : " << box_size << endl;    

  ret = ret && read_value(trnh.vir_size);
  //cout << "vir_size : " << vir_size << endl;    

  ret = ret && read_value(trnh.pres_size);
  //    cout << "pres_size : " << pres_size << endl;    

  ret = ret && read_value(trnh.top_size);
  //cout << "top_size : " << top_size << endl;    

  ret = ret && read_value(trnh.sym_size);
  //cout << "sym_size : " << sym_size << endl;    

  ret = ret && read_value(trnh.x_size);
  //cout << "x_size : " << x_size << endl;    

  ret = ret && read_value(trnh.v_size);
  //cout << "v_size : " << v_size << endl;    

  ret = ret && read_value(trnh.f_size);
  //    cout << "f_size : " << f_size << endl;    

  ret = ret && read_value(trnh.natoms);
  //  cout << "natoms : " << natoms << endl;        
  ret = ret && read_value(trnh.step);
  ret = ret && read_value(trnh.nre);
  ret = ret && read_value(trnh.t);
  ret = ret && read_value(trnh.lambda);

  return ret;
}
