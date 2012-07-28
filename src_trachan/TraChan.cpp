#include "TraChan.h"
using namespace std;

TraChan::TraChan(){
}

int TraChan::setup(int argn, char* argv[])
{
  cout << cp;
  cout << endl;
  cout << cp_gromacs;
  cout << endl;
  cout << endl;
  string fn_cfg;
  if(argn<2){
    generate_sample_config();
    exit(1);
  }

  cfg.set_all(argn,argv);
  if(cfg.fn_cfg!=string())
    cfg.set_all(FileIo(cfg.fn_cfg).read_ascii_strings());
  return 0;  
}
int TraChan::generate_sample_config(){
  cout << "Generating sample configure file: "<< cfg.fn_cfg_sample <<endl;
  cout << "Modify it, and execut trachan as follows,"<<endl;
  cout << "trachan --fn-cfg "<<cfg.fn_cfg_sample<<endl;
  FileIo f_out(cfg.fn_cfg_sample);
  f_out.open_write();
  f_out.write_string("--fn-pdb      initial.pdb\n");
  f_out.write_string("--fn-pore-axis-coordinates    pore_axis.txt\n");
  f_out.write_string("--fn-pore-axis-coordinates-r  pore_axis_r.txt\n");
  f_out.write_string("--dt          20.00\n");
  f_out.write_string("--pore-axis-basis-from   A 374 O\n");
  f_out.write_string("--pore-axis-basis-from   B 374 O\n");
  f_out.write_string("--pore-axis-basis-from   C 374 O\n");
  f_out.write_string("--pore-axis-basis-from   D 374 O\n");
  f_out.write_string("--pore-axis-basis-to    A 377 O\n");
  f_out.write_string("--pore-axis-basis-to    B 377 O\n");
  f_out.write_string("--pore-axis-basis-to    C 377 O\n");
  f_out.write_string("--pore-axis-basis-to    D 377 O\n");
  f_out.write_string("--site-max-radius          10.0\n");
  f_out.write_string("--site-boundary            20.0\n");
  f_out.write_string("--site-boundary           -25.0\n");
  f_out.write_string("--trace-atom-name       K\n");
  f_out.write_string("--fn-trr trajectory/run301_310_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run311_320_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run321_330_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run331_340_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run341_350_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run351_360_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run361_370_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run371_380_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run381_390_dt20.trr\n");
  f_out.write_string("--fn-trr trajectory/run391_400_dt20.trr\n");
  f_out.close();  
  return 0;
}


int TraChan::main_routine()
{
  cout << "TraChan::mainRoutine()" << endl;
  switch(cfg.mode){
  case M_TEST:
    mode_test();
    break;
    //  case M_DIFF_COEFF:
    //    mode_diff_coeff();
    //    break;
  case M_SITE_OCCUPANCY:
    mode_site_occupancy();
    break;
  default:
    cout << "invalid mode" << endl;    
    break;
  }
  return 0;  
}

int TraChan::mode_test(){
  cout << "test mode" << endl;    
  list<string>::iterator i_trr;

  int i_frame=0;

  for(i_trr = cfg.fn_trr.begin();
      i_trr != cfg.fn_trr.end(); i_trr++){
    cout << *i_trr << endl;
    XDRio fin( (*i_trr) );
    fin.open();

    TrnHeader trnh;
    while(fin.read_trn_header(trnh)){
      //cout << "Frame: " << i_frame << endl;

      vector<Crd> box;
      vector<Crd> x;
      vector<Crd> v;
      vector<Crd> f;
      fin.read_trn_frame(trnh, box, x, v, f);

      cout << "x[0][0] " << x[0][0] << endl;

      i_frame++;
    }
    fin.close();
  }
  return 0;
}

/*int TraChan::mode_diff_coeff(){
  cout << "diffusion coefficient mode" << endl;    
  int i_frame=0;

  /// read atom info ///
  System sys;
  {
    PDBio pdbio(cfg.fn_pdb);
    sys.set_atom_info(pdbio.read_pdb());
  }
  sys.set_trace_atom_id_from_atom_names(cfg.trace_atom_names);

  vector<AtomInfo>::iterator i_ai;
  for(i_ai = sys.atom_info.begin();
      i_ai != atom_info.end(); i_ai++){
    if((*i_ai).get_atom_name() != "" ||
       
  // 
  vector<Crd> box;
  vector<Crd> x;
  vector<Crd> x_prev;
  vector<Crd> v;
  vector<Crd> f;
  x.reserve(sys.get_n_atoms());
  x_prev.reserve(sys.get_n_atoms());
  v.reserve(sys.get_n_atoms());
  f.reserve(sys.get_n_atoms());

  vector<Crd> displacement(sys.get_n_atoms(), Crd(0.0,0.0,0.0));

  ////// read trajectory //////
  list<string>::iterator i_trr;
  for(i_trr = cfg.fn_trr.begin();
      i_trr != cfg.fn_trr.end(); i_trr++){
    cout << *i_trr << endl;
    XDRio fin( (*i_trr) );
    fin.open();

    TrnHeader trnh;

    while(fin.read_trn_header(trnh)){
      //      cout << "Frame: " << i_frame << endl;

      box.clear();
      x.clear();
      v.clear();
      f.clear();
      fin.read_trn_frame(trnh, box, x, v, f);
      


      x_prev = x;
      i_frame++;
    }
    fin.close();
  }
  
  }*/

int TraChan::mode_site_occupancy(){
  cout << "site occupancy mode" << endl;    
  list<string>::iterator i_trr;

  int i_frame = cfg.append_time;

  ChannelStructure cs;
  {
    PDBio pdbio(cfg.fn_pdb);
    cs.set_atom_info(pdbio.read_pdb());
    cout << "n_atoms : " << cs.get_n_atoms() << endl;
    
  }
  //cs.set_channel_chain_id(cfg.channel_chain_id);
  //cs.set_selectivity_filter_res(cfg.selectivity_filter_res);
  cs.set_pore_axis_basis_atoms(cfg.pore_axis_basis_chain_a,    cfg.pore_axis_basis_res_a,
			       cfg.pore_axis_basis_atomname_a, cfg.pore_axis_basis_atom_a,
			       cfg.pore_axis_basis_chain_b,    cfg.pore_axis_basis_res_b,
			       cfg.pore_axis_basis_atomname_b, cfg.pore_axis_basis_atom_b);
  cs.set_trace_atom_id_from_atom_names(cfg.trace_atom_names);
  cs.set_site_max_radius(cfg.site_max_radius);
  cs.set_site_hight_margin(cfg.site_hight_margin);
  cs.set_site_boundaries(cfg.site_boundaries);

  ////// prepare output files /////
  FileIo f_out_site(cfg.fn_site_occupancy);
  if(cfg.fn_site_occupancy!=""){
    if(cfg.append_time == 0) f_out_site.open_write();
    else f_out_site.open_append();
  }
  //f_out_site.open_write();
  FileIo f_pore_axis(cfg.fn_pore_axis_density);
  if(cfg.fn_pore_axis_density!=""){
    if(cfg.append_time == 0){
      f_pore_axis.open_write();
      f_pore_axis.write_string("atomname\th\tr\n");
    }else f_pore_axis.open_append();
  }
  FileIo f_pore_axis_crd(cfg.fn_pore_axis_coordinates);
  FileIo f_pore_axis_crd_r(cfg.fn_pore_axis_coordinates_r);
  if(cfg.fn_pore_axis_coordinates!=""){
    if(cfg.append_time == 0){
      f_pore_axis_crd.open_write();
      f_pore_axis_crd.write_string(cs.get_pore_axis_coordinates_header_string());
    }else f_pore_axis_crd.open_append();
  }
  if(cfg.fn_pore_axis_coordinates_r!=""){
    f_pore_axis_crd_r.open_write();
    f_pore_axis_crd_r.write_string(cs.get_pore_axis_coordinates_header_string());
  }
  /*
  list<FileIo> f_pore_axis; 
  if(cfg.fn_pore_axis_density != ""){
    list<string>::iterator i_at;
    for(i_at = cfg.trace_atom_names.begin();
	i_at != cfg.trace_atom_names.end(); i_at++){
      string fn = cfg.fn_pore_axis_density + (*i_at) + ".txt";
      FileIo f_tmp(fn);
      f_tmp.open_write();
      //f_pore_axis.push_back(f_tmp);
    }
  }
  */
  vector<Crd> box;
  vector<Crd> x;
  vector<Crd> v;
  vector<Crd> f;
  x.reserve(cs.get_n_atoms());
  v.reserve(cs.get_n_atoms());
  f.reserve(cs.get_n_atoms());

  ////// read trajectory //////

  double axis_length_sum = 0.0;
  double axis_length_sq_sum = 0.0;

  for(i_trr = cfg.fn_trr.begin();
      i_trr != cfg.fn_trr.end(); i_trr++){
    cout << *i_trr << endl;
    XDRio fin( (*i_trr) );
    if(fin.open() == 1){
      continue;
    }

    TrnHeader trnh;

    while(fin.read_trn_header(trnh)){
      //      cout << "Frame: " << i_frame << endl;
      double time = i_frame * cfg.dt;

      box.clear();
      x.clear();
      v.clear();
      f.clear();
      fin.read_trn_frame(trnh, box, x, v, f);
      cs.set_pore_axis_basis_coordinates(x);
      
      cs.cal_pore_axis_coordinates(x);
      cs.cal_site_occupancy();

      if(f_out_site.is_open()){
	stringstream line_output;
	line_output << time << cs.get_text_site_occupancy() << endl;
	f_out_site.write_string(line_output.str());
      }

      //list<FileIo>::iterator i_file;
      //list<string>::iterator i_at;
      //      for(i_file = f_pore_axis.begin(), i_at = cfg.trace_atom_names.begin();
      //i_file != f_pore_axis.end(); i_file++, i_at++)
      if(f_pore_axis.is_open())
	f_pore_axis.write_string(cs.get_pore_axis_coords_for_density_analysis());
      if(f_pore_axis_crd.is_open()){
	stringstream line_output;
	line_output << time << cs.get_pore_axis_coordinates_h_string() << endl;
	f_pore_axis_crd.write_string(line_output.str());
      }
      if(f_pore_axis_crd_r.is_open()){
	stringstream line_output;
	line_output << time << cs.get_pore_axis_coordinates_r_string() << endl;
	f_pore_axis_crd_r.write_string(line_output.str());
      }
      axis_length_sum += cs.get_pore_axis_basis_vec_ab_sc();
      axis_length_sq_sum += cs.get_pore_axis_basis_vec_ab_ip();

      i_frame++;

    }

    fin.close();
  }

  double axis_length_ave = axis_length_sum/i_frame;
  cout << "average axis length = " << axis_length_ave << endl;
  cout << "sd axis length = " << axis_length_sq_sum/i_frame - axis_length_ave*axis_length_ave << endl;
  
  ///////////// closing output files ///////////////
  if(f_out_site.is_open()) f_out_site.close();
  if(f_pore_axis.is_open()) f_pore_axis.close();
  if(f_pore_axis_crd.is_open()) f_pore_axis_crd.close();
  if(f_pore_axis_crd_r.is_open()) f_pore_axis_crd_r.close();

  //  list<FileIo>::iterator i_file;
  //  for(i_file = f_pore_axis.begin();
  //      i_file != f_pore_axis.end(); i_file++){
  //    (*i_file).close();
  //  }
  return 0;
}
