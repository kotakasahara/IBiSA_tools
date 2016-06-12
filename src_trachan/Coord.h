#ifndef __COORD_H__
#define __COORD_H__

#include <vector>
#include <string>
#include <sstream>
#include <iostream>


template <typename T = float> class Coord {
  private:
  std::vector<T> x;
  public:
  static int dim;
  Coord();
  Coord(const T in_x, const T in_y, const T in_z);
  Coord(const std::vector<T> in_x);
  const T& operator[](int i) const {return x[i];};
  T sum() const;
  T inner_product(const Coord<T>& rh) const;
  T scalar() const;
  Coord<T> operator+(const Coord<T>& rh) const;
  Coord<T> operator-(const Coord<T>& rh) const;
  Coord<T> operator*(const T& rh) const;
  Coord<T> operator/(const T& rh) const;
  Coord<T> operator*(const Coord<T>& rh) const;
  Coord<T> operator/(const Coord<T>& rh) const;
  void operator+=(const Coord<T>& rh);
  void operator-=(const Coord<T>& rh);
  void operator*=(const T& rh);
  void operator/=(const T& rh);
  void operator*=(const Coord<T>& rh);
  void operator/=(const Coord<T>& rh);

  std::string get_string() const;
};
template <typename T> Coord<T> cal_coord_center(std::vector< Coord<T> > crds);


template <typename T> int Coord<T>::dim = 3;

template <typename T> Coord<T>::Coord(){
  x.reserve(dim);
  x.push_back(0.0);
  x.push_back(0.0);
  x.push_back(0.0);
}
template <typename T> Coord<T>::Coord(const T in_x, const T in_y, const T in_z){
  x.reserve(dim);
  x.push_back(in_x);
  x.push_back(in_y);
  x.push_back(in_z);
}
template <typename T> Coord<T>::Coord(const std::vector<T> in_x){
  x = in_x;
}
template <typename T> T Coord<T>::sum() const{
  T sum = 0;
  for(int i=0; i<dim; i++)  sum += x[i];
  return sum;
}
template <typename T> T Coord<T>::inner_product(const Coord<T>& rh) const {
  T ip = 0;
  for(int i=0; i<dim; i++)  ip += x[i]*rh[i];
  return ip;
}
template <typename T> T Coord<T>::scalar() const {
  T sum = 0;
  for(int i=0; i<dim; i++)  sum += x[i]*x[i];
  return sqrt(sum);
}
template <typename T> Coord<T> Coord<T>::operator+(const Coord<T>& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] + rh[i]);
  return Coord<T>(y);
}
template <typename T> Coord<T> Coord<T>::operator-(const Coord<T>& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] - rh[i]);
  return Coord<T>(y);
}
template <typename T> Coord<T> Coord<T>::operator*(const Coord<T>& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] * rh[i]);
  return Coord<T>(y);
}
template <typename T> Coord<T> Coord<T>::operator/(const Coord<T>& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] / rh[i]);
  return Coord<T>(y);
}
template <typename T> Coord<T> Coord<T>::operator*(const T& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] * rh);
  return Coord<T>(y);
}
template <typename T> Coord<T> Coord<T>::operator/(const T& rh) const{
  std::vector<T> y;
  for (int i=0; i<dim; i++) y.push_back(x[i] / rh);
  return Coord<T>(y);
}
template <typename T> void Coord<T>::operator+=(const Coord<T>& rh){
  for (int i=0; i<dim; i++) x[i] += rh[i];  
}
template <typename T> void Coord<T>::operator-=(const Coord<T>& rh){
  for (int i=0; i<dim; i++) x[i] -= rh[i];  
}
template <typename T> void Coord<T>::operator*=(const Coord<T>& rh){
  for (int i=0; i<dim; i++) x[i] *= rh[i];  
}
template <typename T> void Coord<T>::operator/=(const Coord<T>& rh){
  for (int i=0; i<dim; i++) x[i] /= rh[i];  
}
template <typename T> void Coord<T>::operator*=(const T& rh){
  for (int i=0; i<dim; i++) x[i] *= rh;  
}
template <typename T> void Coord<T>::operator/=(const T& rh){
  for (int i=0; i<dim; i++) x[i] /= rh;  
}
template <typename T> std::string Coord<T>::get_string() const{
  std::stringstream ss;
  ss << "(";
  for (int i=0; i<dim; i++)  ss<<" "<<x[i];
  ss << " ) ";
  return ss.str();
}

template <typename T> Coord<T> cal_coord_center(std::vector< Coord<T> > crds){
  
  Coord<T> cent;
  for (int i = 0; i < (int)crds.size(); i++){
    cent += crds[i];
    //    std::cout << "coord " << cent.get_string() << endl;
  }
  return cent/(T)crds.size();
}



/*
class Coord{
 private:
  vector<float> x;
 public:
  static int dim;
  Coord();
  Coord(const float in_x, const float in_y, const float in_z);
  float& operator[](int i) {return x[i];} ;
};
*/

typedef float real;
//typedef double real;
typedef Coord<real> Crd;

#endif
