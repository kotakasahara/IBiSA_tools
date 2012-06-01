#ifndef __FILE_IO_H__
#define __FILE_IO_H__

#include <fstream>
#include <string>
#include <iostream>
#include <sstream>
#include <vector> 

class FileIo
{
 private:
  std::string filename;
 public:
  std::fstream fs;
  bool op;
  //  FileIo();
  FileIo(std::string in_filename);
  int open();
  int open_write();
  int open_append();
  int close();
  std::string get_filename(){return filename;};
  bool is_open(){return op;};
  
  std::vector<std::string> read_ascii_strings();
  int write_string(std::string line);
};

#endif
